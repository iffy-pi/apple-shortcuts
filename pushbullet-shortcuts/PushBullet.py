'''
v1.52
ShortcutInput = any, default = clipboard
'''

TRUE = 1
FALSE = 0

accessTokenPath = 'PushBullet/AccessToken.txt'
file = GetFile(From='Shortcuts', accessTokenPath)
if file is None:
    Menu('Your access token is required to use this shortcut'):
        case 'I have my access token':
            text = AskForInput(Input.Text, prompt="Enter Access Token Below:", allowMultipleLines=False)
            SaveFile(To='Shortcuts', accessTokenPath, overwrite=True)
            ShowAlert(f'Access Token has been saved to {accessTokenPath}')
            IFRESULT = text

        case "I don't have my access token":
            ShowAlert("Get an access token from your PushBullet Account > Settings > Access Tokens")
            StopShortcut()
else:
    IFRESULT = Text(file)

accessToken = IFRESULT

UpdateInfo = {
    'updateLink': 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushbullet/updates.json'
    'version': 1.41,
}

@SETUP('Enter 1 If You Have PushBullet Premium')
pushbulletPremium = 0


remoteFiles = {
    'mime' : 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushbullet/data/ext_to_mime.json',
    'errorCodesInfo' : 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushbullet/data/error_codes_info.txt'
}

res = GetContentsOfURL(remoteFiles['mime'])
mime = Dictionary(res)

pushCall = {
    'push_url': 'https://api.pushbullet.com/v2/pushes',
    'upload_req_url': 'https://api.pushbullet.com/v2/upload-request',
    'method': 'POST',
    'accesstoken': accessToken
}

pushBody = {
    'type': '',
    'url': '',
    'body': '',
    'file_type': '',
    'file_name': '',
    'file_url': ''
}

failedPushes = []

if ShortcutInput is None:
    ShowNotification("Nothing to Push!")
    StopShortcut()


contents = ShortcutInput

typeId = {
    'link': 1,
    'note': 0
    'file': 2
}

for repeatItem in contents:
    item = repeatItem

    itemPushBody = pushBody
    
    # -1 means still determining type
    # -2 means user must determine type
    pushType = -1

    itemType = GetTypeOf(item)
    itemFname = GetDetailsOfFiles("Name", item)
    itemSize = GetDetailsOfFiles("Size", item)
    itemFext = GetDetailsOfFiles("File Extension", item)

    itemErrorCode = 0
    ambiguousType
    itemErrorMsg = ''



    # find the type first then give it to the items
    # so we can add support for user types

    # -------------- ITEM TYPE -------------------------

    # do link
    if pushType == -1:
        files = FilterFiles(
                    itemType, 
                    whereAny=[
                        "Name" is "URL",
                        "Name" is "Safari Web Page",
                    ],
                    limit=1
                )

        if files is not None:
            pushType = typeId['link']

    # do note
    # clipboard.c clipboard.46 clipboard.txt apple.txt "text"
    if pushType == -1:
        # only do text or rich text
        isTextorRichText = MatchText("(text)|(rich text)", itemType, caseSensitive=False)
        if isTextorRichText is not None:
            isRawText = FALSE

            # check if extension is all numbers
            extIsAllNumbers = MatchText("([0-9][0-9]*[^a-z])", itemFext, caseSensitive=False)
            if extIsAllNumbers is not None:
                res = MatchText(".*clipboard.*", itemFname, caseSensitive=False)
                if res is not None:
                    # if extension is all numbers and came from clipboard, most likely raw text
                    # otherwise, it will be treated as file
                    isRawText = TRUE
                
            else:
                res = FilterFiles(f".{itemFext}", whereAny=["Name" is ".txt", "Name" is "."])
                if res is not None:
                    # if txt extension or no extension treat as raw text
                    # other extensions that are not all numbers will be treated as a file (fall through)
                    isRawText = TRUE
                

            if isRawText == TRUE:
                # assume its valid text
                pushType = typeId['note']

                # text greater than 63kb must be a file as they dont fit in text field
                if SetSizeUnits(itemSize, 'KB') > 63:
                    pushType = typeId['file']
                    itemFname = "Pushed Text"
                    itemFext = "txt"

                else:
                    # if its greater than 5, might be a .txt file being interpreted as text 
                    # let user decide what to do
                    if SetSizeUnits(itemSize, 'KB') > 5:
                        pushType = -2

    # do file
    if pushType == -1:
        # assume its file
        pushType = typeId['file']

    # user selects for negative values
    if pushType < 0:
        # let user select
        maxLoops = 15
        exitLoop = FALSE

        for _ in range(maxLoops):
            if exitLoop is FALSE:
                # assume the loop will exit after one iteration
                exitLoop = TRUE

                # then do the stuff
                text = f'''
                    The type of the input could not be determined:
                    Name: 
                    {itemFname}.{itemFext}

                    Guessed Type:
                    {itemType}

                    Size:
                    {itemSize}

                    What is the type of this input?
                '''
                Menu(prompt=text):

                    case "Text":
                        # set the push type to text
                        pushType = typeId['note']
                        item = Text(item)

                    case "Link/URL":
                        pushType = typeId['link']

                    case "File":
                        # filename might be confusing give users a chance to rename
                        Menu(prompt=f"Filename: {itemFname}.{itemFext}"):
                            case "Change Name":
                                res = AskForInput(Input.Text, prompt="Format: {filename}.{ext}", multipleLines=False)
                                matches = MatchText("(.*)\\.(.*)", res)
                                itemFname = GetMatchGroupAt(0, matches)
                                itemFext = GetMatchGroupAt(1, matches)

                            case "Back":
                                exitLoop = FALSE

                        # if the item mime type is none, then we have an errror
                        if Mime[itemFext] is not None:
                            pushType = typeId['file']
                        else
                            itemErrorCode = 5
                            itemErrorMsg = f"Extension: {itemFext}"

                    case "View Item":
                        # reloop to give user options again
                        ShowResult(item)
                        exitLoop = FALSE

    # ------------ HANDLE ITEM --------------

    if pushType == typeId['link']:
        itemPushBody['type'] = 'link'
        itemPushBody['url'] = item

    # note handler
    if pushType == typeId['note']:
        itemPushBody['type'] = 'note'
        itemPushBody['body'] = item

    # file handler
    if pushType == typeId['file']:
        if itemFext == 'heic':
            item = ConvertImage(item, "JPEG")
            itemFext = GetDetailsOfFiles("File Extension", item)

        goodFileSize = TRUE

        size = GetDetailsOfFiles("File Size", item)
        if SetSizeUnits(size, 'MB') > 25:
            if pushbulletPremium != 1:
                goodFileSize = FALSE

        if goodFileSize is FALSE:
            itemErrorCode = 4

        else
            # if file extension is not in mime, then treat as binary stream
            itemMimeType = Mime[itemFext]
            if itemMimeType is None:
                itemMimeType = Mime['bin']

            itemFname = itemFname.replace(",", "")

            text = f"{itemFname}.{itemFext}"

            # upload request
            uploadResponse = GetContentsOfURL(
                    pushCall['upload_req_url'],
                    method=POST,
                    headers={
                        "Access-Token" : pushCall['accesstoken']
                    },
                    type=JSON,
                    body={
                        'file_name': text,
                        'file_type': itemMimeType
                    }
                )

            text = uploadResponse['error']

            if text is not None:
                itemErrorCode = 6
                itemErrorMsg = text

            else
                res = GetContentsOfURL(
                    uploadResponse['upload_url'],
                    method='POST',
                    headers={
                        "Access-Token" : pushCall['accesstoken']
                    },
                    type='FORM',
                    body={
                        'file': item
                    }
                )

                dix = Dictionary(res)
                text = GetDictionaryValue(dix, 'error')

                if text is not None:
                    itemErrorCode = 6
                    itemErrorMsg = text
                else:
                    itemPushBody['type'] = 'file'
                    itemPushBody['file_name'] = uploadResponse['file_name']
                    itemPushBody['file_type'] = uploadResponse['file_type']
                    itemPushBody['file_url'] = uploadResponse['file_url']

    # push the item
    if itemErrorCode == 0:
        res = GetContentsOfURL(
                pushCall['push_url'],
                method='POST',
                headers={
                    "Access-Token" : pushCall['accesstoken']
                },
                type='JSON',
                body=itemPushBody
            )

        text = res['error']

        if text is not None:
            itemErrorCode = 6
            itemErrorMsg = text
        else:
            text = ChangeCase(itemPushBody['type'], casing='Capitalize Every Sentence')
            text = f'{text} pushed successfully'

            title = dix[ itemPushBody['type'] ]
            if Text(itemPushBody['type']) == 'file':
                Notification('', title=title, attachment=item)
            else:
                Notification(item, title=title, attachment=item)


    if itemErrorCode != 0:
        text = f'Item Name: {itemFname}, Error Code: {itemErrorCode}, Message: "{itemErrorMsg}"'
        failedPushes.append(text)

if Count("Items", failedPushes) > 0:
    res = GetContentsOfURL(remoteFiles['errorCodesInfo'])
    errorCodes = Text(res)

    text = f'....{failedPushes}...{errorCodes}' # pushbullet error request

    note = CreateNote(text)
    OpenNote(note)

# Check for updates
UpdateRes = GetContentsOfURL(UpdateInfo['updateLink'])
if Number(UpdateRes['version']) > UpdateInfo['version']:
    Menu('There is a new version of this shortcut available'):
        case 'Install Now':
            split = SplitText(UpdateRes['releaseNotes'], SplitText.By.NewLines)
            dt = Date(UpdateRes['releaseTime'])

            text = f'''
                Pushbullet Shortcut Update
                An update is available for this shortcut
                ...
            '''
            note = CreateNote(Text)
            OpenNote(note)

            StopShortcut()

        case 'Later':
            pass



