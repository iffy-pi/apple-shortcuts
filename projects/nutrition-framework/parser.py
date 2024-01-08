import json
import re



regex1 = r"([0-9][0-9]*[\.]*[0-9]*)x (.*) \(([0-9][0-9]*[\.]*[0-9]*) [kK][cC]al\)"
regex2 = r"([0-9][0-9]*[\.]*[0-9]*) \[(.*) \(([0-9][0-9]*[\.]*[0-9]*) [kK][cC]al\)\]"

with open('foodHistoryDix.txt', 'r') as file:
	history = json.load(file)


newHistory = {}
for dayKey in history.keys():
	if dayKey == "SAMPLE":
		continue

	dayDix = json.loads(history[dayKey])
	newDayDix = newHistory.get(dayKey)

	if newDayDix is None:
		newDayDix = {}

	for timeKey in dayDix.keys():
		logText = dayDix[timeKey]
		newTimeList = newDayDix.get(timeKey)

		if newTimeList is None:
			newTimeList = []

		for log in logText.split('\n'):
			logGroup = []
			res = re.search( regex1, log )
			if res is None:
				res = re.search(regex2, log)
				if res is None:
					logGroup = [1, log, 0]
				else:
					logGroup = list(res.groups())
			else:
				logGroup = list(res.groups())

			totalCals = int(round(float(logGroup[2]), 1))

			try:
				servings = int(logGroup[0])
			except ValueError:
				servings = float(logGroup[0])

			dix = {
				'servings': servings,
				'food': logGroup[1],
				'cals': totalCals
			}

			print(f'Processed {dayKey} {timeKey} {servings}x {logGroup[1]} ({totalCals} cals)')

			newTimeList.append(dix)

		newDayDix[timeKey] = newTimeList;

	newHistory[dayKey] = newDayDix



with open('foodHistoryDix.json', 'w') as file:
	json.dump(newHistory, file)



def history():
	# certain day, between, past week, past month, all time

	# endDate date, 

	# certai day
	startDate = date
	endDate = AddToDate(startDate, days=1)

	# between
	startDate = input(Date)
	endDate = AddToDate(input(Date), days=1)

	# past week
	startDate = SubFromDate(curDate, days=7 )
	endDate = AddToDate(curDate, mins=1)

	# past month
	startDate = SubFromDate(curDate, months=1 )
	endDate = AddToDate(curDate, mins=1)

	# all time 
	# just go through all the keys

