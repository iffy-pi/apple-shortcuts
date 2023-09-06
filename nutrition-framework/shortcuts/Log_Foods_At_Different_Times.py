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
        
        setLogTimes = FALSE
        fromEditOption = FALSE

        Menu(text):
            case 'Log Added Foods':
                # breaks loop, foods are logged outside of loop
                breakLoop = TRUE

            case 'Add Foods':
                # unset Ids tracks the list ids of foods that dont have a log time since they were just added
                # it is used later on
                unsetIds = []
                for food in RunShortcut(nutrDix['Foods List']):
                    foodsInfo[nextId] = food
                    datesInfo[nextId] = date
                    selectedIds.append(nextId)
                    # adding food to list of foods that dont have a log time
                    unsetIds.append(nextId)
                    nextId = nextId+1

                # run set log time interface
                setLogTimes = TRUE

            case 'Set/Edit Log Time For Foods...':
                setLogTimes = TRUE
                # since user is requesting to edit the items
                # we make all the foods changeable by setting unsetIds to the full selectedIds list
                unsetIds = selectedIds
                fromEditOption = TRUE

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

                contacts = macros.textToContacts(REPEATRESULTS)

                selectedContacts = ChooseFromList(contacts, prompt='Select Foods To Remove', selectMultiple=True)
                
                # remove them from the selected Ids list
                for contact in selectedContacts:
                    listId = contact.Notes
                    selectedIds = FilterFiles(selectedIds, where=['Name' != listId])

            case 'Cancel and Exit':
                StopShortcut()

        if setLogTimes == TRUE:
            breakEditLoop = FALSE
            # unsetIds is used here so that:
            # when foods are added, users are immediately prompted to select the time for the added foods
            for _ in Count(unsetIds):
                # break loop when there are no more foods with unset log times
                if Count(unsetIds) == 0:
                    breakEditLoop = TRUE

                if breakEditLoop == FALSE:
                    # use contact vcards to get the list ids of the foods the user wants to change
                    for listId in unsetIds:
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

                    contacts = macros.textToContacts(REPEATRESULTS)

                    prompt = '''
                        Select foods to set/edit log time.
                        Select no foods to return to main menu.
                    '''

                    if hasFoodNotes == TRUE:
                        prompt = f'''
                        {notes}

                        {prompt}
                        '''

                    selectedContacts = ChooseFromList(contacts, prompt=prompt, selectMultiple=True)

                    if Count(selectedContacts) > 0:
                        contact = selectedContacts.getFirstItem()
                        date = datesInfo[contact.Notes]

                        for contact in selectedContacts:
                            food = foodsInfo[contact.Notes]
                            REPEATRESULTS.append(f'{food['Servings']}x {food['Name']}')

                        prompt = f'''
                            Select log time for:
                            {REPEATRESULTS}
                        '''

                        if hasFoodNotes == TRUE:
                            prompt = f'''
                                Food Notes:
                                {notes}

                                {prompt}
                            '''

                        date = AskForInput(Input.DateAndTime, prompt=text, default=date)

                        # for each of the foods, set the date that the user selected
                        # also remove from unset ids, so the loop will break if user sets log times for all unset foods
                        for contact in selectedContacts:
                            listId = contact.Notes
                            datesInfo[listId] = date
                            
                            # if user selected edit option, keep all foods visible
                            # i.e. dont filter out foods with set date.
                            if fromEditOption == FALSE:
                                unsetIds = FilterFiles(unsetIds, where=['Name' != listId])

                    # # if user specifically requested to edit food times, then break immediately after one iteration
                    # if fromEditOption == TRUE:
                    #     breakEditLoop = TRUE


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