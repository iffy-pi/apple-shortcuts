# SHORTCUT LINK: https://www.icloud.com/shortcuts/364c6adcc4db46e6b609785c307c5a34
TRUE = 1
FALSE = 0
saveFile = FALSE
mainBreakLoop = FALSE

sortSummaryByName = GetNumbersFromInput(ShortcutInput())

symbolsText = '''{"0":"🥶","NaN":"❔","0.01":"🥶","0.02":"🥶","0.03":"🥶","0.04":"🥶","0.05":"🥶","0.06":"🥶","0.07":"🥶","0.08":"🥶","0.09":"🥶","0.1":"🥶","0.11":"🥶","0.12":"🥶","0.13":"🥶","0.14":"🥶","0.15":"🥶","0.16":"🥶","0.17":"🥶","0.18":"🥶","0.19":"🥶","0.2":"🥶","0.21":"🥶","0.22":"🥶","0.23":"🥶","0.24":"🥶","0.25":"🥶","0.26":"🥶","0.27":"🥶","0.28":"🥶","0.29":"🥶","0.3":"😊","0.31":"😊","0.32":"😊","0.33":"😊","0.34":"😊","0.35":"😊","0.36":"😊","0.37":"😊","0.38":"😊","0.39":"😊","0.4":"😊","0.41":"😊","0.42":"😊","0.43":"😊","0.44":"😊","0.45":"😊","0.46":"😊","0.47":"😊","0.48":"😊","0.49":"😊","0.5":"😊","0.51":"😊","0.52":"😊","0.53":"😊","0.54":"😊","0.55":"😊","0.56":"😊","0.57":"😊","0.58":"😊","0.59":"😊","0.6":"😊","0.61":"😊","0.62":"😊","0.63":"😊","0.64":"😊","0.65":"😊","0.66":"😊","0.67":"😊","0.68":"😊","0.69":"😊","0.7":"😊","0.71":"😊","0.72":"😊","0.73":"😊","0.74":"😊","0.75":"😊","0.76":"😊","0.77":"😊","0.78":"😊","0.79":"😊","0.8":"🥵","0.81":"🥵","0.82":"🥵","0.83":"🥵","0.84":"🥵","0.85":"🥵","0.86":"🥵","0.87":"🥵","0.88":"🥵","0.89":"🥵","0.9":"🥵","0.91":"🥵","0.92":"🥵","0.93":"🥵","0.94":"🥵","0.95":"🥵","0.96":"🥵","0.97":"🥵","0.98":"🥵","0.99":"🥵"}'''
symbols = Dictionary(symbolsText)

dataFile = 'Plant Waterings/data.json'
separator = '------------------------------------------------------'
file = GetFile(From='Shortcuts', dataFile, errorIfNotFound=False)
plantInfo = Dictionary(file)
today = Date(current)

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
				$IFRESULT2 = 👹 # devil symbol
			else:
				# If we log a watering date ahead of the current day, we can get negative numbers
				# Regex expression just evaluates neagtive numbers to NaN which pulls a question mark from the symbol dictionary
				updatedText = Text(frac).replace('-.*', 'NaN', regex=True, caseSensitive=False)
				$IFRESULT2 = symbols[updatedText]
			#endif
			
			fracStr = $IFRESULT2
		else:
			# No previous watering information so no analysis can be performed
			fracStr = '🔄' # question mark symbol
			prevDaysStr = ''
		#endif

		# Frac str is the symbol for the plant
		if sortSummaryByName == TRUE:
			$IFRESULT1 = f'{plant}|{plant} - {fracStr} {days} days - {prevWateringDate} {prevDaysStr}'		
		else:
			$IFRESULT1 =  f'{days}|{fracStr} {days} days - {plant} - {prevWateringDate} {prevDaysStr}'
		#endif			
			
		$IFRESULT = $IFRESULT1
	else:
		if sortSummaryByName == TRUE:
			$IFRESULT1 = f'|{plant} - ❔ N/A - N/A'
		else:
			$IFRESULT1 = f'|❔ N/A - {plant} - N/A'
		#endif
		$IFRESULT = $IFRESULT1
	#endif
	
	$REPEATRESULTS.append($IFRESULT)
#endfor

for e in FilterFiles(results, sortBy='Name', order='Z to A'):
	splitText = SplitText(e, custom='|')
	$REPEATRESULTS.append(GetItemFromList(splitText, lastitem=True))
#endfor

text = f'''
	{$REPEATRESULTS}
'''
StopShortcut(output=text)