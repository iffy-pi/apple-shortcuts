TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

confirmServings = FALSE

nutrDix = Dictionary(GetFile(f"{storage}/Other/shortcutNames.json"))

if ShortcutInput is not None:
    confirmServings = TRUE
    # if we dont do this, then if result will be the item above the if
    # i.e. nutrDix
    IFRESULT = GetVariable(ShortcutInput)
else:
    IFRESULT = RunShortcut(nutrDix['Foods List'])

foods = IFRESULT

file = GetFile(f'{storage}/Other/nutriKeys.txt')
nutriKeys = SplitText(file, '\n')

foodsDix = {}
selectedIds = []
nextId = 0

breakLoop = FALSE

# create selection system
for item in foods:
    foodsDix[nextId] = item
    selectedIds.append(nextId)
    nextId = nextId+1

# check to make sure it doesnt clash with other food names
folder = GetFile(f"{storage}/Presets/Foods", errorIfNotFound=False)
for file in GetContentsOfFolder(folder):
    presetNames.append(file['Name'])

for _ in Count(foods):
    if breakLoop == FALSE:
        for listId in selectedIds
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

        contacts = textToContacts(REPEATRESULTS)

        if confirmServings == TRUE:
            IFRESULT = f'Select Foods to be made into Preset\nYou can edit the servings of selected foods'
        else:
            IFRESULT = "Select Foods to be made into Preset"

        text = f'{IFRESULT}\nSelect no items if you wish to exit'

        chosenIds = ChooseFrom(contacts, selectMultiple=True, selectAll=True, prompt=IFRESULT)

        if Count(chosenIds) > 0:
            presetFood = {}

            for contact in chosenIds:
                # remove from selectedIds
                selectedIds = filter(selectedIds, where='Name' != contact.Notes)

                item = foodsDix[contact.Notes]
                curFood = Dictionary(item)

                defaultSize = curFood['Serving Size']
                defaultName = curFood['Name']

                askForServings = FALSE

                if confirmServings == TRUE:
                    askForServings = TRUE

                if curFood['Servings'] is None:
                    askForServings = TRUE

                if askForServings == TRUE:
                    IFRESULT = AskForInput(Input.Number, prompt=f'How many servings of "{defaultName}"? (1 serving = {defaultSize})',
                                default=1, allowDecimals=True, allowNegatives=False)
                servings = IFRESULT

                for nutr in nutriKeys:
                    curFoodValue = Number(curFood[nutr])
                    presetValue = Number(presetFood[nutr])
                    num = (curFoodValue*servings) + presetValue
                    num = RoundNumber(num, hundredths)
                    presetFood[nutr] = num


            # now presetFood will have all the items
            if Count(chosenIds) > 1:
                defaultSize = ''
                defaultName = ''

            name = AskForInput(Input.Text, prompt="What is the name of this preset?", default=defaultName)

            if Count(presetNames) > 0:
                breakLoop = FALSE
                for _ in range(10):
                    if breakLoop == FALSE:
                        res = filter(presetNames, where['Name' == name])
                        if res is not None:
                            Menu(f'Preset "{name}" already exists'):
                                case 'Select a different name':
                                    name = AskForInput(Input.Text, prompt=f'"{name}" already exists, please select a new name', default=name)
                                case 'Keep both with same name':
                                    breakLoop = TRUE
                        else:
                            presetNames.append(name)
                            breakLoop = TRUE

            servingSize = AskForInput(Input.Text, prompt="What is the serving size of this preset?", default=defaultSize)

            # then set in the food
            foodId = RunShortcut(nutrDix["GFID"])
            presetFood['id'] = foodId
            presetFood['Serving Size'] = servingSize
            presetFood['Name'] = name

            # save to file
            SaveFile(presetFood, f"{storage}/Presets/Foods/food_{foodId}.json", overwrite=True)

        else:
            breakLoop = TRUE

# delete the cache since it is invalid
file = GetFile(f"{storage}/Presets/vcardCache.txt", errorIfNotFound=False)
DeleteFile(file, deleteImmediately=True)
