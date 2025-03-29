'''
Framework: Nutrition (id = 4)
ID:  6 
Ver: 1.1
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

sumStats = { "Protein": 0, "Fat": 0, "Calories": 0, "Carbs": 0 }

# If we are passing results to a shortcut where the user has to select foods (e.g. Log Foods At Different Times, Make Preset)
# We can eliminate redundant iteration by passing the generated foods dix and unique selection ids
# to that shortcut, instead of just the raw list of foods
# This functionality is requested with the `passToBulkEntry` field in the params

params = Dictionary(ShortcutInput)

if params['calculator'] is not None:
    $IFRESULT = 'Exit Calculator' # TODO translate this
else:
    $IFRESULT = Strings['foodslist.menu.done']
doneOpt = $IFRESULT



file = GetFile(From='Shortcuts', f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
if file is not None:
    notes = f'''
        {Strings['foodnotes']}:
        {file}

    '''
    notes = $IFRESULT
    hasNotes = TRUE

for _ in range(maxLoops):
    if breakLoop == FALSE:
        stats = f'''
        Total: {sumStats['Calories']} kcal
        {sumStats['Carbs']}g Carbs ⸱ {sumStats['Protein']}g Carbs ⸱ {sumStats['Carbs']}g Carbs


        ''' 
        stats = $IFRESULT


        for listId in selectedIds:
            food = foodsDix[listId]
            cals = RoundNumber(food['Calories'] * food['Servings'], 'Hundredths')
            $REPEATRESULTS.append(f'{food['Servings']}x {food['Name']} ({cals} kcal)')

        if $REPEATRESULTS is not None:
            # Is on the same line because stats already has new line in it
            $IFRESULT = f'''
            {stats}{Strings['foodslist.foods.selected']}:
            {$REPEATRESULTS}
            '''
        else:
            $IFRESULT = f'''
            {Strings['foodslist.foods.empty']}
            '''
        prompt = $IFRESULT
        
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
            case doneOpt:
                addMenuResult = FALSE

                if params['passToBulkEntry'] is not None:
                    # sends the foods dictionary and selection ids as foods info to the shortcut
                    dix = {
                        'selectedIds': [],
                        'foodsDix': {}
                    }
                    if selectedIds is not None:
                        dix['selectedIds'] = selectedIds
                        dix['foodsDix'] = foodsDix
                        StopShortcut(output = dix)
                    else:
                        StopShortcut(output = dix)
                else:
                    for listId in selectedIds:
                        food = foodsDix[listId]
                        $REPEATRESULTS.append(food)
                    StopShortcut(output = $REPEATRESULTS)

            case Strings['foodslist.menu.search']:
                $MENURESULT = RunShortcut(nutrDix['Search Algorithm'])

            case Strings['foodslist.menu.saved']:
                $MENURESULT = RunShortcut(nutrDix['Select Saved Foods'], input={'type': 'all'})

            case Strings['foodslist.menu.scan']:
                $MENURESULT = RunShortcut(nutrDix['Barcode Search'], input={'getFood': True})

            case Strings['foodslist.menu.recent']:
                $MENURESULT = RunShortcut(nutrDix['Get Recent'])

            case Strings['foodslist.menu.manual']:
                $MENURESULT = RunShortcut(nutrDix['Make Food Manually'])

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
                    $REPEATRESULTS.append(text)

                # cancel contact card
                text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=UTF-8:{Strings['opts.cancel']}
                    ORG;CHARSET=UTF-8:{Strings['savedfoods.none.desc']}
                    NOTE;CHARSET=UTF-8:Cancel
                    {cancelIcon}
                    END:VCARD
                    {$REPEATRESULTS}
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
                    $REPEATRESULTS.append(text)

                text = Text($REPEATRESULTS)
                renamedItem = SetName(text, 'vcard.vcf')
                contacts = GetContacts(renamedItem)

                deletes = ChooseFrom(contacts, selectMultiple=True, prompt=Strings['foods.remove.select'])

                for delete in deletes:
                    listId = Contact(delete).Notes
                    # remove it from the list
                    selectedIds = FilterFiles(selectedIds, where=['Name' != listId])

            case 'View Total Nutrients': #TODO add this to the String dictionary
                addMenuResult = FALSE
                # TODO FILL THIS IN

                outputFood = Dictionary(Text('{"Serving Size":"","Protein":0,"Trans":0,"Barcode":"0","Cholesterol":0,"Name":"Total Nutrients","Sugar":0,"Monounsaturated":0,"Polyunsaturated":0,"Fat":0,"Fiber":0,"VitC":0,"Calories":0,"Iron":0,"VitA":0,"Potassium":0,"Saturated":0,"Sodium":0,"Calcium":0,"Carbs":0}'))

                for nk in outputFood.keys
                    for listId in selectedIds:
                        foodVal = foodsDix[listId][nk]
                        servings = foodsDix[listId]['Servings']
                        $REPEATRESULTS.append(foodVal * servings)
                    if $REPEATRESULTS is not None:
                        outputFood[nk] = RoundNumber(CalculateStatistics('Sum', $REPEATRESULTS), 'Hundredths')

                prompt = f'''
                Total Nutrients
                {Strings['nutr.cals']}: {outputFood['Calories']}
                {Strings['nutr.carbs']}: {outputFood['Carbs']}g ⸱ {Strings['nutr.fat']}: {outputFood['Fat']}g ⸱ {Strings['nutr.protein']}: {outputFood['Protein']}g
                {Strings['nutr.sugar']}: {outputFood['Sugar']}g ⸱ {Strings['nutr.fiber']}: {outputFood['Fiber']}g 
                {Strings['nutr.monofat']}: {outputFood['Monounsaturated']}g
                {Strings['nutr.polyfat']}: {outputFood['Polyunsaturated']}g
                {Strings['nutr.saturfat']}: {outputFood['Saturated']}g ⸱ {Strings['nutr.cholesterol']}: {outputFood['Cholesterol']}mg ⸱ {Strings['nutr.sodium']}: {outputFood['Sodium']}mg ⸱ {Strings['nutr.potassium']}: {outputFood['Potassium']}mg
                {Strings['nutr.calcium']}: {outputFood['Calcium']}% ⸱ {Strings['nutr.iron']}: {outputFood['Iron']}% ⸱ {Strings['nutr.vita']}: {outputFood['VitA']}% ⸱ {Strings['nutr.vitc']}: {outputFood['VitC']}% 
                '''

                # Using Menu instead of alert because it shows the items in bold
                Menu(prompt):
                    case 'OK':
                        pass

            case 'Pause': # TODO translate this
                Alert(title='Shortcut Paused', body="The shortcut has been paused. When you're ready, open the Shortcuts app and the shortcut will continue running.", showCancel=False)
                WaitToReturn()


        if addMenuResult == TRUE:
            # add the foods to our selected foods
            menuFoods = []

            for food in $MENURESULT:
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

                $REPEATRESULTS.append(GetVariable(food))

            for food in $REPEATRESULTS:
                RunShortcut(nutrDix['Add Recent'], input=food)


        for sk in sumStats.keys
            for listId in selectedIds:
                foodVal = foodsDix[listId][sk]
                servings = foodsDix[listId]['Servings']
                $REPEATRESULTS.append(foodVal * servings)

            sumStats[sk] = RoundNumber(CalculateStatistics('Sum', $REPEATRESULTS), 'Hundredths')

                