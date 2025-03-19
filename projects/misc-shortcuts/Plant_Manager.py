TRUE = 1
FALSE = 0
saveFile = FALSE
mainBreakLoop = FALSE

dataFile = 'Plant Waterings/data.json'
backupDataFile = 'Plant Waterings/data.backup.json'
notification = ''
separator = '------------------------------------------------------'
sortSummaryByName = FALSE


for i in range(15):
	file = GetFile(From='Shortcuts', dataFile, errorIfNotFound=False)
	plantInfo = Dictionary(file)
	count = Count(plantInfo.keys())
	today = Date(current)

	if f'"{notification}"' != '""':
		temp = notification
		notification = ''
		IFRESULT = f'''
		Plant Manager ({count} plants)
		{temp}
		'''
	else:
		IFRESULT = f'Plant Manager ({count} plants)'


	Menu(IFRESULT):
		case 'Water Plant':
			plantNames = FilterFiles(plantInfo.keys, sortBy='Name', order='A to Z')
			selected = ChooseFromList(plantNames, prompt='Select plant(s)', multiple=True)

			if Count(selected) > 1:
				plants = CombineText(selected, custom=', ')
				text = f'''
					Select watering date for
					{plants}:
				'''
				date = AskForInput(Input.Date, prompt=text)
				groupWateringDate = Text(date.format(date=short, time=None))

			
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
				
				if groupWateringDate is None:
					date = AskForInput(Input.Date, prompt=IFRESULT)
					wateringDate = Text(date.format(date=short, time=None))
				else:
					wateringDate = groupWateringDate

				if prevWateringDate is not None:
					if wateringDate != prevWateringDate:
						AddToVariable(waterings, wateringDate)
				else:
					AddToVariable(waterings, wateringDate)


				waterings = FilterFiles(waterings, sortBy='Name', order='A to Z')
				plantDix = plantInfo[plant]
				plantDix['waterings'] = waterings
				plantInfo[plant] = plantDix
				

				REPEATRESULTS.append(f"{plant}'s watering has been updated with new date: {wateringDate}")

			notification = TEXT(REPEATRESULTS)
			saveFile = True


		case 'View Summary':
			text = RunShortcut('Plant Watering Summary', input=sortSummaryByName)
			text = f'''
			Plant Watering Summary - {CurrentDate()}
			{separator}
			text
			'''

		case 'Plant Watering History':
			plantNames = FilterFiles(plantInfo.keys, sortBy='Name', order='A to Z')
			plant = ChooseFromList(plantNames, prompt='Select a plant')

			daysBetweenList = []

			waterings = plantInfo[plant]['waterings']
			if Count(waterings) > 0:
				prevWateringDate = GetItemFromList(waterings, firstitem=True)

				# Constructs a list where the days between each watering date is shown e.g
				# March 1
				#   3 days
				# March 4

				for curWateringDate in waterings:
					daysBetween = GetTimeBetweenDates(prevWateringDate, curWateringDate, days=True)
					prevWateringDate = curWateringDate
					if daysBetween == 0:
						# They are the same date, don't append any days
						# Basically to handle the first iteration where curWateringDate == prevWateringDate
						REPEATRESULTS.append(f'{curWateringDate}')
					else:
						# Append the days between
						daysBetweenList.append(daysBetween)
						REPEATRESULTS.append(f'''
							    | {daysBetween} days
							{curWateringDate}
							''')

				average = Round(CalculateStatistics('average', daysBetweenList), 'tenths')
				appendix = f'({average} day average)'

				days = GetTimeBetweenDates(prevWateringDate, today, days=True)
				IFRESULT = f'''
					{REPEATRESULTS}
						| {between} days and counting
					🕥 {average} day average
				'''
			else:
				appendix = ''
				IFRESULT = f'No watering data for {plant}!'
			
			historyText = f'''
				{plant} Watering History {apppendix}
				{separator}
				{IFRESULT}
			'''	

			ShowResult(historyText)

		case 'Add Plant':
			plant = AskForInput(Input.text, "What's the plant name?", allowMultipleLines=False)
			dix = {
				'waterings': []
			}
			plantInfo[plant] = dix
			
			notification = f'Hi {plant}! Welcome to the family :)'
			saveFile = TRUE

		case 'Remove Plant':
			plantNames = FilterFiles(plantInfo.keys, sortBy='Name', order='A to Z')
			plant = ChooseFromList(plantNames, prompt='Which plant would you like to remove?')
			newDix = {}
			filteredPlants = FilterFiles(plantInfo.keys, where=('Name' != plant))
			for pl in filteredPlants:
				newDix[pl] = plantInfo[pl]

			plantInfo = newDix
			notification = f'Goodbye {plant}. You will be missed :(', title="Plant Removed"
			saveFile = TRUE


		case 'Edit Plant Name':
			plantNames = FilterFiles(plantInfo.keys, sortBy='Name', order='A to Z')
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

			notification = f'Plant name changed from "{plant}" to "{newName}"', title='Plant name changed'
			saveFile = TRUE

		case 'Edit Wateing Dates':
			plantNames = FilterFiles(plantInfo.keys, sortBy='Name', order='A to Z')
			plant = ChooseFromList(plantNames, prompt='Select plant to edit watering dates for')

			waterings = plantInfo[plant]['waterings']

			for wt in waterings:
				REPEATRESULTS.append(Text(Date(wt).format(date='medium', time='None')))

			newWateringList = REPEATRESULTS

			wateringsText = Text(newWateringList)
			updatedListText = AskForInput(Input.Text, 'Edit Watering Dates:', multipleLines=True, default=newWateringList)

			for wt in SplitText(updatedListText, byNewLines=True):
				REPEATRESULTS.append(Text(Date(wt).format(date='short'), time='None'))

			waterings = REPEATRESULTS
			waterings = FilterFiles(waterings, sortBy='Name', order='A to Z')

			plantDix = plantInfo[plant]
			plantDix['waterings'] = waterings
			plantInfo[plant] = plantDix

			notification = f'Watering Dates for {plant} were successfully edited!'
			saveFile = True

		case 'Export Data as CSV':
			plantNames = FilterFiles(plantInfo.keys, sortBy='Name', order='A to Z')
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
					if rowIndex <= count:
						watering = plantInfo[plant]['watering']
						curDate = GetItemFromList(watering, index=rowIndex)
						line = f'{curDate},{line}'
				AddToVariable(table, row)

			data = f'''
				{header}
				{table}
			'''
			Share(data)

		case 'Toggle Summary Sort':
			if sortSummaryByName == TRUE:
				sortSummaryByName = FALSE
				IFRESULT = 'Watering Summary will be sorted by days since last watering'
			else:
				sortSummaryByName = TRUE
				IFRESULT = 'Watering Summary will be sorted by plant names'

		case 'Exit':
			StopShortcut()

	if saveFile == TRUE:
		SaveFile(plantInfo, To='Shortcuts', dataFile, overwrite=True)
		SaveFile(plantInfo, To='Shortcuts', backupDataFile, overwrite=True)