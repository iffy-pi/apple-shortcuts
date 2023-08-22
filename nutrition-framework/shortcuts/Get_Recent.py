'''
Framework: Nutrition (id = 4)
ID:  18
Ver: 1.0
'''

# Select one or more foods from recent

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

cancelIcon = # ... 

dir_ = GetFile(f"{storage}/Recents/Foods")

files = GetContentsOfFolder(dir_, errorIfNotFound=False)
# sorting by latest first allows last used food to be on top
files = filter(files, sortBy='Last Modified Date', order='Latest First')

# Generating contact cards for selected foods
for item in files:
    date = Text(item.lastModifiedDate.format(date="How Long Ago/Until"))
    food = Dictionary(item)

    text = f'''
        BEGIN:VCARD
        VERSION:3.0
        N;CHARSET=UTF-8:{food['name']}
        ORG;CHARSET=UTF-8:{food['Serving Size']} ⸱ {date}
        NOTE;CHARSET=UTF-8:{food['id']}
        END:VCARD
    '''
    REPEATRESULTS.append(text)

# Add cancel button
text = f'''
    BEGIN:VCARD
    VERSION:3.0
    N;CHARSET=UTF-8:No Selection
    ORG;CHARSET=UTF-8:No foods will be selected
    NOTE;CHARSET=UTF-8:Cancel
    {cancelIcon}
    END:VCARD
    {REPEATRESULTS}
'''
contacts = SetName(text, 'vcard.vcf')
            .GetContactsFromInput()

selectedItems = ChooseFrom(contacts, prompt="Select Recent Foods", selectMultiple=True)

for chosen in selectedItems:
    if chosen.Notes == 'Cancel':
        StopShortcut()

    file = GetFile(f"{storage}/Recents/Foods/food_{chosen.Notes}.json")
    selectedFoods.append(Dictionary(file))

StopShorcut(output = selectedFoods)

