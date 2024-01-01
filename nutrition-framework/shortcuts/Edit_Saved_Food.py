'''
Framework: Nutrition (id = 4)
ID:  15
Ver: 1.01
'''

# Used to edit saved foods, either preset or barcode

TRUE = 1
FALSE = 0
storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

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

    Menu(f"What type of editing would you like to do for {oldFood['Name']}?"):
        case 'Scale Serving Size':
            mult = AskForInput(Input.Number, prompt=f'What is the scaling factor?', default=1, allowDecimals=True)
            if mult != 1:
                for item in nutriKeys:
                    num = Number(oldFood[item])
                    num = Calculate(num * mult)
                    num = RoundNumber(num, hundredths)
                    oldFood[item] = num

                oldFood['Serving Size'] = AskForInput(Input.Text, prompt="What is the new serving size?", default=f"{mult} of {oldFood['Serving Size']}")
            
            MENURESULT = oldFood

        case 'Edit Food Fields Manually':
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
                    Menu(f'There is already a food named "{name}"'):
                        case 'Select A Different Name':
                            name = AskForInput(Input.Text, prompt=f'"{name}" already exists, please select a new name')
                        case 'Keep both foods with this name':
                            breakLoop = TRUE
                else:
                    breakLoop = TRUE

    newFood['Name'] = name

    # save the file
    SaveFile(To='Shortcuts', newFood, f"{config['folder']}/food_{foodId}.json", overwrite=True)

# delete the cache since it is invalid
file = GetFile(From='Shortcuts', f"{config['folder']}/vcardCache.txt", errorIfNotFound=False)
DeleteFile(file, deleteImmediately=True)


