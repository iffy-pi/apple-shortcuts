storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))
if ShortcutInput is not None:
    IFRESULT = ShortcutInput
else
    IFRESULT = { 'cache': True, 'backlog': True }
params = Dictionary(IFRESULT)

TRUE = 1
FALSE = 0

res = GetFile(f"{storage}/Other/shortcutNames.json")
shortcutNames = Dictionary(res)

hasHealthApp = FALSE
matches = MatchText(GetDeviceDetails("Model"), "(iPhone)")
if matches is not None:
    hasHealthApp = TRUE

if params['backlog'] is not None:
    # clearing the backlog
    if hasHealthApp == TRUE:
        file = GetFile(f"{storage}/Other/backlog.json", errorIfNotFound=False)
        if file is not None:
            # clear items by logging them
            dix = Dictionary(file)
            for item in dix['backlog']:
                RunShortcut(shortcutNames["Log Algorithm"], input=item)

            # erase the backlog
            file = GetFile(f"{storage}/Other/backlog.json")
            DeleteFile(file, deleteImmediately=True)

        else:
            if reqBacklogClear == TRUE:
                # if user req clear backlog let them no there was nothing to clear
                ShowAlert("There are no foods in the backlog")

if params['cache'] is not None:
    # clear the cache
    file = GetFile(f"{storage}/History/foodHistoryCache.json", errorIfNotFound=False)
    if file is not None:
        dix = Dictionary(file)
        histCache = dix['cache']
        
        file = OpenFile("FLS/History/foodHistory.json", errorIfNotFound=False)
        if file is not None:
            IFRESULT = file
        else:
            IFRESULT = {}
        history = Dictionary( IFRESULT )

        for item in histCache:
            dayKey = item['date']
            timeKey = item['time']

            dayDix = history[dayKey]
            if history[dayKey] is None:
                IFRESULT = history[dayKey]
            else
                IFRESULT = {}
            dayDix = IFRESULT

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
        SaveFile(history, f"{storage}/History/foodHistory.json", overwrite=True)

        # clear our cache by deleting the file
        file = GetFile(f"{storage}/History/foodHistoryCache.json")
        DeleteFile(file, deleteImmediately=True)


