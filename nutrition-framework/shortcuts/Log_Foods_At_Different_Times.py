'''
Framework: Nutrition (id = 4)
ID:  12
Ver: 1.02
'''

# Select foods to log at different times

TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

nutrDix = Dictionary(GetFile(f"{storage}/Other/shortcutNames.json"))

# Get all the foods to log by running Foods_List.py
foodsInfo = RunShortcut(nutrDix['Foods List'], input={ 'passToBulkEntry': True})

# foodsDix maps unique list ID to each food
# selectedIds contains the list IDs of the selected foods
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

# Count the selected items
for _ in range(Count(selectedIds)):
    if Count(selectedIds) > 0:
        # Generate food contact cards
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

        # If there are food notes, add them to the menu prompt so that users can see the time
        if hasNotes == TRUE:
            IFRESULT = f'''
            {notes}

            Select foods to log for time...
            Foods will be logged after all foods have been selected.
            '''
        else:
            IFRESULT = 'Select foods to log for time...\nFoods will be logged after all foods have been selected.'

        chosen = ChooseFrom(contacts, prompt=IFRESULT, selectMultiple=True)
        
        # Ask for the date to log selected foods at time
        date = AskForInput(Input.DateAndTime, "What time should the selected foods be logged at?")

        for item in chosen:
            # Get the list ID from contact notes, filter it from the remaining items in the list
            # Then use the ID to get the food and add it to items to log
            listId = Contact(item).Notes
            selectedIds = filter(selectedIds, where=['Name' == listId])
            food = foodsDix[listId]
            dix = Dictionary({
                'Date': date.format(date="medium", time="short"),
                'Food': food
            })
            logItems.append(dix)

for item in logItems:
    # Log the foods outside the loop, done to fast track user input
    res = RunShortcut(nutrDix['Log Algorithm'], input=item)
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
        RunShortcut(nutrDix['Make Preset'], input={ 'foodsInfo': foodsInfo })
    case 'No':
        pass
