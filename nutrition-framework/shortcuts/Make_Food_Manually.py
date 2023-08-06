'''
Framework: Nutrition (id = 4)
ID:  21
Ver: 1.0
'''

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))
nutrDix = Dictionary(GetFile(f"{storage}/Other/shortcutNames.json"))
exactValDix = {
    'VitA': 1000,
    'VitC': 60,
    'Calcium': 1100,
    'Iron': 14
}

foodDix = RunShortcut(nutrDix['Display Food Item'])

# we need to check if there are any vitamin values before
num = foodDix['VitA'] + foodDix['VitC'] + foodDix['Calcium'] + foodDix['Iron']

if num > 0:
    Menu('Vitamins and Minerals are in'):
        case 'Exact Values':
            MENURESULT = 0
        case 'Daily Percentages':
            MENURESULT = 1
    IFRESULT = 1
else:
    IFRESULT = 0

if IFRESULT == 1:
    for vitKey in exactValDix.keys():
        num = foodDix[vitKey] / 100
        num = num * exactValDix[vitKey]
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

foodId = RunShortcut(nutrDix['GFID'])
foodDix['id'] = foodId
foodDix['Name'] = name
foodDix['Serving Size'] = servingSize

StopShortcut(output = foodDix)

