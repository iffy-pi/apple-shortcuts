TRUE = 1
FALSE = 0

nutrDix = Dictionary(GetFile(f"{storage}/Other/shortcutNames.json"))

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
        dix = Dictionary( Text( GetFile(f"{storage}/History/foodHistoryCache.json") ))
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

