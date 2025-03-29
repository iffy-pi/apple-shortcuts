'''
Framework: Nutrition (id = 4)
ID:  9
Ver: 1.0
'''
# generates a unique FOOD ID

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
file = GetFile(From='Shortcuts', f"{storage}/Other/nextFoodId.txt")
if file is not None:
    $IFRESULT = file
else:
    $IFRESULT = "0"
#endif

nextId = Number($IFRESULT)
num = nextId + 1
SaveFile(To='Shortcuts', num, f"{storage}/Other/nextFoodId.txt")
StopShortcut(output=num) 

