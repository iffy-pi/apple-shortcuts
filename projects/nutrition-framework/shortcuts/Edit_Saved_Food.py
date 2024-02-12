'''
Framework: Nutrition (id = 4)
ID:  15
Ver: 1.1
'''

# Used to edit saved foods, either preset or barcode

TRUE = 1
FALSE = 0
storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))

params = Dictionary(ShortcutInput)

savedInfo = {
    'barcodes': { 'folder': f'{storage}/Barcodes', 'prompt': 'Barcoded Food'}
    'presets': { 'folder': f'{storage}/Presets', 'prompt': 'Preset'}
}

nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))

# To determine whether we are editing for a preset or barcode we use the `type` field in the parameter dictionary passed into the shortcut
# This can either be `barcodes` or `presets`

if params['args'] is not None:
    IFRESULT = params['args']
else:
    IFRESULT = RunShortcut(nutrDix['Select Saved Foods'], input=params)
selectedFoods = IFRESULT

# get the config for the given type from saved info, this includes the food folder as well as the prompt
config = savedInfo [ params['type'] ]

file = GetFile(From='Shortcuts', f"{storage}/Other/nutriKeys.txt")
nutriKeys = SplitText(file, '\n')

for item in selectedFoods:
    oldFood = Dictionary(item)
    
    foodId = food['id']

    Menu(Strings['editfood.action'].replace('$name', food['Name'])):
        case Strings['editfood.opt.scale']:
            mult = AskForInput(Input.Number, prompt=Strings['editfood.scale.input'], default=1, allowDecimals=True)
            if mult != 1:
                for item in nutriKeys:
                    num = Number(oldFood[item])
                    num = Calculate(num * mult)
                    num = RoundNumber(num, hundredths)
                    oldFood[item] = num

                oldFood['Serving Size'] = AskForInput(Input.Text, prompt=Strings['editfood.size.input'], default=f"{oldFood['Serving Size']}")
            
            MENURESULT = oldFood

        case Strings['editfood.opt.edit']:
            # Edit foods with display food item
            MENURESULT = RunShortcut(nutrDix['Display Food Item'], input=oldFood)

    newFood = MENURESULT
    name = newFood['Name']

    if name != oldFood['Name']:
        # need to ensure it isnt taken by something else

        # check to make sure it doesnt clash with other food names
        folder = GetFile(From='Shortcuts', f"{config['folder']}/Foods", errorIfNotFound=False)
        for food in GetContentsOfFolder(folder):
            foodNames.append(food['Name'])

        breakLoop = FALSE
        for _ in range(10):
            if breakLoop == FALSE:
                res = FilterFiles(foodNames, whereAll=['Name' == name, 'Name' != oldFood['Name']])
                if res is not None:
                    Menu(Strings['editfood.name.exists'].replace('$name', name)):
                        case Strings['editfood.name.different']:
                            name = AskForInput(Input.Text, prompt=Strings['editfood.name.new'])
                        case Strings['editfood.name.keep']:
                            breakLoop = TRUE
                else:
                    breakLoop = TRUE

    newFood['Name'] = name

    # save the file
    SaveFile(To='Shortcuts', newFood, f"{config['folder']}/food_{foodId}.json", overwrite=True)

# delete the cache since it is invalid
file = GetFile(From='Shortcuts', f"{config['folder']}/vcardCache.txt", errorIfNotFound=False)
DeleteFile(file, deleteImmediately=True)


