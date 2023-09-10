'''
Framework: Nutrition (id = 4)
ID:  10
Ver: 1.01
'''

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

if ShortcutInput is not None:
    IFRESULT = foodDix
else:
    # the default food dictionary
    IFRESULT = ... # the default food dictionary
foodDix = Dictionary(IFRESULT)


g = '(g)'
mg = '(mg)'

# The goal is to display the dictionary in a way that makes sense to the user
# So we have to use special keys for the dictionary

# displayKeys maps keys in our food object to keys that will be used in the dictionary displayed to the user
displayKeys = {
    "Name":            "Name",
    "Barcode":         "Barcode",
    "Serving Size":    "Serving Size",
    "Calories":        "Calories (kCal)",
    "Carbs":           "Carbs (g)",
    "Protein":         "Protein (g)",
    "Fat":             "Fat (g)",
    "Sugar":           "Sugar (g)",
    "Fiber":           "Fiber (g)",
    "Monounsaturated": "Monounsaturated (g)",
    "Polyunsaturated": "Polyunsaturated (g)",
    "Saturated":       "Saturated (g)",
    "Cholesterol":     "Cholesterol (mg)",
    "Trans":           "Trans (g)",
    "Sodium":          "Sodium (mg)",
    "Potassium":       "Potassium (mg)",
    "VitA":            "VitA (mcg)",
    "VitC":            "VitC (mg)",
    "Calcium":         "Calcium (mg)",
    "Iron":            "Iron (mg)"
}

# displayDix maps the display keys to the values in the food object
# we ask for user input so that the dictionary is displayed to them
displayDix = {
    "Name":                 foodDix["Name"] + AskEachTime(),
    "Barcode":              foodDix["Barcode"],
    "Serving Size":         foodDix["Serving Size"],
    "Calories (kCal)":      foodDix["Calories"],
    "Carbs (g)":            foodDix["Carbs"],
    "Protein (g)":          foodDix["Protein"],
    "Fat (g)":              foodDix["Fat"],
    "Sugar (g)":            foodDix["Sugar"],
    "Fiber (g)":            foodDix["Fiber"],
    "Monounsaturated (g)":  foodDix["Monounsaturated"],
    "Polyunsaturated (g)":  foodDix["Polyunsaturated"],
    "Saturated (g)":        foodDix["Saturated"],
    "Cholesterol (mg)":     foodDix["Cholesterol"],
    "Trans (g)":            foodDix["Trans"],
    "Sodium (mg)":          foodDix["Sodium"],
    "Potassium (mg)":       foodDix["Potassium"],
    "VitA (mcg)":           foodDix["VitA"],
    "VitC (mg)":            foodDix["VitC"],
    "Calcium (mg)":         foodDix["Calcium"],
    "Iron (mg)":            foodDix["Iron"]
}


# Text maps values from displayDix back to food object text version
text = '{' + f'''
    "Name":            "{displayDix["Name"]}",
    "Barcode":         "{displayDix["Barcode"]}",
    "Serving Size":    "{displayDix["Serving Size"]}",
    "Calories":        {displayDix["Calories (kCal)"]},
    "Carbs":           {displayDix["Carbs (g)"]},
    "Protein":         {displayDix["Protein (g)"]},
    "Fat":             {displayDix["Fat (g)"]},
    "Sugar":           {displayDix["Sugar (g)"]},
    "Fiber":           {displayDix["Fiber (g)"]},
    "Monounsaturated": {displayDix["Monounsaturated (g)"]},
    "Polyunsaturated": {displayDix["Polyunsaturated (g)"]},
    "Saturated":       {displayDix["Saturated (g)"]},
    "Cholesterol":     {displayDix["Cholesterol (mg)"]},
    "Trans":           {displayDix["Trans (g)"]},
    "Sodium":          {displayDix["Sodium (mg)"]},
    "Potassium":       {displayDix["Potassium (mg)"]},
    "VitA":            {displayDix["VitA (mcg)"]},
    "VitC":            {displayDix["VitC (mg)"]},
    "Calcium":         {displayDix["Calcium (mg)"]},
    "Iron":            {displayDix["Iron (mg)"]},
''' + '}'

# We create a dictionary from the text to get the viewed/edited food object
# This provides a faster method than just iterating through all the keys

dix = Dictionary(text)
if dix is not None:
    # Parsing could fail if user leaves leading zeros in numbers, in that case we default to key iteration to handle the leading zeros
    
    # If parsing completes, then set the Servings and ID field in the food if they existed
    newFoodDix = dix
    if foodDix['id'] is not None:
        newFoodDix['id'] = foodDix['id']

    if foodDix['Servings'] is not None:
        newFoodDix['Servings'] = foodDix['Servings']

    foodDix = newFoodDix
else:
    # parsing failed, build it the normal way by iterating through the keys
    file = GetFile(From='Shortcuts', 'FLS/Other/nutriKeys.txt')
    nutriKeys = SplitText(file, '\n')

    for key in displayKeys.keys():
        field = displayKeys[key]

        # If this is a nutrient, convert the value in the display dix to a number
        res = FilterFiles(nutriKeys, where=['Name' == key])
        if res is not None:
            # replacing comma with dot to convert european decimals to standard decimals
            text = displayDix[field].replace(',', '.')
            num = Number(text)
            IFRESULT = RoundNumber(IFRESULT, hundredths)
        else:
            IFRESULT = displayDix[field]

        foodDix[key] = IFRESULT

