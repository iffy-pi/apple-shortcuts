'''
Framework: Nutrition (id = 4)
ID:  20
Ver: 1.01
'''

# Get food from databse or seach, or make food from databse or seacrh

TRUE = 1
FALSE = 0

storage = Text(GetFile("Nutrition_Shortcut_Storage_Folder_Name.txt"))
nutrDix = Dictionary(GetFile(f'{storage}/Other/shortcutNames.json'))

params = Dictionary(ShortcutInput)

showMenu = FALSE

# shortcut can either be called to retrieve a food
# or can be called as a standalone for adding a food to the personal database
# 'getFood' in params is used to identify the former function

if params['getFood'] is not None:
    # we are getting a food from the database
    Menu("Get Food"):
        case 'Select from Personal Database':
            # user selects one of the foods saved in the personal databse
            StopShortcut(output=RunShortcut(nutrDix['Get Saved Food'], input={'type': 'barcodes'}))

        case 'Scan Barcode':
            pass

        case 'Cancel':
            StopShortcut()

# scan the barcode
barcode = Text(ScanBarcode())

# barcodeCache maps barcodes to the ID of their food objects, allows immediate access of barcodes alread in personal database
file = GetFile(f'{storage}/Barcodes/barcodeCache.json', errorIfNotFound=False)
if file is not None:
    IFRESULT = file
else:
    # if the barcode cache does not exist, create it and then return the created cache
    barcodeCache = {}
    folder = GetFile(f'{storage}/Barcodes/Foods', errorIfNotFound=False)
    for item in GetContentsOfFolder(folder):
        barcodeCache[ item['Barcode'] ] = item['id']
    
    SaveFile(barcodeCache, f'{storage}/Barcodes/barcodeCache.json', overwrite=True)
    
    IFRESULT = barcodeCache

barcodeCache = IFRESULT

if barcodeCache[barcode] is not None:
    # if barcode is in cache retrieve the food using the food ID i.e. barcodeCache[barcode]
    file = GetFile(f'{storage}/Barcodes/Foods/food_{barcodeCache[barcode]}.json')
    
    if params['getFood'] is not None:
        # if we are getting a food then return the food
        StopShortcut(output = file)
    else:
        # we are adding a food to the personal database but there is already a food mapped to the barcode
        # ask user if they would like to edit the food, remake the food or cancel
        Menu(f'There is a food in your database with the barcode "{barcode}"'):
            case 'Edit Food':
                RunShortcut(nutrDix['Edit Saved Food'], input={'type': 'barcodes', 'args': file})
                StopShortcut()
            case 'Remake Food':
                DeleteFile(file, deleteImmediately=True)
            case 'Cancel'
                StopShortcut()


# if we get here that means we are creating a new food item
foodResolved = FALSE
doSearch = FALSE
testing = FALSE

# Search online database openfoodfacts.org

if testing == TRUE:
    IFRESULT = ... # text of some barcode result (files/barcode.json)
else:
    # query the API
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

    # prompt user if they would like to accept the result, edit the result, or cancel
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
            StopShortcut()

if foodResolved == FALSE:
    # no match in database or in search so we continue
    Menu("There was no match found on OpenFoodFacts.org, what would you like to do?"):
        case 'Search for Food':
            doSearch = TRUE
        case 'Make Food Manually':
            pass
        case 'Cancel':
            StopShortcut()

if doSearch == TRUE:
    # perform search with search algorithm
    outputFood = RunShortcut(nutrDix['Search Algorithm'])
    
    if outputFood is not None:
        foodResolved = TRUE
        
    Menu('Search had no results'):
        case 'Exit with no selection':
            StopShortcut()
        case 'Make Food Manually':
            pass

if foodResolved == FALSE:
    # otherwise we fall through to make food manually
    outputFood = RunShortcut(nutrDix['Make Food Manually'])

# save the new output food to database and then continue
outputFood['Barcode'] = barcode

barcodeCache[barcode] = outputFood['id']
SaveFile(barcodeCache, f'{storage}/Barcodes/barcodeCache.json', overwrite=True)
SaveFile(outputFood, f'{storage}/Barcodes/Foods/food_{outputFood['id']}.json', overwrite=True)

# delete the vcardCache for barcodes since we have added a new item
DeleteFile(GetFile(f"{storage}/Barcodes/vcardCache.txt", errorIfNotFound=False), deleteImmediately=True)

Notification(title='Barcoded Food Created', f'Barcoded Food "{barcode}" has been added to your database allowing you to scan them for later!')

StopShortcut(output = outputFood)