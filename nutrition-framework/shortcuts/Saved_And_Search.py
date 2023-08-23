'''
Framework: Nutrition (id = 4)
ID:  13
Ver: 1.0
'''

# View, Make, Edit and Remove Presets and/or Barcodes, view Recents and do Search items

TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

res = GetFile(f"{storage}/Other/shortcutNames.json")
shortcutNames = Dictionary(res)
Menu("Saved And Search"):
    case "Search and View":
        # run shortcutNames[search algorithm ]and display food with 

        res = RunShortcut(shortcutNames["Display Food Item"], input=RunShortcut(shortcutNames["Search Algorithm"]))
        for item in res:
            searchResult = res
            postSearchMenu = Menu(["Log Entry", "Make Preset", "Exit"])
            Menu():
                case "Log Entry":
                    date = AskForInput("Date:", Input.DateAndTime, default=Date.CurrentDate)

                    dix = {
                        'Date': str(date)
                        'Food': dix(searchResult)
                    }
                    res = RunShortcut(shortcutNames[
                        "Log Algorithm"],
                        input=dix)

                    LoggedFoods2 = res

                    svp = Menu(["Yes", "No"], prompt="Save As Preset?")

                    if svp.opt("Yes"):
                        RunShorctut("Make Preset", input=LoggedFoods2)
                    if svp.opt("No"):
                        pass

                case "Make Preset":
                    RunShortcut(shortcutNames["Make Preset"], input=searchResult)

                case "Exit":
                    pass

    case "Presets":
        Menu("Presets"):
            case "View Presets":
                deletePresetCache = FALSE
                res = RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'presets'})
                for repeatItem in res:
                    changedFood = Dictionary(RunShortcut(shortcutNames["Display Food Item"], input=repeatItem))
                    Menu(f'Save Changes to {changedFood['Name']}?'):
                        case 'Yes':
                            SaveFile(changedFood, f"{storage}/Presets/Foods/food_{changedFood['id']}.json", overwrite=True)
                            deletePresetCache = TRUE
                        case 'No':
                            pass

                if deletePresetCache == TRUE:
                    file = GetFile('FLS/Presets/vcardCache.txt', errorIfNotFound=False)
                    DeleteFile(file, deleteImmediately=True)

            case "Make Preset":
                # run shortcutNames[foods list ]to get list of foods to be made into a preset
                RunShortcut(shortcutNames["Make Preset"])

            case "Edit Preset":
                RunShortcut(shortcutNames["Edit Saved Food"], input={'type': 'presets'})

            case "Remove Preset(s)":
                RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'presets', 'deleteMode': True})

    case "Barcodes":
        brm = Menu(prompt="Barcodes", options=[
            "View Personal Database",
            "Add to Personal Database",
            "Edit Items in Personal Database",
            "Remove From Personal Database"
            ])

        Menu("Barcodes"):
            case "View Personal Database":
                deletePresetCache = FALSE
                res = RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'barcodes'})
                for repeatItem in res:
                    changedFood = Dictionary(RunShortcut(shortcutNames["Display Food Item"], input=repeatItem))
                    Menu(f'Save Changes to {changedFood['Name']}?'):
                        case 'Yes':
                            SaveFile(changedFood, f"{storage}/Barcodes/Foods/food_{changedFood['id']}.json", overwrite=True)
                            deletePresetCache = TRUE
                        case 'No':
                            pass

                if deletePresetCache == TRUE:
                    file = GetFile('FLS/Barcodes/vcardCache.txt', errorIfNotFound=False)
                    DeleteFile(file, deleteImmediately=True)
            case "Add to Personal Database":
                RunShortcut(shortcutNames["Barcode Search"])

            case "Edit Items in Personal Database":
                RunShortcut(shortcutNames["Edit Saved Food"], input={'type': 'barcodes'})

            case "Remove From Personal Database":
                RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'barcodes', 'deleteMode': True})
    
    case "Recent Meals":
        for item in RunShortcut(shortcutNames["Get Recent"]):
            RunShortcut(shortcutNames["Display Food Item"], input=item)

