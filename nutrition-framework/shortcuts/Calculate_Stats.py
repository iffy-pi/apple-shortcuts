'''
Framework: Nutrition (id = 4)
ID:  24
Ver: 1.0
'''

# Generate graph data for charty nutrient plots

TRUE = 1
FALSE = 0

emptyList = []

# averageBreakdown = FALSE
# plotNutrients = TRUE

params = Dictionary(ShortcutInput)

# whether we are calculating the average breakdown
averageBreakdown = params['averageBreakdown']
# whether we are generating pie charts for nutrients
plotNutrients = params['plotNutrients']

# start and end date ranges for calculation, as well as the number of days between (repeats)
start = Date(params['start'])
end = Date(params['end'])
repeats = Number(params['repeats'])

# we have the base code to create a pie chart for a given day

# maps keys in our food object to the name of the health sampe to pull
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

# maps each nutrient key to their units
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
    "Sodium": "mg",
    "Cholesterol": "mg",
    "Potassium": "mg",
    "VitA": "mg",
    "VitC": "mg",
    "Calcium": "mg",
    "Iron": "mg"
}

# maps each nutrient key to a unique color in the generated pie chars
labelColorMap = {
    "Carbs": "FF375F",
    "Fat": "FFD60A",
    "Protein": "32C457",
    "Sugar": "64D2FE",
    "Fiber": "633D01",
    "Monounsaturated": "EC7063",
    "Polyunsaturated": "B8584D",
    "Saturated": "F5B7B1",
    "Sodium": "FFFFFF",
    "Cholesterol": "F2EE89",
    "Potassium": "DB64FE",
    "VitA": "FF0000",
    "VitC": "F98B06",
    "Calcium": "B9B6B2",
    "Iron": "484746"
}

if plotNutrients == TRUE:
    # if we are plotting nutrients then we have to retrieve health sample for the nutrient keys
    # we separate them into two datasets, one for the big nutrients (measured in g) and small nutrienets (Mineral Breakdown), measured in mg
    text = """
        {
            "ds": [
                {
                    "id": 0,
                    "title": "Breakdown",
                    "avgTitle": "Average",
                    "keys": [
                        "Calories",
                        "Carbs",
                        "Fat",
                        "Protein",
                        "Sugar",
                        "Fiber",
                        "Monounsaturated",
                        "Polyunsaturated",
                        "Saturated"
                    ]
                },

                {
                    "id": 1,
                    "title": "Minerals Breakdown",
                    "avgTitle": "Minerals Average",
                    "keys": [
                        "Sodium",
                        "Cholesterol",
                        "Potassium",
                        "VitA",
                        "VitC",
                        "Calcium",
                        "Iron"
                    ]
                },
            ]
        }
    """
else:
    # if we are not plotting nutrients we dont have to query the other nutrients
    # so our dataset query keys are limited only to Calories and no keys at all for minerals breakdown
    text = """
        {
            "ds": [
                {
                    "id": 0,
                    "title": "Breakdown",
                    "avgTitle": "Average",
                    "keys": [
                        "Calories"
                    ]
                },

                {
                    "id": 1,
                    "title": "Minerals Breakdown",
                    "avgTitle": "Minerals Average",
                    "keys": []
                },
            ]
        }
    """
dix = Dictionary(IFRESULT)
datasets = dix['ds']

# the total nutridixes for each of the datasets
# for example, totalDixes['0'] is a dictionary that maps each nutrient to the sum value they have in the date range
    # e.g totalDixes['0']['Carbs'] will be the total carb intake across the requested date range
totalDixes = {
    '0': {},
    '1': {}
}

# we go through every date we are calculating for
for repeatIndex in range(repeats):

    curDate = AddToDate(start, days=repeatIndex-1)

    for item in datasets:
        curSet = Dictionary(item)
        totalNutrDix = totalDixes[ curSet['id'] ]
        labels = emptyList
        values = emptyList
        labelColors = emptyList

        for curNutrKey in curSet['keys']:
            # for each nutrient key, get the health samples logged on that day
            sampleType = keyToSample[curNutrKey]
            unit = nutrUnits[curNutrKey]
            results = FindHealthSamples(type=sampleType, startDateIsOn=curDate, unit=unit)
            
            # sum health samples tot tal
            num = Number( CalculateStatistics("Sum", results.Value))
            daySum = RoundNumber(num, hundredths)

            if curNutrKey == 'Calories':
                # add it to the calorie plots, which are tracked separately
                calorieLabels.append(curDate)
                calorieValues.append(daySum)
            else:
                # add it to the pie chart series for that day
                values.append(daySum)

                # add to the total values for this nutrient
                totalNutrDix[curNutrKey] = Number(totalNutrDix[curNutrKey]) + daySum

        # save the total nutri dix
        totalDixes[curSet['id']] = totalNutrDix

        # calculate the total sum of values for this dataset
        # which is used to calculate the percentage for pie chart legeng
        dayTotal = CalculateStatistics("Sum", values)

        for curNutrKey, index in filter(curSet['keys'], where='Name' != 'Calories'):
            # for each nutrient, calculate its pie chart percentage and use it as the label for the nutrient
            # we filter calories because it is calculated separately

            # we can use the index to get the appropriate nutrient because values also omits the value for calories
            # and curSet[keys] is a list with a defined order
            item = values.getItemAtIndex(index)
            num = (item / dayTotal) * 100
            num = RoundNumber(num, hundredths)
            labels.append(f'{curNutrKey} ({num}%)')
            
            # get the label color for the nutrient
            labelColors.append(labelColorMap[curNutrKey])

        if plotNutrients == TRUE:
            nutrPlots.append({
                'title': f'{curDate.format(date="long")} {curSet['title']}',
                'labels': labels,
                'values': values,
                'labelColors': labelColors
                })

if averageBreakdown == TRUE:
    # we are generating data for the average across the date range not for each date range
    for item in datasets:
        curSet = Dictionary(item)
        totalNutrDix = totalDixes[ curSet['id'] ]
        averageLabels = emptyList
        averageValues = emptyList
        averageColors = emptyList

        nutrTotal = CalculateStatistics("Sum", totalNutrDix.values())
        
        for curNutrKey in filter(curSet['keys'], where='Name' != 'Calories'):
            # divide each nutrient total by the number of dates we sampled 

            # calculates the percentage of the current nutrient in the sample range
            # will be same percentage for averaged nutrient value since average divides by constant number
            curPercent = RoundNumber((totalNutrDix[curNutrKey] / nutrTotal) * 100, hundredths)

            # Calculate the average nutrient value for the plot, by dividing the total nutrient by the number of dates sampled
            averageNutr = totalNutrDix[curNutrKey] / repeats

            averageValues.append(averageNutr)
            averageLabels.append(f'{curNutrKey} ({curPercent}%)')

            # appends the appropriate color for th esystem
            averageColors.append(labelColorMap[curNutrKey])

        REPEATRESULTS.append({
            'title': f'{start.format(custom="MMM dd")} - {end.format(custom="MMM dd")} {curSet['avgTitle']}',
            'labels': averageLabels,
            'values': averageValues,
            'labelColors': averageColors
        })

    IFRESULT = REPEATRESULTS

else:
    # return generated nutrPlots above
    IFRESULT = nutrPlots

chartyPiePlots = IFRESULT

# we return the calorie labels and calorie values along with information to make each plot in charty
res = {}
res['calorieLabels'] = calorieLabels
res['calorieValues'] = calorieValues
if plotNutrients == TRUE:
    res['chartyPiePlots'] = chartyPiePlots

StopShortcut(output = res)

