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
	text = f'0{nutrients["Carbs"]}'
    LogHealthSample("Carbohydrates", text, "g", loggingDate)

if nutrients["Fiber"] is not None:
	text = f'0{nutrients["Fiber"]}'
    LogHealthSample("Fiber", text, "g", loggingDate)

if nutrients["Sugar"] is not None:
	text = f'0{nutrients["Sugar"]}'
    LogHealthSample("Dietary Sugar", text, "g", loggingDate)

if nutrients["Fat"] is not None:
	text = f'0{nutrients["Fat"]}'
    LogHealthSample("Total Fat", text, "g", loggingDate)

if nutrients["Polyunsaturated"] is not None:
	text = f'0{nutrients["Polyunsaturated"]}'
    LogHealthSample("Polyunsaturated Fat", text, "g", loggingDate)

if nutrients["Monounsaturated"] is not None:
	text = f'0{nutrients["Monounsaturated"]}'
    LogHealthSample("Monounsaturated Fat", text, "g", loggingDate)

if nutrients["Saturated"] is not None:
	text = f'0{nutrients["Saturated"]}'
    LogHealthSample("Saturated Fat", text, "g", loggingDate)

if nutrients["Protein"] is not None:
	text = f'0{nutrients["Protein"]}'
    LogHealthSample("Protein", text, "g", loggingDate)

if nutrients["Sodium"] is not None:
	text = f'0{nutrients["Sodium"]}'
    LogHealthSample("Sodium", text, "mg", loggingDate)

if nutrients["Potassium"] is not None:
	text = f'0{nutrients["Potassium"]}'
    LogHealthSample("Potassium", text, "mg", loggingDate)

if nutrients["Cholesterol"] is not None:
	text = f'0{nutrients["Cholesterol"]}'
    LogHealthSample("Dietary Cholesterol", text, "mg", loggingDate)

if nutrients["VitA"] is not None:
	text = f'0{nutrients["VitA"]}'
    LogHealthSample("Vitamin A", text, "mcg", loggingDate)

if nutrients["VitC"] is not None:
	text = f'0{nutrients["VitC"]}'
    LogHealthSample("Vitamin C", text, "mg", loggingDate)

if nutrients["Calcium"] is not None:
	text = f'0{nutrients["Calcium"]}'
    LogHealthSample("Calcium", text, "mg", loggingDate)

if nutrients["Iron"] is not None:
	text = f'0{nutrients["Iron"]}'
    LogHealthSample("Iron", text, "mg", loggingDate)

if nutrients["Calories"] is not None:
	text = f'0{nutrients["Calories"]}'
    LogHealthSample("Dietary Energy", text, "kcal", loggingDate)