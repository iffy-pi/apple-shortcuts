TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

checkForUpdates = TRUE
exitAfterQuickLog = TRUE

# load names of the shortcuts
res = GetFile(f"{storage}/Other/shortcutNames.json")
shortcutNames = Dictionary(res)

text = '''
    Calories
    Carbs
    Fat
    Protein
    Sugar
    Fiber
    Monounsaturated
    Polyunsaturated
    Saturated
    Trans
    Sodium
    Cholesterol
    Potassium
    VitA
    VitC
    Calcium
    Iron
'''
SaveFile(text, f"{storage}/Other/nutriKeys.txt")

# if device does not have health app then we will be adding to backlog
# using regex matching
hasHealthApp = FALSE
matches = MatchText(GetDeviceDetails("Model"), "(iPhone)")
if matches is not None:
    hasHealthApp = TRUE

# save the state of the health app to environment
file = GetFile(f"{storage}/Other/env.json", errorIfNotFound=False)
dix = Dictionary(file)
dix['hasHealthAapp'] = hasHealthApp
SaveFile(dix, f"{storage}/Other/env.json", overwrite=True)


# itemsInHistCache = FALSE
# file = GetFile(f"{storage}/History/foodHistoryCache.json", errorIfNotFound=False)
# if file is not None:
#     itemsInHistCache = TRUE
#     dix = Dictionary(file)
#     if Count(dix['cache']) >= 15:
#         # we need to eventually clear the history cache so that it does not bloat in size
#         exitAfterQuickLog = FALSE


# determine if we are checking for updates
# file = GetFile(f"{storage}/Other/lastUpdateCheck.txt", errorIfNotFound=False)
# if file is not None:
#     IFRESULT = file
# else:
#     IFRESULT = SubFromDate(CurrentDate(), weeks=1)

# if TimeBetweenDates(IFRESULT, CurrentDate()) >= 1:
#     checkForUpdates = TRUE


if hasHealthApp == FALSE:
    text = f"Foods logged on {deviceModel} will be added to backlog"

else:
    calsToday = 0
    healthSamples = HealthApp.Find(
            AllHealthSamples,
            whereAllAreTrue=[
                Type="Dietary Energy",
                StartDate=Today,
            ],
            Unit=cal
        )
    _sum = CalculateStatistics(healthSamples, "Sum")
    calsToday = Round (_sum, "hundredths")

    file = GetFile(f"{storage}/Other/backlog.json", errorIfNotFound=False)
    if file is not None:
        IFRESULT = f"You've eaten {calsToday} calories today.\nThere are foods in your backlog."
    else:
        IFRESULT = f"You've eaten {calsToday} calories today."

    IFRESULT = IFRESULT

prompt = IFRESULT

file = GetFile('FLS/Other/foodNotes.txt', errorIfNotFound=False)
if file is not None:
    prompt = f'''
    {prompt}
    Food Notes:
    {file}
    '''

Menu(prompt):
    case "Quick Log":
        # InRecents does not exist!

        for item in  RunShortcut(shortcutNames['Get Recent']):
            CurFood = item

            RunShortcut(shortcutNames["Add Recent"], input=dix)

            text = f"How many servings of {CurFood['Name']}\n(1 serving = {CurFood['Serving Size']})"
            
            # translates to set dictionary value in CurFood and then set dictionary
            CurFood['Servings'] = AskForInput(text, Input.Number, default=1, allowDecimalNumbers=True, allowNegativeNumbers=False)

            dix = {
                'Date': str(Date.CurrentDate)
                'Food': dix(CurFood)
            }
            RunShortcut(shortcutNames["Log Algorithm"], input=dix)

        if exitAfterQuickLog == TRUE:
            StopShortcut()

    case "Log Foods At Time...":
        RunShortcut(shortcutNames["Log Foods At Time"])
    case "Log Foods At Different Times":
        RunShortcut(shortcutNames["Log Foods At Different Times"])

    case "Make Food Note":
        res = AskForInput(Input.Text, "What is the name of the food you would like to note down?", allowMultipleLines=False)
        text = f'{res} @ {CurrentDate.format(date="medium", time="short")}'
        AppendToFile(text, "FLS/Other/foodNotes.txt", makeNewLine=True)
        StopShortcut()

    case 'Saved Foods and Search':
        RunShortcut(shortcutNames["Saved And Search"])

    case 'History and Stats':
        case "Statistics with Charty":
            if hasHealthApp == FALSE:
                Alert("Statistics require a device with a Health App")
                StopShortcut()

            RunShortcut(shortcutNames["Health Statistics"])

        case "Food History":
            RunShortcut(shortcutNames["Clear Cache And Backlog"])

            file = GetFile(f"{storage}/Other/backlog.json", errorIfNotFound=False)
            if file is not None
                ShowAlert("There are items in the backlog, food history will not be accurate until backlog is cleared", showCancel=True)
            
            RunShortcut(shortcutNames["Food History"])

    case 'Clear... and Other Settings':
        case "Clear Backlog":
            Notification('Clearing backlog....')
            RunShortcut(shortcutNames["Clear Cache And Backlog"])

        case "Clear Food Notes":
            file = GetFile(f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
            DeleteFile(file, deleteImmediately=True)

        case "View Storage Folder":
            folder = GetFile(storage)
            OpenFile(folder)

        case "Rename Storage Folder":
            newStorage = AskForInput(Input.Text, "New folder name", default=storage)
            if newStorage != storage:
                breakLoop = FALSE
                for _ in range(10):
                    if breakLoop == FALSE:
                        if GetFile(newStorage, errorIfNotFound=False) is not None:
                            newStorage = AskForInput(Input.Text, f'Folder "{newStorage}" already exists, please select a different name')
                        else
                            breakLoop = TRUE

                folder = GetFile(storage)
                RenameFile(folder, newStorage)
                storage = newStorage
                SaveFile(storage, "Nutrition_Shortcut_Storage_Folder_Name.txt", overwrite=True)


RunShortcut(shortcutNames['Clear Cache and Backlog'])

if checkForUpdates == TRUE:
    RunShortcut(shortcutNames["Installer"], input={'updateCheck': True})
    #SaveFile(Text(CurrentDate.format(date="short", time=None)), f"{storage}/Other/lastUpdateCheck.txt", overwrite=True)
