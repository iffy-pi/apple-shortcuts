TRUE = 1
FALSE = 0
saveFile = FALSE
mainBreakLoop = FALSE

symbolsText = '''{"0":"🥶","NaN":"❔","0.01":"🥶","0.02":"🥶","0.03":"🥶","0.04":"🥶","0.05":"🥶","0.06":"🥶","0.07":"🥶","0.08":"🥶","0.09":"🥶","0.1":"🥶","0.11":"🥶","0.12":"🥶","0.13":"🥶","0.14":"🥶","0.15":"🥶","0.16":"🥶","0.17":"🥶","0.18":"🥶","0.19":"🥶","0.2":"🥶","0.21":"🥶","0.22":"🥶","0.23":"🥶","0.24":"🥶","0.25":"🥶","0.26":"🥶","0.27":"🥶","0.28":"🥶","0.29":"🥶","0.3":"😊","0.31":"😊","0.32":"😊","0.33":"😊","0.34":"😊","0.35":"😊","0.36":"😊","0.37":"😊","0.38":"😊","0.39":"😊","0.4":"😊","0.41":"😊","0.42":"😊","0.43":"😊","0.44":"😊","0.45":"😊","0.46":"😊","0.47":"😊","0.48":"😊","0.49":"😊","0.5":"😊","0.51":"😊","0.52":"😊","0.53":"😊","0.54":"😊","0.55":"😊","0.56":"😊","0.57":"😊","0.58":"😊","0.59":"😊","0.6":"😊","0.61":"😊","0.62":"😊","0.63":"😊","0.64":"😊","0.65":"😊","0.66":"😊","0.67":"😊","0.68":"😊","0.69":"😊","0.7":"😊","0.71":"😊","0.72":"😊","0.73":"😊","0.74":"😊","0.75":"😊","0.76":"😊","0.77":"😊","0.78":"😊","0.79":"😊","0.8":"🥵","0.81":"🥵","0.82":"🥵","0.83":"🥵","0.84":"🥵","0.85":"🥵","0.86":"🥵","0.87":"🥵","0.88":"🥵","0.89":"🥵","0.9":"🥵","0.91":"🥵","0.92":"🥵","0.93":"🥵","0.94":"🥵","0.95":"🥵","0.96":"🥵","0.97":"🥵","0.98":"🥵","0.99":"🥵"}'''
symbols = Dictionary(symbolsText)

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
			# Print all the summary information about the plant
			results = []
			for plant in FilterFiles(plantInfo.keys, sortBy='Name', order='A to Z'):
				waterings = plantInfo[plant]['waterings']

				wateringsCount = Count(waterings)

				if wateringsCount > 0:
					prevWateringDate = GetItemFromList(waterings, lastitem=True)
					days = GetTimeBetweenDates(prevWateringDate, today, days=True)

					if wateringsCount > 1:
						# Gets the second previous watering date
						prevPrevWateringDate = GetItemFromList(waterings, index=wateringsCount-1)
						# Gets the number of days between second previous watering and previous watering
						prevDaysCount= GetTimeBetweenDates(prevPrevWateringDate, prevWateringDate)
						prevDaysStr = f'- {prevDaysCount}'

						# Getting a percentage of how close the plant is to watering by
						# dividing the number of days since the plant was last watered
						# by number of days between the last two plant waterings
						frac = Round(days/prevDaysCount, to='Hundreths')

						# We use this fraction to select the emoji shown with the plant
						if frac > 1:
							IFRESULT1 = 👹 # devil symbol
						else:
							# If we log a watering date ahead of the current day, we can get negative numbers
							# Regex expression just evaluates neagtive numbers to NaN which pulls a question mark from the symbol dictionary
							updatedText = Text(frac).replace('-.*', 'NaN', regex=True, caseSensitive=False)
							IFRESULT1 = symbols[updatedText]

						fracStr = IFRESULT1
				else:
					# No previous watering information so no analysis can be performed
					fracStr = ... # question mark symbol
					prevDaysStr = ''


					# Frac str is the symbol for the plant
					if sortSummaryByName == TRUE:
						IFRESULT1 = f'{plant}|{plant} - {fracStr} {days} days - {prevWateringDate} {prevDaysStr}'		
					else:
						IFRESULT1 =  f'{days}|{fracStr} {days} days - {plant} - {prevWateringDate} {prevDaysStr}'						
					
					IFRESULT = IFRESULT1
				else:
					if sortSummaryByName == TRUE:
						IFRESULT1 = f'|{plant} - ❔ N/A - N/A'
					else:
						IFRESULT1 = f'|❔ N/A - {plant} - N/A'


					IFRESULT = IFRESULT1
				
				AddToVariable(results, IFRESULT)

			for e in FilterFiles(results, sortBy='Name', order='Z to A'):
				splitText = SplitText(e, custom='|')
				REPEATRESULTS.append(GetItemFromList(splitText, lastitem=True))

			text = f'''
				Plant Watering Summary - {CurrentDate()}
				{separator}
				{REPEATRESULTS}
			'''
			ShowResult(text)

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