'''
Framework: Nutrition (id = 4)
ID:  12
Ver: 1.11
'''

# Select foods to log at different times

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))

hasFoodNotes = FALSE

file = GetFile(From='Shortcuts', f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
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

instructions = '''
            To log foods at different times:
            1. Tap "Add Foods To Log List" to and add all the foods you wish to log for a given time.
            
            2. Tap "Done Selecting Foods".
            
            3. Select the foods from the list and apply the time you wish to log them at.
            
            4. Repeat Steps 1-3 for foods at the other log times.
            
            5. Tap "Log Foods in Log List" to log the foods at their assigned times.
            '''

for _ in range(30):
    if breakLoop == FALSE:
        # Generate a simple menu prompt listing all the foods added with their log times
        if Count(selectedIds) > 0:
            for listId in selectedIds:
                date = datesInfo[listId]
                text = f'''
                        BEGIN:VCARD
                        VERSION:3.0
                        N;CHARSET=UTF-8:{date.format(custom='yyyyMMddHHmm')}
                        NOTE;CHARSET=UTF-8:{listId}
                        END:VCARD
                    '''
                REPEATRESULTS.append(text)

            contacts = macros.textToContacts(f'{REPEATRESULTS}')

            for contact in FilterFiles(contacts, sortBy='Name', order='A to Z'):
                listId = contact.Notes
                food = foodsInfo[listId]
                date = datesInfo[listId]
                warning = ''
                if date is not None:
                    datePrompt = f'{date.format(custom='MMM d, h:mm a')}: '
                else:
                    warning = ' ⚠'
                    datePrompt = ''

                REPEATRESULTS.append(f'{datePrompt}{food['Servings']}x {food['Name']}{warning}')

            IFRESULT = f'''
                Food Log List:
                Foods with ⚠ have no log time.

                {REPEATRESULTS}
            '''
        else:
            IFRESULT = GetVariable(instructions)

        prompt = IFRESULT

        if hasFoodNotes == TRUE:
            prompt = f'''
                {notes}

                {prompt}
            '''
        
        setLogTimes = FALSE
        fromEditOption = FALSE

        Menu(prompt):
            case 'Log Foods In Log List':
                # breaks loop, foods are logged outside of loop
                breakLoop = TRUE

            case 'Add Foods To Log List':
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

            case 'Set/Edit Log Time For Foods In Log List':
                setLogTimes = TRUE
                # since user is requesting to edit the items
                # we make all the foods changeable by setting unsetIds to the full selectedIds list
                unsetIds = selectedIds
                fromEditOption = TRUE

            case 'Remove Food in Log List':
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

            case 'How To Use':
                ShowAlert(instructions, title='Instructions', showCancel=False)

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
            file = GetFile(From='Shortcuts', f"{storage}/Other/foodNotes.txt")
            DeleteFile(file, deleteImmediately=True)
        case 'No':
            pass

Menu('Make Preset?'):
    case 'Yes':
        RunShortcut(nutrDix['Make Preset'], input={ 'foodsInfo': foodsInfo })
    case 'No':
        pass