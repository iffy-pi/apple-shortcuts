'''
Framework: Nutrition (id = 4)
ID:  8
Ver: 1.1
'''
TRUE = 1
FALSE = 0
Strings = Dictionary()

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

NutriDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))

vitDix = {
    'VitA': 1000,
    'VitC': 60,
    'Calcium': 1100,
    'Iron': 14
}

display = {
    "Calories":    "Calories",
    "Total Carbs":              "Carbs",
    "Protein":              "Protein",
    "Total Fat":              "Fat",
    "Sugars":              "Sugar",
    "Dietary Fiber":              "Fiber",
    "Monounsaturated":              "Monounsaturated",
    "Polyunsaturated":              "Polyunsaturated",
    "Saturated":              "Saturated",
    "Cholesterol":              "Cholesterol",
    "Trans":              "Trans",
    "Sodium":              "Sodium",
    "Potassium":              "Potassium",
    "Vitamin A":              "VitA",
    "Vitamin C":              "VitC",
    "Calcium":              "Calcium",
    "Iron":              "Iron"
}

# TODO Translate
prompt = '''
1. Open search website
2. Search and find your desired food.
3. Copy the entire nutrient table (selection begins from Calories and ends on Iron value).
4. Open the Shortcuts app to continue execution

The shortcut will automatically parse the nutrient information from your clipboard.
'''

Menu(prompt):
    case 'Open search in new tab':
        OpenURL('https://www.myfitnesspal.com/food/calorie-chart-nutrition-facts')
    case 'I already have a tab opened':
        OpenApp('Brave') # TODO need to reassess this 

WaitToReturn()

VibrateDevice()

outputFood = Dictionary(Text('{"Serving Size":"","Protein":0,"Trans":0,"Barcode":"0","Cholesterol":0,"Name":"","Sugar":0,"Monounsaturated":0,"Polyunsaturated":0,"Fat":0,"Fiber":0,"VitC":0,"Calories":0,"Iron":0,"VitA":0,"Potassium":0,"Saturated":0,"Sodium":0,"Calcium":0,"Carbs":0}'))

copiedInfo = Text(Clipboard())

breakLoop = FALSE

for _ in range(5):
    if breakLoop == FALSE:
        lines = SplitText(copiedInfo, ByNewLines=True)
        lineCount = Count(lines)

        if lineCount % 2 == 0:
            breakLoop = TRUE
        else:
            # TODO Translate
            text = '''
            Shortcut could not read nutrient information from copied information. Please edit the copied content below to match the following format:
            <Nutrient name>
            <Nutrient value> or -- if no value

            For example:
            Total Fat
            2 g
            Iron
            2.22 %
            Trans
            --
            '''
            copiedInfo = AskForInput(Input.Text, default=copiedInfo, prompt=text)

        # endif
    # endif
# endrepeat


for $REPEATINDEX in range(lineCount / 2):
    nameInd = ($REPEATINDEX-1 * 2) + 1
    valInd = nameInd + 1
    
    $displayName = TrimWhiteSpace(GetItemFromList(lines, index=nameInd))
    nutrKey = display.GetDictionaryValue($displayName)

    if nutrKey is not None:
        # TODO, how do we handle french numbers? regex (what does getnumbersfrominput return?)
        value = GetItemFromList(GetNumbersFromInput(GetItemFromList(lines, index=valInd)) , firstItem=True)
        match = MatchText(r'[0-9]', value)

        if match is not None:
            outputFood[nutrKey] = value
        #endif
    #endif
#endfor

OpenApp('Brave')

# Each option is written as text
$options = [
    {"prompt": Strings["manual.input.name"], "key": "Name" },
    {"prompt": Strings["manual.input.size"], "key": "Serving Size"}
]

for $REPEATITEM in $options:
    opt = GetDictionaryFromInput($REPEATITEM)
    breakLoop = FALSE
    for _ in repeat(10):
        if breakLoop == FALSE:
            # TODO translate this
            $text = f'''
                Need to check the page? Leave the field blank and the shortcut will pause until you return to the Shortcuts app.

                {opt['prompt']}
            '''
            res = AskForInput(Input.Text, prompt=$text, allowMultipleLines=False)
            if res is not None:
                outputFood[opt['key']] = res
                breakLoop = TRUE
            else:
                WaitToReturn()
            #endif
        #endif
    #endfor
#endfor

prompt = f'''
{outputFood['Name']}
{outputFood['Serving Size']}
{Strings['nutr.cals']}: {outputFood['Calories']}
{Strings['nutr.carbs']}: {outputFood['Carbs']}g ⸱ {Strings['nutr.fat']}: {outputFood['Fat']}g ⸱ {Strings['nutr.protein']}: {outputFood['Protein']}g
{Strings['nutr.sugar']}: {outputFood['Sugar']}g ⸱ {Strings['nutr.fiber']}: {outputFood['Fiber']}g 
{Strings['nutr.monofat']}: {outputFood['Monounsaturated']}g
{Strings['nutr.polyfat']}: {outputFood['Polyunsaturated']}g
{Strings['nutr.saturfat']}: {outputFood['Saturated']}g ⸱ {Strings['nutr.cholesterol']}: {outputFood['Cholesterol']}mg ⸱ {Strings['nutr.sodium']}: {outputFood['Sodium']}mg ⸱ {Strings['nutr.potassium']}: {outputFood['Potassium']}mg
{Strings['nutr.calcium']}: {outputFood['Calcium']}% ⸱ {Strings['nutr.iron']}: {outputFood['Iron']}%  ⸱ {Strings['nutr.vita']}: {outputFood['VitA']}%  ⸱ {Strings['nutr.vitc']}: {outputFood['VitC']}%
'''

continueLoop = TRUE
for i in range(10):
    # To do translate this
    Menu(prompt):
        case 'OK':
            # Convert vitamins to exact values
            for nutrKey in vitDix.keys:
                $percent = outputFood[nutrKey]
                $total = vitDix[nutrKey]
                res = CalculateExpression(($percent)/100 * $total)
                outputFood[nutrKey] = RoundNumber(res, 'Hundredths')
            #endfor

            outputFood['id'] = RunShorctut(NutriDix['GFID'])
            StopShortcut(output = outputFood)

        case 'Edit a field':
            outputFood = RunShortcut(nutrDix['Display Food Item'], input=outputFood)

        case 'Discard food and exit':
            StopShortcut()
    #endmenu
#endfor
