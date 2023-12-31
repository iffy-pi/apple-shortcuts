'''
Framework: Nutrition (id = 4)
ID:  21
Ver: 1.0
'''

# Create a food by manually filling in the nutrient fieldds

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))
exactValDix = {
    'VitA': 1000,
    'VitC': 60,
    'Calcium': 1100,
    'Iron': 14
}

# Run display food item to allow user to input values
foodDix = RunShortcut(nutrDix['Display Food Item'])

# If there are any vitamins or minerals, we ask if the value is Exact Values or Daily Percentages

for key in exactValDix:
    REPEATRESULTS.append(Number(foodDix[key]))

calcResult = CalculateStatistics('Sum', REPEATRESULTS)

if calcResult > 0:
    Menu('Vitamins and Minerals are in'):
        case 'Exact Values':
            MENURESULT = 0
        case 'Daily Percentages':
            MENURESULT = 1
    IFRESULT = MENURESULT
else:
    IFRESULT = 0

if IFRESULT == 1:
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
    IFRESULT = AskForInput(Input.Text, 'What is the name of the food?', allowMultipleLines=False)
name = IFRESULT

text = f'[{foodDix['Serving Size']}]'
if text != '[]':
    IFRESULT = foodDix['Serving Size']
else:
    IFRESULT = AskForInput(Input.Text, 'What is the serving size of the food?', allowMultipleLines=False)
servingSize = IFRESULT

# Generate food ID for food
foodId = RunShortcut(nutrDix['GFID'])
foodDix['id'] = foodId
foodDix['Name'] = name
foodDix['Serving Size'] = servingSize

StopShortcut(output = foodDix)

