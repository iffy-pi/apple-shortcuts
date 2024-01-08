'''
Framework: Nutrition (id = 4)
ID:  23
Ver: 1.02
'''

# Calculate statsistics for nutrients

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))

getDateRange = TRUE
makeCaloriePlot = FALSE
averageBreakdown = FALSE
plotNutrients = TRUE


Menu("Statistics"):
    case Strings['stats.menu.breakdown.ondate']:
        getDateRange = FALSE

    case Strings['stats.menu.breakdown.between']:
        pass
    
    case Strings['stats.menu.breakdown.average']:
        # where we just plot an average breakdown
        averageBreakdown = TRUE

    case Strings['stats.menu.cals.breakdown']:
        makeCaloriePlot = TRUE
        plotNutrients = FALSE

start = AskForInput(Input.Date, prompt=Strings['stats.select.start'])

if getDateRange == TRUE:
    IFRESULT = AskForInput(Input.Date, prompt=trings['stats.select.end'], default=start)
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
        seriesLabel = Charty.AddSeries(Strings['stats.graph.nutr'], chartId, 'Pie', values=plot['values'], labels=plot['labels'])
        Charty.StylePieSeries(seriesLabel, chartId, colors=plot['labelColors'], labels=plot['labels'])


if makeCaloriePlot == TRUE:
    averageCals = CalculateStatistics("Average", stats['calorieValues'])
    for _ in range(repeats):
        averageCalValues.append(averageCals)

    # create the chart
    updatedText = Strings['stats.graph.cals.title'].replace('$start', start.format(custom="MMM dd"))
    updatedText = updatedText.replace('$end', end.format(custom="MMM dd"))
    chartId = Charty.NewChart(updatedText)
    Charty.AddSeries(Strings['stats.graph.cals.daily'], chartId, 'Line', xValues=stats['calorieLabels'], yValues=stats['calorieValues'])
    Charty.AddSeries(Strings['stats.graph.cals.avg'], chartId, 'Line', xValues=stats['calorieLabels'], yValues=averageCalValues)
    Charty.StyleAxis("X Axis", chartId, title=Strings['stats.graph.dates'], formatValuesAs='Date', options={'custom': 'd'})

OpenApp("Charty")

