'''
Framework: Nutrition (id = 4)
ID:  20
Ver: 1.1
'''

# Get food from databse or seach, or make food from databse or seacrh

TRUE = 1
FALSE = 0

storage = Text(GetFile(From='Shortcuts', "Nutrition_Shortcut_Storage_Folder_Name.txt"))
Strings = Dictionary(GetFile(From='Shortcuts', f"{storage}/Other/gui_strings.json"))
nutrDix = Dictionary(GetFile(From='Shortcuts', f'{storage}/Other/shortcutNames.json'))

params = Dictionary(ShortcutInput)

showMenu = FALSE

# shortcut can either be called to retrieve a food
# or can be called as a standalone for adding a food to the personal database
# 'getFood' in params is used to identify the former function

if params['getFood'] is not None:
    # we are getting a food from the database
    Menu("Get Food"):
        case Strings['barcodes.select']:
            # user selects one of the foods saved in the personal databse
            StopShortcut(output=RunShortcut(nutrDix['Get Saved Food'], input={'type': 'barcodes'}))

        case Strings['barcodes.scan']:
            pass

        case Strings['opts.cancel']:
            StopShortcut()
    #endmenu
#endif

# scan the barcode
barcode = Text(ScanBarcode())

# barcodeCache maps barcodes to the ID of their food objects, allows immediate access of barcodes alread in personal database
file = GetFile(From='Shortcuts', f'{storage}/Barcodes/barcodeCache.json', errorIfNotFound=False)
if file is not None:
    $IFRESULT = file
else:
    # if the barcode cache does not exist, create it and then return the created cache
    barcodeCache = {}
    folder = GetFile(From='Shortcuts', f'{storage}/Barcodes/Foods', errorIfNotFound=False)
    for item in GetContentsOfFolder(folder):
        barcodeCache[ item['Barcode'] ] = item['id']
    #endfor
    
    SaveFile(To='Shortcuts', barcodeCache, f'{storage}/Barcodes/barcodeCache.json', overwrite=True)
    
    $IFRESULT = barcodeCache
#endif

barcodeCache = $IFRESULT

if barcodeCache[barcode] is not None:
    # if barcode is in cache retrieve the food using the food ID i.e. barcodeCache[barcode]
    file = GetFile(From='Shortcuts', f'{storage}/Barcodes/Foods/food_{barcodeCache[barcode]}.json')
    
    if params['getFood'] is not None:
        # if we are getting a food then return the food
        StopShortcut(output = file)
    else:
        # we are adding a food to the personal database but there is already a food mapped to the barcode
        # ask user if they would like to edit the food, remake the food or cancel

        Menu(Strings['barcodes.code.exists'].replace('$barcode', barcode)):
            case Strings['barcodes.food.edit']:
                RunShortcut(nutrDix['Edit Saved Food'], input={'type': 'barcodes', 'args': file})
                StopShortcut()
            case Strings['barcodes.food.remake']:
                DeleteFile(file, deleteImmediately=True)
            case Strings['opts.cancel']:
                StopShortcut()
        #endmenu
    #endif
#endif


# if we get here that means we are creating a new food item
foodResolved = FALSE
doSearch = FALSE
testing = FALSE

# Search online database openfoodfacts.org

if testing == TRUE:
    $IFRESULT = ... # text of some barcode result (files/barcode.json)
else:
    # query the API
    url = URL(f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json')
    $IFRESULT = GetContentsOfURL(url)
#endif

res = Dictionary($IFRESULT)

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

    # prompt user if they would like to accept the result, edit the result, or cancel
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
            foodResolved = TRUE
        case Strings['search.item.edit']:
            res = RunShorctut(NutriDix['Display Food Item'], input=outputFood)
            Menu(Strings['search.item.save'])
                case Strings['opts.yes']:
                    outputFood = res
                    foodResolved = TRUE
                
                case Strings['search.item.prevvalues']:
                    foodResolved = TRUE
                
                case f'{Strings['opts.no'], Strings['barcode.searchmanual']}':
                    pass
            #endmenu
        case Strings['barcodes.searchmanual']:
            pass
        
        case Strings['opts.cancel']:
            StopShortcut()
    #endmenu
#endif

if foodResolved == FALSE:
    # no match in database or in search so we continue
    Menu(Strings['barcodes.nomatch.prompt']):
        case Strings['foodslist.menu.search']:
            doSearch = TRUE
        case Strings['foodslist.menu.manual']:
            pass
        case Strings['opts.cancel']:
            StopShortcut()
    #endmenu
#endif

if doSearch == TRUE:
    # perform search with search algorithm
    outputFood = RunShortcut(nutrDix['Search Algorithm'])
    
    if outputFood is not None:
        foodResolved = TRUE
    #endif
        
    Menu(Strings['barcodes.search.none']):
        case Strings['barcodes.exit.withnone']:
            StopShortcut()
        case Strings['foodslist.menu.manual']:
            pass
    #endmenu
#endif

if foodResolved == FALSE:
    # otherwise we fall through to make food manually
    outputFood = RunShortcut(nutrDix['Make Food Manually'])
#endif

# save the new output food to database and then continue
outputFood['Barcode'] = barcode

barcodeCache[barcode] = outputFood['id']
SaveFile(To='Shortcuts', barcodeCache, f'{storage}/Barcodes/barcodeCache.json', overwrite=True)
SaveFile(To='Shortcuts', outputFood, f'{storage}/Barcodes/Foods/food_{outputFood['id']}.json', overwrite=True)

# delete the vcardCache for barcodes since we have added a new item
DeleteFile(GetFile(From='Shortcuts', f"{storage}/Barcodes/vcardCache.txt", errorIfNotFound=False), deleteImmediately=True)

updatedText = Strings['barcodes.created.notif.msg']
                .replace('$name', outputFood['Name'])
                .replace('$barcode', barcode)
Notification(title=Strings['barcodes.created.notif.title'], updatedText)

StopShortcut(output = outputFood)