FALSE = 0
TRUE = 1

updateInfo = {
	'updateLink': 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushlist/updates.json',
	'version': 1.03
}

constants = {
	'cfgFile': 'PushBullet/config.json',
	'api': 'https://api.pushbullet.com/v2/pushes'
}

linkIcon = ... # linkIcon.txt
fileIcon = ... # fileIcon.txt
textIcon = ... # textIcon.txt
exitIcon = ... # exitIcon.txt

config = Dictionary(GetFile(From='Shortcuts', constants['cfgFile'], errorIfNotFound=False))
accessToken = config['access_token']

if accessToken is None:
	accessToken = AskForInput(Input.Text, 'Enter PushBullet Access Token')
	config['access_token'] = accessToken
	SaveFile(config, To='Shortcuts', constants['cfgFile'], overwrite=True)


itemCount = AskForInput(Input.Number, prompt='How many items would you like to pull?', allowDecimals=False, allowNegatives=False)

epoch = Date('January 1, 1970 00:00 GMT')

# Pipe, where _ represents pipe input
curUnixTime = ConvertDateTimeZone('', 'Bamako') | GetTimeBetween(epoch, _, 'seconds')

url = URL(f'{api}?active=true&limit={itemCount}')
pushes = GetContentsOfURL(url, headers={'Access-Token': accessToken}) | GetDictionaryValue('pushes', _) 

pushDix = {}

for pushObject in pushes:
	pushObject = Dictionary(pushObject)
	
	if f'{pushObject['file_name']}' == 'Pushed Text.txt':
		textContent = Text(GetContentsOfURL(pushObject['file_url']))
		pushObject['body'] = textContent
		pushObject['type'] = 'note'

	pushDix[pushObject['iden']] = pushObject
	pushIdens.append(pushObject['iden'])


vcardCache = {}


for curIden in pushIdens:
	pushObject = pushDix[curIden]
	dateStr = Text(AdjustDate(epoch, seconds=pushObject['modified']).format('How Long Ago/Until'))
	pushObjName = ''

	dix = {
		'file': 'Pushed File',
		'note': 'Pushed Note',
		'link': 'Pushed Link'
	}

	pushObjType = dix[pushObject['type']]

	pushTypeRaw = Text(pushObject['type'])

	if pushTypeRaw == 'note':
		pushObjName = Text(pushObject['body'])
		icon = textIcon

	if pushTypeRaw == 'link':
		pushObjName = Text(pushObject['url'])
		icon = linkIcon

	if pushTypeRaw == 'file':
		pushObjName = Text(pushObject['file_name'])
		icon = fileIcon

		imageUrl = pushObject['image_url']
		if imageUrl is not None:
			icon = GetContentsOfURL(imageUrl) 
					| ConvertImage(_, 'JPEG', quality=0.3) 
					| Base64Encode(_, lineBreaks='None') 
					| f'PHOTO;ENCODING=b;TYPE=JPEG:{_}'

	# Limiting the contact name size
	splitText = SplitText(pushObjName, byNewLines=True)
	if Count(splitText) > 1:
		pushObjName = f'{splitText.getItemFromList(1)}...'

	charList = SplitText(pushObjName, everyCharacter=True)
	if Count(charList) > 50:
		pushObjName = charList.GetItemRange(1, 47) | CombineText(_, '') | f'{_}...'

	pushObjName = pushObjName.replace(';', r'\;')

	text = f'''
		BEGIN:VCARD
		VERSION:3.0
		N;CHARSET=UTF-8:{pushObjName}
		ORG;CHARSET=UTF-8: {pushObjType} ⸱ {dateStr}
		NOTE;CHARSET=UTF-8:{pushObj['iden']}
		{icon}
		END:VCARD
	'''
	vcardCache[curIden] = text

continueLoop = TRUE

for _ in range(itemCount):
	if continueLoop == TRUE:
		for item in pushIdens:
			REPEATRESULTS.append(vcardCache[item])

		contacts = Text(REPEATRESULTS) | SetName(_, 'vcard.vcf') | GetContactsFromInput(_)

		text = f'''
			Push List
			Select pushes to save/share
		'''
		selected = ChooseFromList(contacts, prompt=text, selectMultiple=True, selectAllInitially=True)
		selecedIdens = GetConactDetails('notes', selected)

		for curIden in selectedIdens:
			pushObject = Dictionary(pushDix[curIden])
			pushType = Text(pushObject['type'])
			
			if pushType == 'note':
				content = pushObject['body']

			if pushType == 'link'
				content = pushObject['url']

			if pushType == 'file'
				content = GetContentsOfURL(pushObject['file_url']) | SetName(_, pushObject['file_name'], dontIncludeExtension=True)

			pushIdens = pushIdens.filter(x -> x.Name != curIden)

			REPEATRESULTS.append(content)

		if Count(REPEATRESULTS) > 0:
			Share(REPEATRESULTS)
		else:
			continueLoop = FALSE

		if (count := Count(pushIdens)) == 0:
			continueLoop = FALSE
		else:
			if count == 1:
				IFRESULT = 'is still 1 push that has'
			else:
				IFRESULT = f'are still {count} that have'

			Menu(prompt=f'There {IFRESULT} not been saved. What would you like to do?'):
				case "Exit, I've saved the pushes I wanted":
					continueLoop = FALSE
				case "Go back, I want to save more pushes":
					pass

	else:
		updateRes = GetContentsOfURL(updateInfo['updateLink'])
		if Number(updateRes['version']) > updateInfo['version']:
			splitText = Split(updateRes['releaseNotes'], custom='\n')
			date = Date(updateRes['releaseTime'])

            text = f'''
                {updateRes['name']} Shortcut Update
				An update is available for this shortcut:
				{updateInfo['version']} ➡️ {updateRes['version']}

				🕦 Released:
				{date}

				✅ Install:
				{updateRes['link']}

				📝 Release Notes:
				{splitText}

				📬 Developer:
				Reddit: iffythegreat (https://www.reddit.com/user/iffythegreat)
				RoutineHub: iffy-pi (https://routinehub.co/user/iffy-pi)

				📚 Full Update History:
				{updateRes['rhub']}/changelog
            '''
            note = CreateNote(Text)
            OpenNote(note)

        StopShortcut()

