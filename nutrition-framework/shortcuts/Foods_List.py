'''
Framework: Nutrition (id = 4)
ID:  6 
Ver: 1.05
'''

# Select one or more foods from the different available foods sources

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))

cancelIcon = #.. cancelIcon.txt

foodsDix = {}

# list ids
selectedIds = []

nextId = 0

maxLoops = 30
breakLoop = FALSE

hasNotes = FALSE

# If we are passing results to a shortcut where the user has to select foods (e.g. Log Foods At Different Times, Make Preset)
# We can eliminate redundant iteration by passing the generated foods dix and unique selection ids
# to that shortcut, instead of just the raw list of foods
# This functionality is requested with the `passToBulkEntry` field in the params

params = Dictionary(ShortcutInput)


file = GetFile(From='Shortcuts', f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
if file is not None:
    notes = f'''
        {Strings['foodnotes']}:
        {file}

    '''
    notes = IFRESULT
    hasNotes = TRUE

for _ in range(maxLoops):
    if breakLoop == FALSE:
        for listId in selectedIds:
            food = foodsDix[listId]
            REPEATRESULTS.append(f'{food['Servings']}x {food['Name']}')

        if REPEATRESULTS is not None:
            IFRESULT = f'''
            {Strings['foodslist.foods.selected']}:
            {REPEATRESULTS}
            '''
        else:
            IFRESULT = f'''
            {Strings['foodslist.foods.empty']}
            '''
        prompt = IFRESULT
        
        # append our food notes if they are any
        if hasNotes == TRUE:
            prompt = f'''
                {notes}
                {prompt}
            '''

        if params['inputPrompt'] is not None:
            prompt = f'''
            {params['inputPrompt']}
            {prompt}
            '''

        addMenuResult = TRUE

        Menu(prompt):
            case Strings['foodslist.menu.done']:
                addMenuResult = FALSE

                if params['passToBulkEntry'] is not None:
                    # sends the foods dictionary and selection ids as foods info to the shortcut
                    dix = {}
                    dix['selectedIds'] = selectedIds
                    dix['foodsDix'] = foodsDix
                    StopShortcut(output = dix)
                else:
                    for listId in selectedIds:
                        food = foodsDix[listId]
                        REPEATRESULTS.append(food)
                    StopShortcut(output = REPEATRESULTS)

            case Strings['foodslist.menu.search']:
                MENURESULT = RunShortcut(nutrDix['Search Algorithm'])

            case Strings['foodslist.menu.saved']:
                MENURESULT = RunShortcut(nutrDix['Select Saved Foods'], input={'type': 'all'})

            case Strings['foodslist.menu.scan']:
                MENURESULT = RunShortcut(nutrDix['Barcode Search'], input={'getFood': True})

            case Strings['foodslist.menu.recent']:
                MENURESULT = RunShortcut(nutrDix['Get Recent'])

            case Strings['foodslist.menu.manual']:
                # TODO, make manual maker
                MENURESULT = RunShortcut(nutrDix['Make Food Manually'])

            case Strings['foodslist.menu.edit']:
                addMenuResult = FALSE
                
                # generate contact cards or user to select food using list ID
                for listId in selectedIds:
                    food = foodsDix[listId]
                    updatedText = Strings['food.servings'].replace('$num', food['Servings'])
                    text = f'''
                        BEGIN:VCARD
                        VERSION:3.0
                        N;CHARSET=UTF-8:{food['Name']}
                        ORG;CHARSET=UTF-8:{updatedText}
                        NOTE;CHARSET=UTF-8:{listId}
                        END:VCARD
                    '''
                    REPEATRESULTS.append(text)

                # cancel contact card
                text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=UTF-8:{Strings['opts.cancel']}
                    ORG;CHARSET=UTF-8:{Strings['savedfoods.none.desc']}
                    NOTE;CHARSET=UTF-8:Cancel
                    {cancelIcon}
                    END:VCARD
                    {REPEATRESULTS}
                '''
                renamedItem = SetName(text, 'vcard.vcf')
                contacts = GetContacts(renamedItem)

                edit = ChooseFrom(contacts, prompt=Strings['foods.viewedit.select'])

                listId = Contact(edit.Notes)
                if listId != 'Cancel':
                    # get the food at the id
                    food = foodsDix[listId]
                    Menu(Strings['foodslist.select.action']):
                        case Strings['foodslist.edit.servings']:
                            updatedText = Strings['ask.for.servings'].replace('$name', food['Name'])
                            updatedText = updatedText.replace('$size', food['Serving Size'])

                            res = AskForInput(Input.Number, updatedText, allowNegatives=False)
                            food['Servings'] = Number(res)
                            foodsDix[listId] = food
                            RunShortcut(nutrDix['Add Recent'], input=food)

                        case Strings['foodslist.edit.other']:
                            changedFood = RunShortcut(nutrDix['Display Food Item'], input=food)
                            updatedText = Strings['foodslist.savechanges'].replace('$item', changedFood['Name'])
                            Menu(updatedText):
                                case Strings['opts.yes']:
                                    # if we edit a food, it is now different from its source food so generate a new food ID for it
                                    changedFood['id'] = RunShortcut(nutrDix['GFID'])
                                    foodsDix[listId] = changedFood
                                    RunShortcut(nutrDix['Add Recent'], input=changedFood)
                                case Strings['opts.no']:
                                    pass

            case Strings['foodslist.menu.remove']:
                addMenuResult = FALSE
                # Remove selection
                for listId in selectedIds:
                    food = foodsDix[listId]
                    text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=UTF-8:{food['Name']}
                    ORG;CHARSET=UTF-8:{food['Servings']} servings
                    NOTE;CHARSET=UTF-8:{listId}
                    END:VCARD
                    '''
                    REPEATRESULTS.append(text)

                text = Text(REPEATRESULTS)
                renamedItem = SetName(text, 'vcard.vcf')
                contacts = GetContacts(renamedItem)

                deletes = ChooseFrom(contacts, selectMultiple=True, prompt=Strings['foods.remove.select'])

                for delete in deletes:
                    listId = Contact(delete).Notes
                    # remove it from the list
                    selectedIds = FilterFiles(selectedIds, where=['Name' != listId])

        if addMenuResult == TRUE:
            # add the foods to our selected foods
            menuFoods = []

            for food in MENURESULT:
                text = Text(food)
                SaveFile(To='Shortcuts', text, f'{storage}/Other/tempNutrientsDix.txt', overwrite=True)
                food = Dictionary( Text(GetFile(From='Shortcuts', f'{storage}/Other/tempNutrientsDix.txt')) )

                menuFoods.append(food)

                updatedText = Strings['ask.for.servings'].replace('$name', food['Name'])
                updatedText = updatedText.replace('$size', food['Serving Size'])

                # Ask for the servings
                servings = Number(AskForInput(Input.Number, updatedText, allowDecimals=True, allowNegatives=False))
                food['Servings'] = Number(servings)

                # generate list Id for the item
                foodsDix[nextId] = food
                selectedIds.append(nextId)
                nextId = nextId + 1

                REPEATRESULTS.append(GetVariable(food))

            for food in REPEATRESULTS:
                RunShortcut(nutrDix['Add Recent'], input=food)