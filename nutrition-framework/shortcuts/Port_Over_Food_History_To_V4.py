'''
New Food history format:
{
    'YYYY-MM-DD': {
        'HH-MM': [{
            'food': ...,
            'servings': ...,
            'cals': ...,
        },
        ...
        ...
        ],
        
        # can either be dictionary if only one item or list of dictionaries if more
    }
}

For: "1x Fried egg (90.16 kCal"
([0-9][0-9]*[\.]*[0-9]*)x (.*) \(([0-9][0-9]*[\.]*[0-9]*) kCal\)

For "1 [Chicken Noodles Super Pack (430 Kcal)]"
([0-9][0-9]*[\.]*[0-9]*) \[(.*) \(([0-9][0-9]*[\.]*[0-9]*) Kcal\)\]
'''

newHistory = Dictionary()
history = Dictionary(GetFile("FLS/History/foodHistoryDix.txt"))

regex1 = text("([0-9][0-9]*[\.]*[0-9]*)x (.*) \(([0-9][0-9]*[\.]*[0-9]*) [kK][cC]al\)")
regex2 = text("([0-9][0-9]*[\.]*[0-9]*) \[(.*) \(([0-9][0-9]*[\.]*[0-9]*) [kK][cC]al\)\]")

for repeatItem in history.keys():
    dayKey = repeatItem
    text = history[dayKey]
    dayDix = Dictionary(text)
    newDayDix = newHistory[dayKey]

    if newDayDix is None:
        newDayDix = Dictionary()
    
    for repeatItem2 in FilterFiles(dayDix.keys() where=['Name' != "SAMPLE"]):
        timeKey = repeatItem2
        logText = dayDix[timeKey]
        newTimeList = newDayDix[timeKey]

        # if it does not have any value, we will add it to the variable

        for log in logText.splitByNewLines():
            logGroup = []

            # 0 -> servings
            # 1 -> food name
            # 2 -> calories

            # try the first regex
            logGroup = GetAllGroups( MatchText(log, regex1) )
            if Count(logGroup) == 0:
                # try the other regex
                logGroup = GetAllGroups( MatchText(log, regex2) )
                if Count(logGroup) == 0:
                    logGroup = [1, log, 0]

            totalCals = RoundNumber(logGroup[2])
            servings = Number(logGroup[0])

            dix = {
                'servings': servings,
                'food': logGroup[1],
                'cals': totalCals
            }

            newTimeList.append(dix)

        # set in the new day dix
        newDayDix[timeKey] = newTimeList

    # set the new day key
    newHistory[dayKey] = newDayDix

    # save it to the file
    SaveFile(newHistory, "FLS/History/foodHistory.json", overwrite=True)

