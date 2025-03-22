'''
Framework: Nutrition (id = 4)
ID:  11
Ver: 1.1
'''

# Log foods at a selected time

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))

res = GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json")
shortcutNames = Dictionary(res)

prompt = Strings['input.logtime']
menuPrompt = 'Select and log foods at a certain date and time' # TODO string this

file = GetFile(From='Shortcuts', f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
if file is not None:
    prompt = f'''
        {Strings['foodnotes']}:
        {file}

        {prompt}
    '''

    menuPrompt = f'''
        {menuPrompt}
        {Strings['foodnotes']}:
        {file}
    '''

Menu(menuPrompt):
    case 'Select Date and Time':
        pass
    case 'Back':
        # Return to calling shortcut
        StopShortcut()



dating = AskForInput(prompt, Input.DateAndTime)

for item in RunShortcut(shortcutNames["Foods List"]):
    CurFood = item
    dix = {
        'Date': str(dating)
        'Food': dix(CurFood)
    }

    res = RunShortcut(shortcutNames["Log Algorithm"], input=dix)
    loggedFoods.append(res)

file = GetFile(From='Shortcuts', f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
if file is not None:
    Menu(Strings['logt.clearnotes']):
        case Strings['opts.yes']:
            DeleteFile(file, deleteImmediately=True)
        case Strings['opts.no']:
            pass

makePreset = TRUE

# If we only logged one item and the food is already a preset, then we dont prompt the make preset option
if Count(loggedFoods) == 1:
    file = GetFile(From='Shortcuts', f"{storage}/Presets/Foods/food_{loggedFoods['id']}.json")
    if file is not None:
        makePreset = FALSE

if makePreset == TRUE:
    Menu(Strings['logt.makepreset']):
        case Strings['opts.yes']:
            RunShortcut(shortcutNames["Make Preset"], input=loggedFoods)
        case Strings['opts.no']:
            pass

