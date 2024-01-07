'''
Framework: Nutrition (id = 4)
ID:  12
Ver: 1.11
'''

# Select foods to log at different times

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))
nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))

hasFoodNotes = FALSE

file = GetFile(From='Shortcuts', f"{storage}/Other/foodNotes.txt", errorIfNotFound=False)
if file is not None:
    notes = f'''
        {Strings['foodnotes']}:
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

instructions = Strings['logdiff.instr']
                .replace('$addopt', Strings['logdiff.action.add'])
                .replace('$donesel', Strings['foodslist.menu.done'])
                .replace('$logopt', Strings['logdiff.action.log'])

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


            updatedText = Strings['logdiff.loglist.prompt'].replace('$warn', '⚠')
            IFRESULT = f'''
                {updatedText}

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
            case Strings['logdiff.action.log']:
                # breaks loop, foods are logged outside of loop
                breakLoop = TRUE

            case Strings['logdiff.action.add']:
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

            case Strings['logdiff.action.edit']:
                setLogTimes = TRUE
                # since user is requesting to edit the items
                # we make all the foods changeable by setting unsetIds to the full selectedIds list
                unsetIds = selectedIds
                fromEditOption = TRUE

            case Strings['logdiff.action.remove']:
                # use contact vcards to get the list ids of the foods the user wants to remove
                for listId in selectedIds:
                    food = foodsInfo[listId]
                    date = datesInfo[listId]

                    if date is not None:
                        updatedText = Strings['logdiff.logtime'].replace('$date', date.format(custom='h:mm a, MMMM d'))
                        datePrompt = updatedText
                    else:
                        datePrompt = Strings['logdiff.notime.warn'].replace('$warn', '⚠')

                    updatedText = Strings['food.servings'].replace('$num', food['Servings'])

                    text = f'''
                        BEGIN:VCARD
                        VERSION:3.0
                        N;CHARSET=UTF-8:{food['Name']}{warning}
                        ORG;CHARSET=UTF-8:{updatedText} ⸱ {datePrompt}
                        NOTE;CHARSET=UTF-8:{listId}
                        END:VCARD
                    '''
                    REPEATRESULTS.append(text)

                contacts = macros.textToContacts(REPEATRESULTS)

                selectedContacts = ChooseFromList(contacts, prompt=Strings['foods.remove.select'], selectMultiple=True)
                
                # remove them from the selected Ids list
                for contact in selectedContacts:
                    listId = contact.Notes
                    selectedIds = FilterFiles(selectedIds, where=['Name' != listId])

            case Strings['nutr.menu.howtouse']:
                ShowAlert(instructions, title=Strings['logdiff.instr.title'], showCancel=False)

            case Strings['logdiff.exit']:
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
                            updatedText = Strings['logdiff.logtime'].replace('$date', date.format(custom='h:mm a, MMMM d'))
                            datePrompt = updatedText
                            warning = ''
                        else:
                            datePrompt = Strings['logdiff.notime.warn'].replace('$warn', '⚠')

                        updatedText = Strings['food.servings'].replace('$num', food['Servings'])

                        text = f'''
                            BEGIN:VCARD
                            VERSION:3.0
                            N;CHARSET=UTF-8:{food['Name']}{warning}
                            ORG;CHARSET=UTF-8:{updatedText} ⸱ {datePrompt}
                            NOTE;CHARSET=UTF-8:{listId}
                            END:VCARD
                        '''
                        REPEATRESULTS.append(text)

                    contacts = macros.textToContacts(REPEATRESULTS)

                    prompt = Strings['logdiff.settime.instr']

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
                            {Strings['logdiff.settime.select']}
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
        updatedText = Strings['logdiff.food.notime']
                        .replace('$servings', food['Servings'])
                        .replace('$name', food['Name'])
        Menu(updatedText):
            case Strings['logdiff.notime.log']:
                date = AskForInput(Input.DateAndTime, prompt=Strings['input.logtime'])
            case Strings['logdiff.notime.discard']:
                logFood = FALSE
    
    if logFood == TRUE:
        res = RunShortcut(nutrDix['Log Algorithm'], input={'Date': date, 'Food': food})
        loggedFoods.append(res)

# clearing foods notes and making preset
if hasNotes == TRUE:
    Menu(Strings['logt.clearnotes']):
        case Strings['opts.yes']:
            file = GetFile(From='Shortcuts', f"{storage}/Other/foodNotes.txt")
            DeleteFile(file, deleteImmediately=True)
        case Strings['opts.no']:
            pass

Menu(Strings['logt.makepreset']):
    case Strings['opts.yes']:
        RunShortcut(nutrDix['Make Preset'], input={ 'foodsInfo': foodsInfo })
    case Strings['opts.no']:
        pass