'''
Framework: Nutrition (id = 4)
ID:  12
Ver: 1.0
'''

TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

nutrDix = Dictionary(GetFile(f"{storage}/Other/shortcutNames.json"))

foodsInfo = RunShortcut(nutrDix['Foods List'], input={ 'passToBulkEntry': True})

foodsDix = Dictionary(foodsInfo['foodsDix'])
selectedIds = foodsInfo['selectedIds']

hasNotes = FALSE

file = GetFile(f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
if file is not None:
    notes = f'''
        Food Notes:
        {file}

    '''
    notes = IFRESULT
    hasNotes = TRUE

for _ in range(Count(selectedIds)):
    if Count(selectedIds) > 0:
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

    # max repeat will be at most items
    contacts = textToContacts(REPEATRESULTS)

    if hasNotes == TRUE:
        IFRESULT = f'''
        {notes}

        Select foods to log for time...
        '''
    else:
        IFRESULT = 'Select foods to log for time...'

    chosen = ChooseFrom(contacts, prompt=IFRESULT, selectMultiple=True)
    
    date = AskForInput(Input.DateAndTime, "What time should the selected foods be logged at?")

    for item in chosen:
        # remove from the list
        listId = Contact(item).Notes
        selectedIds = filter(selectedIds, where=['Name' == listId])
        food = foodsDix[listId]
        text = {
            'Date': date.format(date="medium", time="short"),
            'Food': food
        }
        res = RunShortcut('Log Algorithm', input=text)
        loggedFoods.append(res)

    if hasNotes == TRUE:
        Menu('Clear food notes?'):
            case 'Yes':
                file = GetFile(f"{storage}/Other/foodNotes.txt")
                DeleteFile(file, deleteImmediately=True)
            case 'No':
                pass
    
    Menu('Make Preset?'):
        case 'Yes':
            RunShortcut(nutrDix['Make Preset'], input=loggedFoods)
        case 'No':
            pass
