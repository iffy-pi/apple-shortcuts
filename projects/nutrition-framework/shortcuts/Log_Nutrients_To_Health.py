'''
Framework: Nutrition (id = 4)
ID:  26
Ver: 1.0
'''

# Log Nutrients to Apple Health

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

# We save the dictionary to file and repull it because it enables us to fast track permissions
# If we don't do it, fast tracking permissions wont work
SaveFile(To='Shortcuts', f'{storage}/Other/tempNutrientsDix.txt', Text(ShortcutInput), overwrite=True)
nutrients = Dictionary( Text( GetFile(From='Shortcuts', f'{storage}/Other/tempNutrientsDix.txt') ) )

loggingDate = Date(nutrients['Date'])

if nutrients["Carbs"] is not None:
    LogHealthSample("Carbohydrates", {nutrients["Carbs"]}, "g", loggingDate)
#endif

if nutrients["Fiber"] is not None:
    LogHealthSample("Fiber", {nutrients["Fiber"]}, "g", loggingDate)
#endif

if nutrients["Sugar"] is not None:
    LogHealthSample("Dietary Sugar", {nutrients["Sugar"]}, "g", loggingDate)
#endif

if nutrients["Fat"] is not None:
    LogHealthSample("Total Fat", {nutrients["Fat"]}, "g", loggingDate)
#endif

if nutrients["Polyunsaturated"] is not None:
    LogHealthSample("Polyunsaturated Fat", {nutrients["Polyunsaturated"]}, "g", loggingDate)
#endif

if nutrients["Monounsaturated"] is not None:
    LogHealthSample("Monounsaturated Fat", {nutrients["Monounsaturated"]}, "g", loggingDate)
#endif

if nutrients["Saturated"] is not None:
    LogHealthSample("Saturated Fat", {nutrients["Saturated"]}, "g", loggingDate)
#endif

if nutrients["Protein"] is not None:
    LogHealthSample("Protein", {nutrients["Protein"]}, "g", loggingDate)
#endif

if nutrients["Sodium"] is not None:
    LogHealthSample("Sodium", {nutrients["Sodium"]}, "mg", loggingDate)
#endif

if nutrients["Potassium"] is not None:
    LogHealthSample("Potassium", {nutrients["Potassium"]}, "mg", loggingDate)
#endif

if nutrients["Cholesterol"] is not None:
    LogHealthSample("Dietary Cholesterol", {nutrients["Cholesterol"]}, "mg", loggingDate)
#endif

if nutrients["VitA"] is not None:
    LogHealthSample("Vitamin A", {nutrients["VitA"]}, "mcg", loggingDate)
#endif

if nutrients["VitC"] is not None:
    LogHealthSample("Vitamin C", {nutrients["VitC"]}, "mg", loggingDate)
#endif

if nutrients["Calcium"] is not None:
    LogHealthSample("Calcium", {nutrients["Calcium"]}, "mg", loggingDate)
#endif

if nutrients["Iron"] is not None:
    LogHealthSample("Iron", {nutrients["Iron"]}, "mg", loggingDate)
#endif

if nutrients["Calories"] is not None:
    LogHealthSample("Dietary Energy", {nutrients["Calories"]}, "kcal", loggingDate)
#endif