'''
Framework: Nutrition (id = 4)
ID:  19 
Ver: 1.01
'''

# Add input food to recents

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

# Text of shortcut input to unlink from file handler of food file
# Without it, overwrites dont really work as it just passes the same file to the system
food = Dictionary(Text(ShortcutInput))

if food is None:
    StopShortcut()

nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))

maxRecents = 30


if food['id'] is not None:
    $IFRESULT = food['id']
else:
    $IFRESULT = RunShorctut(nutrDix['GFID'])

foodId = $IFRESULT

# add food to recent if it doesn't already exist
# by saving it, it will be at top of list when we get recents
SaveFile(To='Shortcuts', food, f"{storage}/Recents/Foods/{fileName}.json", overwrite=True)

dir_ = GetFile(From='Shortcuts', f"{storage}/Recents/Foods")
files = GetContentsOfFolder(dir_)
files = FilterFiles(files, sortBy='Last Modified Date', order='Latest First')

if Count(files) > maxRecents:
    # delete the latest exisiting food files until under maxRecents amount
    for _ in range(Count(files)-maxRecents):
        deletefile = files.getLastItem()
        DeleteFile(foodFile, deleteImmediately=True)

