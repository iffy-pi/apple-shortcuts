# SHORTCUT: https://www.icloud.com/shortcuts/45f7cb77a657436ba31aabe32615cf9a
TRUE = 1
FALSE = 0
saveFile = FALSE
mainBreakLoop = FALSE

dataFile = 'Plant Waterings/data.json'
previousDataFile = 'Plant Waterings/data.previous.json' # Stores data file before last made change
backupDataFile = 'Plant Waterings/data-backup.json' # Used for manual backups
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
		$IFRESULT = f'''
		Plant Manager ({count} plants)
		{temp}
		'''
	else:
		$IFRESULT = f'Plant Manager ({count} plants)'
	#endif

	Menu($IFRESULT):
		case 'Water Plant':
			groupWateringDate = "-"
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
			#endif
			
			for plant in selected:
				waterings = plantInfo[plant]['waterings']
				if Count(waterings) > 0:
					prevWateringDate = GetItemFromList(waterings, lastitem=True)
					days = GetTimeBetweenDates(prevWateringDate, today, days=True)
					
					$IFRESULT = f'''
					Enter watering date for {plant}.
					{plant} was last watered on {prevWateringDate} ({days} days ago).
					'''
				else:
					$IFRESULT = f'Enter watering date for {plant}!'
				#endif
				
				if groupWateringDate is None:
					date = AskForInput(Input.Date, prompt=$IFRESULT)
					wateringDate = Text(date.format(date=short, time=None))
				else:
					wateringDate = groupWateringDate
				#endif

				if prevWateringDate is not None:
					if wateringDate != prevWateringDate:
						AddToVariable(waterings, wateringDate)
					#endif
				else:
					AddToVariable(waterings, wateringDate)
				#endif

				waterings = FilterFiles(waterings, sortBy='Name', order='A to Z')
				plantDix = plantInfo[plant]
				plantDix['waterings'] = waterings
				plantInfo[plant] = plantDix
				

				$REPEATRESULTS.append(f"{plant}'s watering has been updated with new date: {wateringDate}")
			#endfor

			notification = TEXT($REPEATRESULTS)
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
						$REPEATRESULTS.append(f'{curWateringDate}')
					else:
						# Append the days between
						daysBetweenList.append(daysBetween)
						$REPEATRESULTS.append(f'''
							    | {daysBetween} days
							{curWateringDate}
							''')
					#endif
				#endfor

				average = Round(CalculateStatistics('average', daysBetweenList), 'tenths')
				appendix = f'({average} day average)'

				days = GetTimeBetweenDates(prevWateringDate, today, days=True)
				$IFRESULT = f'''
					{$REPEATRESULTS}
						| {between} days and counting
					🕥 {average} day average
				'''
			else:
				appendix = ''
				$IFRESULT = f'No watering data for {plant}!'
			#endif
			
			historyText = f'''
				{plant} Watering History {apppendix}
				{separator}
				{$IFRESULT}
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
			#endfor

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
					#endif
				#endif
			#endfor

			updatedText = Text(plantInfo).replace(f'"{plant}":', f'"{newName}":')
			plantInfo = Dictionary(plantInfo)

			notification = f'Plant name changed from "{plant}" to "{newName}"', title='Plant name changed'
			saveFile = TRUE

		case 'Edit Watering Dates':
			plantNames = FilterFiles(plantInfo.keys, sortBy='Name', order='A to Z')
			plant = ChooseFromList(plantNames, prompt='Select plant to edit watering dates for')

			waterings = plantInfo[plant]['waterings']

			for wt in waterings:
				$REPEATRESULTS.append(Text(Date(wt).format(date='long', time='None')))
			#endfor

			newWateringList = $REPEATRESULTS

			wateringsText = Text(newWateringList)
			updatedListText = AskForInput(Input.Text, 'Edit Watering Dates:', multipleLines=True, default=newWateringList)

			for wt in SplitText(updatedListText, byNewLines=True):
				$REPEATRESULTS.append(Text(Date(wt).format(date='short'), time='None'))
			#endfor

			waterings = $REPEATRESULTS
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
			#endfor

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
					#endif
				#endfor
				AddToVariable(table, row)
			#endfor

			data = f'''
				{header}
				{table}
			'''
			Share(data)

		case 'Toggle Summary Sort':
			if sortSummaryByName == TRUE:
				sortSummaryByName = FALSE
				$IFRESULT = 'Watering Summary will be sorted by days since last watering'
			else:
				sortSummaryByName = TRUE
				$IFRESULT = 'Watering Summary will be sorted by plant names'
			#endif

		case 'Other Features':
			Menu('Other Features'):
				case 'Make backup':
					SaveFile(plantInfo, To='Shortcuts', backupDataFile, overwrite=True)
					$MENURESULT = 'Backup created!'

				case 'Restore backup':
					file = GetFile(From='Shortcuts', backupDataFile, errorIfNotFound=True)
					plantInfo = Dictionary(file)
					SaveFile(plantInfo, To='Shortcuts', dataFile, overwrite=True)
					$MENURESULT = 'Backup restored!'

				case 'Toggle Summary Sort':
					if sortSummaryByName == TRUE:
						sortSummaryByName = FALSE
						$IFRESULT = 'Watering Summary will be sorted by days since last watering'
					else:
						sortSummaryByName = TRUE
						$IFRESULT = 'Watering Summary will be sorted by plant names'
					#endif
					$MENURESULT = $IFRESULT
			#endmenu
			notification = $MENURESULT

		case 'Exit':
			StopShortcut()
	#endmenu

	if saveFile == TRUE:
		dix = Dictionary(GetFile(From='Shortcuts', dataFile, errorIfNotFound=True))
		SaveFile(dix, To='Shortcuts', previousDataFile, overwrite=True)

		SaveFile(plantInfo, To='Shortcuts', dataFile, overwrite=True)
	#endif
#endfor