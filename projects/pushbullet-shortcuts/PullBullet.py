# v1.2
TRUE = 1
FALSE = 0

maxDisplayLinkWidth = 160

updateInfo = {
    'updateLink': '...',
    'version': 1.32
}


filePaths = {
    'premium': 'PushBullet/HasPremium.txt',
    'token': 'PushBullet/AccessToken.txt',
    'config': 'PushBullet/config.json'
}


file = GetFile(From='Shortcuts', filePaths['config'], errorIfNotFound=False)
if file is None:
    # Move over access token and premium state from legacy file structure
    config = Dictionary()
    file = GetFile(From='Shortcuts', filePaths['token'], errorIfNotFound=False)
    if file is not None:
        config['access_token'] = Text(file)
else:
    config = Dictionary(file)


if config.get('access_token') is None:
    Menu('Your access token is required to use this shortcut'):
        case 'I have my access token':
            text = AskForInput(Input.Text, prompt="Enter Access Token Below:", allowMultipleLines=False)
            config['access_token'] = Text(file)
            SaveFile(config, To='Shortcuts', filePaths['config'], overwrite=True)

        case "I don't have my access token":
            ShowAlert("Get an access token from your PushBullet Account > Settings > Access Tokens")
            StopShortcut()


accessToken = config['access_token']
copiedLink = FALSE
returnContent = FALSE


params = {
    'limit': 1,
    'active': True
}

openLinkIcon = ... # openLinkIcon.txt
copyIcon = ... # copyIcon.txt

url = f"https://api.pushbullet.com/v2/pushes?active={active}&limit={limit}"

if Dictionary(ShortcutInput)['returnContent'] is not None:
    returnContent = TRUE

dixOut = GetContentsOfURL(
        url,
        headers = { 'Access-Token': accessToken }
    )

item = dixOut['pushes'][0]

dixValue = item['type']
filterContents = FilterFiles(
        dixValue,
        whereAny=[
            "Name" is "note",
            "Name" is "link"
        ]
    )

if filterContents is not None:
    # note or link, but could contain a URL in the body
    bodyIsLink = FALSE
    text = filterContents

    if item['url'] is not None:
        # always has url
        foundLink = item['url']
    else:
        size = GetDetailsOfFiles('File Size', item['body'])
        if SetSizeUnits(size, 'bytes') <= 1024:
            # only consider when body is less than 1024 characters
            # body may contain a url
            urls = GetURLsFrom(item['body'])
            if urls is not None:
                if urls.contains(item['body']):
                    # URLS are evaluated to full length
                    # if its just standard body then there will be other stuff that dont get evaluated to it
                    foundLink = item['body']
                    bodyIsLink = TRUE

    if foundLink is not None:
        # if we are returning content, then just stop and output the link immediately
        if returnContent == TRUE:
            StopShortcut(output=foundLink)

        if bodyIsLink == TRUE:
            item['body'] = ''

        # Otherwise, create user selection to either open link, copy link,
        # copy title (if available) and copy message (if available)

        optionsVcard = f'''
            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=utf-8:Open Link
            ORG:Open link in your default browser
            NOTE;CHARSET=UTF-8:open-link
            {openLinkIcon}
            END:VCARD

            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=utf-8:Copy Link
            ORG:Copy link to your clipboard
            NOTE;CHARSET=UTF-8:copy-link
            {copyIcon}
            END:VCARD
        '''

        if Text(item['title']) != '':
            optionsVcard = f'''
                {optionsVcard}
                BEGIN:VCARD
                VERSION:3.0
                N;CHARSET=utf-8:Copy Title
                ORG:{item['title']}
                NOTE;CHARSET=UTF-8:copy-title
                {copyIcon}
                END:VCARD
            '''

        if Text(item['body']) != '':
            optionsVcard = f'''
                {optionsVcard}
                BEGIN:VCARD
                VERSION:3.0
                N;CHARSET=utf-8:Copy Message
                ORG:{item['body']}
                NOTE;CHARSET=UTF-8:copy-message
                {copyIcon}
                END:VCARD
            '''

        renamedItem = SetName(optionsVcard, 'vcard.vcf')
        contacts = GetContacts(renamedItem)

        displayedLink = foundLink

        splitText = SplitText(displayedLink, everyCharacter=True)

        if Count(splitText) > maxDisplayLinkWidth:
            items = splitText.getItemRange(1, maxDisplayLinkWidth)
            displayedLink = f'''
                {CombineText(items, '')}... (full link not shown)
                '''

        chosen = ChooseFrom(contacts, prompt=f'''
                Link:
                {displayedLink}
            ''')

        option = GetDetailsOfContacts(chosen, 'Notes')

        if option == 'open-link':
            OpenURL(foundLink)

        if option == 'copy-link':
            copiedLink = TRUE
            copyContent = foundLink
        
        if option == 'copy-title':
            copyContent = item['title']
        
        if option == 'copy-message':
            copyContent = item['body']

        if copyContent is not None:
            itemForClipboard = copyContent

    else:
        if item['title'] is not None:
            IFRESULT = f'''
                {item['title']}
                {item['body']}
            '''
        else:
            IFRESULT = f"{item['body']}"

        itemForClipboard = IFRESULT

else:
    # it is a file
    urlContents = GetContentsOfURL(item['file_url'])
    renamedItem = SetName(urlContents, item['file_name'], dontIncludeFileExtension=True)

    if item['file_name'] == 'Pushed Text.txt':
        # was text that overflowed
        itemForClipboard = urlContents
        
    else:
        # If we are returning content then just output the file and exit
        # Otherwise open share sheet (will run update script after)
        if returnContent == TRUE:
            StopShortcut(output=renamedItem)
        else:
            Share(renamedItem)
    

# If we are returning content then just output the text, otherwise copy the item to the clipboard.
if returnContent == TRUE:
    StopShortcut(output=itemForClipboard)
else:
    if itemForClipboard is not None:
        CopyToClipboard(itemForClipboard)
        if copiedLink == TRUE:
            IFRESULT = 'Link'
        else:
            IFRESULT = 'Text'
            
        Notification(itemForClipboard, title=f"{IFRESULT} copied to clipboard", attachment=itemForClipboard)

# Check for updates
UpdateRes = GetContentsOfURL(UpdateInfo['updateLink'])
if Number(UpdateRes['version']) > UpdateInfo['version']:
    Menu('There is a new version of this shortcut available'):
        case 'Install Now':
            split = SplitText(UpdateRes['releaseNotes'], SplitText.By.NewLines)
            dt = Date(UpdateRes['releaseTime'])

            text = f'''
                Pullbullet Shortcut Update
                An update is available for this shortcut
                ...
            '''
            note = CreateNote(Text)
            OpenNote(note)

            StopShortcut()

        case 'Later':
            pass

