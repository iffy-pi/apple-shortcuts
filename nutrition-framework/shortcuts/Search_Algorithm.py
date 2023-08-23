'''
Framework: Nutrition (id = 4)
ID:  8
Ver: 1.02
'''

# Search for food in MyFitnessPal Database

TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

NutriDix = Dictionary(GetFile(f"{storage}/Other/shortcutNames.json"))

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


query = AskForInput(Input.Text, prompt="What Food/Drink?")

for _ in range (50):
    if searchExit == FALSE:
        searchItems = {}

        # make the query and savethe items
        url = URL(f"https://api.myfitnesspal.com/public/nutrition?q={query}&page={pageNo}&per_page={noSearchResults}")
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
                servingSize = f"{servingSize} (and more...)"


            if item['brand_name'] is not None:
                IFRESULT=f"{item['brand_name']} | {servingSize}"
            else:
                IFRESULT = f"{servingSize}"

            # Note this is actually a literal \n, not a newline character
            subtitle = f'''
                {IFRESULT}\nCals: {item['nutritional_contents.energy.value']} ⸱ Carbs: {item['nutritional_contents.carbohydrates']}g ⸱ Fat: {item['nutritional_contents.fat']}g ⸱ Protein: {item['nutritional_contents.protein']}g
            '''

            # Add verifIcon if it is a best match
            files = filter(tags, whereAny=['Name' == 'canonical', 'Name' == 'best_match'])
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
            N;CHARSET=utf-8:Next Page
            ORG: Page {nextPage}
            NOTE;CHARSET=UTF-8:Next
            {forwardIcon}
            END:VCARD

            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=utf-8:Previous Page
            ORG: Page {prevPage}
            NOTE;CHARSET=UTF-8:Prev
            {backwardIcon}
            END:VCARD

            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=utf-8:New Search
            ORG: Try a different query
            NOTE;CHARSET=UTF-8:New
            {searchIcon}
            END:VCARD

            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=utf-8:Cancel Search
            ORG:No food will be selected
            NOTE;CHARSET=UTF-8:Cancel
            {searchIcon}
            END:VCARD
        '''

        renamedItem = SetName(text, 'vcard.vcf')
        contacts = GetContacts(renamedItem)

        text = f'''
        "{query}" Search Results ⸱ Page {pageNo}
        {verifIcon} - Verified Best Matches
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
                Alert("This is the first page of the search!")
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

            # append a back button to make sure they are fine
            text = f'''
                {REPEATRESULTS}
                BEGIN:VCARD
                VERSION:3.0
                N;CHARSET=UTF-8:Back
                ORG;CHARSET=UTF-8:Go Back To Search
                {backwardIcon}
                END:VCARD
                '''
            # choose from it
            renamedItem = SetName(text, 'vcard.vcf')
            contacts = GetContacts(renamedItem)

            chosenSize = ChooseFrom(contacts, prompt="Which Serving Size?")

            if chosenSize.Name != "Back"
                # we have the users food now we just need to create it
                # aggregate the needed information and send it out
                searchExit = TRUE
                selectedItem = item
                selectedServingSize = Text(chosenSize.Name)
                multiplier = Number(chosenSize.Notes)


                outputFood = {
                    # that special dictionary that has all the values
                    # set Calories to item['nutritional_contents.energy.value']
                    # set serving size to selectedServingSize 
                    # set name to name
                    # set id to res
                }

                # apply servings multiplier on nutrients
                file = GetFile('FLS/Other/nutriKeys.txt')
                nutrients = SplitText(file, '\n')
                for item in nutrients:
                    num = Number(outputFood[item])
                    num = num * multiplier
                    num = RoundNumber(num, hundredths)
                    outputFood[item] = num

                prompt = f'''
                Search Result:
                {outputFood['Name']} ({outputFood['Serving Size']})
                Cals: {outputFood['Calories']} ⸱ Carbs: {outputFood['Carbs']}g ⸱ Fat: {outputFood['Fat']}g ⸱ Protein: {outputFood['Protein']}g
                Sugar: {outputFood['Sugar']}g ⸱ Fiber: {outputFood['Fiber']}g ⸱ Saturated Fat: {outputFood['Saturated']}g
                Sodium: {outputFood['Sodium']}mg ⸱ Cholesterol: {outputFood['Cholesterol']}mg ⸱ Potassium: {outputFood['Potassium']}mg
                VitA: {outputFood['VitA']}% ⸱ VitC: {outputFood['VitC']}% ⸱ Calcium: {outputFood['Calcium']}% ⸱ Iron: {outputFood['Iron']}%
                '''
                Menu(prompt):
                    case 'Accept':
                        searchExit = TRUE
                    case 'Edit':
                        res = RunShorctut(NutriDix['Display Food Item'], input=outputFood)
                        Menu('Save changes?')
                            case 'Yes':
                                searchExit = TRUE
                                outputFood = res
                            case 'No, use previous values':
                                searchExit = TRUE
                            case 'No, back to search':
                                pass
                    case 'Back To Search':
                        pass

                    case 'Cancel Search':
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
    num = (outputFood[item] / 100) * vitDix[item]
    outputFood[item] = RoundNumber(num, hundredths)

StopShortcut(output = outputFood)

