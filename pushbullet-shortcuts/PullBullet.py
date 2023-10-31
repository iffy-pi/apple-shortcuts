# v1.1 https://www.icloud.com/shortcuts/5d150871e03c4d30a217ca92fe8096dd
@SETUP("Paste access token here")
accessToken = '...'

TRUE = 1
FALSE = 0

returnContent = FALSE

updateInfo = {
	'updateLink': '...',
	'version': 1.1
}

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
		if bodyIsLink == TRUE:
			item['body'] = ''

		optionsVcard = f'''
			BEGIN:VCARD
	        VERSION:3.0
	        N;CHARSET=utf-8:Open Link
	        ORG:Open the link in your default browser
	        NOTE;CHARSET=UTF-8:open-link
	        {openLinkIcon}
	        END:VCARD

	        BEGIN:VCARD
	        VERSION:3.0
	        N;CHARSET=utf-8:Copy Link
	        ORG:Copy the link to your clipboard
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

        chosen = ChooseFrom(contacts, prompt=f'''
				Link:
				{foundLink}
			''')

        option = Contact(chosen).Notes

        if option == 'open-link':
			OpenURL(foundLink)

        if option == 'copy-link':
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
		if returnContent == FALSE:
			Share(renamedItem)
		
		StopShortcut(output=renamedItem)

# Copy the item to clipboard
if returnContent == TRUE:
	StopShortcut(output=itemForClipboard)
else:
	CopyToClipboard(itemForClipboard)
	Notification(itemForClipboard, title="Most recent push has been copied to your clipboard")

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

