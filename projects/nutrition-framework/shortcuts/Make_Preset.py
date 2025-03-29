'''
Framework: Nutrition (id = 4)
ID:  17
Ver: 1.1
'''

# Make a preset with passed in foods or a new list of foods

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))
nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))

TRUE = 1
FALSE = 0

confirmServings = FALSE

foodsDix = {}
selectedIds = []
nextId = 0


if shortcutInput is not None:
    # If foods are passed in, then the user should be allowed to edit the servings
    confirmServings = TRUE

    item = shortcutInput.getItemAtIndex(1)
    if item['foodsInfo'] is not None:
        foodsInfo = item['foodsInfo']
else:
    # there is no input so use Foods List, with optimization
    foodsInfo = RunShortcut(nutrDix['Foods List'], input={ 'passToBulkEntry': True})


if foodsInfo is not None:
    # Get the selected IDs and foodsDix from output of Foods List
    selectedIds = foodsInfo['selectedIds']
    foodsDix = Dictionary(foodsInfo['foodsDix'])
else:
    foods = ShortcutInput
    # Generate selectedIds and foodsDix
    for item in foods:
        foodsDix[nextId] = item
        selectedIds.append(nextId)
        nextId = nextId+1

file = GetFile(From='Shortcuts', f'{storage}/Other/nutriKeys.txt')
nutriKeys = SplitText(file, '\n')

breakLoop = FALSE

# Get the presetNames
folder = GetFile(From='Shortcuts', f"{storage}/Presets/Foods", errorIfNotFound=False)
for file in GetContentsOfFolder(folder):
    presetNames.append(file['Name'])

for _ in Count(selectedIds):
    if breakLoop == FALSE:
        # Generate food contact cards
        for listId in selectedIds
            food = foodsDix[listId]
            updatedText = Strings['food.servings'].replace('$num', food['Servings'])
            text = f'''
            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=UTF-8:{food['Name']}
            ORG;CHARSET=UTF-8:{food['Serving Size']} ⸱ {updatedText}
            NOTE;CHARSET=UTF-8:{listId}
            END:VCARD
            '''
            $REPEATRESULTS.append(text)

        contacts = macros.textToContacts($REPEATRESULTS)

        if confirmServings == TRUE:
            $IFRESULT = f'''
            {Strings['makepreset.select.foods']}
            {Strings['makepreset.servings.editable']}
            '''
        else:
            $IFRESULT = Strings['makepreset.select.foods']

        text = f'''
            {$IFRESULT}
            {Strings['makepreset.howto.exit']}
        '''

        chosenIds = ChooseFrom(contacts, selectMultiple=True, selectAll=True, prompt=text)

        if Count(chosenIds) > 0:
            presetFood = {}

            for contact in chosenIds:
                # remove from selectedIds
                selectedIds = FilterFiles(selectedIds, where='Name' != contact.Notes)

                item = foodsDix[contact.Notes]
                curFood = Dictionary(item)

                # set the default name and serving size for preset food and name auto fill
                defaultSize = curFood['Serving Size']
                defaultName = curFood['Name']

                # Ask for servings if there are no servings or confirmServings is true
                askForServings = FALSE
                if confirmServings == TRUE:
                    askForServings = TRUE

                if curFood['Servings'] is None:
                    askForServings = TRUE

                if askForServings == TRUE:
                    updatedText = Strings['ask.for.servings']
                                    .replace('$name', defaultName)
                                    .replace('$size', defaultSize)
                    $IFRESULT = AskForInput(Input.Number, prompt=updatedText,
                                default=curFood['Servings'], allowDecimals=True, allowNegatives=False)
                else:
                    $IFRESULT = curFood['Servings']
                
                servings = Number($IFRESULT)

                # For each selected food, multiply food value by servings and add to preset Food
                for nutr in nutriKeys:
                    curFoodValue = Number(curFood[nutr])
                    presetValue = Number(presetFood[nutr])
                    calcResult = Calculate(curFoodValue * servings)
                    calcResult = Calculate(calcResult + presetValue)
                    num = RoundNumber(calcResult, hundredths)
                    presetFood[nutr] = num


            # now presetFood will have all the items
            if Count(chosenIds) > 1:
                defaultSize = ''
                defaultName = ''

            # Check if the current name already exists as a preset, and prompt user if it does
            name = AskForInput(Input.Text, prompt=Strings['makepreset.input.name'], default=defaultName)

            if Count(presetNames) > 0:
                breakNameLoop = FALSE
                for _ in range(10):
                    if breakNameLoop == FALSE:
                        res = FilterFiles(presetNames, where['Name' == name])
                        if res is not None:
                            Menu(Strings['editfood.name.exists'].replace('$name', name)):
                                case Strings['editfood.name.different']:
                                    name = AskForInput(Input.Text, prompt=Strings['editfood.name.new'])
                                case Strings['editfood.name.keep']:
                                    breakNameLoop = TRUE
                        else:
                            presetNames.append(name)
                            breakNameLoop = TRUE

            servingSize = AskForInput(Input.Text, prompt=Strings['makepreset.input.size'], default=defaultSize)

            # then set in the food
            foodId = RunShortcut(nutrDix["GFID"])
            presetFood['id'] = foodId
            presetFood['Serving Size'] = servingSize
            presetFood['Name'] = name

            # save to file
            SaveFile(To='Shortcuts', presetFood, f"{storage}/Presets/Foods/food_{foodId}.json", overwrite=True)

            Notification(
                Strings['makepreset.notif.msg'].replace('$name', presetFood['Name']),
                title=Strings['makepreset.notif.title']
                )

        else:
            breakLoop = TRUE

# delete the cache since it is invalid
file = GetFile(From='Shortcuts', f"{storage}/Presets/vcardCache.txt", errorIfNotFound=False)
DeleteFile(file, deleteImmediately=True)
