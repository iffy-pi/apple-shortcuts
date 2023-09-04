'''
Framework: Nutrition (id = 4)
ID:  6 
Ver: 1.03
'''

# Select one or more foods from the different available foods sources

TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

nutrDix = Dictionary(GetFile(f"{storage}/Other/shortcutNames.json"))
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


file = GetFile(f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
if file is not None:
    notes = f'''
        Food Notes:
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
            Current Selected Foods:
            {REPEATRESULTS}
            '''
        else:
            IFRESULT = f'''
            No foods selected
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
            case 'Done Selecting Foods':
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

            case 'Search Food':
                MENURESULT = RunShortcut(nutrDix['Search Algorithm'])

            case 'Get Preset(s) Or Barcoded Food(s)':
                MENURESULT = RunShortcut(nutrDix['Select Saved Foods'], input={'type': 'all'})

            case 'Get Recent Meals':
                MENURESULT = RunShortcut(nutrDix['Get Recent'])

            case 'Scan Barcode':
                MENURESULT = RunShortcut(nutrDix['Barcode Search'], input={'getFood': True})

            case 'Make Food Manually':
                # TODO, make manual maker
                MENURESULT = RunShortcut(nutrDix['Make Food Manually'])

            case 'View/Edit Selected Foods':
                addMenuResult = FALSE
                
                # generate contact cards or user to select food using list ID
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

                # cancel contact card
                text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=UTF-8:Cancel
                    ORG;CHARSET=UTF-8:No foods will be selected
                    NOTE;CHARSET=UTF-8:Cancel
                    {cancelIcon}
                    END:VCARD
                    {REPEATRESULTS}
                '''
                renamedItem = SetName(text, 'vcard.vcf')
                contacts = GetContacts(renamedItem)

                edit = ChooseFrom(contacts, prompt='Select Food To View')

                listId = Contact(edit.Notes)
                if listId != 'Cancel':
                    # get the food at the id
                    food = foodsDix[listId]
                    Menu('Select an action'):
                        case 'Edit Servings':
                            res = AskForInput(Input.Number, f'How many servings? (1 serving = {food['Serving Size']})', allowNegatives=False)
                            food['Servings'] = res
                            foodsDix[listId] = food
                            RunShortcut(nutrDix['Add Recent'], input=food)

                        case 'View/Edit Other Fields':
                            changedFood = RunShortcut(nutrDix['Display Food Item'], input=food)
                            Menu(f'Save Changes to {changedFood['Name']}?'):
                                case 'Yes':
                                    # if we edit a food, it is now different from its source food so generate a new food ID for it
                                    changedFood['id'] = RunShortcut(nutrDix['GFID'])
                                    foodsDix[listId] = changedFood
                                    RunShortcut(nutrDix['Add Recent'], input=changedFood)
                                case 'No':
                                    pass

            case 'Remove Selected Foods':
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

                deletes = ChooseFrom(contacts, selectMultiple=True, prompt='Select foods to remove')

                for delete in deletes:
                    listId = Contact(delete).Notes
                    # remove it from the list
                    selectedIds = filter(selectedIds, where=['Name' != listId])

        if addMenuResult == TRUE:
            # add the foods to our selected foods
            for food in MENURESULT:
                # Ask for the servings
                servings = AskForInput(Input.Number, f'How many servings of {food['Name']}? (1 serving = {food['Serving Size']})', allowDecimals=True, allowNegatives=False)
                food['Servings'] = servings
                RunShortcut(nutrDix['Add Recent'], input=food)

                # generate list Id for the item
                foodsDix[nextId] = food
                selectedIds.append(nextId)
                nextId = nextId + 1