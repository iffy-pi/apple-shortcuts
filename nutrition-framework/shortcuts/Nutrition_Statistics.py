'''
Framework: Nutrition (id = 4)
ID:  23
Ver: 1.0
'''

# Calculate statsistics for nutrients

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))

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

# We make the calorie breakdown graph if there is more than one day in our sample range
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
    Charty.StyleAxis("X Axis", chartId, title="Dates", formatValuesAs='Date', options={'custom': 'd'})

OpenApp("Charty")

