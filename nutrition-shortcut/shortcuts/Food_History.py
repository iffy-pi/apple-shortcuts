TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

file = GetFile(f"{storage}/History/foodHistory.json")
if file is not None:
    IFRESULT = file
else:
    IFRESULT = {}

history = Dictionary(IFRESULT)

# show foods today in main menu
today = CurrentDate()

dayDix = history[ today.format(custom="yyyy-MM-dd") ]
if dayDix is not None:
    keys = FilterFiles(dayDix[keys], sortBy="Name", AtoZ=True)
    for timeKey in keys:
        timeList = dayDix[timeKey]
        for logItem in timeList:
            text = f'''{timeKey}: {logItem['servings']}x {logItem['food']} ({logItem['cals']} kCals)'''
            todaysLogs.append(text)


if Count(todaysLogs) > 0:
    IFRESULT = f'''
        Foods eaten today:
        {todaysLogs}
    '''
else:
    IFRESULT = 'You have not eaten any foods today'

prompt = IFRESULT

mainMenu = Menu(prompt=prompt, ['More History Options', 'Exit'])
if mainMenu.opt("More History Options"):
    subMenu = Menu(prompt="History Options", [
            'Foods Logged On Day',
            'Foods Logged Between...',
            'Foods Logged In Past Week',
            'Foods Logged In Past Month',
            'Foods Logged All Time',
            'Exit'
        ])

    if subMenu.opt('Foods Logged On Day'):
        start = AskForInput(Input.Date)
        end = AddToDate(start, days=1)

    elif subMenu.opt('Foods Logged Between...'):
        start = AskForInput(Input.Date)
        end = AddToDate(AskForInput(Input.Date), days=1)

    elif subMenu.opt('Foods Logged In Past Week'):
        start = SubFromDate(today, weeks=1)
        end = AddToDate(today, days=1)

    elif subMenu.opt('Foods Logged In Past Month'):
        start = SubFromDate(today, months=1)
        end = AddToDate(today, days=1)

    elif subMenu.opt('Foods Logged All Time'):
        useDateList = TRUE
        # go through all the keys
        # reverse because we want the latest ones first
        dateList = filter(history.keys(), sortBy=(Name, ZtoA))

    if subMenu.opt('Exit'):
        StopShortcut()

    if useDateList == TRUE
        IFRESULT = Count(dateList)
    else:
        IFRESULT = TimeBetweenDates(start, end, inDays=True)
    repeats = IFRESULT


    for repeatIndex in range( repeats ):
        if useDateList == TRUE
            IFRESULT = dateList.getItemAtIndex(repeatIndex)
        else:
            # shortcuts are one indexes, so subtract by 1 and add to start
            # doing it so we get latest date first
            res = repeats - repeatndex
            res = AddToDate(start, res)
            IFRESULT = Text(res.format(custom="yyyy-MM-dd"))

        dayKey = IFRESULT
        dayDix = history[dayKey] 

        if dayDix is not None:
            resultsForDay = []
            keys = filter(dayDix.keys(), sortBy=(Name, ZtoA))

            text = Date(f'{timeKey}h').format(custom="h:mm a")
            dispTime = text

            for timeKey in keys:
                for log in dayDix[timeKey]:
                    resultsForDay.append( 
                        f'{logItem['servings']}x {logItem['food']} ({logItem['cals']} kCals) @ {dispTime}'
                    )
            
            logResults.append(f'''
                    {dayKey}
                    {resultsForDay}
                ''')

    # show results of the search
    text = f"{logResults}"
    text = SetName(text, "Query Results")
    QuickLook(text)

elif mainMenu.opt("Exit"):
    StopShortcut()
