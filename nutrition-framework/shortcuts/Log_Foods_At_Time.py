'''
Framework: Nutrition (id = 4)
ID:  11
Ver: 1.01
'''

# Log foods at a selected time

TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

res = GetFile(f"{storage}/Other/shortcutNames.json")
shortcutNames = Dictionary(res)

Dating = AskForInput("What date and time? Click Done for Right Now", Input.DateAndTime)

for item in RunShortcut(shortcutNames["Foods List"]):
    CurFood = item
    dix = {
        'Date': str(Dating)
        'Food': dix(CurFood)
    }

    res = RunShortcut(shortcutNames["Log Algorithm"], input=dix)
    loggedFoods.append(res)

file = GetFile(f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
if file is not None:
    Menu('Clear food notes?'):
        case 'Yes':
            DeleteFile(file, deleteImmediately=True)
        case 'No':
            pass

makePreset = TRUE

# If we only logged one item and the food is already a preset, then we dont prompt the make preset option
if Count(loggedFoods) == 1:
    file = GetFile(f"{storage}/Presets/Foods/food_{loggedFoods['id']}.json")
    if file is not None:
        makePreset = FALSE

if makePreset == TRUE:
    Menu("Make Preset?"):
        case "Yes":
            RunShortcut(shortcutNames["Make Preset"], input=loggedFoods)
        case "No":
            pass

