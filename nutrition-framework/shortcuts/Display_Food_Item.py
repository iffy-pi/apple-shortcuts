'''
Framework: Nutrition (id = 4)
ID:  10
Ver: 1.0
'''

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

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


# unit Dix maps the keys of the food dictionary to their user understandable fields

# displayDix maps the user fields to the appropriate key values

# displayKeys translate keys in foodDix to the key that will be displayed to user
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

# display dix is where the user does the actual editing
displayDix = {
    # uses the displayKeys (i.e. for key i, the key field in displayDix is displayKeys[i])
    # for key in displayKeys:
    #     dispKey = displayKeys[key]
    #     displayDix[key] = foodDix[key]

    # Note: Number fields are typed as text because shortcuts dictionary does not support decimal number entering
    ... # see actual shortcut
}

# Text takes keys in displayDix and maps them back to the food dictionary
# in code terms:
# for key in displayKeys:
#     dispKey = displayKeys[key]
#     textDix[key] = displayDix[dispKey]
text = ... # see actual shortcut

dix = Dictionary(text)
if dix is not None:
    newFoodDix = dix
    # it could be parsed correctly
    # If the user keeps 0s before values, parsing will fail so we need to check
    # set the food ID if it is present
    if foodDix['id'] is not None:
        newFoodDix['id'] = foodDix['id']

    if foodDix['Servings'] is not None:
        newFoodDix['id'] = foodDix['id']

    foodDix = newFoodDix
else:
    # parsing failed, build it the normal way
    file = GetFile('FLS/Other/nutriKeys.txt')
    nutriKeys = SplitText(file, '\n')

    for key in displayKeys.keys():
        field = displayKeys[key]

        # get the field from the displayDix and set it in food
        res = filter(nutriKeys, where=['Name' == key])
        if res is not None:
            # replacing comma with dot to convert european decimals to standard decimals
            text = displayDix[field].replace(',', '.')
            num = Number(text)
            IFRESULT = RoundNumber(IFRESULT, hundredths)
        else:
            IFRESULT = displayDix[field]

        foodDix[key] = IFRESULT

