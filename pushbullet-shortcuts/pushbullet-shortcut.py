

def main(ShortcutInput, type="Any", source="Share Sheet", default="Clipboard"):
	'''
	v1.51 (https://www.icloud.com/shortcuts/99bf20d3538240ada2dacaca8245d486)
	TODO:

	DONE:
	- Add user selection of a type 
	- Add set up for pushbullet premium
	- Update MIME to remote calls to github pages
	'''

	UpdateInfo = {
		'updateLink': 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushbullet/updates.json'
		'version': 1.41,
	}

	@SETUP
	AccessToken = '...'

	@SETUP
	pushbulletPremium = 0

	TRUE = 1
	FALSE = 0

	remoteFiles = {
		'mime' : 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushbullet/data/ext_to_mime.json',
		'errorCodesInfo' : 'https://iffy-pi.github.io/apple-shortcuts/versioning/pushbullet/data/error_codes_info.txt'
	}

	res = GetContentsOfURL(remoteFiles['mime'])
	mime = Dictionary(res)

	PushCall = {
		'push_url': '...',
		'upload_req_url': '...',
		'method': 'POST',
		'accesstoken': AccessToken
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


	Contents = ShortcutInput

	typeId = {
		'link': 1,
		'note': 0
		'file': 2
	}

	for repeatItem in Contents:
		item = repeatItem

		itemPushBody = pushBody
		
		# -1 means still determining type
		# -2 means user must determine type
		pushType = -1

		itemType = GetTypeOf(item)
		itemFname = GetFileDetails("Name", item)
		itemSize = GetFileDetails("Size", item)
		itemFext = GetFileDetails("File Extension", item)

		itemErrorCode = 0
		ambiguousType
		itemErrorMsg = ''



		# find the type first then give it to the items
		# so we can add support for user types

		# -------------- ITEM TYPE -------------------------

		# do link
		if pushType == -1:
			files = Filter(
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
					res = filter(f".{itemFext}", whereAny=["Name" is ".txt", "Name" is "."])
					if res is not None:
						# if txt extension or no extension treat as raw text
						# other extensions that are not all numbers will be treated as a file (fall through)
						isRawText = TRUE
					

				if isRawText == TRUE:
					# assume its valid text
					pushType = ['note']

					# text greater than 63kb must be a file as they dont fit in text box
					if itemSize.Kilobytes() > 63:
						pushType = typeId['file']
						itemFname = "Pushed Text"
						itemFext = "txt"

					else:
						# if its greater than 5, might be a txt file being interpreted as text 
						# let user decide
						if itemSize.Kilobytes() > 5:
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
					typeMenu = Menu(
							prompt=text,
							[
								"Text",
								"Link/URL",
								"File",
								"View Item",
							]
						)

					if typeMenu.opt("Text"):
						# set the push type to text
						pushType = typeId['note']
						item = Text(item)

					elif typeMenu.opt("Link/URL"):
						pushType = typeId['link']

					elif typeMenu.opt("File"):
						# filename might be confusing give users a chance to rename
						cm = Menu(prompt=f"Filename: {itemFname}.{itemFext}", options=["Accept Name", "Change Name", "Back"])

						if cm.opt("Change Name"):
							res = AskForInput(Input.Text, prompt="Format: {filename}.{ext}", multipleLines=False)
							matches = MatchText("(.*)\\.(.*)", res)
							itemFname = GetMatchGroupAt(0, matches)
							itemFext = GetMatchGroupAt(1, matches)

						if cm.opt("Back"):
							exitLoop = FALSE

						filename = AskForInput
						# if the item mime type is none, then we have an errror
						if Mime[itemFext] is not None:
							pushType = typeId['file']
						else
							itemErrorCode = 5
							itemErrorMsg = f"Extension: {itemFext}"

					elif typeMenu.opt("View Item"):
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
				itemFext = GetFileDetails("File Extension", item)

			goodFileSize = TRUE

			if GetFileDetails("File Size", item).MegaBytes() > 25:
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
				UploadResponse = GetContentsOfURL(
						PushCall['upload_req_url'],
						method=POST,
						headers={
							"Access-Token" : PushCall['accesstoken']
						},
						type=JSON,
						body={
							'file_name': text,
							'file_type': itemMimeType
						}
					)

				text = UploadResponse['error']

				if text is not None:
					itemErrorCode = 6
					itemErrorMsg = text

				else
					GetContentsOfURL(
						UploadResponse['upload_url'],
						method=POST,
						headers={
							"Access-Token" : PushCall['accesstoken']
						},
						type=FORM,
						body={
							'file': item
						}
					)

					itemPushBody['type'] = 'file'
					itemPushBody['file_name'] = UploadResponse['file_name']
					itemPushBody['file_type'] = UploadResponse['file_type']
					itemPushBody['file_url'] = UploadResponse['file_url']

		# push the item
		if itemErrorCode == 0:
			res = GetContentsOfURL(
					PushCall['push_url'],
					method=POST,
					headers={
						"Access-Token" : PushCall['accesstoken']
					},
					type=JSON,
					body=itemPushBody
				)

			text = res['error']

			if text is not None:
				itemErrorCode = 6
				itemErrorMsg = text


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



