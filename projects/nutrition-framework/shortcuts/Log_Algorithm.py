'''
Framework: Nutrition (id = 4)
ID:  7
Ver: 1.2
'''

# Takes { Food: ... , Date: ... } and logs the food at the given date
# Can fast track permissions if the key 'setPerms' exists in the shortcut input

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))

Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))
nutrDix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/shortcutNames.json"))

setPerms = FALSE

if ShortcutInput['setPerms'] is not None:
    Alert(Strings['loga.healthperms.enable'], showCancel=False, Title=Strings['loga.healthperms.title'])
    setPerms = TRUE
    $IFRESULT = {
        'Food': { 'Servings': 1 },
        'Date': CurrentDate()
    }
else:
    $IFRESULT = f'{ShortcutInput}'
#endif

res = Dictionary($IFRESULT)

loggingDate = Date(res['Date'])
foodDix = Dictionary(res['Food'])

# set servings in food dictionary
if foodDix['Servings'] is not None:
    $IFRESULT = Number(foodDix['Servings'])
else:
    updatedText = Strings['ask.for.servings'].replace('$name', foodDix['Name']).replace('$size', foodDix['Serving Size'])
    $IFRESULT = AskForInput(InputTypes.Number, updatedText, allowNegatives=False, allowDecimals=True)
#endif

num = Number($IFRESULT)
foodDix['Servings'] = num
servings = num



# get health app environment var
dix = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/env.json"))
hasHelathApp = dix['hasHealthApp']

# add to backlog and exit if we are not on a device with a health app
if hasHealthApp == FALSE:
        if setPerms == TRUE:
            Alert(Strings['loga.healthperms.baddevice'], Title=Strings['loga.healthperms.title'])
            StopShortcut()
        #endif
    
    updatedText = Strings['loga.backlog.title'].replace('$name', foodDix['Name'])
    Notification(
        Strings['loga.backlog.msg'],
        title=updatedText,
    )

    # get the backlog file 
    file = GetFile(From='Shortcuts', f"{storage}/Other/backlog.json", noErrors=True)

    if file is not None:
        $IFRESULT = Dictionary(file)
    else:
        $IFRESULT = { 'backlog': [] }
    #endif

    backlog = $IFRESULT['backlog']

    # add it to the backlog
    dix = {
        'Date': Text(loggingDate),
        'Food': Dictionary(foodDix)
    }
    backlog.append(dix)

    # save file
    dix = { 'backlog': List(backlog) }
    SaveFile(To='Shortcuts', dix, f"{storage}/Other/backlog.json", overwrite=True)

    StopShortcut(output = foodDix)

else:
    if setPerms == TRUE:
        # If we are fast tracking permissions, we just pass in a food with 0 value nutrients into Log Nutrients To Health
        text = '''
            { "0": { "Protein": 0, "Trans": 0, "Cholesterol": 0, "Sugar": 0, "Monounsaturated": 0,
            "Polyunsaturated": 0, "Fat": 0, "Fiber": 0, "VitC": 0, "Calories": 0,
            "Iron": 0, "VitA": 0, "Potassium": 0, "Saturated": 0, "Calcium": 0,
            "Sodium": 0, "Carbs": 0 } }
        '''
        foodItems = Dictionary(text)

        text = f'''
            BEGIN:VCARD
            VERSION:3.0
            N;CHARSET=UTF-8:Test Food
            ORG;CHARSET=UTF-8:Test Servings
            NOTE;CHARSET=UTF-8:0
            END:VCARD
        '''

        contact = macros.textToContacts(text)

        res = f'{foodItems[contact.Notes]}'
        res['Date'] = CurrentDate()
        RunShortcut('Log Nutrients To Health', input=res)

        Alert(Strings['loga.healthperms.complete'], showCancel=False, Title=Strings['loga.healthperms.title'])
        StopShortcut()
    #endif
#endif


# nutrients will be the dictionary of nutrients that have values above our threshold
# used below when logging the system
nutrients = Dictionary()

# Normally we skip any nutrient values that are 0, but for setting permissions we want to log 0 values, so set threshold to -1
if setPerms == TRUE:
    $IFRESULT = -1
else:
    $IFRESULT = 0
#endif
threshold = $IFRESULT

file = GetFile(From='Shortcuts', 'FLS/Other/nutriKeys.txt')
# store the nutrients in the dictionary
for item in SplitText(file, ByNewLines):
    num = Number(foodDix[item])
    foodDix[item] = RoundNumber(num, hundredths)
    if num > threshold:
        num = num * servings
        num = Round(num, "hundredths")
        nutrients[item] = num
    #endif
#endfor

# Log nutrients
nutrients['Date'] = loggingDate
RunShortcut("Log Nutrients To Health", input=Text(nutrients))

updatedText = Strings['loga.notif.logged'].replace('$name', foodDix['Name'])
Notification(
    updatedText,
    title=Strings['loga.notif.yummy']
)

# make logging experience fast by logging to cache instead of bigger dictionary
# cache is cleared in main nutrition function
cals = RoundNumber(nutrients['Calories'], ones)

# check if cache file exists and make one by default if not available
file = GetFile(From='Shortcuts', f"{storage}/History/foodHistoryCache.json", errorIfNotFound=False)
if file is not None:
    $IFRESULT = Text(file)
else:
    $IFRESULT = "{ 'cache': [] }"
#endif

res = Dictionary($IFRESULT)
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
SaveFile(To='Shortcuts', dix, f"{storage}/History/foodHistoryCache.json", overwrite=True)

StopShortcut(output=foodDix)

