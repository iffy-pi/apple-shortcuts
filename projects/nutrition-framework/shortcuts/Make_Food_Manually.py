'''
Framework: Nutrition (id = 4)
ID:  21
Ver: 1.1
'''

# Create a food by manually filling in the nutrient fieldds

noteTemplate = '''
Populate the food information below. When finished return to the Shortcuts app for the Shortcut to continue.

Name: 
Barcode: 
Serving Size: 
Calories (kCal): 
Fat (g): 
Saturated Fat (g): 
Trans Fat (g): 
Carbs (g): 
Fiber (g): 
Sugar (g): 
Protein (g): 
Cholesterol (mg): 
Sodium (mg): 
Calcium (mg or %): 
Iron (mg or %): 
Potassium (mg or %): 
VitA (mcg or %): 
VitC (mg or %): 
Monounsaturated Fat (g): 
Polyunsaturated Fat (g): 
'''

display = {
    "Name":               "Name",
    "Barcode":            "Barcode",
    "Serving Size":       "Serving Size",
    "Calories (kCal)":    "Calories",
    "Carbs (g)":              "Carbs",
    "Protein (g)":              "Protein",
    "Fat (g)":              "Fat",
    "Sugar (g)":              "Sugar",
    "Fiber (g)":              "Fiber",
    "Monounsaturated Fat (g)":              "Monounsaturated",
    "Polyunsaturated Fat (g)":              "Polyunsaturated",
    "Saturated Fat (g)":              "Saturated",
    "Cholesterol (mg)":              "Cholesterol",
    "Trans Fat (g)":              "Trans",
    "Sodium (mg)":              "Sodium",
    "Potassium (mg or %)":              "Potassium",
    "VitA (mcg or %)":              "VitA",
    "VitC (mg or %)":              "VitC",
    "Calcium (mg or %)":              "Calcium",
    "Iron (mg or %)":              "Iron"
}


noteTitle = 'Nutrition Food Importer'


prompt = '''
How would you like to make it?
Make immediately - You will be presented with a dictionary to fill in all the information about the food item
Make and return - A new note will be created in your Notes app to fill the item. Once you're finished, return to the shortcut to resume execution
'''

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))
nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))
exactValDix = {
    'VitA': 1000,
    'VitC': 60,
    'Calcium': 1100,
    'Iron': 14
}

newFood = Dictionary(Text('{"Serving Size":"","Protein":0,"Trans":0,"Barcode":"0","Cholesterol":0,"Name":"","Sugar":0,"Monounsaturated":0,"Polyunsaturated":0,"Fat":0,"Fiber":0,"VitC":0,"Calories":0,"Iron":0,"VitA":0,"Potassium":0,"Saturated":0,"Sodium":0,"Calcium":0,"Carbs":0}'))

Menu(prompt='How would you like to make it?'):
    case 'Make immediately': # TODO workshop these!!
        pass
    
    case 'Make and return':
        if (note := FindNotes('All Notes', where=['Name' == noteTitle])) is not None:
            DeleteNotes(note)


        note = CreateNote(contents=noteTemplate, name=noteTitle)
        OpenNote(note)

        # Wait for user to come back
        WaitToReturn()

        note = Text(FindNotes('All Notes', where=['Name' == noteTitle], limit=1))
        lines = SplitText(note, ByNewLines=True)

        for line in lines:
            parts = SplitText(line, custom=': ')

            if Count(parts) > 1:
                displayName = TrimWhitespace(GetItemsFromList(part, index=1))
                nutrKey = display.GetDictionaryValue(displayName)
                
                if nutrKey is not None:
                    rem = TrimWhiteSpace( CombineText(GetItemsFromList(startIndex=2), custom=': ') )
                    
                    if nutrKey == 'Name' or nutrKey == 'Barcode' or nutrKey == 'Serving Size':
                        IFRESULT = rem
                    else:
                        if f'"{rem}"' == ""
                            IFRESULT2 = 0
                        else:
                            IFRESULT2 = GetNumbersFromInput(rem)
                        IFRESULT = IFRESULT2

                    newFood[nutrKey] = IFRESULT




# Run display food item to allow user to input values
foodDix = RunShortcut(nutrDix['Display Food Item'], input=newFood)

# If there are any vitamins or minerals, we ask if the value is Exact Values or Daily Percentages

for key in exactValDix:
    REPEATRESULTS.append(Number(foodDix[key]))

calcResult = CalculateStatistics('Sum', REPEATRESULTS)

if calcResult > 0:
    Menu(Strings['manual.vtype.prompt']):
        case Strings['manual.vtype.exact']:
            # Is exact values
            MENURESULT = 0
        case Strings['manual.vtype.percentages']:
            # Is daily percentages
            MENURESULT = 1
    IFRESULT = MENURESULT
else:
    IFRESULT = 0

if IFRESULT == 1:
    # Vitamins were in daily percentages convert to exact values
    for vitKey in exactValDix.keys():
        num = Calculate(foodDix[vitKey] / 100)
        num = Calculate(num * exactValDix[vitKey])
        num = RoundNumber(num)
        foodDix[vitKey] = num

# check to make sure food has a name and a serving size
text = f'[{foodDix['Name']}]'
if text != '[]':
    IFRESULT = foodDix['Name']
else:
    IFRESULT = AskForInput(Input.Text, Strings['manual.input.name'], allowMultipleLines=False)
name = IFRESULT

text = f'[{foodDix['Serving Size']}]'
if text != '[]':
    IFRESULT = foodDix['Serving Size']
else:
    IFRESULT = AskForInput(Input.Text, Strings['manual.input.size'], allowMultipleLines=False)
servingSize = IFRESULT

# Generate food ID for food
foodId = RunShortcut(nutrDix['GFID'])
foodDix['id'] = foodId
foodDix['Name'] = name
foodDix['Serving Size'] = servingSize

StopShortcut(output = foodDix)

