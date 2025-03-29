'''
Framework: Nutrition (id = 4)
ID:  8
Ver: 1.1
'''

# Search for food in MyFitnessPal Database
# # TODO Translate this
# ShowAlert(
#     title='Search is no longer available',
#     body='''
#     Unfortunately, the search functionality is no longer available as the MFP public API has been permanently shutdown.
#     You can 
#     An alternative which integrates with ChatGPT or some other similar search engine will be released in future.
#     '''
# )
# StopShortcut()

TRUE = 1
FALSE = 0
Strings = Dictionary()

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

NutriDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))


OpenURL('https://www.myfitnesspal.com/food/calorie-chart-nutrition-facts')

ShowAlert("Search and find your desired food. When found, select and copy the nutrient information (selection begins from Calories and ends on Iron value)")

WaitToReturn()

VibrateDevice()





# vcard base64 photo icons
servingSizeIcon = # ... , see servingSizeIcon.txt
forwardIcon = # forwardIcon.txt
backwardIcon = # backwardIcon.txt
searchIcon = # searchIcon.txt
cancelIcon = # cancelIcon.txt
verifIcon = '★'


resCount = 6
searchExit = FALSE
pageNo = 1


query = AskForInput(Input.Text, prompt=Strings['search.query.instr'])

updatedText = query.ReplaceText(' ', '')
if updatedText is None:
    StopShortcut()

for _ in range (50):
    if searchExit == FALSE:
        searchItems = {}

        # make the query and savethe items
        url = URL(f"https://api.myfitnesspal.com/public/nutrition?q={query}&page={pageNo}&per_page={resCount}")
        res = Dictionary(GetContentsOfURL(URL))

        for repeatItem in res['items']:
            # cache the item away using its id
            tags = repeatItem['tags']
            item = repeatItem['item']
            itemId = item['id']
            searchItems[ itemId ] = item

            # construct the vcard 
            sizes = item['serving_sizes']
            dix = sizes.atIndex(1)

            num = Number(dix['value'])
            servingSize = f"{num} {dix['unit']}"

            if Count(sizes) > 1:
                servingSize = f"{servingSize} ({Strings['search.moresizes']})"


            if item['brand_name'] is not None:
                IFRESULT=f"{item['brand_name']} | {servingSize}"
            else:
                IFRESULT = f"{servingSize}"

            subtitle = IFRESULT

            dix = item['nutritional_contents']
            
            # if a food has no energy dictionary, add a zeroed out dictionary
            # avoids key errors when accessing nested value key for missing energy dictionary
            if item['nutritional_contents.energy'] is None:
                dix['energy'] = {
                    "unit": "calories",
                    "value": 0
                },

                item['nutritional_contents'] = dix
                searchItems[itemId] = item

            # only add the subtitle if all the relevant keys exist in the food
            res = FilterFiles(dix.keys, whereAny=[
                    'Name' == 'energy',
                    'Name' == 'carbohydrates',
                    'Name' == 'fat',
                    'Name' == 'protein'
                ])

            if Count(res) == 4:
                # In shortcuts, you can access nested keys using dot notation
                # so item['a.b.c'] is equivalent to python item['a']['b']['c']
                # Note this is actually a literal \n, not a newline character
                subtitle = f'''
                    {subtitle}\n{Strings['nutr.cals']}: {item['nutritional_contents.energy.value']} ⸱ {Strings['nutr.carbs']}: {item['nutritional_contents.carbohydrates']}g ⸱ {Strings['nutr.fat']}: {item['nutritional_contents.fat']}g ⸱ {Strings['nutr.protein']}: {item['nutritional_contents.protein']}g
                '''

            # Add verifIcon if it is a best match
            files = FilterFiles(tags, whereAny=['Name' == 'canonical', 'Name' == 'best_match'])
            if Count(files) == 2:
                IFRESULT = f' {verifIcon}'
            else:
                IFRESULT = ''
            
            text = f'''
            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=UTF-8:{item['description']}{IFRESULT}
            ORG;CHARSET=UTF-8:{subtitle}
            NOTE;CHARSET=UTF-8:{itemId}
            END:VCARD
            '''
            
            REPEATRESULTS.append(text)
        itemCards = REPEATRESULTS

        # Add next, previous, new search and cancel search buttons
        nextPage = pageNo+1
        prevPage = nextPage-2

        text = f'''
            {itemCards}

            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=utf-8:{Strings['search.opts.next']}
            ORG: {Strings['search.page']} {nextPage}
            NOTE;CHARSET=UTF-8:Next
            {forwardIcon}
            END:VCARD

            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=utf-8:{Strings['search.opts.prev']}
            ORG: {Strings['search.page']} {prevPage}
            NOTE;CHARSET=UTF-8:Prev
            {backwardIcon}
            END:VCARD

            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=utf-8:{Strings['search.opts.search']}
            ORG: {Strings['search.opts.search.desc']}
            NOTE;CHARSET=UTF-8:New
            {searchIcon}
            END:VCARD

            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=utf-8:{Strings['search.opts.cancel']}
            ORG:{Strings['search.opts.cancel.desc']}
            NOTE;CHARSET=UTF-8:Cancel
            {searchIcon}
            END:VCARD
        '''

        renamedItem = SetName(text, 'vcard.vcf')
        contacts = GetContacts(renamedItem)

        text = f'''
        "{query}" {Strings['search.results']} ⸱ {Strings['search.page']} {pageNo}
        {verifIcon} - {Strings['search.bestmatches']}
        '''

        chosenItem = ChooseFrom(contacts, prompt=text)
        isControlItem = FALSE

        if chosenItem.Notes == 'Next':
            isControlItem = TRUE
            pageNo = pageNo + 1

        if chosenItem.Notes == 'Prev':
            isControlItem = TRUE
            pageNo = pageNo - 1
            if pageNo == 0:
                Alert(Strings['search.warning.firstpage'])
                pageNo = pageNo + 1

        if chosenItem.Notes == 'New':
            isControlItem = TRUE
            res = RunShorctut(NutriDix['Search Algorithm'])
            StopShortcut(output = res)

        if chosenItem.Notes == 'Cancel':
            isControlItem = TRUE
            StopShortcut()
        
        if isControlItem == FALSE:
            # then its not a control item
            itemId = chosenItem.Notes
            item = searchItems[ itemId ]

            # ask the user what serving size they want
            # if only one size automatically select it
            # first accumulate serving size information

            baseCal = item['nutritional_contents.energy.value']

            for repeatItem in item['serving_sizes']:
                curSize = Dictionary(repeatItem)
                servingVal = Number(curSize['value'])
                num = baseCal * curSize['nutrition_multiplier']
                sizeCal = RoundNumber(num, hundredths)

                # create the vcard
                text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=UTF-8:{servingVal} {curSize['unit']}
                    ORG;CHARSET=UTF-8:{sizeCal} (x{curSize['nutrition_multiplier']})
                    NOTE;CHARSET=UTF-8:{curSize['nutrition_multiplier']}
                    {servingSizeIcon}
                    END:VCARD
                    '''
                REPEATRESULTS.append(text)

            if Count(REPEATRESULTS) == 1:
                # if only one, skip selection
                text = f'{REPEATRESULTS}'
                contacts = macros.textToContacts(text)
                chosenSize = contacts.getFirstItem()
            else:
                # For multiple sizes, add a back button to go back to search page
                text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=UTF-8:{Strings['search.opts.back']}
                    ORG;CHARSET=UTF-8:{Strings['search.opts.back.desc']}
                    {backwardIcon}
                    END:VCARD
                    {REPEATRESULTS}
                '''
                # choose from it
                renamedItem = SetName(text, 'vcard.vcf')
                contacts = GetContacts(renamedItem)

                chosenSize = ChooseFrom(contacts, prompt=Strings['search.select.servingsize'])


            if chosenSize.Name != "Back"
                # we have the users food now we just need to create it
                # aggregate the needed information and send it out
                searchExit = TRUE
                selectedItem = item
                selectedServingSize = Text(chosenSize.Name)
                multiplier = Number(chosenSize.Notes)
                nutrInfo = Dictionary(selectedItem['nutritional_contents'])

                outputFood = {
                    "Name":            item['description'],
                    "Barcode":         "",
                    "Serving Size":    selectedServingSize,
                    "Calories":        nutrInfo['energy.value'],
                    "Carbs":           nutrInfo['carbohydatrates'],
                    "Sugar":           nutrInfo['sugar'],
                    "Fiber":           nutrInfo['fiber'],
                    "Protein":         nutrInfo['protein'],
                    "Fat":             nutrInfo['fat'],
                    "Monounsaturated": nutrInfo['monounsaturated_fat'],
                    "Polyunsaturated": nutrInfo['polyunsaturated_fat'],
                    "Saturated":       nutrInfo['saturated_fat'],
                    "Trans":           0,
                    "Sodium":          nutrInfo['sodium'],
                    "Cholesterol":     nutrInfo['cholesterol'],
                    "Potassium":       nutrInfo['potassium'],
                    "VitA":            nutrInfo['vitamin_a'],
                    "VitC":            nutrInfo['vitamin_c'],
                    "Calcium":         nutrInfo['calcium'],
                    "Iron":            nutrInfo['iron']
                }


                # apply servings multiplier on nutrients
                file = GetFile(From='Shortcuts', 'FLS/Other/nutriKeys.txt')
                nutrients = SplitText(file, '\n')
                for item in nutrients:
                    num = Number(outputFood[item])
                    num = num * multiplier
                    num = RoundNumber(num, hundredths)
                    outputFood[item] = num

                prompt = f'''
                Search Result:    
                {outputFood['Name']}
                {outputFood['Serving Size']}
                {Strings['nutr.cals']}: {outputFood['Calories']}
                {Strings['nutr.carbs']}: {outputFood['Carbs']}g ⸱ {Strings['nutr.fat']}: {outputFood['Fat']}g ⸱ {Strings['nutr.protein']}: {outputFood['Protein']}g
                {Strings['nutr.sugar']}: {outputFood['Sugar']}g ⸱ {Strings['nutr.fiber']}: {outputFood['Fiber']}g 
                {Strings['nutr.monofat']}: {outputFood['Monounsaturated']}g
                {Strings['nutr.polyfat']}: {outputFood['Polyunsaturated']}g
                {Strings['nutr.saturfat']}: {outputFood['Saturated']}g ⸱ {Strings['nutr.cholesterol']}: {outputFood['Cholesterol']}mg ⸱ {Strings['nutr.sodium']}: {outputFood['Sodium']}mg ⸱ {Strings['nutr.potassium']}: {outputFood['Potassium']}mg
                {Strings['nutr.calcium']}: {outputFood['Calcium']}% ⸱ {Strings['nutr.iron']}: {outputFood['Iron']}% ⸱ {Strings['nutr.vita']}: {outputFood['VitA']}% ⸱ {Strings['nutr.vitc']}: {outputFood['VitC']}% 
                '''
                Menu(prompt):
                    case Strings['search.item.accept']:
                        searchExit = TRUE
                    
                    case Strings['search.item.edit']:
                        res = RunShorctut(NutriDix['Display Food Item'], input=outputFood)
                        Menu(Strings['search.item.save'])
                            case Strings['opts.yes']:
                                searchExit = TRUE
                                outputFood = res
                            case Strings['search.item.prevvalues']:
                                searchExit = TRUE
                            case Strings['search.item.backtosearch']:
                                pass
                    
                    case Strings['search.opts.back.desc']:
                        pass

                    case Strings['search.opts.cancel.desc']:
                        StopShortcut()


# used to generate id for shortcut
outputFood['id'] = RunShorctut(NutriDix['GFID'])

# vitamins are inputted as percentages, change them to exact values
# source https://www.canada.ca/en/health-canada/services/understanding-food-labels/percent-daily-value.html
vitDix = {
    'VitA': 1000,
    'VitC': 65,
    'VitD': 1100,
    'Iron': 14
}

for item in vitDix.keys():
    # fractional value
    percentageVal = outputFood[item]
    vitFullVal = vitDix[item]


    # Issue #1
    # Have to use calculate actions rather than calculate expression
    # To support different number formats
    num = Calculate(percentageVal /  100)
    num = Calculate(num * vitFullVal)
    outputFood[item] = RoundNumber(num, hundredths)

StopShortcut(output = outputFood)

