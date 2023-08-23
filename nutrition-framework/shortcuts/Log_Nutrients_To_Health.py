'''
Framework: Nutrition (id = 4)
ID:  ?
Ver: ?
'''

# Log Nutrients to Health

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))
SaveFile(f'{storage}/Other/temp.txt', Text(ShortcutInput), overwrite=True)

nutrients = Dictionary( Text( GetFile(f'{storage}/Other/temp.txt') ) )

loggingDate = Date(nutrients['Date'])

if nutrients["Carbs"] is not None:
    LogHealthSample("Carbohydrates", {nutrients["Carbs"]}, "g", loggingDate)

if nutrients["Fiber"] is not None:
    LogHealthSample("Fiber", {nutrients["Fiber"]}, "g", loggingDate)

if nutrients["Sugar"] is not None:
    LogHealthSample("Dietary Sugar", {nutrients["Sugar"]}, "g", loggingDate)

if nutrients["Fat"] is not None:
    LogHealthSample("Total Fat", {nutrients["Fat"]}, "g", loggingDate)

if nutrients["Polyunsaturated"] is not None:
    LogHealthSample("Polyunsaturated Fat", {nutrients["Polyunsaturated"]}, "g", loggingDate)

if nutrients["Monounsaturated"] is not None:
    LogHealthSample("Monounsaturated Fat", {nutrients["Monounsaturated"]}, "g", loggingDate)

if nutrients["Saturated"] is not None:
    LogHealthSample("Saturated Fat", {nutrients["Saturated"]}, "g", loggingDate)

if nutrients["Protein"] is not None:
    LogHealthSample("Protein", {nutrients["Protein"]}, "g", loggingDate)

if nutrients["Sodium"] is not None:
    LogHealthSample("Sodium", {nutrients["Sodium"]}, "mg", loggingDate)

if nutrients["Potassium"] is not None:
    LogHealthSample("Potassium", {nutrients["Potassium"]}, "mg", loggingDate)

if nutrients["Cholesterol"] is not None:
    LogHealthSample("Dietary Cholesterol", {nutrients["Cholesterol"]}, "mg", loggingDate)

if nutrients["VitA"] is not None:
    LogHealthSample("Vitamin A", {nutrients["VitA"]}, "mcg", loggingDate)

if nutrients["VitC"] is not None:
    LogHealthSample("Vitamin C", {nutrients["VitC"]}, "mg", loggingDate)

if nutrients["Calcium"] is not None:
    LogHealthSample("Calcium", {nutrients["Calcium"]}, "mg", loggingDate)

if nutrients["Iron"] is not None:
    LogHealthSample("Iron", {nutrients["Iron"]}, "mg", loggingDate)

if nutrients["Calories"] is not None:
    LogHealthSample("Dietary Energy", {nutrients["Calories"]}, "kcal", loggingDate)