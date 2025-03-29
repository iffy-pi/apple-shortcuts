'''
Framework: Nutrition (id = 4)
Is installer shortcut
'''

# Installer for the nutrition shortcut

Alert("""
    This Nutrition Installer fixes the broken formatting in the notes generated for installation/updates in IOS 17.
    Select check for updates and download the included nutrition installer shortcut which will have the fix built in.
""")

TRUE = 1
FALSE = 0

newInstall = TRUE
proceedWithUpdates = FALSE

updateInfo = {
    'updateLink' : 'https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/updates.json',
    'version':'4.06'
}

# also now includes information about the children
childVers = {
    "19":"1.01",      # Add Recent
    "20":"1.01",      # Barcode Search
    "24":"1.0",      # Calculate Stats
    "14":"1.01",      # Clear Cache And Backlog
    "10":"1.01",     # Display Food Item
    "15":"1.0",      # Edit Saved Food
    "22":"1.01",      # Food History
    "6":"1.03",      # Foods List
    "9":"1.0",       # Generate Food ID
    "18":"1.0",      # Get Recent
    "7":"1.1",       # Log Algorithm
    "12":"1.02",     # Log Foods At Different Times
    "11":"1.01",     # Log Foods At Time
    "25":"1.0",      # Log Nutrients to Health
    "21":"1.0",      # Make Food Manually
    "17":"1.03",     # Make Preset
    "5":"1.03",       # Nutrition
    "23":"1.0",      # Nutrition Statistics
    "13":"1.01",      # Saved And Search
    "8":"1.02",      # Search Algorithm
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

if params['updateCheck'] is not None:
    newInstall = FALSE
else:
    Menu('What are you doing?'):
        case "Installing the Shortcut":
        case "Checking For Updates":
            newInstall = FALSE

if params['useTest'] is not None:
    updateInfo['updateLink'] = 'https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/testupdates.json'

if newInstall == TRUE:
    # If we are doing a new install, we have to save the shortcutNames
    # And also generate installation links for all the children files

    # Let user select the storage folder 
    file = GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt", errorIfNotFound=False)
    if file is not None:
        $IFRESULT = file
    
    else:
        newStorage = AskForInput(Input.Text, prompt="Enter folder name to store saved foods and configuration files", default='Nutrition')

        breakLoop = FALSE
        for _ in range(10):
            if breakLoop == FALSE:
                if GetFile(From='Shortcuts', newStorage, errorIfNotFound=False) is not None:
                    newStorage = AskForInput(Input.Text, prompt=f'Folder "{newStorage}" already exists, please select a different name', default=text)
                else:
                    breakLoop = TRUE

        Alert('The folder name is saved in Shortcuts/Nutrition_Shortcut_Storage_Folder_Name.txt. To change the folder name, rename the folder and edit the text file'
            title=f'Shortcut files will be saved to Shortcuts/{newStorage}')

        SaveFile(To='Shortcuts', newStorage, "Nutrition_Shortcut_Storage_Folder_Name.txt", overwrite=True)

        $IFRESULT = newStorage

    storage = $IFRESULT

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
            $IFRESULT = f"""
                #  Installing {updateRes['name']} Shortcut
                ## &#x1F50E; Description:
                The Nutrition Shortcut is made up of several helper shortcuts for its extensive functionality. Please install all the shortcuts listed in the Install section below.
                &nbsp;
                After installation, the main shortcut to run is Nutrition. Not sure where to start? Check out the [tutorial](https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/data/tutorial.html).
                &nbsp;
                Note: If you wish to use Nutrition Statistics, you must install [Charty](https://apps.apple.com/ca/app/charty-for-shortcuts/id1494386093).
                &nbsp;
                If you run into any errors or issues, please contact developer. (See developer contact below)
            """
        else:
            $IFRESULT = f"""
                # {updateRes['name']} Shortcut Update
                ## Updates are available for shortcuts:
                {updateText}

                &nbsp;
                ## &#x1F566; Released:
                {date.format(date="long", time=None)}
            """

        text = f"""
            {$IFRESULT}

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
            
            $IFRESULT = CreateNote(warningText)
        else:
            $IFRESULT = CreateNote(richText)

        OpenNote($IFRESULT)

