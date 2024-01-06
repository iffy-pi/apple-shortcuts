'''
Framework: Nutrition (id = 4)
ID:  5 
Ver: 1.06
'''

# Main shortcut

TRUE = 1
FALSE = 0

storageExists = FALSE

file = GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt", errorIfNotFound=False)

if file is not None:
    storage = Text(file)
else:
    # Let the user select a language
    langs = Dictionary(GetContentsOfURL('https://iffy-pi.github.io/apple-shortcuts/public/nutrition/languages/language_options.json'))

    selectedLang = ChooseFromList(langs.Keys)

    Strings = Dictionary(GetContentsOfURL(f'https://iffy-pi.github.io/apple-shortcuts/public/nutrition/languages/{selectedLang}'))


    Menu(Strings['nutr.storage.notfound']):
        case Strings['nutr.storage.select']:
            folder = SelectFile(folders=True)
            storage = f'{folder.Name}'
        case Strings['nutr.storage.create']:
            storage = AskForInput(Input.Text, prompt=Strings['nutr.storage.input'], default='Nutrition')

            breakLoop = FALSE
            for _ in range(10):
                if breakLoop == FALSE:
                    if GetFile(From='Shortcuts', storage, errorIfNotFound=False) is not None:

                        text = Strings['nutr.storage.exists'].replace("$storage", storage)
                        Menu(text):
                            case Strings['nutr.storage.newname']:
                                storage = AskForInput(Input.Text, prompt=Strings['nutr.storage.input'])
                            case Strings['nutr.storage.use']:
                                breakLoop = TRUE
                    else:
                        breakLoop = TRUE

    SaveFile(To='Shortcuts', storage, "Nutrition_Shortcut_Storage_Folder_Name.txt", overwrite=True)

    SaveFile(To='Shortcuts', Strings, f'{storage}/Other/gui_strings.json', overwrite=True)

checkForUpdates = TRUE
exitAfterQuickLog = TRUE

# load names of the shortcuts
res = GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json")
shortcutNames = Dictionary(res)

Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json", errorIfNotFound=False))

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
SaveFile(To='Shortcuts', text, f"{storage}/Other/nutriKeys.txt")

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
file = GetFile(From='Shortcuts', f"{storage}/Other/env.json", errorIfNotFound=False)
env = Dictionary(file)
env['hasHealthApp'] = hasHealthApp
SaveFile(To='Shortcuts', env, f"{storage}/Other/env.json", overwrite=True)

# fast track health app permissions
if env['permsEnabled'] is None:
    if hasHealthApp == TRUE:
        # run log algorithm
        updatedText = Strings['nutr.healthperms.instr'].replace('$othersettings', Strings['nutr.menu.othersettings'])
        updatedText =  updatedText.replace('$healthperms', Strings['nutr.menu.healthperms'])

        Alert(updatedText)
        RunShortcut(shortcutNames['Log Algorithm'], input={'setPerms': True})
        env['permsEnabled'] = TRUE
        SaveFile(To='Shortcuts', env, f"{storage}/Other/env.json", overwrite=True)


if hasHealthApp == FALSE:
    IFRESULT = Strings['nutr.backlog.notif'].replace('$device', deviceModel)
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

    REPEATRESULTS = [ Number(healthSample.Value) for healthSample in healthSamples ]
    _sum = CalculateStatistics("Sum", REPEATRESULTS)
    calsToday = Round (_sum, "hundredths")

    file = GetFile(From='Shortcuts', f"{storage}/Other/backlog.json", errorIfNotFound=False)

    prompt = Strings['nutr.calorie.summary'].replace('$cals', calsToday)

    if file is not None:
        prompt = f"""
            {prompt}
            {Strings['nutr.backlog.nonempty']}
        """

    IFRESULT = prompt

prompt = IFRESULT

file = GetFile(From='Shortcuts', 'FLS/Other/foodNotes.txt', errorIfNotFound=False)
if file is not None:
    prompt = f'''
    {prompt}
    {Strings['foodnotes']}:
    {file}
    '''

Menu(prompt):
    case Strings['nutr.menu.quicklog']:
        # Log food from Recent and exit immediately
        for item in  RunShortcut(shortcutNames['Get Recent']):
            curFood = item

            updatedText = Strings['ask.for.servings'].replace('$name', curFood['Name'])
            updatedText = updatedText.replace('$size', curFood['Serving Size'])
            # translates to set dictionary value in curFood and then set dictionary
            curFood['Servings'] = Number(AskForInput(updatedText, Input.Number, default=1, allowDecimalNumbers=True, allowNegativeNumbers=False))
            REPEATRESULTS.append(curFood)

        # we log foods in different iteration to fast track user input
        for food in RunShortcut(shortcutNames['Get Recent']):
            RunShortcut(shortcutNames["Add Recent"], input=food)
            dix = Text({
                'Date': str(Date.CurrentDate)
                'Food': dix(food)
            })
            RunShortcut(shortcutNames["Log Algorithm"], input=food)

        if Number(exitAfterQuickLog) == TRUE:
            StopShortcut()

    case Strings['nutr.menu.logattime']:
        RunShortcut(shortcutNames["Log Foods At Time"])
    
    case Strings['nutr.menu.logdifferent']:
        RunShortcut(shortcutNames["Log Foods At Different Times"])

    case Strings['nutr.menu.makenote']:
        res = AskForInput(Input.Text, Strings['nutr.foodnotes.name'], allowMultipleLines=False)
        date = AskForInput(Input.DateAndTime, Strings['nutr.foodnotes.time'])
        text = f'{res} @ {date.format(date="medium", time="short")}'
        AppendToFile(text, f"{storage}/Other/foodNotes.txt", makeNewLine=True)
        StopShortcut()

    case Strings['nutr.menu.savedsearch']:
        RunShortcut(shortcutNames["Saved And Search"])

    case Strings['nutr.menu.historystats']:
        Menu(Strings['nutr.menu.historystats']):
            case Strings['nutr.menu.stats']:
                if hasHealthApp == FALSE:
                    Alert(Strings['nutr.stats.nocharty'])
                    StopShortcut()

                RunShortcut(shortcutNames["Nutrition Statistics"])

            case Strings['nutr.menu.history']:
                RunShortcut(shortcutNames["Clear Cache And Backlog"])

                file = GetFile(From='Shortcuts', f"{storage}/Other/backlog.json", errorIfNotFound=False)
                if file is not None
                    ShowAlert(Strings['nutr.history.backlog.nonempty'], showCancel=True)
                
                RunShortcut(shortcutNames["Food History"])

    case Strings['nutr.menu.othersettings']:
        Menu(Strings['nutr.menu.othersettings']):
            case Strings['nutr.menu.clearbacklog']:
                Notification(Strings['nutr.backlog.clearing'])
                RunShortcut(shortcutNames["Clear Cache And Backlog"])

            case Strings['nutr.menu.clearfoodnotes']:
                file = GetFile(From='Shortcuts', f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
                DeleteFile(file, deleteImmediately=True)

            case Strings['nutr.menu.healthperms']:
                Alert(Strings['nutr.healthperms.warning.msg'], title=Strings['nutr.healthperms.warning.title'])
                RunShortcut(shortcutNames['Log Algorithm'], input={'setPerms': True})

            case Strings['nutr.menu.storage.view']:
                folder = GetFile(From='Shortcuts', storage)
                OpenFile(folder)

            case Strings['nutr.menu.storage.rename']:
                newStorage = AskForInput(Input.Text, Strings['nutr.storage.create'], default=storage)
                if newStorage != storage:
                    breakLoop = FALSE
                    for _ in range(10):
                        if breakLoop == FALSE:
                            if GetFile(From='Shortcuts', newStorage, errorIfNotFound=False) is not None:
                                updatedText = Strings['nutr.storage.exists'].replace("$storage", newStorage)
                                newStorage = AskForInput(Input.Text, updatedText)
                            else
                                breakLoop = TRUE

                    folder = GetFile(From='Shortcuts', storage)
                    RenameFile(folder, newStorage)
                    storage = newStorage
                    SaveFile(To='Shortcuts', storage, "Nutrition_Shortcut_Storage_Folder_Name.txt", overwrite=True)

            case Strings['nutr.lang.change']:
                langs = Dictionary(GetContentsOfURL('https://iffy-pi.github.io/apple-shortcuts/public/nutrition/languages/language_options.json'))

                selectedLang = ChooseFromList(langs.Keys)
                
                Strings = Dictionary(GetContentsOfURL(f'https://iffy-pi.github.io/apple-shortcuts/public/nutrition/languages/{selectedLang}'))

                SaveFile(To='Shortcuts', Strings, f'{storage}/Other/gui_strings.json', overwrite=True)

            case Strings['nutr.menu.tutorial']:
                OpenURL("https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/data/tutorial.html")

    case Strings['nutr.menu.howtouse']::
            OpenURL("https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/data/tutorial.html")


RunShortcut(shortcutNames['Clear Cache and Backlog'])

if checkForUpdates == TRUE:
    RunShortcut(shortcutNames["Installer"], input={'updateCheck': True})
    #SaveFile(To='Shortcuts', Text(CurrentDate.format(date="short", time=None)), f"{storage}/Other/lastUpdateCheck.txt", overwrite=True)
