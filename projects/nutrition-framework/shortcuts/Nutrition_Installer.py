'''
Framework: Nutrition (id = 4)
Is installer shortcut
'''

# Installer for the nutrition shortcut

TRUE = 1
FALSE = 0

newInstall = TRUE
proceedWithUpdates = FALSE
exitAfterConfig = FALSE
freshConfig = FALSE

updateInfo = {
    'updateLink' : 'https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/updates.json',
    'version':'4.22'
}

# also now includes information about the children
childVers = {
    "19":"1.01",      # Add Recent
    "20":"1.1",      # Barcode Search
    "24":"1.1",      # Calculate Stats
    "14":"1.01",      # Clear Cache And Backlog
    "10":"1.01",     # Display Food Item
    "15":"1.1",      # Edit Saved Food
    "22":"1.1",      # Food History
    "6":"1.1",      # Foods List
    "9":"1.0",       # Generate Food ID
    "18":"1.1",      # Get Recent
    "7":"1.2",       # Log Algorithm
    "12":"1.2",     # Log Foods At Different Times
    "11":"1.1",     # Log Foods At Time
    "25":"1.0",      # Log Nutrients to Health
    "21":"1.1",      # Make Food Manually
    "17":"1.1",     # Make Preset
    "5":"1.11",       # Nutrition
    "23":"1.1",      # Nutrition Statistics
    "13":"1.1",      # Saved And Search
    "8":"1.1",      # Search Algorithm
    "16":"1.1",      # Select Saved Foods
}

emojiUnicodes = {
    "arrow": "&#x27A1;&#xFE0F;",
    "clock": "&#x1F566;",
    "checkmark": "&#x2705;",
    "notes": "&#x1F4DD;",
    "mailbox": "&#x1F4EC;",
    "books": "&#x1F4DA;",
    "magnifier": "&#x1F50E;"
}

params = Dictionary(ShortcutInput)


Strings = {}

# Configure storage and language here
# First get the storage if it exists
storageFile = GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt", errorIfNotFound=False)

# Set the strings dictionary if it exists
if storageFile is not None:
    text = Text(storageFile)
    stringsFile = GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json", errorIfNotFound=False)
    if stringsFile is not None:
        Strings = Dictionary(stringsFile)
    #endif
#endif


# If the dictionary is empty then we go online to get the language
if Count(Strings.keys) == 0:
    # If there is no storage we don't know the language, let the user select it here
    langs = Dictionary(GetContentsOfURL('https://iffy-pi.github.io/apple-shortcuts/public/nutrition/languages/language_options.json'))
    item = ChooseFromList(langs.Keys, prompt='Select a language')
    selectedLang = langs[item]
    Strings = Dictionary(GetContentsOfURL(f'https://iffy-pi.github.io/apple-shortcuts/public/nutrition/languages/{selectedLang}'))
#endif


if storageFile is not None:
    storage = Text(storageFile)
    SaveFile(To='Shortcuts', Strings, f"{storage}/Other/gui_strings.json", overwrite=True)
else:
    freshConfig = TRUE
#endif


if params['updateCheck'] is not None:
    newInstall = FALSE
else:
    Menu():
        case Strings['installer.action.install']:
        case Strings['installer.action.update']:
            newInstall = FALSE
        case Strings['installer.action.config']:
            newInstall = FALSE
            freshConfig = TRUE
            exitAfterConfig = TRUE
    #endmenu
#endif


if freshConfig == TRUE:
    blockIfFolderExists = TRUE

    # If its a new install then let user enter folder
    if newInstall == TRUE:
        newStorage = AskForInput(Input.Text, prompt=Strings['installer.storage.input'], default='Nutrition')
    else:
        # Not new install means folder cannot be found, let user select it
        Menu(Strings['installer.storage.notfound']):
            case Strings['installer.storage.select']:
                folder = SelectFile(folders=True)
                newStorage = f'{folder.Name}'
                blockIfFolderExists = FALSE
            case Strings['installer.storage.create']:
                newStorage = AskForInput(Input.Text, prompt=Strings['installer.storage.input'], default='Nutrition')
        #endmenu
    #endif

    if blockIfFolderExists == TRUE:
        breakLoop = FALSE
        for _ in range(10):
            if breakLoop == FALSE:
                if GetFile(From='Shortcuts', newStorage, errorIfNotFound=False) is not None:
                    updatedText = Strings['installer.storage.exists'].replace('$storage', newStorage)
                    newStorage = AskForInput(Input.Text, prompt=updatedText)
                else:
                    breakLoop = TRUE
                #endif
            #endif
        #endfor
    #endif

    storage = newStorage

    SaveFile(To='Shortcuts', storage, "Nutrition_Shortcut_Storage_Folder_Name.txt", overwrite=True)
    SaveFile(To='Shortcuts', Strings, f'{storage}/Other/gui_strings.json', overwrite=True)

    if newInstall == TRUE:
        Alert(Strings['installer.storage.info'], showCancel=False)
    #endif
#endif


if exitAfterConfig == TRUE:
    StopShortcut()
#endif


if params['useTest'] is not None:
    updateInfo['updateLink'] = 'https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/testupdates.json'
#endif

if newInstall == TRUE:
    # If we are doing a new install, we have to save the shortcutNames
    # And also generate installation links for all the children files

    dix = Dictionary(...) # shortcutNames.json
    SaveFile(To='Shortcuts', dix, f"{storage}/Other/shortcutNames.json") # save shortcut names file

    proceedWithUpdates = TRUE

    # reset updateInfo version to 0.0 to force check
    updateInfo['version'] = 0.0

    # reset child vers to 0
    childVers = {}
#endif

updateRes = Dictionary(GetContentsOfURL(updateInfo['updateLink']))

if Number(updateRes['version']) > updateInfo['version']:
    if proceedWithUpdates == FALSE:
        # ask the user
        for _ in range(5):
            if proceedWithUpdates == FALSE:
                text = f'''
                    {Strings['installer.updating.new']}
                    v{updateInfo['version']} => v{updateRes['version']}
                '''
                Menu(text):
                    case Strings['installer.updating.whatsnew']:
                        text = f'''
                        # In v{updateRes['version']}:
                        {updateRes['releaseNotes']}
                        '''
                        richText = MakeRichTextFromMarkdown(text)
                        QuickLook(richText)
                    
                    case Strings['installer.updating.update']:
                        proceedWithUpdates = TRUE
                    
                    case Strings['opts.exit']:
                        StopShortcut()
                #endmenu
            #endif
        #endfor
    #endif


    if proceedWithUpdates == TRUE:
        # download the new gui strings
        Strings = Dictionary(GetContentsOfURL(f'https://iffy-pi.github.io/apple-shortcuts/public/nutrition/languages/{Strings['_string_lang_file']}'))
        SaveFile(To='Shortcuts', Strings, f'{storage}/Other/gui_strings.json', overwrite=True)

        updateText = []
        updateLinks = []

        # updater shorcut needs to be updated
        if newInstall == FALSE:
            updateText.append(f"- Nutrition Installer: v{updateInfo['version']} {emojiUnicodes['arrow']} v{updateRes['version']}")
            updateLinks.append(f"- Nutrition Installer - [Download]({updateRes['link']})")
        #endif

        for child in updateRes['children']:
            curVer = childVers[ child['id'] ]
            # using number action so if curver does not exist, then its evaluated to 0
            if Number(child['version']) > Number(curVer):
                updateText.append(f"- {child['name']}: v{curVer} {emojiUnicodes['arrow']} v{child['version']}")
                updateLinks.append(f"- {child['name']} - [Download]({child['link']})")
            #endif
        #endfor

        date = Date(updateRes['releaseTime'])

        if newInstall == TRUE:
            $IFRESULT = Strings['installer.docs.installmd'].replace('$name', updateRes['name'])
        else:
            updatedText = Strings['installer.docs.updatemd']
                            .replace('$name', updateRes['name'])
                            .replace('$update', updateText)
                            .replace('$date', date.format(date="long", time=None))
            $IFRESULT = updatedText
        #endif


        updatedText = Strings['installer.docs.othermd']
                        .replace('$info', $IFRESULT)
                        .replace('$links', updateLinks)
                        .replace('$notes', {updateRes['releaseNotes']})
                        .replace('$rhublink', f'{updateRes['rhub']}/changelog')

        richText = MakeRichTextFromMarkdown(updatedText)

        sysVers = GetDeviceDetails('System Version')

        # for now bug affects 17.0 and onwards
        if sysVers >= 17.0:
            # use the patch
            CopyToClipboard(richText)
            $IFRESULT = CreateNote(Strings['installer.badmd.warning'])
        else:
            $IFRESULT = CreateNote(richText)
        #endif

        OpenNote($IFRESULT)
    #endif
#endif


