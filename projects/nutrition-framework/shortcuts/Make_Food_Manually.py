'''
Framework: Nutrition (id = 4)
ID:  21
Ver: 1.1
'''

# Create a food by manually filling in the nutrient fieldds

# TODO translate instructions
noteTemplate = '''
Enter information about the food below. When you're done, open/return to the Shortcuts app and the entered food information will be parsed from this note.
Letters and other special symbols are only allowed for the Name, Barcode and Serving Size. Only numbers should be used for nutrients.
Nutrients that are 0 in value don't have to be manually entered, leaving the field blank will automatically give the nutrient a value of 0.
For minerals and vitamins, the shortcut will ask if they are exact values or daily percentages.

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
Polyunsaturated Fat (g): 
Monounsaturated Fat (g): 
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


if (note := FindNotes('All Notes', where=['Name' == noteTitle])) is not None:
    DeleteNotes(note)


note = CreateNote(contents=noteTemplate, name=noteTitle)
OpenNote(note)

# Wait for user to come back
WaitToReturn()

note = Text(FindNotes('All Notes', where=['Name' == noteTitle], limit=1))
lines = SplitText(note, ByNewLines=True)

for line in lines:
    matches = MatchText(r'([^:]*): *(.*)', line)
    if res is not None:
        displayName = TrimWhiteSpace(GetGroupFromMatchedText(1, matches))
        nutrKey = display.GetDictionaryValue(displayName)
        
        if nutrKey is not None:
            value = TrimWhiteSpace(GetGroupFromMatchedText(2, matches))            
            if nutrKey == 'Name' or nutrKey == 'Barcode' or nutrKey == 'Serving Size':
                IFRESULT = value
            else:
                # Validates the actual text is a number, if not it prompts the user to enter a number
                res = MatchText(r'(^[0-9][0-9]*$)|(^[0-9][0-9]*\.[0-9][0-9]*$)|(^[0-9][0-9]*,[0-9][0-9]*$)', value)
                if res is None:
                    if f"{value}" != "":
                        # Todo string this
                        IFRESULT3 = AskForInput(Input.Number, prompt=f'Value "{value}" for '{displayName}' could not be converted into a number. Please enter value below.', allowDecimals=True, allowNegatives=False)
                    else:
                        IFRESULT3 = 0
                    IFRESULT2 = IFRESULT3
                else:
                    IFRESULT2 = GetNumbersFromInput(value)
               
                IFRESULT = IFRESULT2

            newFood[nutrKey] = IFRESULT

# To do translate this
Menu('What would you like to do with the created food'):
    case 'View/edit created food':
        pass
    case 'Discard created food':
        StopShortcut()


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

