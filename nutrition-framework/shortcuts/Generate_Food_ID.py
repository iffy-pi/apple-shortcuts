'''
Framework: Nutrition (id = 4)
ID:  9
Ver: 1.0
'''

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))
file = GetFile(f"{storage}/Other/nextFoodId.txt")
if file is not None:
    IFRESULT = file
else:
    IFRESULT = "0"

_id = Number(IFRESULT)
num = _id + 1
SaveFile(num, f"{storage}/Other/nextFoodId.txt")
StopShortcut() 

