'''
Framework: Nutrition (id = 4)
ID:  14
Ver: 1.01
'''

# Clear the food backlog and food history cache

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
if ShortcutInput is not None:
    $IFRESULT = ShortcutInput
else
    $IFRESULT = { 'cache': True, 'backlog': True }
params = Dictionary($IFRESULT)

TRUE = 1
FALSE = 0

res = GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json")
shortcutNames = Dictionary(res)

hasHealthApp = FALSE
file = GetFile(From='Shortcuts', f"{storage}/Other/env.json")
if file['hasHealthApp'] is not None:
    hasHealthApp = file['hasHealthApp']

if params['backlog'] is not None:
    # clearing the backlog
    if hasHealthApp == TRUE:
        file = GetFile(From='Shortcuts', f"{storage}/Other/backlog.json", errorIfNotFound=False)
        if file is not None:
            # clear items by logging them
            dix = Dictionary(file)
            for item in dix['backlog']:
                RunShortcut(shortcutNames["Log Algorithm"], input=item)

            # erase the backlog
            file = GetFile(From='Shortcuts', f"{storage}/Other/backlog.json")
            DeleteFile(file, deleteImmediately=True)


if params['cache'] is not None:
    # clear the cache
    file = GetFile(From='Shortcuts', f"{storage}/History/foodHistoryCache.json", errorIfNotFound=False)
    if file is not None:
        dix = Dictionary(file)
        histCache = dix['cache']
        
        file = OpenFile("FLS/History/foodHistory.json", errorIfNotFound=False)
        if file is not None:
            $IFRESULT = file
        else:
            $IFRESULT = {}
        history = Dictionary( $IFRESULT )

        # add items in cache to history
        for item in histCache:
            dayKey = item['date']
            timeKey = item['time']

            dayDix = history[dayKey]
            if history[dayKey] is None:
                $IFRESULT = history[dayKey]
            else
                $IFRESULT = {}
            dayDix = $IFRESULT

            timeList = dayDix[timeKey]

            timeList.append({
                    'food': item['food'],
                    'servings': item['servings'],
                    'cals': item['cals'],
                    'id': item['id']
                })

            dayDix[timeKey] = timeList
            history[dayKey] = dayDix

        # save our history
        SaveFile(To='Shortcuts', history, f"{storage}/History/foodHistory.json", overwrite=True)

        # clear our cache by deleting the file
        file = GetFile(From='Shortcuts', f"{storage}/History/foodHistoryCache.json")
        DeleteFile(file, deleteImmediately=True)


