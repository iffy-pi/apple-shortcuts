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
                warning = ''
                if date is not None:
                    datePrompt = f' for {date.format(custom='h:mm a, MMM d')}'
                else:
                    warning = ' ⚠'
                    datePrompt = ''

                REPEATRESULTS.append(f'{food['Servings']}x {food['Name']}{datePrompt}{warning}')

            IFRESULT = f'''
                Added Foods:
                {REPEATRESULTS}
            '''
        else:
            IFRESULT = 'No Foods Added'

        prompt = IFRESULT

        if hasFoodNotes == TRUE:
            prompt = f'''
                {notes}

                {prompt}
            '''
        text = f'''
            Foods with ⚠ have no log time.
            
            {prompt}
        '''
        Menu(text):
            case 'Log Added Foods':
                # breaks loop, foods are logged outside of loop
                breakLoop = TRUE

            case 'Add Foods':
                for food in RunShortcut(nutrDix['Foods List']):
                    foodsInfo[nextId] = food
                    datesInfo[nextId] = date
                    selectedIds.append(nextId)
                    nextId = nextId+1

            case 'Set/Edit Log Time For Foods...':
                # use contact vcards to get the list ids of the foods the user wants to change
                for listId in selectedIds:
                    food = foodsInfo[listId]
                    date = datesInfo[listId]
                    warning = ''

                    if date is not None:
                        datePrompt = f'Log Time: {date.format(custom='h:mm a, MMMM d')}'
                    else:
                        datePrompt = 'No Log Time Added ⚠'

                    text = f'''
                        BEGIN:VCARD
                        VERSION:3.0
                        N;CHARSET=UTF-8:{food['Name']}{warning}
                        ORG;CHARSET=UTF-8:{food['Servings']} servings ⸱ Log Time: {date.format(custom='h:mm a, MMMM d')}
                        NOTE;CHARSET=UTF-8:{listId}
                        END:VCARD
                    '''
                    REPEATRESULTS.append(text)

                contacts = textToContacts(REPEATRESULTS)

                selectedContacts = ChooseFromList(contacts, prompt='Select Foods To Edit', selectMultiple=True)

                if Count(selectedContacts) > 0:

                    contact = selectedContacts.getFirstItem()
                    date = datesInfo[contact.Notes]
                    date = AskForInput(Input.DateAndTime, prompt=f'Select log time for selected foods', default=date)

                    
                    # for each of the foods, set the date that the user selected
                    for contact in selectedContacts:
                        listId = contact.Notes
                        datesInfo[listId] = date

            case 'Remove Added Food...':
                # use contact vcards to get the list ids of the foods the user wants to remove
                for listId in selectedIds:
                    food = foodsInfo[listId]
                    date = datesInfo[listId]

                    if date is not None:
                        datePrompt = f'Log Time: {date.format(custom='h:mm a, MMMM d')}'
                        warning = ''
                    else:
                        datePrompt = 'No Log Time Added! ⚠'

                    text = f'''
                        BEGIN:VCARD
                        VERSION:3.0
                        N;CHARSET=UTF-8:{food['Name']}{warning}
                        ORG;CHARSET=UTF-8:{food['Servings']} servings ⸱ {datePrompt}
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
    logFood = TRUE
    if date is None:
        Menu(f'{food['Servings']}x {food['Name']} does not have a log time'):
            case 'Set Log Time':
                date = AskForInput(Input.DateAndTime, prompt='Enter Log Time')
            case 'Do Not Log Food':
                logFood = FALSE
    
    if logFood == TRUE:
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