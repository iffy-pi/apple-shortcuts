'''
Framework: Nutrition (id = 4)
ID:  16
Ver: 1.01
'''

TRUE = 1
FALSE = 0
storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

cancelIcon = Text() 

deleteMode = FALSE

savedInfo = {
    'barcodes': { 'folder': 'Barcodes', 'prompt': 'Barcoded Foods'}
    'presets': { 'folder': 'Presets', 'prompt': 'Presets'}
    'all': { 'prompt' : 'Preset(s) and Barcoded Food(s)'}
}

params = Dictionary(ShortcutInput)

if typeDir[ params['type']] is None:
    Alert('No type specified')
    StopShortcut()
else:
    config = savedInfo [ params['type'] ]


if params['deleteMode'] is not None:
    deleteMode = TRUE


if params['type'] == 'all':
    IFRESULT = [ 'presets', 'barcodes' ]
else:
    IFRESULT = params['type']
searchTypes = IFRESULT

for curType in searchTypes:
    dixVal = savedInfo[curType]
    parentFolder = dixVal['folder']
    prompt = dixVal['prompt']

    file = GetFile(f"{storage}/{parentFolder}/vcardCache.txt", errorIfNotFound=False)
    if file is not None:
        IFRESULT = Text(file)
    else:
        # create the vcard cache
        folder = GetFile(f"{storage}/{parentFolder}/Foods")
        files = GetContentsOfFolder(folder)
        files = filter(files, sortBy='Last Modified Date', order='Latest First')
        for item in files:
            food = Dictionary(file)
            # some weird bug is limiting me to have to pull ID separately
            dixVal = food['id']
            dix = {
                'folder': parentFolder,
                'id': dixVal
            }
            text = f'''
                BEGIN:VCARD
                VERSION:3.0
                N;CHARSET=UTF-8:{food['Name']}
                ORG;CHARSET=UTF-8:{prompt} ⸱ {food['Serving Size']}
                NOTE;CHARSET=UTF-8:{dix}
                END:VCARD

            '''
            REPEATRESULTS.append(text)

        SaveFile(Text(REPEATRESULTS), f"{storage}/{parentFolder}/vcardCache.txt", overwrite=True)

        IFRESULT = Text(REPEATRESULTS)

vcardCache = Text(REPEATRESULTS)


text = f'''
    BEGIN:VCARD
    VERSION:3.0
    N;CHARSET=UTF-8:No Selection
    ORG;CHARSET=UTF-8:No foods will be selected
    NOTE;CHARSET=UTF-8:Cancel
    {cancelIcon}
    END:VCARD
'''

renamedItem = SetName(text, 'vcard.vcf')
contact = GetContacts(renamedItem)
choices.append(contact)

SetName(vcardCache, 'vcard.vcf')
contacts = GetContacts(renamedItem)
files = filter(contacts, sortBy='Name')
choices.append(files)


if deleteMode == TRUE:
    IFRESULT = f"Select {config['prompt']} to Delete"
else:
    IFRESULT = f"Select {config['prompt']}"

selectedItems = ChooseFrom(choices, prompt=IFRESULT, selectMultiple=True)
for chosen in selectedItems:
    if chosen.Notes == 'Cancel':
        StopShortcut()

    dix = Dictionary(chosen.Notes)

    foodId = dix['id']
    parentFolder = dix['folder']

    # make this the most used one
    file = GetFile(f"{storage}/{parentFolder}/Foods/food_{foodId}.json")
    if file is not None:
        food = Dictionary(file)

        if deleteMode == TRUE:
            # delete the file
            DeleteFile(file, deleteImmediately=True)
            Notification(f'{config['prompt']} {food['Name']} has been deleted!')
    
        # add the food
        selectedFoods.append(food)

if deleteMode == TRUE:
    # delete the cache since it is invalid
    file = GetFile(f"{storage}/{parentFolder}/vcardCache.txt", errorIfNotFound=False)
    DeleteFile(file, deleteImmediately=True)

    if params['type'] == 'barcodes':
        file = GetFile(f"{storage}/{parentFolder}/barcodeCache.json", errorIfNotFound=False)
        DeleteFile(file, deleteImmediately=True)

StopShortcut(output = selectedFoods)
    
