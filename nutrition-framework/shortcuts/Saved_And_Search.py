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

            if postSearchMenu.opt("Log Entry"):
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

            elif postSearchMenu.opt("Make Preset"):
                RunShortcut(shortcutNames["Make Preset"], input=searchResult)

            elif postSearchMenu.opt("Exit"):
                pass

    case "Presets":
        prm = Menu(prompt="Presets", options=["View Presets", "Make Preset", "Edit Preset", "Remove Preset(s)"])

        if prm.opt("View Presets"):
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


        elif prm.opt("Make Preset"):
            # run shortcutNames[foods list ]to get list of foods to be made into a preset
            RunShortcut(shortcutNames["Make Preset"])

        elif prm.opt("Edit Preset"):
            RunShortcut(shortcutNames["Edit Saved Food"], input={'type': 'presets'})

        elif prm.opt("Remove Preset(s)"):
            RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'presets', 'deleteMode': True})

    case "Barcodes":
        brm = Menu(prompt="Barcodes", options=[
            "View Personal Database",
            "Add to Personal Database",
            "Edit Items in Personal Database",
            "Remove From Personal Database"
            ])


        if brm.opt("View Personal Database"):
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
        elif brm.opt("Add to Personal Database"):
            RunShortcut(shortcutNames["Barcode Search"])

        elif brm.opt("Edit Items in Personal Database"):
            RunShortcut(shortcutNames["Edit Saved Food"], input={'type': 'barcodes'})

        elif brm.opt("Remove From Personal Database"):
            RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'barcodes', 'deleteMode': True})
    
    case "Recent Meals":
        res = RunShortcut(shortcutNames["Get Recent"])
        for item in res:
            RunShortcut(shortcutNames["Display Food Item"], input=item)
