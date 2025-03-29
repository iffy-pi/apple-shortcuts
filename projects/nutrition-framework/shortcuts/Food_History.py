'''
Framework: Nutrition (id = 4)
ID:  22 
Ver: 1.1
'''

# View food history through different options

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))

file = GetFile(From='Shortcuts', f"{storage}/History/foodHistory.json")
if file is not None:
    $IFRESULT = file
else:
    $IFRESULT = {}

history = Dictionary($IFRESULT)

# get the foods logged today
today = CurrentDate()

dayDix = history[ today.format(custom="yyyy-MM-dd") ]
if dayDix is not None:
    keys = FilterFiles(dayDix[keys], sortBy="Name", AtoZ=True)
    for timeKey in keys:
        timeList = dayDix[timeKey]
        for logItem in timeList:
            text = f'''{timeKey}: {logItem['servings']}x {logItem['food']} ({logItem['cals']} kCals)'''
            todaysLogs.append(text)

# Show foods logged today in menu prompt and then continue
if Count(todaysLogs) > 0:
    $IFRESULT = f'''
        {Strings['history.foods.today']}
        {todaysLogs}
    '''
else:
    $IFRESULT = Strings['history.foods.today.none']

prompt = $IFRESULT

Menu(prompt=prompt):
    case Strings['history.menu.moreopts']:
        Menu(prompt=Strings['history.menu.moreopts']):
            case Strings['history.query.day']:
                start = AskForInput(Input.Date, prompt=Strings['history.day.date'])
                end = AddToDate(start, days=1)

            case Strings['history.query.inlast']:
                # allow the user to specify how much to subtract from the date
                # Users can configure which options they would like
                date = SubFromDate(today, days=AskEachTime())
                start = AddToDate(date, days=1)
                end = AddToDate(today, days=1)

            case Strings['history.query.between']:
                start = AskForInput(Input.Date, prompt=Strings['history.window.start'])
                end = AddToDate(AskForInput(Input.Date), days=1, prompt=Strings['history.window.end'])

            case Strings['history.query.all']:
                useDateList = TRUE
                # go through all the keys
                # reverse because we want the latest ones first
                dateList = FilterFiles(history.keys(), sortBy=(Name, ZtoA))

            case 'Back': # TODO translate this
                StopShortcut()

        if useDateList == TRUE
            $IFRESULT = Count(dateList)
        else:
            $IFRESULT = TimeBetweenDates(start, end, inDays=True)
        repeats = $IFRESULT


        for repeatIndex in range( repeats ):
            if useDateList == TRUE
                $IFRESULT = dateList.getItemAtIndex(repeatIndex)
            else:
                # shortcuts are one indexes, so subtract by 1 and add to start
                # doing it so we get latest date first
                res = repeats - repeatIndex
                res = AddToDate(start, res)
                $IFRESULT = Text(res.format(custom="yyyy-MM-dd"))

            dayKey = $IFRESULT
            dayDix = history[dayKey] 

            if dayDix is not None:
                resultsForDay = []
                keys = FilterFiles(dayDix.keys(), sortBy=(Name, ZtoA))

                # using this specific format as it remove ambiguity when converting from 24 h to 12 h time
                text = Date(f'{timeKey}h').format(custom="h:mm a")
                dispTime = text

                for timeKey in keys:
                    for log in dayDix[timeKey]:
                        resultsForDay.append( 
                            f'{logItem['servings']}x {logItem['food']} ({logItem['cals']} kCals) @ {dispTime}'
                        )
                
                logResults.append(f'''
                        {dayKey.format(date='long')}
                        {resultsForDay}
                    ''')

        # show results of the search
        if logResults is None:
            Alert(Strings['history.nofoods'], title=Strings['history.nofoods.title'], showCancel=False)
            StopShortcut()

        QuickLook(logResults)

    case 'Back': # TODO translate
        StopShortcut()

