dataFile = 'Plant Waterings/data.json'
TRUE = 1
FALSE = 0


for i in range(15):
	file = GetFile(From='Shortcuts', dataFile, errorIfNotFound=False)
	plantInfo = Dictionary(file)
	plantNames = plantInfo.keys()
	today = Date(current)
	Menu('Main Menu'):
		case 'Water Plant':
			plantNames = FilterFiles(plantInfo.keys, sortBy='A to Z')
			selected = ChooseFromList(plantNames, prompt='Select plant(s)', multiple=True)
			for plant in selected:
				waterings = plantInfo[plant]['waterings']
				if Count(waterings) > 0:
					prevWateringDate = GetItemFromList(waterings, lastitem=True)
					days = GetTimeBetweenDates(prevWateringDate, today, days=True)
					
					IFRESULT = f'''
					Enter watering date for {plant}.
					{plant} was last watered on {prevWateringDate} ({days} days ago).
					'''
				else:
					IFRESULT = f'Enter watering date for {plant}!'
				
				wateringDate = f'{AskForInput(Input.Date, prompt=IFRESULT).format(date=medium, time=None)}'
				
				AddToVariable(waterings, wateringDate)
				plantInfo = SetDictionaryValue(plantInfo, f'{plant}.waterings', waterings)

				Notification(f"{plant}'s watering has been updated with new date: {wateringDate}", title="Plant has been watered")

		case 'Watering History for Plant':
			plantNames = FilterFiles(plantInfo.keys, sortBy='A to Z')
			plant = ChooseFromList(plantNames, prompt='Select a plant')
			waterings = plantInfo[plant]['waterings']
			if Count(waterings) > 0:
				prevWateringDate = GetItemFromList(waterings, firstitem=True)

				for curWateringDate in waterings:
					daysBetween = GetTimeBetweenDates(prevWateringDate, curWateringDate, days=True)
					prevWateringDate = curWateringDate
					REPEATRESULTS.append(f'{curWateringDate} ({daysBetween} days)')

				days = GetTimeBetweenDates(prevWateringDate, today, days=True)
				IFRESULT = f'''
					{REPEATRESULTS}
				'''
			else:
				IFRESULT = 'This plant has never been watered!'
			
			ShowResult(IFRESULT)

		case 'Add Plant':
			plant = AskForInput(Input.text, "What's the plant name?", allowMultipleLines=False)
			dix = {
				'waterings': []
			}
			plantInfo[plant] = dix
			Notification(f'Hi {plant}! Welcome to the family :)', title="Plant Added")

		case 'Edit Plant Name':
			plantNames = FilterFiles(plantInfo.keys, sortBy='A to Z')
			plant = ChooseFromList(plantNames, prompt='Select plant to edit')

			breakLoop = FALSE
			for i in range(5):
				if breakLoop == FALSE:
					newName = AskForInput(Input.Text, f'Enter new plant name for {plant}')
					if Filter(plantInfo.keys, where=['Name' == newName]) is None:
						breakLoop = TRUE
					else:
						ShowAlert(f'There is already a plant named "{newName}". Please select a different name.')

			updatedText = Text(plantInfo).replace(f'"{plant}":', f'"{newName}":')
			plantInfo = Dictionary(plantInfo)

			ShowNotification(f'Plant name changed from "{plant}" to "{newName}"', title='Plant name changed')


		case 'Remove Plant':
			plantNames = FilterFiles(plantInfo.keys, sortBy='A to Z')
			plant = ChooseFromList(plantNames, prompt='Which plant would you like to remove?')
			newDix = {}
			filteredPlants = FilterFiles(plantInfo.keys, where=('Name' != plant))
			for pl in filteredPlants:
				newDix[pl] = plantInfo[pl]

			plantInfo = newDix
			Notification(f'Goodbye {plant}. You will be missed :(', title="Plant Removed")

		case 'View Summary Information':
			# Print all the summary information about the plant
			results = []
			for plant in plantInfo.keys:
				waterings = plantInfo[plant]['waterings']
				if Count(waterings) > 0:
					prevWateringDate = GetItemFromList(waterings, lastitem=True)
					days = GetTimeBetweenDates(prevWateringDate, today, days=True)
					IFRESULT = f'{days}|{days} days - {plant} - {prevWateringDate}'
				else:
					IFRESULT = f'0|{days} days - N/A - N/A'
				
				AddToVariable(results, IFRESULT)

			for e in FilterFiles(results, sortBy='Z to A'):
				splitText = SplitText(e, custom='')
				REPEATRESULTS.append(GetItemFromList(splitText, lastitem=True))

			text = f'''
				Plant Watering Summary
				{REPEATRESULTS}
			'''
			ShowResult(text)

		case 'Export Data...':
			plantNames = FilterFiles(plantInfo.keys, sortBy='A to Z')
			selected = ChooseFromList(plantNames, 'Select plants for export')
			plantCounts = {}
			header = ''
			for plant in selected:
				header = f'{plant},{header}'
				plantCounts[plant] = Count(plantInfo[plant]['waterings'])

			maxCount = CalculateStatistics('maximum', plantCounts.values)

			table = []

			for rowIndex in range(maxCount): # starts at 1
				row = ''
				for plant in selected:
					count = plantCounts[plant]
					if repeatIndex <= count:
						watering = plantInfo[plant]['watering']
						curDate = GetItemFromList(watering, index=i)
						line = f'{curDate},{line}'
				AddToVariable(table, row)

			data = f'''
				{header}
				{table}
			'''
			Share(data)

		case 'Exit':
			StopShortcut()


	SaveFile(plantInfo, To='Shortcuts', dataFile, overwrite=True)