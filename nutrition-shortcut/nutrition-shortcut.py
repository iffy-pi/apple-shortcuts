# pylint: skip-file
'''
ON THE TODO:
    - Shortcut Review
        - Search Algorithm next! performance is not giving
        - Do the rest

    - Refactor NutriDix updater for the new update process
    - # Regex for illegal characters, use when saving to file [\*\/\\><\.":\?\|]

UDPATES AND CHANGES:
- File/Strucutral Changes:
    - JSON Everything
        - All "*dix.txt" files are now converted to JSON,
        - This includes Food files, and any other relevant dictionaries
        - Done with port over to JSON

    - Food IDs
        - Each food is assigned a unique ID to track it within the system
        - The shortcut Generate Food ID is used to generate the food ID
        - ID is tracked with FLS/Other/nextFoodId.txt

    - New backlogging:
        - Backlog is now stored in new format at FLS/Other/backlog.json
        - Backlog is managed in Nutrition function as usual, but is now deleted when it is empty
        - Log algorithm puts stuff in the backlog
        - Storage format:
            {
                backlog: [
                        {
                            Date: '...',
                            Food: ...,
                        },
                        ...
                    ]
            }

    - History Cache
        - Improve logging speeds by adding a history cache
        - Log Algorithm shortcut puts things in cache, and main shortcut clears it at end of execution
        - Makes sure that large size of history file does not slow logging process down
        - History Cache is saved to FLS/History/foodHistoryCache.json,
        - Format:
            {
                cache : [
                    food: ...,
                    servings: ...,
                    cals: ...,
                    date: ...,
                    time: ...,
                ]
            }

    - Refactored Food History
        - Food history is revamped from FLS/History/foodHistoryDix.txt => FLS/History/foodHistory.json
        - Has new format, see PortOverFoodHistory
        - Used in the main shortcut when clearing cache

    - Environment Variables
        - JSON dictionary stored in FLS/Other/env.json
        - Is formatted:
            {
                '<env var name>' : '<env var value>'
            }
        - Used to contain flags or values that we would like to share between shortcuts:
            - Share hasHealthApp between Nutrition and Log Algorithm

    - New Recents Format
        - Foods are named food_<food ID>.json
        - Foods are now sorted by date when getting recents
        - Shortcut Port Over Recents converts files to new format

    - New Presets Format
        - There is a file presets.json that maintains access times of Presets
            {
                '219' : {
                    'date': '2023-06-09 09:41' # the last time the food was accessed
                },
                < more food IDs>
            }
        - Also have a vcardCache.txt, which is used to cache the vcards used in selecting presets. It is of the format:
            <vcard for food where name=food name, org = serving size, notes = food id>
        - Foods in Presets folder are named in food_<food ID>.json
        - Shortcut Port Over Presets converts files to new format

- Shortcut Changes
    - Added Shortcuts
        - Save Env Vars
            - Saves environment variables for a given shortcut run so that other shortcuts can access it easily
            - See environment variables above.
        
        - Port Over Food History
            - Converts old foodHistoryDix.txt format to foodHistory.json

        - Port Over Foods
            - Updates food files to JSON
            - Adds a unique ID so they can be identified

        - Generate Food ID
            - Generates a unique id for each food object

        - Port Over Recents and Presets
            - Converting to new format for recents and presets

    - Removed Shortcuts
        - Get History On

    - Updated Shortcuts
        - Nutrition
            - Improved methods to check when a device has a health app.
            - Improved backlog clearing
            - Added history cache clearing

        - Log Algorithm
            - Improved logging speeds by minor refactoring of code
            - Implemented history caching using new history cache files

        - Food History
            - Refactored to handle new food history format
            - Other improvements are under the hood

        - Search Algorithm
        - Get Recents
        - Add Recent
        - Get Preset
        - Make Preset
        - Remove Preset
        - Edit Preset


CURRENT STATE:
    - Current file structure (FLS):
        - Presets
            - presetNames.txt : For names of presets
            - Foods
                - Food JSON files in the format of food_{food id}.json

        - Recents:
            - recentNames.txt : For names of recents foods
            - Foods:
                - Food JSON files in the format of food_{food id}.json

        - Barcodes
            - barcodesInfo.json : Maps barcodes to food IDs

            - barcodeDix.txt : Maps barcodes to food names
            - Foods
                - Food JSON files in the format of food_{food id}.json
        
        - History
            - foodHistoryDix.txt => foodHistory.json
            - foodHistoryCache.json

        - Other
            - backlog.txt and backtag.txt => backlog.json
            - nextFoodId.txt : Generates next Unique ID for food
            - lastUpdateCheck: : Date of last checked update
            - nutriKeys.txt : Keys in the food dictionary that are the nutrients
            - env.json : Stores environment variables
            - shortcutNames.json : Stores the name of shortcuts which are used in Run Shortcut actions, ideally should allow user to configure it
                See saved version
                // The porting over shortcuts
                {
                    "Port Over Food History": "Port Over Food History",
                    "Port Over Foods": "Port Over Foods",
                    "Port Over Recents and Presets": "Port Over Recents and Presets",
                }
                // deperectated
                {
                    "Correct Dictionary":"Correct Dictionary",
                    "Number Converter":"Number Converter",
                    "Make Food Item":"Make Food Item",
                    "Save Env Vars": "Save Env Vars",
                    "Add Preset":"Add Preset 1.1",
                }

            - shortcutLinksDix.txt : ? Maps shortcuts to their icloud links
'''

# GLOBAL VARS
FLS = "Shortcuts/FLS"

def textToContacts(var):
    text = Text(var)
    renamedItem = SetName(var, 'vcard.vcf')
    return GetContacts(renamedItem)

def convertTextFileToJSON():
    GetFile(f"{folder}/{filename}.txt")
    RenameFile(f"{filename}.json")

#---------------------------------------------------------------------------------------------------------------------------------PortOverFoods

def PortOverFoods():
    file = GetFile("FLS/Other/nextFoodId.txt")
    if file is not None:
        IFRESULT = file
    else:
        IFRESULT = "0"
    nextId = Number(IFRESULT)

    foodLocs = [
        "FLS/Recents/Foods",
        "FLS/Presets/Foods"
        "FLS/Barcodes/Foods"
    ]

    for loc in foodLocs:
        dirr = GetFile(f"{loc}", errorIfNotFound=False)
        for item in GetContentsOfFolder(dirr):
            food = Dictionary(item)
            food['id'] = nextId
            nextId  = nextId + 1

            # save the new food file
            SaveFile(food, f"{loc}/{food['Name']}.json")

            file = GetFile(f"{loc}/{food['Name']}.txt", errorIfNotFound=False)
            if file is not None:
                DeleteFile(file, deleteImmediately=True)

    SaveFile(nextId, "FLS/Other/nextFoodId.txt", overwrite=True)

#---------------------------------------------------------------------------------------------------------------------------------PortOverRecentsAndPresets

def PortOverRecentsAndPresets():
    nameFiles = [
        "FLS/Presets/presetNames.txt",
        "FLS/Recents/recentNames.txt"
    ]

    foodDirs = [
        "FLS/Presets/Foods",
        "FLS/Recents/Foods"
    ]

    # note files are originally text files without food ids

    for REPEATITEM in nameFiles:
        foodsDir = foodDirs.getItemAtIndex(REPEATINDEX)
        file = GetFile(REPEATITEM, errorIfNotFound=False)
        names = SplitText(file, '\n')
        for name in names:
            # Add the name to list
            file = GetFile(f"{foodsDir}/{name}.json")
            if file is not None:
                food = Dictionary(file)

                if food['id'] is None:
                    res = RunShortcut(nutrDix['GFID'])
                    food['id'] = res
                    SaveFile(food, f'{foodsDir}/food_{foodId}.json', overwrite=True)
                    IFRESULT = Number(res)
                else:
                    RenameFile(file, f"food_{IFARG}.json")
                    IFRESULT = Number(IFARG)

                foodId = IFRESULT

                if name == 'FLS/Presets/presetNames.txt':
                    text = f'''
                        BEGIN:VCARD
                        VERSION:3.0
                        N;CHARSET=UTF-8:{food['Name']}
                        ORG;CHARSET=UTF-8:{food['Serving Size']}
                        NOTE;CHARSET=UTF-8:{foodId}
                        END:VCARD

                    '''
                    vcardCache.append(text)

    if vcardCache is not None:
        SaveFile(Text(vcardCache), 'FLS/Presets/vcardCache.txt', overwrite=True)

#---------------------------------------------------------------------------------------------------------------------------------PortOverRecentsAndPresets

def PortOverBarcodes():
    # note files are originally text files without food ids

    barcodesFile = GetFile('FLS/Barcodes/barcodeDix.txt', errorIfNotFound=False)
    barcodes = Dictionary(barcodesFile)

    file = GetFile("FLS/Other/nextFoodId.txt", errorIfNotFound=False)
    if file is not None:
        IFRESULT = Number(file)
    else:
        IFRESULT = 0
    nextId = IFRESULT

    for item in barcodes.keys():
        barcode = Text(item)
        foodName = barcodes[item]
        file = GetFile(f'FLS/Barcodes/Foods/{foodName}.json', errorIfNotFound=False)
        if file is not None:
            food = Dictionary(file)
            if food['id'] is None:
                num = nextId
                nextId = nextId+1
                IFRESULT = num
            else:
                IFRESULT = food['id']
            foodId = IFRESULT

            food['id'] = foodId
            food['Barcode'] = barcode
            SaveFile(f'FLS/Barcodes/Foods/food_{nextId}.json', overwrite=True)

            nextId = nextId+1

            DeleteFile(file)

    DeleteFile(barcodesFile, deleteImmediately=True)
    SaveFile(nextId, "FLS/Other/nextFoodId.txt", overwrite=True)

#---------------------------------------------------------------------------------------------------------------------------------PortOverFoodHistory

def PortOverFoodHistory():

    '''
    New Food history format:
    {
        'YYYY-MM-DD': {
            'HH-MM': [{
                'food': ...,
                'servings': ...,
                'cals': ...,
            },
            ...
            ...
            ],
            
            # can either be dictionary if only one item or list of dictionaries if more
        }
    }
    
    For: "1x Fried egg (90.16 kCal"
    ([0-9][0-9]*[\.]*[0-9]*)x (.*) \(([0-9][0-9]*[\.]*[0-9]*) kCal\)
    
    For "1 [Chicken Noodles Super Pack (430 Kcal)]"
    ([0-9][0-9]*[\.]*[0-9]*) \[(.*) \(([0-9][0-9]*[\.]*[0-9]*) Kcal\)\]
    '''

    newHistory = Dictionary();
    history = Dictionary(GetFile("FLS/History/foodHistoryDix.txt"))

    regex1 = text("([0-9][0-9]*[\.]*[0-9]*)x (.*) \(([0-9][0-9]*[\.]*[0-9]*) [kK][cC]al\)")
    regex2 = text("([0-9][0-9]*[\.]*[0-9]*) \[(.*) \(([0-9][0-9]*[\.]*[0-9]*) [kK][cC]al\)\]")

    for repeatItem in history.keys():
        dayKey = repeatItem
        text = history[dayKey]
        dayDix = Dictionary(text)
        newDayDix = newHistory[dayKey]

        if newDayDix is None:
            newDayDix = Dictionary()
        
        for repeatItem2 in dayDix.keys().filter( name => name != "SAMPLE"):
            timeKey = repeatItem2
            logText = dayDix[timeKey]
            newTimeList = newDayDix[timeKey]

            # if it does not have any value, we will add it to the variable

            for log in logText.splitByNewLines():
                logGroup = []

                # 0 -> servings
                # 1 -> food name
                # 2 -> calories

                # try the first regex
                logGroup = GetAllGroups( MatchText(log, regex1) )
                if Count(logGroup) == 0:
                    # try the other regex
                    logGroup = GetAllGroups( MatchText(log, regex2) )
                    if Count(logGroup) == 0:
                        logGroup = [1, log, 0]

                totalCals = RoundNumber(logGroup[2])
                servings = Number(logGroup[0])

                dix = {
                    'servings': servings,
                    'food': logGroup[1],
                    'cals': totalCals
                }

                newTimeList.append(dix)

            # set in the new day dix
            newDayDix[timeKey] = newTimeList

        # set the new day key
        newHistory[dayKey] = newDayDix;

        # save it to the file
        SaveFile(newHistory, "FLS/History/foodHistory.json", overwrite=True)



#---------------------------------------------------------------------------------------------------------------------------------NutriDixUpdater

def NutriDixUpdater():
    pass

#---------------------------------------------------------------------------------------------------------------------------------WeekSummary

def WeekSummary():

    TRUE = 1
    FALSE = 0

    nutrDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))

    getDateRange = TRUE
    makeCaloriePlot = FALSE
    averageBreakdown = FALSE
    plotNutrients = TRUE


    Menu("Statistics"):
        case 'Nutrient Breakdown For Date...':
            getDateRange = FALSE

        case 'Nutrient Breakdown For Dates...':
            pass
        
        case 'Average Nutrient Breakdown Between Dates...':
            # where we just plot an average breakdown
            averageBreakdown = TRUE

        case 'Calories Breakdown For Dates...': 
            makeCaloriePlot = TRUE
            plotNutrients = FALSE

    start = AskForInput(Input.Date, prompt="Select Start Date")
    
    if getDateRange == TRUE:
        IFRESULT = AskForInput(Input.Date, prompt="Select End Date", default=start)
    else:
        IFRESULT = start

    end = IFRESULT
    termEnd = AddToDate(end, days=1)

    repeats = TimeBetweenDates(start, termEnd, inDays=True)
    if repeats > 1:
        makeCaloriePlot = TRUE

    dix = {
        'averageBreakdown': averageBreakdown,
        'plotNutrients': plotNutrients,
        'start': start,
        'end': end,
        'repeats' : repeats
    }

    stats = RunShortcut(nutrDix['Calculate Stats'], input=dix)

    if plotNutrients == TRUE:
        for plot in stats['chartyPiePlots']:
            chartId = Charty.NewChart(plot['title'])
            seriesLabel = Charty.AddSeries('Nutrient Breakdown', chartId, 'Pie', values=plot['values'], labels=plot['labels'])
            Charty.StylePieSeries(seriesLabel, chartId, colors=plot['labelColors'], labels=plot['labels'])


    if makeCaloriePlot == TRUE:
        averageCals = CalculateStatistics("Average", stats['calorieValues'])
        for _ in range(repeats):
            averageCalValues.append(averageCals)

        # create the chart
        chartId = Charty.NewChart(f"{start.format(custom="MMM dd")} - {end.format(custom="MMM dd")} Energy")
        Charty.AddSeries("Daily Energy", chartId, 'Line', xValues=stats['calorieLabels'], yValues=stats['calorieValues'])
        Charty.AddSeries("Average Energy", chartId, 'Line', xValues=stats['calorieLabels'], yValues=averageCalValues)
        Charty.StyleAxis("X Axis", chartId, title="Dates", formatValuesAsDate={'custom'="MMM dd"})

    OpenApp("Charty")

#---------------------------------------------------------------------------------------------------------------------------------CalculateStats

def CalculateStats():

    TRUE = 1
    FALSE = 0

    emptyList = []

    # averageBreakdown = FALSE
    # plotNutrients = TRUE

    params = Dictionary(ShortcutInput)

    averageBreakdown = params['averageBreakdown']
    plotNutrients = params['plotNutrients']
    start = Date(params['start'])
    end = Date(params['end'])
    repeats = Number(params['repeats'])

    # we have the base code to create a pie chart for a given day

    keyToSample = {
            "Calories": "Dietary Calories",
            "Carbs": "Carbohydrates",
            "Fat": "Total Fat",
            "Protein": "Protein",
            "Sugar": "Sugar",
            "Fiber": "Fiber",
            "Monounsaturated": "Monounsaturated Fat",
            "Polyunsaturated": "Polyunsaturated Fat",
            "Saturated": "Saturated Fat",
            "Sodium": "Sodium",
            "Cholesterol": "Dietary Cholesterol",
            "Potassium": "Potassium",
            "VitA": "Vitamin A",
            "VitC": "Vitamin C",
            "Calcium": "Calcium",
            "Iron": "Iron"
        }

    nutrUnits = {
        "Calories": "kcal",
        "Carbs": "g",
        "Fat": "g",
        "Protein": "g",
        "Sugar": "g",
        "Fiber": "g",
        "Monounsaturated": "g",
        "Polyunsaturated": "g",
        "Saturated": "g",
        "Trans": "g",
        "Sodium": "g",
        "Cholesterol": "g",
        "Potassium": "g",
        "VitA": "g",
        "VitC": "g",
        "Calcium": "g",
        "Iron": "g"
    }

    labelColorMap = {
        "Carbs": "ffff375f",
        "Fat": "ffffd60a",
        "Protein": "ff30d158",
        "Sugar": "ff64d2fe",
        "Fiber": "633D01",
        "Monounsaturated": "AD9700",
        "Polyunsaturated": "AD7200",
        "Saturated": "F4B4EF",
        "Sodium": "FFFFFF",
        "Cholesterol": "F2EE89",
        "Potassium": "ff64d2fe",
        "VitA": "97001e",
        "VitC": "F98B06",
        "Calcium": "B9B6B2",
        "Iron": "484746"
    }

    res = SplitText(GetFile("FLS/Other/nutriKeys.txt"), '\n')
    nutriKeys = filter(res, whereAll=['Name' != 'Trans'])

    if plotNutrients == FALSE:
        nutriKeys = 'Calories'

    # stores the total values for the nutrients on that day
    totalNutrDix = {}

    for repeatIndex in range(repeats):

        curDate = AddToDate(start, days=repeatIndex-1)
        labels = emptyList
        values = emptyList
        labelColors = emptyList

        for curNutrKey in nutriKeys:
            sampleType = keyToSample[curNutrKey]
            unit = nutrUnits[curNutrKey]
            results = FindHealthSamples(type=sampleType, startDateIsOn=curDate, unit=unit)
            
            num = Number( CalculateStatistics("Sum", results.Value))
            daySum = RoundNumber(num, hundredths)

            if curNutrKey == 'Calories':
                # add it to the calorie plots
                calorieLabels.append(curDate)
                calorieValues.append(daySum)
            else:
                values.append(daySum)

                # add to total values for this lenght
                totalNutrDix[curNutrKey] = Number(totalNutrDix[curNutrKey]) + daySum


        dayTotal = CalculateStatistics("Sum", values)

        for repeatItem2, repeatIndex2 in filter(nutriKeys, where='Name' != 'Calories'):
            item = values.getItemAtIndex(repeatIndex2)
            num = (item / dayTotal) * 100
            num = RoundNumber(num, hundredths)
            labels.append(f'{repeatItem2} ({num}%)')
            labelColors.append(labelColorMap[repeatItem2])


        nutrPlots.append({
            'title': f'{curDate.format(date="medium")} Breakdown',
            'labels': labels,
            'values': values,
            'labelColors': labelColors
            })

    if averageBreakdown == TRUE:
        nutrTotal = CalculateStatistics("Sum", totalNutrDix.values())
        
        for curNutrKey in nutriKeys:
            # divide each nutrient total by the number of dates we samples 

            # calculates the percentage of the current nutrient in the sample range
            # it will be the same as when average since average divides by constant factor
            curPercent = RoundNumber((totalNutrDix[curNutrKey] / nutrTotal) * 100, hundredths)

            # Calculate the average nutrient value for the plot
            averageNutr = totalNutrDix[curNutrKey] / repeats

            averageValues.append(averageNutr)
            averageLabels.append(f'{curNutrKey} ({curPercent}%)')

        IFRESULT = {
            'title': f'{start.format(custom="MMM dd")} - {end.format(custom="MMM dd")} Average',
            'labels': averageLabels,
            'values': averageValues
        }

    else:
        IFRESULT = nutrPlots
    
    chartyPiePlots = IFRESULT

    res = {}
    res['calorieLabels'] = calorieLabels
    res['calorieValues'] = calorieValues
    if plotNutrients == TRUE:
        res['chartyPiePlots'] = chartyPiePlots

    return res


#---------------------------------------------------------------------------------------------------------------------------------FoodHistory

def FoodHistory()
    file = GetFile("FLS/History/foodHistory.json")
    if file is not None:
        IFRESULT = file
    else:
        IFRESULT = {}

    history = Dictionary(IFRESULT)

    # show foods today in main menu
    today = CurrentDate()

    dayDix = history[ today.format(date="short", time=None) ]
    if dayDix is not None:
        keys = FilterFiles(dayDix[keys], sortBy="Name", AtoZ=True)
        for timeKey in keys:
            timeList = dayDix[timeKey]
            for logItem in timeList:
                text = f'''{timeKey}: {logItem['servings']}x {logItem['food']} ({logItem['cals']} kCals)'''
                todaysLogs.append(text)


    if Count(todaysLogs) > 0:
        IFRESULT = f'''
            Foods eaten today:
            {todaysLogs}
        '''
    else:
        IFRESULT = 'You have not eaten any foods today'

    prompt = IFRESULT

    mainMenu = Menu(prompt=prompt, ['More History Options', 'Exit'])
    if mainMenu.opt("More History Options"):
        subMenu = Menu(prompt="History Options", [
                'Foods Logged On Day',
                'Foods Logged Between...',
                'Foods Logged In Past Week',
                'Foods Logged In Past Month',
                'Foods Logged All Time',
                'Exit'
            ])

        if subMenu.opt('Foods Logged On Day'):
            start = AskForInput(Input.Date)
            end = AddToDate(start, days=1)

        elif subMenu.opt('Foods Logged Between...'):
            start = AskForInput(Input.Date)
            end = AddToDate(AskForInput(Input.Date), days=1)

        elif subMenu.opt('Foods Logged In Past Week'):
            start = SubFromDate(today, weeks=1)
            end = AddToDate(today, days=1)

        elif subMenu.opt('Foods Logged In Past Month'):
            start = SubFromDate(today, months=1)
            end = AddToDate(today, days=1)

        elif subMenu.opt('Foods Logged All Time'):
            useDateList = TRUE
            # go through all the keys
            # reverse because we want the latest ones first
            dateList = filter(history.keys(), sortBy=(Name, ZtoA))

        if subMenu.opt('Exit'):
            return

        if useDateList == TRUE
            IFRESULT = Count(dateList)
        else:
            IFRESULT = TimeBetweenDates(start, end, inDays=True)
        repeats = IFRESULT


        for repeatIndex in range( repeats ):
            if useDateList == TRUE
                IFRESULT = dateList.getItemAtIndex(repeatIndex)
            else:
                # shortcuts are one indexes, so subtract by 1 and add to start
                # doing it so we get latest date first
                res = repeats - repeatndex
                res = AddToDate(start, res)
                IFRESULT = text(res.format(date="short", time=None))

            dayKey = IFRESULT
            dayDix = history[dayKey] 

            if dayDix is not None:
                resultsForDay = []
                keys = filter(dayDix.keys(), sortBy=(Name, ZtoA))

                text = Date(f'{timeKey}h').format(custom="h:mm a")
                dispTime = text

                for timeKey in keys:
                    for log in dayDix[timeKey]:
                        resultsForDay.append( 
                            f'{logItem['servings']}x {logItem['food']} ({logItem['cals']} kCals) @ {dispTime}'
                        )
                
                logResults.append(f'''
                        {dayKey}
                        {resultsForDay}
                    ''')

        # show results of the search
        text = f"{logResults}"
        text = SetName(text, "Query Results")
        QuickLook(text)

    elif mainMenu.opt("Exit"):
        return

#---------------------------------------------------------------------------------------------------------------------------------BarcodeSearch

def BarcodeSearch():
    TRUE = 1
    FALSE = 0

    nutrDix = Dictionary(GetFile('FLS/Other/shortcutNames.json'))

    params = Dictionary(ShortcutInput)

    showMenu = FALSE


    if params['getFood'] is not None:
        # we are getting a food from the database
        Menu("Get Food"):
            case 'Select from Personal Database':
                return RunShortcut(nutrDix['Get Saved Food'], input={'type': 'barcodes'})

            case 'Scan Barcode':
                pass

            case 'Cancel':
                return None

    # we are adding to the database so scan immediately
    barcode = Text(ScanBarcode())

    file = GetFile('FLS/Barcodes/barcodeCache.json', errorIfNotFound=False)
    if file is not None:
        IFRESULT = file
    else:
        barcodeCache = {}
        folder = GetFile('FLS/Barcodes/Foods', errorIfNotFound=False)
        for item in GetContentsOfFolder(folder):
            barcodeCache[ item['Barcode'] ] = item['id']
        SaveFile(barcodeCache, 'FLS/Barcodes/barcodeCache.json', overwrite=True)
        IFRESULT = barcodeCache
    barcodeCache = IFRESULT

    if barcodeCache[barcode] is not None:
        file = GetFile(f'FLS/Barcodes/Foods/food_{barcodeCache[barcode]}.json')
        if params['getFood'] is not None:
            return file
        else:
            # the barcode has a match in the personal database, either edit it, cancel or remke it
            Menu(f'There is a food in your database with the barcode "{barcode}"'):
                case 'Edit Food':
                    RunShortcut(nutrDix['Edit Saved Food'], input={'type': 'barcodes', 'args': file})
                    return None
                case 'Remake Food':
                    DeleteFile(file, deleteImmediately=True)
                case 'Cancel'
                    return None


    # if we get here that means we are creating a new food item
    foodResolved = FALSE
    doSearch = FALSE
    testing = FALSE

    # Search online database

    if testing == TRUE:
        IFRESULT = ... # text of some barcode result
    else:
        url = URL(f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json')
        IFRESULT = GetContentsOfURL(url)

    res = Dictionary(IFRESULT)

    if res['status'] == 1:
        # we found the product, now we just map the dictionary values
        nutrInfo = res['product.nutriments']

        foodId = RunShortcut(nutrDix['GFID'])

        outputFood = {
            'Name': res['product.generic_name_en'],
            'Barcode': barcode,
            'id': foodId,
            'Serving Size': res['product.serving_size'],
            'Calories': nutrInfo['energy-kcal_value'],
            'Carbs': nutrInfo['carbohydrates_value'],
            'Fat': nutrInfo['fat_value'],
            'Protein': nutrInfo['proteins_value'],
            'Sugar': nutrInfo['sugars_value'],
            'Fiber': nutrInfo['fiber_value'],
            'Monounsaturated': 0
            'Polyunsaturated': 0
            'Saturated': nutrInfo['saturated-fat_value'],
            'Trans': nutrInfo['trans-fat_value'],
            'Sodium': nutrInfo['sodium_value'],
            'Cholesterol': nutrInfo['cholesterol_value'],
            'Potassium': nutrInfo['potassium_value'],
            'VitA': 0,
            'VitC': nutrInfo['vitamin-c_value'],
            'Calcium': nutrInfo['calcium_value'],
            'Iron': nutrInfo['iron_value'],
        }

        # vitamin a is in IU, convert to mcg
        num = Number(nutrInfo['vitamin-a_value']) * 0.3
        outputFood['VitA'] = num

        prompt = f'''
        Search Result:
        {outputFood['Name']} ({outputFood['Serving Size']})
        Cals: {outputFood['Calories']} ⸱ Carbs: {outputFood['Carbs']}g ⸱ Fat: {outputFood['Fat']}g ⸱ Protein: {outputFood['Protein']}g
        Sugar: {outputFood['Sugar']}g ⸱ Fiber: {outputFood['Fiber']}g ⸱ Saturated Fat: {outputFood['Saturated']}g
        Sodium: {outputFood['Sodium']}mg ⸱ Cholesterol: {outputFood['Cholesterol']}mg ⸱ Potassium: {outputFood['Potassium']}mg
        VitA: {outputFood['VitA']}mcg ⸱ VitC: {outputFood['VitC']}mg ⸱ Calcium: {outputFood['Calcium']}mg ⸱ Iron: {outputFood['Iron']}mg
        '''
        Menu(prompt):
            case 'Accept And Continue':
                foodResolved = TRUE
            case 'Edit':
                res = RunShorctut(NutriDix['Display Food Item'], input=outputFood)
                Menu('Save changes?')
                    case 'Yes':
                        outputFood = res
                        foodResolved = TRUE
                    case 'No, use previous values':
                        foodResolved = TRUE
                    case 'No, search for food or make manually':
                        pass
            case 'Search for food or make food manually':
                pass
            case 'Cancel':
                return None

    if foodResolved == FALSE:
        # no match in database or in search so we continue
        Menu("There was no match found on OpenFoodFacts.org, what would you like to do?"):
            case 'Search for Food':
                doSearch = TRUE
            case 'Make Food Manually':
                pass
            case 'Cancel':
                return None

    if doSearch == TRUE:
        # perform search
        outputFood = RunShortcut(nutrDix['Search Algorithm'])
        
        if outputFood is not None:
            foodResolved = TRUE
            
        Menu('Search had no results'):
            case 'Exit with no selection':
                return None
            case 'Make Food Manually':
                pass

    if foodResolved == FALSE:
        # otherwise we fall through to make food manually
        outputFood = RunShortcut(nutrDix['Make Food Manually'])

    # save the new output food to database and then continue
    outputFood['Barcode'] = barcode

    barcodeCache[barcode] = outputFood['id']
    SaveFile(barcodeCache, 'FLS/Barcodes/barcodeCache.json', overwrite=True)

    SaveFile(outputFood, f'FLS/Barcodes/Foods/food_{outputFood['id']}.json', overwrite=True)

    return outputFood

#---------------------------------------------------------------------------------------------------------------------------------MakeFoodManually

def MakeFoodManually(): # Make Food Manually
    nutrDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))
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

    return foodDix

#---------------------------------------------------------------------------------------------------------------------------------MakePreset

def MakePreset(): # Make Preset
    # < whatever method we use to make the preset >

    TRUE = 1
    FALSE = 0

    nutrDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))
    
    if ShortcutInput is not None:
        # if we dont do this, then if result will be the item above the if
        # i.e. nutrDix
        IFRESULT = GetVariable(ShortcutInput)
    else:
        IFRESULT = RunShortcut(nutrDix['Foods List'])

    foods = IFRESULT

    file = GetFile('FLS/Other/nutriKeys.txt')
    nutriKeys = SplitText(file, '\n')

    foodsDix = {}
    selectedIds = []
    nextId = 0


    # create selection system
    for item in foods:
        foodsDix[nextId] = item
        selectedIds.append(nextId)
        nextId = nextId+1

    # check to make sure it doesnt clash with other food names
    folder = GetFile("FLS/Presets/Foods", errorIfNotFound=False)
    for file in GetContentsOfFolder(folder):
        presetNames.append(file['Name'])

    for _ in Count(foods):
        if Count(selectedIds) > 0:
            for listId in selectedIds
                food = foodsDix[listId]
                text = f'''
                BEGIN:VCARD
                VERSION:3.0
                N;CHARSET=UTF-8:{food['Name']}
                ORG;CHARSET=UTF-8:{food['Servings']} servings
                NOTE;CHARSET=UTF-8:{listId}
                END:VCARD
                '''
                REPEATRESULTS.append(text)

            contacts = textToContacts(REPEATRESULTS)
            chosenIds = ChooseFrom(contacts, selectMultiple=True, selectAll=True, prompt="Select Foods to be made into Preset")
        
            presetFood = {}

            for contact in chosenIds:
                # remove from selectedIds
                selectedIds = filter(selectedIds, where='Name' != contact.Notes)

                item = foodsDix[contact.Notes]
                curFood = Dictionary(item)

                defaultSize = curFood['Serving Size']
                defaultName = curFood['Name']

                if curFood['Servings'] is None:
                    IFRESULT = AskForInput(Input.Number, prompt=f'How many servings of "{defaultName}"? (1 serving = {defaultSize})',
                                default=1, allowDecimals=True, allowNegatives=False)
                else:
                    IFRESULT = Number(curFood['Servings'])
                servings = IFRESULT

                for nutr in nutriKeys:
                    num = Number(curFood[nutr])
                    # multiply nutrients by serving size
                    num = num * servings

                    # add to total nutrients of preset
                    num2 = Number(presetFood[nutr])
                    num = num + num2
                    num = RoundNumber(num, hundredths)

                    presetFood[nutr] = num


            # now presetFood will have all the items
            if Count(chosenIds) > 1:
                defaultSize = ''
                defaultName = ''

            name = AskForInput(Input.Text, prompt="What is the name of this preset?", default=defaultName)

            if Count(presetNames) > 0:
                breakLoop = FALSE
                for _ in range(10):
                    if breakLoop == FALSE:
                        res = filter(presetNames, where['Name' == name])
                        if res is not None:
                            Menu(f'Preset "{name}" already exists'):
                                case 'Select a different name':
                                    name = AskForInput(Input.Text, prompt=f'"{name}" already exists, please select a new name', default=name)
                                case 'Keep both with same name':
                                    breakLoop = TRUE
                        else:
                            presetNames.append(name)
                            breakLoop = TRUE

            servingSize = AskForInput(Input.Text, prompt="What is the serving size of this preset?", default=defaultSize)

            # then set in the food
            foodId = RunShortcut(nutrDix["GFID"])
            presetFood['id'] = foodId
            presetFood['Serving Size'] = servingSize
            presetFood['Name'] = name

            # save to file
            SaveFile(presetFood, f"FLS/Presets/Foods/food_{foodId}.json", overwrite=True)

    # delete the cache since it is invalid
    file = GetFile("FLS/Presets/vcardCache.txt", errorIfNotFound=False)
    DeleteFile(file, deleteImmediately=True)

#---------------------------------------------------------------------------------------------------------------------------------SelectSavedFoods

def SelectSavedFoods():
    TRUE = 1
    FALSE = 0

    cancelIcon = Text() 

    deleteMode = FALSE

    savedInfo = {
        'barcodes': { 'folder': 'FLS/Barcodes', 'prompt': 'Barcoded Foods'}
        'presets': { 'folder': 'FLS/Presets', 'prompt': 'Presets'}
        'both': { 'prompt' : 'Preset(s) and Barcoded Food(s)'}
    }

    params = Dictionary(ShortcutInput)

    if typeDir[ params['type']] is None:
        Alert('No type specified')
        return None
    else:
        config = savedInfo [ params['type'] ]
        parentFolder = config['folder']


    if params['deleteMode'] is not None:
        deleteMode = TRUE


    if params['type'] == 'all':
        IFRESULT = [ 'presets', 'barcodes' ]
    else:
        IFRESULT = params['type']
    searchTypes = IFRESULT

    for curType in searchTypes:
        dixVal = savedInfo[curType]
        parentFolder = dixVal['folder']
        prompt = dixVal['prompt']

        file = GetFile(f"{parentFolder}/vcardCache.txt", errorIfNotFound=False)
        if file is not None:
            IFRESULT = Text(file)
        else:
            # create the vcard cache
            folder = GetFile(f"{parentFolder}/Foods")
            files = GetContentsOfFolder(folder)
            files = filter(files, sortBy='Last Modified Date', order='Latest First')
            for item in files:
                food = Dictionary(file)
                # some weird bug is limiting me to have to pull ID separately
                dixVal = food['id']
                dix = {
                    'folder': parentFolder,
                    'id': dixVal
                }
                text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=UTF-8:{food['Name']}
                    ORG;CHARSET=UTF-8:{prompt} ⸱ {food['Serving Size']}
                    NOTE;CHARSET=UTF-8:{dix}
                    END:VCARD

                '''
                REPEATRESULTS.append(text)

            SaveFile(Text(REPEATRESULTS), f"{parentFolder}/vcardCache.txt", overwrite=True)

            IFRESULT = Text(REPEATRESULTS)

    vcardCache = Text(REPEATRESULTS)


    text = f'''
        BEGIN:VCARD
        VERSION:3.0
        N;CHARSET=UTF-8:No Selection
        ORG;CHARSET=UTF-8:No foods will be selected
        NOTE;CHARSET=UTF-8:Cancel
        {cancelIcon}
        END:VCARD
    '''

    renamedItem = SetName(text, 'vcard.vcf')
    contact = GetContacts(renamedItem)
    choices.append(contact)

    SetName(vcardCache, 'vcard.vcf')
    contacts = GetContacts(renamedItem)
    files = filter(contacts, sortBy='Name')
    choices.append(files)


    if deleteMode == TRUE:
        IFRESULT = f"Select {config['prompt']} to Delete"
    else:
        IFRESULT = f"Select {config['prompt']}"

    selectedItems = ChooseFrom(choices, prompt=IFRESULT, selectMultiple=True)
    for chosen in selectedItems:
        if chosen.Notes == 'Cancel':
            return None

        dix = Dictionary(chosen.Notes)

        foodId = dix['id']
        parentFolder = dix['folder']

        # make this the most used one
        file = GetFile(f"{parentFolder}/Foods/food_{foodId}.json")
        food = Dictionary(file)

        if deleteMode == TRUE:
            # delete the file
            DeleteFile(file, deleteImmediately=True)
            Notification(f'{config['prompt']} {food['Name']} has been deleted!')
        else:
            # save the file to update last modified after
            SaveFile(file, f"{parentFolder}/Foods/food_{foodId}.json", overwrite=True)
        
        # add the food
        selectedFoods.append(food)

    if deleteMode == TRUE:
        # delete the cache since it is invalid
        file = GetFile(f"{parentFolder}/vcardCache.txt", errorIfNotFound=False)
        DeleteFile(file, deleteImmediately=True)

        if params['type'] == 'barcodes':
            file = GetFile(f"{parentFolder}/barcodeCache.json", errorIfNotFound=False)
            DeleteFile(file, deleteImmediately=True)

    return selectedFoods
    
#---------------------------------------------------------------------------------------------------------------------------------EditSavedFood

def EditSavedFood(): # Edit Saved Food

    TRUE = 1
    FALSE = 0

    params = Dictionary(ShortcutInput)

    savedInfo = {
        'barcodes': { 'folder': 'FLS/Barcodes', 'prompt': 'Barcoded Food'}
        'presets': { 'folder': 'FLS/Presets', 'prompt': 'Preset'}
    }



    nutrDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))
    
    if params['args'] is not None:
        IFRESULT = params['args']
    else:
        IFRESULT = RunShortcut(nutrDix['Select Saved Foods'], input=params)
    selectedFoods = IFRESULT

    config = savedInfo [ params['type'] ]

    file = GetFile("FLS/Other/nutriKeys.txt")
    nutriKeys = SplitText(file, '\n')

    for item in selectedFoods:
        oldFood = Dictionary(item)
        
        foodId = food['id']

        Menu(f"What type of editing would you like to do for {oldFood['Name']}?"):
            case 'Scale Serving Size':
                mult = AskForInput(Input.Number, prompt=f'What is the scaling factor?', default=1, allowDecimals=True)
                if mult != 1:
                    for item in nutriKeys:
                        num = Number(oldFood[item])
                        num = num * mult
                        num = RoundNumber(num, hundredths)
                        oldFood[item] = num

                    oldFood['Serving Size'] = AskForInput(Input.Text, prompt="What is the new serving size?", default=f"{mult} of {oldFood['Serving Size']}")
                
                MENURESULT = oldFood

            case 'Edit Food Fields Manually':
                # do display food editing TODO
                MENURESULT = RunShortcut(nutrDix['Display Food Item'], input=oldFood)

        newFood = MENURESULT
        name = newFood['Name']

        if name != oldFood['Name']:
            # need to ensure it isnt taken by something else

            # check to make sure it doesnt clash with other food names
            folder = GetFile(f"{config['folder']}/Foods", errorIfNotFound=False)
            for food in GetContentsOfFolder(folder):
                foodNames.append(food['Name'])

            breakLoop = FALSE
            for _ in range(10):
                if breakLoop == FALSE:
                    res = filter(foodNames, whereAll=['Name' == name, 'Name' != oldFood['Name']])
                    if res is not None:
                        Menu(f'There is already a food named "{name}"'):
                            case 'Select A Different Name':
                                name = AskForInput(Input.Text, prompt=f'"{name}" already exists, please select a new name')
                            case 'Keep both foods with this name':
                                breakLoop = TRUE
                    else:
                        breakLoop = TRUE

        newFood['Name'] = name

        # save the file
        SaveFile(newFood, f"{config['folder']}/food_{foodId}.json", overwrite=True)

    # delete the cache since it is invalid
    file = GetFile(f"{config['folder']}/vcardCache.txt", errorIfNotFound=False)
    DeleteFile(file, deleteImmediately=True)


#---------------------------------------------------------------------------------------------------------------------------------GetRecent

def GetRecent(): # "Get Recent"
    cancelIcon = # ... 

    dir_ = GetFile(f"FLS/Recents/Foods")

    files = GetContentsOfFolder(dir_, errorIfNotFound=False)
    files = filter(files, sortBy='Last Modified Date', order='Latest First')

    for item in files:
        date = Text(item.lastModifiedDate.format(date="How Long Ago/Until"))
        food = Dictionary(item)

        text = f'''
            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=UTF-8:{food['name']}
            ORG;CHARSET=UTF-8:{food['Serving Size']} ⸱ {date}
            NOTE;CHARSET=UTF-8:{food['id']}
            END:VCARD
        '''
        REPEATRESULTS.append(text)

    text = f'''
        BEGIN:VCARD
        VERSION:3.0
        N;CHARSET=UTF-8:No Selection
        ORG;CHARSET=UTF-8:No foods will be selected
        NOTE;CHARSET=UTF-8:Cancel
        {cancelIcon}
        END:VCARD
        {REPEATRESULTS}
    '''
    contacts = SetName(text, 'vcard.vcf')
                .GetContactsFromInput()

    selectedItems = ChooseFrom(contacts, prompt="Select Recent Foods", selectMultiple=True)

    for chosen in selectedItems:
        if chosen.Notes == 'Cancel':
            return None

        file = GetFile(f"FLS/Recents/Foods/food_{chosen.Notes}.json")
        selectedFoods.append(Dictionary(file))
    
    return selectedFoods

#---------------------------------------------------------------------------------------------------------------------------------AddRecent

def AddRecent():
    # Text of shortcut input to unlink from file handler of food file
    # Without it, overwrites dont really work as it just passes the same file to the system
    food = Dictionary(Text(ShortcutInput))

    if food is None:
        return

    nutrDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))
    
    maxRecents = 30


    if food['id'] is not None:
        IFRESULT = food['id']
    else:
        IFRESULT = RunShorctut(nutrDix['GFID'])
    
    foodId = IFRESULT

    # add food to recent if it doesn't already exist
    # by saving it, it will be at top of list since sorted by modified after
    SaveFile(food, f"FLS/Recents/Foods/{fileName}.json", overwrite=True)

    dir_ = GetFile("FLS/Recents/Foods")
    files = GetContentsOfFolder(dir_)
    files = filter(files, sortBy='Last Modified Date', order='Latest First')

    if Count(files) > maxRecents:
        for _ in range(Count(files)-maxRecents):
            deletefile = files.getLastItem()
            DeleteFile(foodFile, deleteImmediately=True)

#---------------------------------------------------------------------------------------------------------------------------------DisplayFoodItem

def DisplayFoodItem():
    # params = Dictionary(ShortcutInput)
    # foodDix = params['food']

    # action = params['action']
    
    if ShortcutInput is not None:
        IFRESULT = foodDix
    else:
        # the default food dictionary
        IFRESULT = ... # the default food dictionary
    foodDix = Dictionary(IFRESULT)

    # if action == 'view':
    #     # Use menu prompt first
    #     outputFood = foodDix
    #     prompt = f'''
    #     {outputFood['Name']}
    #     Serving Size: ({outputFood['Serving Size']}) ⸱ Cals: {outputFood['Calories']}
    #     Carbs: {outputFood['Carbs']}g ⸱ Fat: {outputFood['Fat']}g ⸱ Protein: {outputFood['Protein']}g
    #     Sugar: {outputFood['Sugar']}g ⸱ Fiber: {outputFood['Fiber']}g 
    #     Monosaturated Fat: {outputFood['Monosaturated']}g ⸱ Polyunsaturated Fat: {outputFood['Polyunsaturated']}g
    #     Saturated Fat: {outputFood['Saturated']}g ⸱ Sodium: {outputFood['Sodium']}mg ⸱ Cholesterol: {outputFood['Cholesterol']}mg
    #     Potassium: {outputFood['Potassium']}mg ⸱ Calcium: {outputFood['Calcium']}mg ⸱ Iron: {outputFood['Iron']}mg
    #     VitA: {outputFood['VitA']}mcg ⸱ VitC: {outputFood['VitC']}mg
    #     '''
    #     Menu(prompt):
    #         case 'Done':
    #             searchExit = TRUE
    #             return outputFood
    #         case 'Edit Food':
    #             res = RunShorctut(NutriDix['Display Food Item'], input=outputFood)
    #             Menu('Save changes?')
    #                 case 'Yes':
    #                     searchExit = TRUE
    #                     outputFood = res
    #                 case 'No, use previous values':
    #                     searchExit = TRUE
    #                 case 'No, back to search':
    #                     pass
    #         case 'Back To Search':
    #             pass

    #         case 'Cancel Search':
    #             return None



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
                num = Number(displayDix[field])
                IFRESULT = RoundNumber(IFRESULT, hundredths)
            else:
                IFRESULT = displayDix[field]

            foodDix[key] = IFRESULT

#---------------------------------------------------------------------------------------------------------------------------------GenerateFoodId

def GenerateFoodId():
    file = GetFile("FLS/Other/nextFoodId.txt")
    if file is not None:
        IFRESULT = file
    else:
        IFRESULT = "0"
    
    _id = Number(IFRESULT)
    num = _id + 1
    SaveFile(num, "FLS/Other/nextFoodId.txt")
    return 

#---------------------------------------------------------------------------------------------------------------------------------LogAlgorithm

def LogAlgorithm(): # Log Algorithm
    '''
    Update to use new backlog system
    Update to use dictionary from input
    {
        'Date':..
        'Food':...
    }
    '''

    '''
    Changelist:
    - Removed contin
    '''

    TRUE = 1
    FALSE = 0

    nutrDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))

    res = Dictionary(Text(ShortcutInput))

    loggingDate = Date(res['Date'])
    foodDix = Dictionary(res['Food'])

    foodName = foodDix['Name']
    servingSize = foodDix['Serving Size']

    dixValue = foodDix['Servings']
    if res is None:
        IFRESULT = AskForInput(Input.Number, prompt=f"How many servings? (1 serving = {servingSize})",
                    default=1, allowDecimals=True, allowNegatives=True)
    else:
        IFRESULT = GetNumbers(dixValue)

    # set servings in food dictionary
    mulitplier = IFRESULT
    foodDix['Servings'] = multiplier
    servings = Number(foodDix['Servings'])


    # get health app environment var
    dix = Dictionary(GetFile("FLS/Other/env.json"))
    hasHelathApp = dix['HasHealthApp']

    # add to backlog and exit if we are not on a device with a health app
    if hasHealthApp == FALSE:
        Notification(
            "Food will be logged when next on iPhone",
            title=f'{foodName} Has Been Added to Backlog',
        )

        # get the backlog file 
        file = GetFile("FLS/Other/backlog.json", noErrors=True)

        if file is not None:
            IFRESULT = Dictionary(file)
        else:
            IFRESULT = { 'backlog': [] }

        backlog = IFRESULT['backlog']

        dix = {
            'Date': Text(loggingDate),
            'Food': Text(foodDix)
        }
        backlog.append(dix)

        # add it to list

        # save file
        dix = { 'backlog': backlog }
        SaveFile(dix, "FLS/Other/backlog.json", overwrite=True)

        return foodDix


    # comment set of nutrients logged by the system

    nutrients = Dictionary()

    file = GetFile('FLS/Other/nutriKeys.txt')
    # store the nutrients in the dictionary
    for item in SplitText(file, ByNewLines):
        num = Number(foodDix[item])
        foodDix[item] = RoundNumber(num, hundredths)
        if num > 0:
            num = num * servings
            num = Round(num, "hundredths")
            nutrients[item] = num

    # now just go through each nutrient and add them 
    if nutrients["Carbs"] is not None:
        LogHealthSample("Carbohydrates", nutrients[@aboveKey], "g", loggingDate)

    if nutrients["Fiber"] is not None:
        LogHealthSample("Fiber", nutrients[@aboveKey], "g", loggingDate)

    if nutrients["Sugar"] is not None:
        LogHealthSample("Dietary Sugar", nutrients[@aboveKey], "g", loggingDate)

    if nutrients["Fat"] is not None:
        LogHealthSample("Total Fat", nutrients[@aboveKey], "g", loggingDate)

    if nutrients["Polyunsaturated"] is not None:
        LogHealthSample("Polyunsaturated Fat", nutrients[@aboveKey], "g", loggingDate)

    if nutrients["Monounsaturated"] is not None:
        LogHealthSample("Monounsaturated Fat", nutrients[@aboveKey], "g", loggingDate)

    if nutrients["Saturated"] is not None:
        LogHealthSample("Saturated Fat", nutrients[@aboveKey], "g", loggingDate)

    if nutrients["Protein"] is not None:
        LogHealthSample("Protein", nutrients[@aboveKey], "g", loggingDate)

    if nutrients["Sodium"] is not None:
        LogHealthSample("Sodium", nutrients[@aboveKey], "mg", loggingDate)

    if nutrients["Potassium"] is not None:
        LogHealthSample("Potassium", nutrients[@aboveKey], "mg", loggingDate)

    if nutrients["Cholesterol"] is not None:
        LogHealthSample("Dietary Cholesterol", nutrients[@aboveKey], "mg", loggingDate)

    if nutrients["VitA"] is not None:
        LogHealthSample("Vitamin A", nutrients[@aboveKey], "mcg", loggingDate)

    if nutrients["VitC"] is not None:
        LogHealthSample("Vitamin C", nutrients[@aboveKey], "mg", loggingDate)

    if nutrients["Calcium"] is not None:
        LogHealthSample("Calcium", nutrients[@aboveKey], "mg", loggingDate)

    if nutrients["Iron"] is not None:
        LogHealthSample("Iron", nutrients[@aboveKey], "mg", loggingDate)

    if nutrients["Calories"] is not None:
        LogHealthSample("Dietary Energy", nutrients[@aboveKey], "kcal", loggingDate)

    Notification(
        f'{foodName} has been logged to your meals',
        title='Yummy!'
    )

    # make logging experience fast by logging to cache instead of bigger dictionary
    # cache is cleared in main nutrition function

    dateKey = loggingDate.format(date="short", time=None)
    timeKey = loggingDate.format(custom="HH:mm")
    cals = RoundNumber(nutrients['Calories'], ones)

    # check if cache file exists and make one by default if not available
    file = GetFile("FLS/History/foodHistoryCache.json", errorIfNotFound=False)
    if file is not None:
        IFRESULT = Text(file)
    else:
        IFRESULT = "{ 'cache': [] }"

    res = Dictionary(IFRESULT)
    cache = res['cache']

    # put the item in the cache
    dix = {
        'date' : dateKey,
        'time' :  timeKey,
        'food' : foodName,
        'servings': servings,
        'cals': cals
    }
    cache.append(dix)

    dix = {
        'cache' : cache
    }

    # save cache away for later
    SaveFile(dix, "FLS/History/foodHistoryCache.json", overwrite=True)


    # TODO in Main: Check and empty food history cache


    return foodDix

#---------------------------------------------------------------------------------------------------------------------------------SearchAlgorithm

def SearchAlgorithm():
    TRUE = 1
    FALSE = 0

    NutriDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))

    # vcard base64 photo icons
    servingSizeIcon = # ... , see servingSizeIcon.txt
    forwardIcon = # forwardIcon.txt
    backwardIcon = # backwardIcon.txt
    searchIcon = # searchIcon.txt
    cancelIcon = # cancelIcon.txt


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

                subtitle = f'''
                    {IFRESULT}\nCals: {item['nutritional_contents.energy.value']} ⸱ Carbs: {item['nutritional_contents.carbohydrates']}g ⸱ Fat: {item['nutritional_contents.fat']}g ⸱ Protein: {item['nutritional_contents.protein']}g
                '''
                
                text = f'''
                BEGIN:VCARD
                VERSION:3.0
                N;CHARSET=UTF-8:{item['description']}
                ORG;CHARSET=UTF-8:{subtitle}
                NOTE;CHARSET=UTF-8:{itemId}
                END:VCARD
                '''
                
                REPEATRESULTS.append(text)
            itemCards = REPEATRESULTS

            # we need to create the vcards for next and previous
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

            chosenItem = ChooseFrom(contacts, prompt=f'"{query}" Search Results | Page {pageNo}')
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
                return res

            if chosenItem.Notes == 'Cancel':
                isControlItem = TRUE
                return None
            
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
                            return None


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

    return outputFood

#---------------------------------------------------------------------------------------------------------------------------------FoodsList

def FoodsList(): # Foods List
    TRUE = 1
    FALSE = 0

    nutrDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))
    cancelIcon = #.. cancelIcon.txt
    
    foodsDix = {}

    # list ids
    selectedIds = []

    nextId = 0

    maxLoops = 30
    breakLoop = FALSE

    hasNotes = FALSE

    file = GetFile("FLS/Other/foodNotes.txt", errorIfNotFound=False)
    if file is not None:
        notes = f'''
            Food Notes:
            {file}

        '''
        notes = IFRESULT
        hasNotes = TRUE

    for _ in range(maxLoops):
        if breakLoop == FALSE:
            for listId in selectedIds:
                food = foodsDix[listId]
                REPEATRESULTS.append(f'{food['Servings']}x {food['Name']}')

            if REPEATRESULTS is not None:
                IFRESULT = f'''
                Current Selected Foods:
                {REPEATRESULTS}
                '''
            else:
                IFRESULT = f'''
                No foods selected
                '''
            if hasNotes == TRUE:
                IFRESULT2 = f'''
                    {notes}
                    {IFRESULT}
                '''
            else:
                IFRESULT2 = IFRESULT


            addMenuResult = TRUE

            Menu(IFRESULT2):
            case 'Done Selecting Foods':
                addMenuResult = FALSE
                for listId in selectedIds:
                    food = foodsDix[listId]
                    RunShortcut(nutrDix['Add Recent'], input=food)
                    REPEATRESULTS.append(food)
                
                return REPEATRESULTS

            case 'Search Food':
                MENURESULT = RunShortcut(nutrDix['Search Algorithm'])

            case 'Get Preset(s) Or Barcoded Food(s)':
                MENURESULT = RunShortcut(nutrDix['Select Saved Foods'], input={'type': 'all'})

            case 'Get Recent Meals':
                MENURESULT = RunShortcut(nutrDix['Get Recent'])

            case 'Scan Barcode':
                MENURESULT = RunShortcut(nutrDix['Barcode Search'], input={'getFood': True})

            case 'Make Food Manually':
                # TODO, make manual maker
                MENURESULT = RunShortcut(nutrDix['Make Food Manually'])

            case 'View/Edit Food':
                addMenuResult = FALSE
                # Remove selection
                for listId in selectedIds:
                    food = foodsDix[listId]
                    text = f'''
                        BEGIN:VCARD
                        VERSION:3.0
                        N;CHARSET=UTF-8:{food['Name']}
                        ORG;CHARSET=UTF-8:{food['Servings']} servings
                        NOTE;CHARSET=UTF-8:{listId}
                        END:VCARD
                    '''
                    REPEATRESULTS.append(text)

                text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=UTF-8:Cancel
                    ORG;CHARSET=UTF-8:No foods will be selected
                    NOTE;CHARSET=UTF-8:Cancel
                    {cancelIcon}
                    END:VCARD
                    {REPEATRESULTS}
                '''
                renamedItem = SetName(text, 'vcard.vcf')
                contacts = GetContacts(renamedItem)

                edit = ChooseFrom(contacts, prompt='Select Food To View')

                listId = Contact(edit.Notes)
                if listId != 'Cancel':
                    # get the food at the id
                    food = foodsDix[listId]
                    Menu('Select an action'):
                        case 'Edit Serving Size':
                            res = AskForInput(Input.Number, f'How many servings? (1 serving = {food['Serving Size']})', allowNegatives=False)
                            food['Servings'] = res
                            foodsDix[listId] = food

                        case 'View/Edit Other Fields':
                            changedFood = RunShortcut(nutrDix['Display Food Item'], input=food)
                            Menu(f'Save Changes to {changedFood['Name']}?'):
                                case 'Yes':
                                    # if we edit a food, it is now different from its source food so generate a new food ID for it
                                    changedFood['id'] = RunShortcut(nutrDix['GFID'])
                                    foodsDix[listId] = changedFood
                                case 'No':
                                    pass

            case 'Remove Selected Foods':
                addMenuResult = FALSE
                # Remove selection
                for listId in selectedIds:
                    food = foodsDix[listId]
                    text = f'''
                    BEGIN:VCARD
                    VERSION:3.0
                    N;CHARSET=UTF-8:{food['Name']}
                    ORG;CHARSET=UTF-8:{food['Servings']} servings
                    NOTE;CHARSET=UTF-8:{listId}
                    END:VCARD
                    '''
                    REPEATRESULTS.append(text)

                text = Text(REPEATRESULTS)
                renamedItem = SetName(text, 'vcard.vcf')
                contacts = GetContacts(renamedItem)

                deletes = ChooseFrom(contacts, selectMultiple=True, prompt='Select foods to remove')

                for delete in deletes:
                    listId = Contact(delete).Notes
                    # remove it from the list
                    selectedIds = filter(selectedIds, where=['Name' != listId])

            if addMenuResult == TRUE:
                # add the foods to our selected foods
                for food in MENURESULT:
                    # Ask for the servings
                    servings = AskForInput(Input.Number, f'How many servings of {food['Name']}? (1 serving = {food['Serving Size']})', allowDecimals=True, allowNegatives=False)
                    food['Servings'] = servings

                    # generate list Id for the item
                    foodsDix[nextId] = food
                    selectedIds.append(nextId)
                    nextId = nextId + 1

#---------------------------------------------------------------------------------------------------------------------------------clearCacheAndBacklog

def clearCacheAndBacklog():
    if ShortcutInput is not None:
        IFRESULT = ShortcutInput
    else
        IFRESULT = { 'cache': True, 'backlog': True }
    params = Dictionary(IFRESULT)

    TRUE = 1
    FALSE = 0

    res = GetFile("FLS/Other/shortcutNames.json")
    shortcutNames = Dictionary(res)

    hasHealthApp = FALSE
    matches = MatchText(GetDeviceDetails("Model"), "(iPhone)")
    if matches is not None:
        hasHealthApp = TRUE
    
    if params['backlog'] is not None:
        # clearing the backlog
        if hasHealthApp == TRUE:
            file = GetFile("FLS/Other/backlog.json", errorIfNotFound=False)
            if file is not None:
                # clear items by logging them
                dix = Dictionary(file)
                for item in dix['backlog']:
                    RunShortcut(shortcutNames["Log Algorithm"], input=item)

                # erase the backlog
                file = GetFile("FLS/Other/backlog.json")
                DeleteFile(file, deleteImmediately=True)

            else:
                if reqBacklogClear == TRUE:
                    # if user req clear backlog let them no there was nothing to clear
                    ShowAlert("There are no foods in the backlog")

    if params['cache'] is not None:
        # clear the cache
        file = GetFile("FLS/History/foodHistoryCache.json", errorIfNotFound=False)
        if file is not None:
            dix = Dictionary(file)
            histCache = dix['cache']
            
            file = OpenFile("FLS/History/foodHistory.json", errorIfNotFound=False)
            if file is not None:
                IFRESULT = file
            else:
                IFRESULT = {}
            history = Dictionary( IFRESULT )

            for item in histCache:
                dayKey = item['date']
                timeKey = item['time']

                dayDix = history[dayKey]
                if history[dayKey] is None:
                    IFRESULT = history[dayKey]
                else
                    IFRESULT = {}
                dayDix = IFRESULT

                timeList = dayDix[timeKey]

                timeList.append({
                        'food': item['food'],
                        'servings': item['servings'],
                        'cals': item['cals']
                    })

                dayDix[timeKey] = timeList
                history[dayKey] = dayDix

            # save our history
            SaveFile(history, "FLS/History/foodHistory.json", overwrite=True)

            # clear our cache by deleting the file
            file = GetFile("FLS/History/foodHistoryCache.json")
            DeleteFile(file, deleteImmediately=True)


#---------------------------------------------------------------------------------------------------------------------------------SavedAndSearch

def SavedAndSearch():
    TRUE = 1
    FALSE = 0

    res = GetFile("FLS/Other/shortcutNames.json")
    shortcutNames = Dictionary(res)
    Menu("Saved And Search"):
        case "Search and View":
            # run shortcutNames[search algorithm ]and display food with 

            res = RunShortcut(shortcutNames["Display Food Item"], input=RunShortcut(shortcutNames["Search Algorithm"]))
            for item in res:
                searchResult = res
                postSearchMenu = Menu(["Log Entry", "Make Preset", "Exit"])

                if postSearchMenu.opt("Log Entry"):
                    date = AskForInput("Date:", Input.DateAndTime, default=Date.CurrentDate)

                    dix = {
                        'Date': str(date)
                        'Food': dix(searchResult)
                    }
                    res = RunShortcut(shortcutNames[
                        "Log Algorithm"],
                        input=dix)

                    LoggedFoods2 = res

                    svp = Menu(["Yes", "No"], prompt="Save As Preset?")

                    if svp.opt("Yes"):
                        RunShorctut("Make Preset", input=LoggedFoods2)
                    if svp.opt("No"):
                        pass

                elif postSearchMenu.opt("Make Preset"):
                    RunShortcut(shortcutNames["Make Preset"], input=searchResult)

                elif postSearchMenu.opt("Exit"):
                    pass

        case "Presets":
            prm = Menu(prompt="Presets", options=["View Presets", "Make Preset", "Edit Preset", "Remove Preset(s)"])

            if prm.opt("View Presets"):
                deletePresetCache = FALSE
                res = RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'presets'})
                for repeatItem in res:
                    changedFood = Dictionary(RunShortcut(shortcutNames["Display Food Item"], input=repeatItem))
                    Menu(f'Save Changes to {changedFood['Name']}?'):
                        case 'Yes':
                            SaveFile(changedFood, f"FLS/Presets/Foods/food_{changedFood['id']}.json", overwrite=True)
                            deletePresetCache = TRUE
                        case 'No':
                            pass

                    if deletePresetCache == TRUE:
                        file = GetFile('FLS/Presets/vcardCache.txt', errorIfNotFound=False)
                        DeleteFile(file, deleteImmediately=True)


            elif prm.opt("Make Preset"):
                # run shortcutNames[foods list ]to get list of foods to be made into a preset
                RunShortcut(shortcutNames["Make Preset"])

            elif prm.opt("Edit Preset"):
                RunShortcut(shortcutNames["Edit Saved Food"], input={'type': 'presets'})

            elif prm.opt("Remove Preset(s)"):
                RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'presets', 'deleteMode': True})

        case "Barcodes":
            brm = Menu(prompt="Barcodes", options=[
                "View Personal Database",
                "Add to Personal Database",
                "Edit Items in Personal Database",
                "Remove From Personal Database"
                ])


            if brm.opt("View Personal Database"):
                deletePresetCache = FALSE
                res = RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'barcodes'})
                for repeatItem in res:
                    changedFood = Dictionary(RunShortcut(shortcutNames["Display Food Item"], input=repeatItem))
                    Menu(f'Save Changes to {changedFood['Name']}?'):
                        case 'Yes':
                            SaveFile(changedFood, f"FLS/Barcodes/Foods/food_{changedFood['id']}.json", overwrite=True)
                            deletePresetCache = TRUE
                        case 'No':
                            pass

                    if deletePresetCache == TRUE:
                        file = GetFile('FLS/Barcodes/vcardCache.txt', errorIfNotFound=False)
                        DeleteFile(file, deleteImmediately=True)
            elif brm.opt("Add to Personal Database"):
                RunShortcut(shortcutNames["Barcode Search"])

            elif brm.opt("Edit Items in Personal Database"):
                RunShortcut(shortcutNames["Edit Saved Food"], input={'type': 'barcodes'})

            elif brm.opt("Remove From Personal Database"):
                RunShortcut(shortcutNames["Select Saved Foods"], input={'type': 'barcodes', 'deleteMode': True})
        
        case "Recent Meals":
            res = RunShortcut(shortcutNames["Get Recent"])
            for item in res:
                RunShortcut(shortcutNames["Display Food Item"], input=item)

#---------------------------------------------------------------------------------------------------------------------------------LogFoodsAtTime

def LogFoodsAtTime():
    TRUE = 1
    FALSE = 0
    res = GetFile("FLS/Other/shortcutNames.json")
    shortcutNames = Dictionary(res)

    Dating = AskForInput("What date and time? Click Done for Right Now", Input.DateAndTime)

    for item in RunShortcut(shortcutNames["Foods List"]):
        CurFood = item
        dix = {
            'Date': str(Dating)
            'Food': dix(CurFood)
        }

        res = RunShortcut(shortcutNames["Log Algorithm"], input=dix)
        REPEATRESULTS.append(res)

    loggedFoods = REPEATRESULTS

    file = GetFile("FLS/Other/foodNotes.txt", errorIfNotFound=False)
    if file is not None:
        Menu('Clear food notes?'):
            case 'Yes':
                DeleteFile(file, deleteImmediately=True)
            case 'No':
                pass

    makePreset = TRUE

    if Count(loggedFoods) == 1:
        file = GetFile(f"FLS/Presets/Foods/food_{loggedFoods['id']}.json")
        if file is not None:
            makePreset = FALSE

    if makePreset == TRUE:
        Menu("Make Preset?")
            case "Yes":
                RunShortcut(shortcutNames["Make Preset"], input=REPEATRESULTS)
            
            case "No":
                pass

#---------------------------------------------------------------------------------------------------------------------------------LogFoodsAtDifferentTimes

def LogFoodsAtDifferentTimes(): # Log Foods At Different Times
    nutrDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))
    selectedFoods = RunShortcut(nutrDix['Foods List'])

    nextId = 0
    foodsDix = {}
    selectedIds = []

    hasNotes = FALSE

    file = GetFile("FLS/Other/foodNotes.txt", errorIfNotFound=False)
    if file is not None:
        notes = f'''
            Food Notes:
            {file}

        '''
        notes = IFRESULT
        hasNotes = TRUE


    for food in selectedFoods:
        # generate list Id for the item
        foodsDix[nextId] = food
        selectedIds.append(nextId)
        nextId = nextId + 1

    for _ in range(Count(selectedFoods)):
        if Count(selectedIds) > 0:
            for listId in selectedIds
                food = foodsDix[listId]
                text = f'''
                BEGIN:VCARD
                VERSION:3.0
                N;CHARSET=UTF-8:{food['Name']}
                ORG;CHARSET=UTF-8:{food['Servings']} servings
                NOTE;CHARSET=UTF-8:{listId}
                END:VCARD
                '''
                REPEATRESULTS.append(text)

        # max repeat will be at most items
        contacts = textToContacts(REPEATRESULTS)

        if hasNotes == TRUE:
            IFRESULT = f'''
            {notes}

            Select foods to log for time...
            '''
        else:
            IFRESULT = 'Select foods to log for time...'

        chosen = ChooseFrom(contacts, prompt=IFRESULT, selectMultiple=True)
        
        date = AskForInput(Input.DateAndTime, "What time should the selected foods be logged at?")

        for item in chosen:
            # remove from the list
            listId = Contact(item).Notes
            selectedIds = filter(selectedIds, where=['Name' == listId])
            food = foodsDix[listId]
            text = {
                'Date': date.format(date="medium", time="short"),
                'Food': food
            }
            res = RunShortcut('Log Algorithm', input=text)
            loggedFoods.append(res)

        if hasNotes == TRUE:
            Menu('Clear food notes?'):
                case 'Yes':
                    file = GetFile("FLS/Other/foodNotes.txt")
                    DeleteFile(file, deleteImmediately=True)
                case 'No':
                    pass
        
        Menu('Make Preset?'):
            case 'Yes':
                RunShortcut(nutrDix['Make Preset'], input=loggedFoods)
            case 'No':
                pass


# --------------------------------------------------------------------------------------------------------------------------------Nutrition

def Nutrition():
    TRUE = 1
    FALSE = 0
    checkForUpdates = FALSE
    exitAfterQuickLog = TRUE

    # load names of the shortcuts
    res = GetFile("FLS/Other/shortcutNames.json")
    shortcutNames = Dictionary(res)

    text = '''
      Calories
        Carbs
        Fat
        Protein
        Sugar
        Fiber
        Monounsaturated
        Polyunsaturated
        Saturated
        Trans
        Sodium
        Cholesterol
        Potassium
        VitA
        VitC
        Calcium
        Iron
    '''
    SaveFile(text, "FLS/Other/nutriKeys.txt")

    # if device does not have health app then we will be adding to backlog
    # using regex matching
    hasHealthApp = FALSE
    matches = MatchText(GetDeviceDetails("Model"), "(iPhone)")
    if matches is not None:
        hasHealthApp = TRUE

    # save the state of the health app to environment
    file = GetFile("FLS/Other/env.json", errorIfNotFound=False)
    dix = Dictionary(file)
    dix['hasHealthAapp'] = hasHealthApp
    SaveFile(dix, "FLS/Other/env.json", overwrite=True)


    # itemsInHistCache = FALSE
    # file = GetFile("FLS/History/foodHistoryCache.json", errorIfNotFound=False)
    # if file is not None:
    #     itemsInHistCache = TRUE
    #     dix = Dictionary(file)
    #     if Count(dix['cache']) >= 15:
    #         # we need to eventually clear the history cache so that it does not bloat in size
    #         exitAfterQuickLog = FALSE


    # determine if we are checking for updates
    file = GetFile("FLS/Other/lastUpdateCheck.txt", errorIfNotFound=False)
    if file is not None:
        IFRESULT = file
    else:
        IFRESULT = SubFromDate(CurrentDate(), weeks=1)

    if TimeBetweenDates(IFRESULT, CurrentDate()) >= 1:
        checkForUpdates = TRUE


    if hasHealthApp == FALSE:
        text = f"Foods logged on {deviceModel} will be added to backlog"

    else:
        calsToday = 0
        healthSamples = HealthApp.Find(
                AllHealthSamples,
                whereAllAreTrue=[
                    Type="Dietary Energy",
                    StartDate=Today,
                ],
                Unit=cal
            )
        _sum = CalculateStatistics(healthSamples, "Sum")
        calsToday = Round (_sum, "hundredths")

        file = GetFile("FLS/Other/backlog.json", errorIfNotFound=False)
        if file is not None:
            IFRESULT = f"You've eaten {calsToday} calories today.\nThere are foods in your backlog."
        else:
            IFRESULT = f"You've eaten {calsToday} calories today."

        IFRESULT = IFRESULT

    prompt = IFRESULT

    file = GetFile('FLS/Other/foodNotes.txt', errorIfNotFound=False)
    if file is not None:
        prompt = f'''
        {prompt}
        Food Notes:
        {file}
        '''

    Menu(prompt):
        case "Quick Log":
            # InRecents does not exist!

            for item in  RunShortcut(shortcutNames['Get Recent']):
                CurFood = item

                RunShortcut(shortcutNames["Add Recent"], input=dix)

                text = f"How many servings of {CurFood['Name']}\n(1 serving = {CurFood['Serving Size']})"
                
                # translates to set dictionary value in CurFood and then set dictionary
                CurFood['Servings'] = AskForInput(text, Input.Number, default=1, allowDecimalNumbers=True, allowNegativeNumbers=False)

                dix = {
                    'Date': str(Date.CurrentDate)
                    'Food': dix(CurFood)
                }
                RunShortcut(shortcutNames["Log Algorithm"], input=dix)

            if exitAfterQuickLog == TRUE:
                return

        case "Log Foods At Time...":
            RunShortcut(shortcutNames["Log Foods At Time"])
        case "Log Foods At Different Times":
            RunShortcut(shortcutNames["Log Foods At Different Times"])

        case "Make Food Note":
            res = AskForInput(Input.Text, "What is the name of the food you would like to note down?", allowMultipleLines=False)
            text = f'{res} @ {CurrentDate.format(date="medium", time="short")}'
            AppendToFile(text, "FLS/Other/foodNotes.txt", makeNewLine=True)
            return

        case 'Saved Foods and Search':
            RunShortcut(shortcutNames["Saved And Search"])

        case 'History and Stats':
            case "Statistics with Charty":
                RunShortcut(shortcutNames["Health Statistics"])

            case "Food History":
                RunShortcut(shortcutNames["Clear Cache And Backlog"])

                file = GetFile("FLS/Other/backlog.json", errorIfNotFound=False)
                if file is not None
                    ShowAlert("There are items in the backlog, food history will not be accurate until backlog is cleared", showCancel=True)
                
                RunShortcut(shortcutNames["Food History"])

        case 'Clear... and more':
            case "Clear Backlog":
                Notification('Clearing backlog....')
                RunShortcut(shortcutNames["Clear Cache And Backlog"])

            case "Clear Food Notes":
                file = GetFile("FLS/Other/foodNotes.txt", errorIfNotFound=False)
                DeleteFile(file, deleteImmediately=True)

    RunShortcut(shortcutNames['Clear Cache and Backlog'])

    if checkForUpdates == TRUE:
        RunShortcut(shortcutNames["NutriDix Updater"])
        SaveFile(Text(CurrentDate.format(date="short", time=None)), "FLS/Other/lastUpdateCheck.txt", overwrite=True)

#---------------------------------------------------------------------------------------------------------------------------------

def LogAlgorithmTestBench():

    TRUE = 1
    FALSE = 0

    nutrDix = Dictionary(GetFile("FLS/Other/shortcutNames.json"))

    # clear cache before test
    RunShortcut(nutrDix['Clear Cache and Backlog'])

    startDate = AskForInput(Input.DateAndTime, prompt="Start Date")
    emptyFood = { ... } # default food dictionary

    nutrUnits = Dictionary({
        "Calories": "kcal",
        "Carbs": "g",
        "Fat": "g",
        "Protein": "g",
        "Sugar": "g",
        "Fiber": "g",
        "Monounsaturated": "g",
        "Polyunsaturated": "g",
        "Saturated": "g",
        "Sodium": "mg",
        "Cholesterol": "mg",
        "Potassium": "mg",
        "VitA": "mcg",
        "VitC": "mg",
        "Calcium": "mg",
        "Iron": "mg"
    })

    nutrSample = Dictionary({
        "Calories": "Dietary Energy",
        "Carbs": "carbohydrates",
        "Fat": "Total Fat",
        "Protein": "Protein",
        "Sugar": "Dietary Sugar",
        "Fiber": "Fiber",
        "Monounsaturated": "Monounsaturated Fat",
        "Polyunsaturated": "Polyunsaturated Fat",
        "Saturated": "Saturated Fat",
        "Sodium": "Sodium",
        "Cholesterol": "Dietary Cholesterol",
        "Potassium": "Potassium",
        "VitA": "Vitamin A",
        "VitC": "Vitamin C",
        "Calcium": "Calcium",
        "Iron": "Iron"
    })

    # test that each nutrient is logged correctly
    file = GetFile('FLS/Other/nutriKeys.txt')
    nutrients = SplitText(file, '\n')
    for i in (1,2):
        servings = i;
        for item in nutrients:
            nutr = item
            # create food where that nutrient value is set to 0.1, with 1 serving
            logValue = 0.1
            servings = 1
            checkValue = logValue * servings
            
            testFood = emptyFood
            testFood['Name'] = f'{nutr} Food Test' 
            testFood['Servings'] = servings
            testFood[nutr] = logValue

            # pass through log algorithm with the given date
            outputFood = RunShortcut(nutrDix["Log Algorithm"], input={'Date': startDate, 'Food': testFood})

            # check the log test
            # get health samples from that day in the appropriate unit and compare them
            logTestPassed = FALSE
            sampleType = nutrSample[nutr]
            sampleUnits = nutrUnits[nutr]
            sample = FindHealthSamples(    type=sampleType, 
                                            startDateIsOn=startDate,
                                            unit=sampleUnits,
                                            sortby="Start Date",
                                            order="Latest First",
                                            limit=1
                                        )
            if sample is not None:
                if GetHealthSampleDetails(sample, "Start Date") == startDate:
                    if GetHealthSampleDetails(sample, "Value") == checkValue:
                        logTestPassed = TRUE


            # check to make sure the output food is correct
            outputPassed = TRUE
            for item in nutrients:
                op = RoundNumber(outputFood[item], hundredths)
                ref = RoundNumber(testFood[item], hundredths)
                if op != ref:
                    outputPassed = FALSE

            # check to make sure output food is logged to cache as expected
            cacheTestPassed = FALSE
            dix = Dictionary( Text( GetFile("FLS/History/foodHistoryCache.json") ))
            cache = dix['cache']
            if cache is not None:
                cacheTestPassed = TRUE
                entry = Dictionary(cache.getLastItem())
                refEntry = {
                    'date' : startDate.format(date="short", time=None),
                    'time' :  startDate.format(custom="HH:mm"),
                    'food' : f'{nutr} Food Test' ,
                    'servings': servings,
                }
                for item in ref.keys:
                    if entry[item] != refEntry[item]:
                        cacheTestPassed = FALSE

            # log our results

            if logTestPassed == TRUE:
                IFRESULT = f'Health Sample Log Test - {servings}x - {nutr} - PASS'
            else:
                IFRESULT = f'Health Sample Log Test - {servings}x - {nutr} - FAIL'
            results.append(IFRESULT)

            if outputPassed == TRUE:
                IFRESULT = f'Output Food Test - {servings}x - {nutr} - PASS'
            else:
                IFRESULT = f'Output Food Test - {servings}x - {nutr} - FAIL'
            results.append(IFRESULT)

            if cacheTestPassed == TRUE:
                IFRESULT = f'Cache Test - {servings}x - {nutr} - PASS'
            else:
                IFRESULT = f'Cache Test - {servings}x - {nutr} - FAIL'
            results.append(IFRESULT)

    # at the end of the test, delete cache and save results

