'''
Framework: Nutrition (id = 4)
ID:  5 
Ver: 1.02
'''

# Main shortcut

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

# Device has health app if on iphone or iPad on OS 17 and higher
hasHealthApp = FALSE
deviceModel = GetDeviceDetails("Model")
matches = MatchText(deviceModel, "(iPhone)")

if matches is not None:
    hasHealthApp = TRUE

if deviceModel == 'iPad':
    if GetDeviceDetails('System Version') >= 17:
        hasHealthApp = TRUE

# save the state of the health app to environment
file = GetFile(f"{storage}/Other/env.json", errorIfNotFound=False)
env = Dictionary(file)
env['hasHealthApp'] = hasHealthApp
SaveFile(env, f"{storage}/Other/env.json", overwrite=True)

# fast track health app permissions
if env['permsEnabled'] is None:
    if hasHealthApp == TRUE:
        # run log algorithm
        text = '''
            Your Apple Health permissions may have not been fully set, the shortcut will fast track through sample logging permissions.
            You can do this again by going to Clear and Other Settings > Fast Track Health Permissions.
        '''
        Alert("Your Apple Health permissions may have not been fully set, the shortcut will fast track through sample logging permissions", title="Health Sample Permissions")
        RunShortcut(shortcutNames['Log Algorithm'], input={'setPerms': True})
        env['permsEnabled'] = TRUE
        SaveFile(env, f"{storage}/Other/env.json", overwrite=True)


if hasHealthApp == FALSE:
    text = f"Foods logged on {deviceModel} will be added to backlog"

else:
    # if on health app, calculate total calories consumed today and show in menu prompt
    calsToday = 0
    healthSamples = HealthApp.Find(
            AllHealthSamples,
            whereAllAreTrue=[
                Type == "Dietary Energy",
                StartDate == Today,
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
        # Log food from Recent and exit immediately
        for item in  RunShortcut(shortcutNames['Get Recent']):
            curFood = item

            RunShortcut(shortcutNames["Add Recent"], input=curFood)

            text = f"How many servings of {curFood['Name']}\n(1 serving = {curFood['Serving Size']})"
            
            # translates to set dictionary value in curFood and then set dictionary
            curFood['Servings'] = AskForInput(text, Input.Number, default=1, allowDecimalNumbers=True, allowNegativeNumbers=False)
            REPEATRESULTS.append(curFood)

        # we log foods in different iteration to fast track user input
        for food in REPEATRESULTS:
            dix = Text({
                'Date': str(Date.CurrentDate)
                'Food': dix(food)
            })
            RunShortcut(shortcutNames["Log Algorithm"], input=food)

        if exitAfterQuickLog == TRUE:
            StopShortcut()

    case "Log Foods At Time...":
        RunShortcut(shortcutNames["Log Foods At Time"])
    case "Log Foods At Different Times":
        RunShortcut(shortcutNames["Log Foods At Different Times"])

    case "Make Food Note":
        res = AskForInput(Input.Text, "What is the name of the food you would like to note down?", allowMultipleLines=False)
        date = AskForInput(Input.DateAndTime, "What is the date and time?")
        text = f'{res} @ {date.format(date="medium", time="short")}'
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

        case "Fast Track Health Permissions":
            Alert("Your Apple Health permissions may have not been fully set, the shortcut will fast track through sample logging permissions", title="Health Sample Permissions")
            RunShortcut(shortcutNames['Log Algorithm'], input={'setPerms': True})

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

        case 'Tutorial':
            OpenURL("https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/data/tutorial.html")


RunShortcut(shortcutNames['Clear Cache and Backlog'])

if checkForUpdates == TRUE:
    RunShortcut(shortcutNames["Installer"], input={'updateCheck': True})
    #SaveFile(Text(CurrentDate.format(date="short", time=None)), f"{storage}/Other/lastUpdateCheck.txt", overwrite=True)
