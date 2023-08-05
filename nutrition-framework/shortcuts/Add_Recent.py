storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

# Text of shortcut input to unlink from file handler of food file
# Without it, overwrites dont really work as it just passes the same file to the system
food = Dictionary(Text(ShortcutInput))

if food is None:
    StopShortcut()

nutrDix = Dictionary(GetFile(f"{storage}/Other/shortcutNames.json"))

maxRecents = 30


if food['id'] is not None:
    IFRESULT = food['id']
else:
    IFRESULT = RunShorctut(nutrDix['GFID'])

foodId = IFRESULT

# add food to recent if it doesn't already exist
# by saving it, it will be at top of list since sorted by modified after
SaveFile(food, f"{storage}/Recents/Foods/{fileName}.json", overwrite=True)

dir_ = GetFile(f"{storage}/Recents/Foods")
files = GetContentsOfFolder(dir_)
files = filter(files, sortBy='Last Modified Date', order='Latest First')

if Count(files) > maxRecents:
    for _ in range(Count(files)-maxRecents):
        deletefile = files.getLastItem()
        DeleteFile(foodFile, deleteImmediately=True)

