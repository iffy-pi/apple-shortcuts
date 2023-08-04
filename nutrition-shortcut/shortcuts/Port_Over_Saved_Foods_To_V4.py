nameFiles = [
    "FLS/Presets/presetNames.txt",
    "FLS/Recents/recentNames.txt",
    "FLS/Barcodes/barcodeDix.txt"
]

foodDirs = [
    "FLS/Presets/Foods",
    "FLS/Recents/Foods",
    "FLS/Barcodes/Foods"
]

# note files are originally text files without food ids
file = GetFile("FLS/Other/nextFoodId.txt", errorIfNotFound=False)
if file is not None:
    IFRESULT = Number(file)
else:
    IFRESULT = 0
nextId = IFRESULT


for REPEATITEM in nameFiles:
    foodsDir = foodDirs.getItemAtIndex(REPEATINDEX)
    for foodFile in GetContentsOfFolder(foodsDir):

        filename = GetFileDetails("Name", foodFile)

        # only convert for those that are applicable, so that the shortcut supports failure
        if MatchText(filename, "food_[0-9][0-9]*") is not None:
            # Add the name to list
            food = Dictionary(foodFile)
            if food['Name'] is not None:
                if food['id'] is None:
                    num = Number(nextId)
                    nextId = nextId+1
                    SaveFile(nextId, "FLS/Other/nextFoodId.txt", overwrite=True)
                    IFRESULT = num
                else:
                    IFRESULT = Number(food['id'])
                
                foodId = IFRESULT
                SaveFile(food, f'{foodsDir}/food_{foodId}.json', overwrite=True)

            DeleteFile(foodFile)
    namesFile = GetFile(REPEATITEM, errorIfNotFound=False)
    DeleteFile(namesFile, deleteImmediately=True)

SaveFile(nextId, "FLS/Other/nextFoodId.txt", overwrite=True)

