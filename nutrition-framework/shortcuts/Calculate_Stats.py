'''
Framework: Nutrition (id = 4)
ID:  24
Ver: 1.0
'''

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
    "Sodium": "mg",
    "Cholesterol": "mg",
    "Potassium": "mg",
    "VitA": "mg",
    "VitC": "mg",
    "Calcium": "mg",
    "Iron": "mg"
}

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
totalDixes = {
    '0': {},
    '1': {}
}

for repeatIndex in range(repeats):

    curDate = AddToDate(start, days=repeatIndex-1)

    for item in datasets:
        curSet = Dictionary(item)
        totalNutrDix = totalDixes[ curSet['id'] ]
        labels = emptyList
        values = emptyList
        labelColors = emptyList

        for curNutrKey in curSet['keys']:
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

        # save the total nutri dix
        totalDixes[curSet['id']] = totalNutrDix

        dayTotal = CalculateStatistics("Sum", values)

        for curNutrKey, index in filter(curSet['keys'], where='Name' != 'Calories'):
            item = values.getItemAtIndex(index)
            num = (item / dayTotal) * 100
            num = RoundNumber(num, hundredths)
            labels.append(f'{curNutrKey} ({num}%)')
            labelColors.append(labelColorMap[curNutrKey])

        if plotNutrients == TRUE:
            nutrPlots.append({
                'title': f'{curDate.format(date="long")} {curSet['title']}',
                'labels': labels,
                'values': values,
                'labelColors': labelColors
                })

if averageBreakdown == TRUE:
    for item in datasets:
        curSet = Dictionary(item)
        totalNutrDix = totalDixes[ curSet['id'] ]
        averageLabels = emptyList
        averageValues = emptyList
        averageColors = emptyList

        nutrTotal = CalculateStatistics("Sum", totalNutrDix.values())
        
        for curNutrKey in filter(curSet['keys'], where='Name' != 'Calories'):
            # divide each nutrient total by the number of dates we samples 

            # calculates the percentage of the current nutrient in the sample range
            # it will be the same as when average since average divides by constant factor
            curPercent = RoundNumber((totalNutrDix[curNutrKey] / nutrTotal) * 100, hundredths)

            # Calculate the average nutrient value for the plot
            averageNutr = totalNutrDix[curNutrKey] / repeats

            averageValues.append(averageNutr)
            averageLabels.append(f'{curNutrKey} ({curPercent}%)')

            averageColors.append(labelColorMap[curNutrKey])

        REPEATRESULTS.append({
            'title': f'{start.format(custom="MMM dd")} - {end.format(custom="MMM dd")} {curSet['avgTitle']}',
            'labels': averageLabels,
            'values': averageValues,
            'labelColors': averageColors
        })

    IFRESULT = REPEATRESULTS

else:
    IFRESULT = nutrPlots

chartyPiePlots = IFRESULT

res = {}
res['calorieLabels'] = calorieLabels
res['calorieValues'] = calorieValues
if plotNutrients == TRUE:
    res['chartyPiePlots'] = chartyPiePlots

StopShortcut(output = res)

