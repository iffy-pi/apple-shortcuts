'''
Framework: Nutrition (id = 4)
Is installer shortcut
v4.0
'''
TRUE = 1
FALSE = 0

newInstall = TRUE
proceedWithUpdates = FALSE

updateInfo = {
    'updateLink' : 'https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/updates.json',
    'version' : 4.0
}

# also now includes information about the children
childVers = {
    "5":1.0,    # Nutrition
    "6":1.01,    # Foods List
    "7":1.0,    # Log Algorithm
    "8":1.01,    # Search Algorithm
    "9":1.0,    # Generate Food ID
    "10":1.01,   # Display Food Item
    "11":1.01,   # Log Foods At Time
    "12":1.01,   # Log Foods At Different Times
    "13":1.0,   # Saved And Search
    "14":1.0,   # Clear Cache And Backlog
    "15":1.0,   # Edit Saved Food
    "16":1.0,   # Select Saved Foods
    "17":1.01,   # Make Preset
    "18":1.0,   # Get Recent
    "19":1.0,   # Add Recent
    "20":1.0,   # Barcode Search
    "21":1.0,   # Make Food Manually
    "22":1.0,   # Food History
    "23":1.0,   # Nutrition Statistics
    "24":1.0    # Calculate Stats
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

    file = GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt", errorIfNotFound=False)
    if file is not None:
        IFRESULT = file
    
    else:
        newStorage = AskForInput(Input.Text, prompt="Enter folder name to store saved foods and configuration files", default='Nutrition')

        breakLoop = FALSE
        for _ in range(10):
            if breakLoop == FALSE:
                if GetFile(newStorage, errorIfNotFound=False) is not None:
                    newStorage = AskForInput(Input.Text, prompt=f'Folder "{newStorage}" already exists, please select a different name', default=text)
                else:
                    breakLoop = TRUE

        Alert('The folder name is saved in Shortcuts/Nutrition_Shortcut_Storage_Folder_Name.txt. To change the folder name, rename the folder and edit the text file'
            title=f'Shortcut files will be saved to Shortcuts/{newStorage}')

        SaveFile(newStorage, "Nutrition_Shortcut_Storage_Folder_Name.txt", overwrite=True)

        IFRESULT = newStorage

    storage = IFRESULT

    dix = Dictionary(...) # shortcutNames.json
    SaveFile(dix, f"{storage}/Other/shortcutNames.json") # save shortcut names file

    proceedWithUpdates = TRUE

    # reset updateInfo version to 0.0 to force check
    updateInfo['version'] = 0.0

    # reset child vers to 0
    childVers = childVers = {
        "5":0.0,
        "6":0.0,
        "7":0.0,
        "8":0.0,
        "9":0.0,
        "10":0.0,
        "11":0.0,
        "12":0.0,
        "13":0.0,
        "14":0.0,
        "15":0.0,
        "16":0.0,
        "17":0.0,
        "18":0.0,
        "19":0.0,
        "20":0.0,
        "21":0.0,
        "22":0.0,
        "23":0.0,
        "24":0.0
    }

updateRes = Dictionary(GetContentsOfURL(updateInfo['updateLink']))

if Number(updateRes['version']) > updateInfo['version']:
    if proceedWithUpdates == FALSE:
        # ask the user
        Menu(f'There is a new version ({updateRes['version']}) available for this shortcut'):
            case 'Update':
                proceedWithUpdates = TRUE
            case 'Exit':
                pass

    if proceedWithUpdates == TRUE:
        updateText = []
        updateLinks = []

        # updater shorcut needs to be updated
        if newInstall == FALSE:
            updateText.append(f"Updater Shortcut: {updateInfo['version']} ➡️ {updateRes['version']}")
            updateLinks.append(f"Updater Shortcut: {updateRes['link']}\n")

        for child in updateRes['children']:
            curVer = childVers[ child['id'] ]
            if Number(child['version']) > curVer:
                updateText.append(f"{child['name']}: {curVer} ➡️ {child['version']}")
                updateLinks.append(f"{child['name']}: {child['link']}\n")

        date = Date(updateRes['releaseTime'])
        splitText = SplitText(updateRes['releaseNotes'], '\\n')

        if newInstall == TRUE:
            IFRESULT = f"""
                Installing {updateRes['name']}  Shortcut

                The Nutrition Shortcut is made up of several helper shortcuts for its extensive functionality. Please install the shortcuts listed below.
                Note: If you wish to use Nutrition Statistics, you must install Charty: (https://apps.apple.com/ca/app/charty-for-shortcuts/id1494386093)

                ✅ Install:
                {updateLinks}

                Tutorial:
                Not sure where to start? See the tutorial here: ...

                📬 Developer:
                Reddit: iffythegreat
            """
        else:
            IFRESULT = f"""
                {updateRes['name']} Shortcut Update
                Updates are available for shortcuts:
                {updateText}

                🕦 Released:
                {date.format(date="long", time=None)}

                ✅ Install:
                {updateLinks}

                📝 Release Notes:
                {splitText}

                📬 Developer:
                Reddit: iffythegreat

                📚 Full Update History:
                {updateRes['rhub']}/changelog
            """
        note = CreateNote(IFRESULT)
        OpenNote(note)
