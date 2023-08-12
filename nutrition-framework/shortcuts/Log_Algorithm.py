'''
Framework: Nutrition (id = 4)
ID:  7
Ver: 1.0
'''

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

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))

nutrDix = Dictionary(GetFile(f"{storage}/Other/shortcutNames.json"))

setPerms = FALSE

if ShortcutInput['setPerms'] is not None:
    Alert("To enable permissions, just click 'Always Allow' when prompted", showCancel=False, Title="Permissions")
    setPerms = TRUE
    IFRESULT = {
        'Food': { 'Servings': 1 },
        'Date': CurrentDate()
    }
else:
    IFRESULT = f'{ShortcutInput}'

res = Dictionary(IFRESULT)

loggingDate = Date(res['Date'])
foodDix = Dictionary(res['Food'])

# set servings in food dictionary
servings = Number(foodDix['Servings'])

# get health app environment var
dix = Dictionary(GetFile(f"{storage}/Other/env.json"))
hasHelathApp = dix['hasHealthApp']

# add to backlog and exit if we are not on a device with a health app
if hasHealthApp == FALSE:
    if setPerms == TRUE:
        Alert("You must be on a device with Apple Health to run through permissions", Title="Permissions")
        StopShortcut()

    Notification(
        "Food will be logged when next on iPhone",
        title=f'{foodDix['Name']} Has Been Added to Backlog',
    )

    # get the backlog file 
    file = GetFile(f"{storage}/Other/backlog.json", noErrors=True)

    if file is not None:
        IFRESULT = Dictionary(file)
    else:
        IFRESULT = { 'backlog': [] }

    backlog = IFRESULT['backlog']

    # add it to the backlog
    dix = {
        'Date': Text(loggingDate),
        'Food': Text(foodDix)
    }
    backlog.append(dix)

    # save file
    dix = { 'backlog': backlog }
    SaveFile(dix, f"{storage}/Other/backlog.json", overwrite=True)

    StopShortcut(output = foodDix)

# nutrients will be the dictionary of nutrients that have values above our threshold
# used below when logging the system
nutrients = Dictionary()

# Normally we skip any nutrient values that are 0, but for setting permissions we want to log 0 values, so set threshold to -1
if setPerms == TRUE:
    IFRESULT = -1
else:
    IFRESULT = 0
threshold = IFRESULT

file = GetFile('FLS/Other/nutriKeys.txt')
# store the nutrients in the dictionary
for item in SplitText(file, ByNewLines):
    num = Number(foodDix[item])
    foodDix[item] = RoundNumber(num, hundredths)
    if num > threshold:
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

if setPerms == TRUE:
    Alert("All nutrient permissions have been set!", showCancel=False, Title="Permissions")
    StopShortcut()

Notification(
    f'{foodDix['Name']} has been logged to your meals',
    title='Yummy!'
)

# make logging experience fast by logging to cache instead of bigger dictionary
# cache is cleared in main nutrition function
cals = RoundNumber(nutrients['Calories'], ones)

# check if cache file exists and make one by default if not available
file = GetFile(f"{storage}/History/foodHistoryCache.json", errorIfNotFound=False)
if file is not None:
    IFRESULT = Text(file)
else:
    IFRESULT = "{ 'cache': [] }"

res = Dictionary(IFRESULT)
cache = res['cache']

# put the item in the cache
dix = {
    'date' : loggingDate.format(custom="yyyy-MM-dd"),
    'time' :  loggingDate.format(custom="HH:mm"),
    'food' : foodDix['Name'],
    'servings': servings,
    'id': foodDix['id'],
    'cals': cals
}
cache.append(dix)

dix = {
    'cache' : cache
}

# save cache away for later
SaveFile(dix, f"{storage}/History/foodHistoryCache.json", overwrite=True)

StopShortcut(output=foodDix)

