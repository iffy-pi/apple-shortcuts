'''
Framework: Nutrition (id = 4)
ID:  13
Ver: 1.02
'''

# View, Make, Edit and Remove Presets and/or Barcodes, view Recents and do Search items

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))

res = GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json")
shortcutNames = Dictionary(res)
Menu(Strings['nutr.menu.savedsearch']):
    case Strings['savedsearch.view']:
        # run shortcutNames[search algorithm ]and display food with 

        res = RunShortcut(shortcutNames["Display Food Item"], input=RunShortcut(shortcutNames["Search Algorithm"]))
        for item in res:
            searchResult = res
            Menu(Strings['savedsearch.view.prompt']):
                case Strings['savedsearch.logentry']:
                    date = AskForInput(Strings['input.logtime'], Input.DateAndTime, default=Date.CurrentDate)

                    dix = {
                        'Date': str(date)
                        'Food': dix(searchResult)
                    }
                    res = RunShortcut(shortcutNames[
                        "Log Algorithm"],
                        input=dix)

                    LoggedFoods2 = res

                    Menu(Strings['savedsearch.savepreset']):
                        case Strings['opts.yes']:
                            RunShorctut("Make Preset", input=LoggedFoods2)
                        case Strings['opts.no']:
                            pass

                case Strings['presets.make']:
                    RunShortcut(shortcutNames["Make Preset"], input=searchResult)

                case Strings['opts.exit']:
                    pass

    case Strings['presets']:
        breakPresetLoop = FALSE
        for _ in range(10):
            Menu(Strings['presets']):
                case Strings['presets.view']:
                    deletePresetCache = FALSE
                    res = RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'presets'})
                    for repeatItem in res:
                        changedFood = Dictionary(RunShortcut(shortcutNames["Display Food Item"], input=repeatItem))
                        Menu(Strings['savechanges'].replace('$item', changedFood['Name'])):
                            case Strings['opts.yes']:
                                SaveFile(To='Shortcuts', changedFood, f"{storage}/Presets/Foods/food_{changedFood['id']}.json", overwrite=True)
                                deletePresetCache = TRUE
                            case Strings['opts.no']:
                                pass

                    if deletePresetCache == TRUE:
                        file = GetFile(From='Shortcuts', 'FLS/Presets/vcardCache.txt', errorIfNotFound=False)
                        DeleteFile(file, deleteImmediately=True)

                case Strings['presets.make']:
                    # run shortcutNames[foods list ]to get list of foods to be made into a preset
                    RunShortcut(shortcutNames["Make Preset"])

                case Strings['presets.edit']:
                    RunShortcut(shortcutNames["Edit Saved Food"], input={'type': 'presets'})

                case Strings['presets.remove']:
                    RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'presets', 'deleteMode': True})

                case Strings['opts.exit']:
                    breakPresetLoop = TRUE

    case Strings['barcodes']:
        breakPresetLoop = FALSE
        for _ in range(10):
            Menu(Strings['barcodes']):
                case Strings['barcodes.view.database']:
                    deletePresetCache = FALSE
                    res = RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'barcodes'})
                    for repeatItem in res:
                        changedFood = Dictionary(RunShortcut(shortcutNames["Display Food Item"], input=repeatItem))
                        Menu(Strings['savechanges'].replace('$item', changedFood['Name'])):
                            case Strings['opts.yes']:
                                SaveFile(To='Shortcuts', changedFood, f"{storage}/Barcodes/Foods/food_{changedFood['id']}.json", overwrite=True)
                                deletePresetCache = TRUE
                            case Strings['opts.no']:
                                pass

                    if deletePresetCache == TRUE:
                        file = GetFile(From='Shortcuts', 'FLS/Barcodes/vcardCache.txt', errorIfNotFound=False)
                        DeleteFile(file, deleteImmediately=True)
                
                case Strings['barcodes.add']:
                    RunShortcut(shortcutNames["Barcode Search"])

                case Strings['barcodes.edit']:
                    RunShortcut(shortcutNames["Edit Saved Food"], input={'type': 'barcodes'})

                case Strings['barcodes.remove']:
                    RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'barcodes', 'deleteMode': True})

                case Strings['opts.exit']:
                    breakPresetLoop = TRUE
    
    case Strings['recents']:
        for item in RunShortcut(shortcutNames["Get Recent"]):
            RunShortcut(shortcutNames["Display Food Item"], input=item)

