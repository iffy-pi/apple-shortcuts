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
    'version':'4.10'
}

# also now includes information about the children
childVers = {
    "19":"1.01",      # Add Recent
    "20":"1.01",      # Barcode Search
    "24":"1.02",      # Calculate Stats
    "14":"1.01",      # Clear Cache And Backlog
    "10":"1.01",     # Display Food Item
    "15":"1.01",      # Edit Saved Food
    "22":"1.01",      # Food History
    "6":"1.05",      # Foods List
    "9":"1.0",       # Generate Food ID
    "18":"1.0",      # Get Recent
    "7":"1.12",       # Log Algorithm
    "12":"1.11",     # Log Foods At Different Times
    "11":"1.02",     # Log Foods At Time
    "25":"1.0",      # Log Nutrients to Health
    "21":"1.01",      # Make Food Manually
    "17":"1.05",     # Make Preset
    "5":"1.06",       # Nutrition
    "23":"1.02",      # Nutrition Statistics
    "13":"1.02",      # Saved And Search
    "8":"1.04",      # Search Algorithm
    "16":"1.01",      # Select Saved Foods
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

# Configure storage and language here
# First get the storage if it exists
file = GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt", errorIfNotFound=False)
if file is not None:
    storage = Text(file)
    Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))
else:
    # If there is no storage we don't know the language, let the user select it here
    langs = Dictionary(GetContentsOfURL('https://iffy-pi.github.io/apple-shortcuts/public/nutrition/languages/language_options.json'))
    selectedLang = ChooseFromList(langs.Keys)
    Strings = Dictionary(GetContentsOfURL(f'https://iffy-pi.github.io/apple-shortcuts/public/nutrition/languages/{selectedLang}'))

    freshConfig = TRUE


if params['updateCheck'] is not None:
    newInstall = FALSE
else:
    Menu():
        case Strings['installer.action.install']:
        case Strings['installer.action.update']:
            newInstall = FALSE
        case Strings['installer.action.config']:
            newInstall = FALSE
            exitAfterConfig = TRUE


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

    if blockIfFolderExists == TRUE:
        breakLoop = FALSE
        for _ in range(10):
            if breakLoop == FALSE:
                if GetFile(From='Shortcuts', newStorage, errorIfNotFound=False) is not None:
                    updatedText = Strings['installer.storage.exists'].replace('$storage', newStorage)
                    newStorage = AskForInput(Input.Text, prompt=updatedText)
                else:
                    breakLoop = TRUE

    storage = newStorage

    SaveFile(To='Shortcuts', storage, "Nutrition_Shortcut_Storage_Folder_Name.txt", overwrite=True)
    SaveFile(To='Shortcuts', Strings, f'{storage}/Other/gui_strings.json', overwrite=True)

    if newInstall == TRUE:
        Alert(Strings['installer.storage.info'], showCancel=False)


if exitAfterConfig == TRUE:
    StopShortcut()


if params['useTest'] is not None:
    updateInfo['updateLink'] = 'https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/testupdates.json'

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

updateRes = Dictionary(GetContentsOfURL(updateInfo['updateLink']))

if Number(updateRes['version']) > updateInfo['version']:
    if proceedWithUpdates == FALSE:
        # ask the user
        for _ in range(5):
            if proceedWithUpdates == FALSE:
                Menu(f'There is a new version ({updateRes['version']}) available for this shortcut'):
                    case "What's New?":
                        text = f'''
                        # What's New in v4.03:
                        {updateRes['releaseNotes']}
                        '''
                        richText = MakeRichTextFromMarkdown(text)
                        QuickLook(richText)
                    case 'Update':
                        proceedWithUpdates = TRUE
                    case 'Exit':
                        StopShortcut()


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

        for child in updateRes['children']:
            curVer = childVers[ child['id'] ]
            # using number action so if curver does not exist, then its evaluated to 0
            if Number(child['version']) > Number(curVer):
                updateText.append(f"- {child['name']}: v{curVer} {emojiUnicodes['arrow']} v{child['version']}")
                updateLinks.append(f"- {child['name']} - [Download]({child['link']})")

        date = Date(updateRes['releaseTime'])

        if newInstall == TRUE:
            IFRESULT = f"""
                #  Installing {updateRes['name']} Shortcut
                ## &#x1F50E; Description:
                The Nutrition Shortcut is made up of several helper shortcuts for its extensive functionality. Please install all the shortcuts listed in the Install section below.
                &nbsp;
                After installation, the main shortcut to run is Nutrition. Not sure where to start? Check out the [tutorial](https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/data/tutorial.html).
                &nbsp;
                Note: Make sure to give the shortcut access to read and write Health data, refer to Allowing Health Access in the tutorial.
                &nbsp;
                Note: If you wish to use Nutrition Statistics, you must install [Charty](https://apps.apple.com/ca/app/charty-for-shortcuts/id1494386093).
                &nbsp;
                If you run into any errors or issues, please contact developer. (See developer contact below)
            """
        else:
            IFRESULT = f"""
                # {updateRes['name']} Shortcut Update
                ## Updates are available for shortcuts:
                {updateText}

                &nbsp;
                ## &#x1F566; Released:
                {date.format(date="long", time=None)}
            """

        text = f"""
            {IFRESULT}

            &nbsp;
            ## &#x2705; Install:
            {updateLinks}

            &nbsp;
            ## &#x1F4DD; Release Notes:
            {updateRes['releaseNotes']}

            &nbsp;
            ## &#x1F4EC; Developer Contact:
            Reddit: [u/iffythegreat](https://www.reddit.com/user/iffythegreat)
            RoutineHub: [iffy-pi](https://routinehub.co/user/iffy-pi)

            &nbsp;
            ## &#x1F4DA; Full Update History:
            {updateRes['rhub']}/changelog
        """
        richText = MakeRichTextFromMarkdown(text)

        sysVers = GetDeviceDetails('System Version')

        # for now bug affects 17.0 and onwards
        if sysVers >= 17.0:
            # use the patch
            CopyToClipboard(richText)

            warningText = '''
                Instructions
                Paste the contents of your clipboard into this note to see the instructions!
                This is a patch to a rich text issue introduced with iOS 17.0.
            '''
            
            IFRESULT = CreateNote(warningText)
        else:
            IFRESULT = CreateNote(richText)

        OpenNote(IFRESULT)


