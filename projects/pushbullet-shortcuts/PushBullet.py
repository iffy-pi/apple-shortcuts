'''
v1.53
ShortcutInput = any, default = clipboard
- Updated notifications
- Shortcut now saves PushBullet Premium configuration to file rather than in set up.
'''

TRUE = 1
FALSE = 0

UpdateInfo = {
    'updateLink': 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushbullet/updates.json'
    'version': 1.61,
}

filePaths = {
    'premium': 'PushBullet/HasPremium.txt',
    'token': 'PushBullet/AccessToken.txt',
    'config': 'PushBullet/config.json'
}

openConfigMenu = FALSE
exitAfterConfig = FALSE

if ShortcutInput is None:
    openConfigMenu = TRUE
    exitAfterConfig = TRUE
    contents = Clipboard
else:
    contents = ShortcutInput


file = GetFile(From='Shortcuts', filePaths['config'], errorIfNotFound=False)
if file is None:
    openConfigMenu = TRUE
    # Move over access token and premium state from legacy file structure
    config = Dictionary()
    file = GetFile(From='Shortcuts', filePaths['token'], errorIfNotFound=False)
    if file is not None:
        config['access_token'] = Text(file)

    file = GetFile(From='Shortcuts', filePaths['premium'], errorIfNotFound=False)
    if file is not None:
        config['premium'] = Number(file)
else:
    config = Dictionary(file)

configPrompts = f'''
    PushBullet Configuration
    You can access this menu again by running the shortcut without any input.
    '''

if config.get('access_token') is None:
    configPrompts.append('You need to configure your access token')
if config.get('premium') is None:
    configPrompts.append('You need to configure your premium status')


if openConfigMenu == TRUE:
    Menu(Text(configPrompts)):
        case 'Set Access Token':
            prompt = f'''
            Enter Access Token Below
            You can generate an access token from your PushBullet Account > Settings > Access Tokens.
            '''
            text = AskForInput(Input.Text, prompt=prompt, default=config.get('access_token') allowMultipleLines=False)
            config['access_token'] = text

        case 'Set Premium Status':
            Menu('Do you have PushBullet Premium?'):
            case 'Yes':
                MENURESULT = TRUE
            case 'No':
                MENURESULT = FALSE
            config['premium'] = MENURESULT

        case 'Send pushes to device...':
            if config.get('access_token') is None:
                ShowAlert('Access Token has not been configured')
                StopShortcut()
            
            # Get the list of devices
            res = GetContentsOfURL('https://api.pushbullet.com/v2/devices', headers={'Access-Token': config['access_token']})
            for dev in res['devices']:
                text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=utf-8:{dev['nickname']}
                    ORG: {dev['model']}
                    NOTE;CHARSET=UTF-8:{dev['iden']}
                    END:VCARD
                '''
                REPEATRESULTS.append(text)

            text = f'''
                {REPEATRESULTS}

                BEGIN:VCARD
                VERSION:3.0
                N;CHARSET=utf-8:All devices
                ORG:Push to all devices
                NOTE;CHARSET=UTF-8:_all
                END:VCARD
            '''

            renamedItem = SetName(REPEATRESULTS, 'vcard.vcf')
            contacts = GetContacts(renamedItem)
            selected = ChooseFrom(contacts, prompt='Select device option')

            config['target_device'] = Contact(selected).Notes
            config['target_device_name'] = Contact(selected).Name

        case 'Push Item In Clipboard':
            exitAfterConfig = FALSE

    # Save the config file
    SaveFile(config, To='Shortcuts', filePaths['config'], overwrite=True)

    if exitAfterConfig == TRUE:
        StopShortcut()

if config.get('access_token') is None:
    ShowAlert('''
        Access Token has not been configured.
        Run the shortcut without any input to configure.''')
    StopShortcut()

if config.get('premium') is None:
    ShowAlert('''
        Premium Status has not been configured.
        Run the shortcut without any input to configure.''')
    StopShortcut()


targetIden = ''
if config.get('target_device') is not None:
    if Text(config['target_device']) != '_all':
        targetIden = config['target_device']

remoteFiles = {
    'mime' : 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushbullet/data/ext_to_mime.json',
    'errorCodesInfo' : 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushbullet/data/error_codes_info.txt'
}

res = GetContentsOfURL(remoteFiles['mime'])
mime = Dictionary(res)

failedPushes = []

accessToken = config['access_token']
pushbulletPremium = config['premium']

maxNonPremiumFileSizeMB = 25

pushBody = {
    'type': '',
    'url': '',
    'body': '',
    'file_type': '',
    'file_name': '',
    'file_url': ''
    'device_iden': targetIden
}


pushCall = {
    'push_url': 'https://api.pushbullet.com/v2/pushes',
    'upload_req_url': 'https://api.pushbullet.com/v2/upload-request',
    'method': 'POST',
    'accesstoken': accessToken
}

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
        matches = MatchText("(url)|(safari web page)", itemType, caseSensitive=False)
        if matches is not None:
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
        if ChangeCase(itemType, 'lowercase') == 'safari web page':
            item = GetDetailsOfSafariWebPage('Page URL', item)

        itemPushBody['type'] = 'link'
        itemPushBody['url'] = item

    # note handlerz
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
        if SetSizeUnits(size, 'MB') > maxNonPremiumFileSizeMB:
            if pushbulletPremium == FALSE:
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
                body={
                    'type': itemPushBody['type'],
                    'url': itemPushBody['url'],
                    'body': itemPushBody['body'],
                    'file_type': itemPushBody['file_type'],
                    'file_name': itemPushBody['file_name'],
                    'file_url': itemPushBody['file_url'],
                    'device_iden': itemPushBody['device_iden']
                }
            )

        text = res['error']

        if text is not None:
            itemErrorCode = 6
            itemErrorMsg = text
        else:
            if f'[{targetIden}]' != '[]':
                IFRESULT = f' to {config['target_device_name']}'
            else:
                IFRESULT = ''
            deviceAppend = IFRESULT

            # Successful push so notify user
            typ = ChangeCase(itemPushBody['type'], 'lowercase')
            
            if typ == 'note':
                Notification(f'"{item}"', title=f'Text pushed successfully{deviceAppend}', attachment=item)

            if typ == 'link':
                Notification(item, title=f'Link pushed successfully{deviceAppend}')

            if typ == 'file':
                generalType = ReplaceText(GetTypeOf(item), 'Text', 'Text File')
                Notification(itemPushBody['file_name'], title=f'{generalType} pushed successfully{deviceAppend}', attachment=item)

    # Report and collate errors
    if itemErrorCode != 0:
        text = f'Item Name: {itemFname}, Error Code: {itemErrorCode}, Message: "{itemErrorMsg}"'
        failedPushes.append(text)

# Open all failed items in a note
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



