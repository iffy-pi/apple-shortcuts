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

hasFoodNotes = FALSE

file = GetFile(f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
if file is not None:
    notes = f'''
        Food Notes:
        {file}

    '''
    hasFoodNotes = TRUE


# Each food item has a unique list ID which is different from their food id
# For a given listId i, foodsInfo[i] is the food for that listId and
# datesInfo[i] is the date and time for that list id
foodsInfo = {}
datesInfo = {}
selectedIds = []
breakLoop = FALSE
nextId = 0

for _ in range(30):
    if breakLoop == FALSE:
        # Generate a simple menu prompt listing all the foods added with their log times
        if Count(selectedIds) > 0:
            for listId in selectedIds:
                food = foodsInfo[listId]
                date = datesInfo[listId]

                REPEATRESULTS.append(f'{food['Servings']}x {food['Name']} for {date.format(custom='h:mm a, MMM d')}')

            IFRESULT = f'''
                Added Foods:
                {REPEATRESULTS}
            '''
        else:
            IFRESULT = 'No Foods Added'

        basePrompt = IFRESULT

        if hasFoodNotes == TRUE:
            IFRESULT = f'''
                {notes}

                {basePrompt}
            '''
        else:
            IFRESULT = basePrompt

        text = f'''
            {IFRESULT}
            Select An Option
        '''

        Menu(text):
            case 'Log Added Foods':
                # breaks loop, foods are logged outside of loop
                breakLoop = TRUE

            case 'Add Foods For Time':
                # Asks user for the date, runs foods list and maps 
                # the selected foods to the given date and time 
                date = AskForInput(Input.DateAndTime, prompt='Select Date and Time')
                for food in RunShortcut(nutrDix['Foods List']):
                    foodsInfo[nextId] = food
                    datesInfo[nextId] = date
                    selectedIds.append(nextId)
                    nextId = nextId+1

            case 'Edit Times For Food...':
                # use contact vcards to get the list ids of the foods the user wants to change
                for listId in selectedIds:
                    food = foodsInfo[listId]
                    date = datesInfo[listId]
                    text = f'''
                        BEGIN:VCARD
                        VERSION:3.0
                        N;CHARSET=UTF-8:{food['Name']}
                        ORG;CHARSET=UTF-8:{food['Servings']} servings ⸱ {date.format(custom='h:mm a, MMMM d')}
                        NOTE;CHARSET=UTF-8:{listId}
                        END:VCARD
                    '''
                    REPEATRESULTS.append(text)

                contacts = textToContacts(REPEATRESULTS)

                selectedContacts = ChooseFromList(contacts, prompt='Select Foods To Edit', selectMultiple=True)
                
                # for each of the foods, use the input prompt to get the new date and time
                for contact in selectedContacts:
                    listId = contact.Notes
                    food = foodsInfo[listId]
                    date = datesInfo[listId]
                    date = AskForInput(Input.Date, prompt=f'Select new date and time for {food['Servings']}x {food['Name']}', default=date)
                    datesInfo[listId] = date

            case 'Remove Added Food...':
                # use contact vcards to get the list ids of the foods the user wants to remove
                for listId in selectedIds:
                    food = foodsInfo[listId]
                    date = datesInfo[listId]
                    text = f'''
                        BEGIN:VCARD
                        VERSION:3.0
                        N;CHARSET=UTF-8:{food['Name']}
                        ORG;CHARSET=UTF-8:{food['Servings']} servings ⸱ {date.format(custom='h:mm a, MMMM d')}
                        NOTE;CHARSET=UTF-8:{listId}
                        END:VCARD
                    '''
                    REPEATRESULTS.append(text)

                contacts = textToContacts(REPEATRESULTS)

                selectedContacts = ChooseFromList(contacts, prompt='Select Foods To Remove', selectMultiple=True)
                
                # remove them from the selected Ids list
                for contact in selectedContacts:
                    listId = contact.Notes
                    selectedIds = filter(selectedIds, where=['Name' == listId])

            case 'Cancel and Exit':
                StopShortcut()

# log the foods in the selected Ids list
for listId in selectedIds:
    food = foodsInfo[listId]
    date = datesInfo[listId]
    res = RunShortcut(nutrDix['Log Algorithm'], input={'Date': date, 'Food': food})
    loggedFoods.append(res)

# clearing foods notes and making preset
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