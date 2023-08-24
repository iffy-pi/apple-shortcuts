# Nutrition Shortcut
## Basic Information
Log foods from the MyFitnessPal and OpenFoodFacts.org directly to your Apple Health. No applications or accounts required!. Save foods you eat regularly as Presets, access what you've eaten in the past with your Food History. Get statistics with Charty and more!

<p style="align:center;display:flex;justify-content:space-between;flex-wrap:wrap;">
  <img src="./readme-assets/main_menu.png" alt="Main Menu" height="500"/>
  <img src="./readme-assets/display_food.png" alt="Display Food Item" height="500"/>
  <img src="./readme-assets/foods_list.png" alt="Foods List" height="500"/>
</p>

<p style="align:center;display:flex;justify-content:space-between;flex-wrap:wrap;">
  <img src="./readme-assets/search.png" alt="Main Menu" height="500"/>
  <img src="./readme-assets/ask_for_servings.png" alt="Ask For Servings" height="500"/>
  <img src="./readme-assets/saved_foods.png" alt="Display Food Item" height="500"/>
</p>

# Tutorial
View Tutorial [here](https://iffy-pi.github.io/apple-shortcuts/versioning/nutrition/data/tutorial.html).

# Technical Documentation
## Shortcut Links
This documentation will refer to shortcuts by their standard name using bold text e.g. **Log Algorithm**. The table below, maps each of the standard names to their shortcut file on the repo.
 
| Shortcut Name                | Link                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------ |
| Add Recent                   | [Add_Recent.py](./shortcuts/Add_Recent.py)                                     |
| Barcode Search               | [Barcode_Search.py](./shortcuts/Barcode_Search.py)                             |
| Calculate Stats              | [Calculate_Stats.py](./shortcuts/Calculate_Stats.py)                           |
| Clear Cache And Backlog      | [Clear_Cache_And_Backlog.py](./shortcuts/Clear_Cache_And_Backlog.py)           |
| Display Food Item            | [Display_Food_Item.py](./shortcuts/Display_Food_Item.py)                       |
| Edit Saved Food              | [Edit_Saved_Food.py](./shortcuts/Edit_Saved_Food.py)                           |
| Food History                 | [Food_History.py](./shortcuts/Food_History.py)                                 |
| Foods List                   | [Foods_List.py](./shortcuts/Foods_List.py)                                     |
| Generate Food ID             | [Generate_Food_ID.py](./shortcuts/Generate_Food_ID.py)                         |
| Get Recent                   | [Get_Recent.py](./shortcuts/Get_Recent.py)                                     |
| Log Algorithm                | [Log_Algorithm.py](./shortcuts/Log_Algorithm.py)                               |
| Log Foods At Different Times | [Log_Foods_At_Different_Times.py](./shortcuts/Log_Foods_At_Different_Times.py) |
| Log Foods At Time            | [Log_Foods_At_Time.py](./shortcuts/Log_Foods_At_Time.py)                       |
| Make Food Manually           | [Make_Food_Manually.py](./shortcuts/Make_Food_Manually.py)                     |
| Make Preset                  | [Make_Preset.py](./shortcuts/Make_Preset.py)                                   |
| Nutrition                    | [Nutrition.py](./shortcuts/Nutrition.py)                                       |
| Nutrition Statistics         | [Nutrition_Statistics.py](./shortcuts/Nutrition_Statistics.py)                 |
| Saved And Search             | [Saved_And_Search.py](./shortcuts/Saved_And_Search.py)                         |
| Search Algorithm             | [Search_Algorithm.py](./shortcuts/Search_Algorithm.py)                         |
| Select Saved Foods           | [Select_Saved_Foods.py](./shortcuts/Select_Saved_Foods.py)                     |
## Storage Structure
Users select a storage folder during the installation process. The storage follows the given structure:

```
- Storage Folder/
|	- Presets/
|	|	- Foods/
|	|	- vcardCache.txt
|	
| 	- Recents/
|	|	- Foods/
|
|	- Barcodes/
|	|	- Foods/
|	|	- vcardCache.txt
|	|	- barcodeCache.json
|
|	- History/
|	|	- foodHistory.json
|	|	- foodHistoryCache.json
|
|	- Other/
|	|	- shortcutNames.json
|	|	- nextFoodId.txt
|	|	- tempNutrientsDix.txt
|	|	- env.json
|	|	- nutriKeys.txt
```

- **Presets/**
	- **Foods/**
		- *Contains all the foods that are presets,  where foods are saved in the format `food_<food ID>.json`.*
	- **vcardCache.txt**
		- *Food contact vcards generated from presets. Read more in [Contact VCards](#todo-contact-vcards)*
- **Recents/**
	- **Foods/**
		- *All recent foods, where foods are saved in the format `food_<food ID>.json`.*
- **Barcodes**
	- **Foods/**
		- *Contains all the foods that are barcoded foods, where foods are saved in the format `food_<food ID>.json`.*
	- **vcardCache.txt**
		- *Food contact vcards generated from barcoded foods. Read more in [Contact VCards](#todo-contact-vcards)*
	- **barcodeCache.json**
		- *Cache dictionary that maps barcodes to the food ID of barcoded foods*
- **History/**
	- **foodHistory.json**
		- *The history of all foods eaten.*
	- **foodHistoryCache.json**
		- *A cache of foods that are to be added to history. Generated by Log Algorithm.*
- **Other/**
	- **shortcutNames.json**
		- *JSON dictionary which maps names used in the framework with the actual names of the shortcut.*
	- **nextFoodId.txt**
		- *The value of the next ID to be used when a food ID is generated.*
	- **tempNutrientsDix.txt**
		- *Temp file used during the logging process.*
	- **env.json**
		- *JSON dictionary which holds different environment variables*.
	- **nutriKeys.txt**
		-  *The list of all keys that are nutrients in a food object. Used by shortcuts which needs the nutrient keys.*
## *env.json*
This is a JSON dictionary used to store the value of environment variables, variables that are used across different shortcuts. An example of the file is shown below

```json
{
	"permsEnabled": 1,
	"hasHealthApp": 1,
}
```

`hasHealthApp` is an environment variable which determines if the running device has the Apple Health App (1) or not (0). It is always set during the start up of *Nutrition* and accessed by shortcuts which rely on the presence of the Health App, such as **Log Algorithm**, **Clear Cache and Backlog** etc.

## Food Object
The basis of the shortcut is food object, which contains all relevant information about a food: the food name, serving size, barcode, ID and nutrient values. It can also include the number of servings if the food is to be logged.

The food object is handled as a JSON dictionary with the following keys:
  
| JSON Key          | Data Type | Description                                                                                           |
| ----------------- | --------- | ----------------------------------------------------------------------------------------------------- |
| `Name`            | String    | Food Name                                                                                             |
| `Serving Size`    | String    | Food Serving Size                                                                                     |
| `Barcode`         | String    | The barcode number of the food, key is omitted or is an empty string if the food does not have it.    |
| `id`              | Number    | The unique ID assigned to this food object. This does not change when the food is edited.             |
| `Servings`        | Number    | The number of servings for the food, set by one of the shortcuts when the food is about to be logged. |
| `Calories`        | Number    | Calories in food, (g)                                                                                 |
| `Carbs`           | Number    | Carbohydrates in food (g)                                                                             |
| `Fat`             | Number    | Total Fat in food (g)                                                                                 |
| `Protein`         | Number    | Total Protein in food (g)                                                                             |
| `Sugar`           | Number    | Sugar in food (g)                                                                                     |
| `Fiber`           | Number    | Fiber in food (g)                                                                                     |
| `Monounsaturated` | Number    | Monounsaturated Fat in food (g)                                                                       |
| `Polyunsaturated` | Number    | Polyunsaturated Fat in food (g)                                                                       |
| `Saturated`       | Number    | Saturated Fat in food (g)                                                                             |
| `Trans`           | Number    | Trans Fat in food (g) (Note there is no Trans Fat in Apple Health so it is never logged)              |
| `Sodium`          | Number    | Sodium in food (mg)                                                                                   |
| `Cholesterol`     | Number    | Cholesterol in food (mg)                                                                              |
| `Potassium`       | Number    | Potassium in food (mg)                                                                                |
| `VitA`            | Number    | Vitamin A  in food (mcg)                                                                              |
| `VitC`            | Number    | Vitamin C in food (mcg)                                                                               |
| `Calcium`         | Number    | Calcium in food (mg)                                                                                  |
| `Iron`            | Number    | Iron in food (mg)                                                                                     |                  |           |                                                                                                       |

## Logging Foods
Foods are logged through **Log Foods At Time** and **Log Foods At Different Times**, both shortcuts eventually pass the food to **Log Algorithm** along with a date:

```json
// Dictionary that is input to the log algorithm shortcut
{
	"Date": "Aug 23, 2023 at 14:39",
	"Food": { ... } // Food object
}
```

**Log Algorithm** multiplies all the nutrient keys by the value of `Servings` in the food object, and then passes a dictionary of the non-zero nutrients to **Log Nutrients to Health** which logs the nutrients to their appropriate Health Samples.

### Adding to Backlog
**Log Algorithm** reads the `hasHealthApp` field from *env.json* before proceeding with logging to Apple Health, as this tells the shortcut if it is running on a device with Apple Health. If `hasHealthApp` is false (`0`), the food is added to the system backlog. Read more in [Food Backlog](#food-backlog).
### Fast Tracking Health Permissions
The logging of nutrients to health samples was separated to a different shortcut to allow the fast tracking of health permissions. The shortcut provides an option to enable all required health permissions with a sample zero-nutrient food so that users don't have to deal with allowing permissions afterward. This fast tracking of permissions is done by passing the dictionary `{ "setPerms" : true }` to  **Log Algorithm**.

Because of the nature of the shortcuts app, the fast tracking of permissions didn't work when the health sample logging was done within **Log Algorithm** different files and other items were being shared with Health that changed with each food object. With **Log Nutrients to Health**, the nutrient dictionary is first saved to a temp file and then pulled from that file, allowing it to be the same object no matter the food. This means the permissions set for the test food will apply to the remaining foods.
### Adding To Food History
After the food is logged, the food, servings and calories are added to the Food History, particularly to *History/foodHistoryCache.json*, which is a cache for the food history.

The format of the cache is shown below:

```json
{
	"cache": [
		{
		    "date" : "2023-08-23",
		    "time" : "14:50",
		    "food" : "Apple",
		    "servings": 1,
		    "id": 2
		    "cals": 52
		},
		...
	]
}
```

The cache is cleared by running **Clear Cache and Backlog**, which is run after the logging process in the main shortcut **Nutrition**. The cache is used since the main history file can be large and slow to open, which will slow down the logging process. Read more about the food history in [Food History](#food-history).
## Food Sources
### Foods List
The shortcut **Foods List** manages the different methods a food can be obtained for logging. Each method is a food source, and **Foods List** manages the selected food objects to allow the user to edit or remove foods in the list. This is done with the variables `foodsDix` and `selectedIds`.

`selctedIds` is a list of numbers, which are unique list IDs for a given food object in the current foods list. `foodsDix` is a dictionary that maps IDs in `selectedIds` to their food object:

```python
selectedIds = [ 0, 1, 2 ]
foodsDix = {
	"0": { ... }, # food object for list ID 0
	"1": { ... }, # food object for list ID 1
	"2": { ... }  # food object for list ID 2
}
```

Each food is assigned a unique list ID by using the variable `nextID`. When a food object has been selected:
- The value of `nextID` is used as the list ID of the food object
- That is, it is added to the list `selectedIds`
- And is set to the food object in `foodsDix`
- `nextID` is incremented by 1 to keep generating unique IDs

This allows foods to be easily edited and or removed:
- To edit a food, simply selected the correct list ID, edit the food object retrieved from `foodsDix` and re-set it in `foodsDix`
- To remove a food, filter the list ID from `selectedIds`. We don't need to edit `foodsDix`, since `selectedIds` is always used to retrieve foods

The following are the currently available food sources, presented as menu options to the user:
- Search for the food on the MyFitnessPal Database
- Get Saved Food
- Scan a barcode to search in the database
- Get a recent meal
- Make the food manually
### Search Food
Users can search the MyFitnessPal database for foods they would like. This is possible as MyFitnessPal provides a URL based API which returns JSON responses containing all the relevant information about the food. The search process is faciliated by **Search Algorithm**.

Queries are made to the URL: `https://api.myfitnesspal.com/public/nutrition?q={query}&page={pageNo}&per_page={noSearchResults}`
- `{query}` is the URL encoded search food or drink.
- `{pageNo}` is the search results page number.
- `{noSearchResults}` is the number of search results per page.

With this, the shortcut is able to provide access to different pages by providing *Next Page* and *Previous Page* buttons.

When called, **Search Algorithms** takes the user's search query as input and makes a call to the API endpoint for the JSON response. It parses the JSON response getting key information for each search result:
- The food name
- The food ID
- The brand name (if any)
- The available serving sizes (and their multipliers)

The food ID is unique to the food and is therefore used to cache the search result in the `searchItems` dictionary. The other information is made into [Contact VCards](#todo-contact-vcards) and used for the selection process.

When a food is selected, the cache result is pulled from `searchItems` and the user now selects a desired serving size. The search results are structured such that a food can have multiple serving sizes, where each serving sizes applies a multiplication factor to the base nutrients included for the food, for example:

```json
"serving_sizes":[
	   {
		  "id":"238480111169341",
		  "index":0,
		  "nutrition_multiplier":2,
		  "unit":"medium",
		  "value":1.0
	   },
	   {
		  "id":"237930355355581",
		  "index":1,
		  "nutrition_multiplier":1.65,
		  "unit":"small",
		  "value":1.0
	   },
	   {
		  "id":"238480111169469",
		  "index":2,
		  "nutrition_multiplier":2.42,
		  "unit":"large",
		  "value":1.0
	   }
]
```

`nutrition_multiplier` is the multiplication factor for the serving size. The serving size itself is created by concatenating the `value` field with the `unit` field.

Contact VCards are again used for the selection process, of servings sizes, where the multiplier is included as the contact note. Once the user makes their selection, the multiplier is used to scale the nutrients included in the search results and then transfer them into a new food object.

The user will be shown the created food object and will have the option to edit any of the field values as they choose. When this is completed, a food ID is generated for the food using **Generate Food ID**, giving the food a unique tracker in the framework.
### Saved Food(s)
For this option, barcoded foods and presets are combined into a single list, allowing the users to select foods from both options. This is done with **Select Saved Foods**, when `type: all` is passed as the input parameter. The shortcut adds information on each food so that the user knows which type of food it is:

**TODO: Picture of select saved foods with distinction**

You can read more about [Barcoded Foods](#barcoded-foods) and [Presets](#presets).
#### Selection Contacts and Caches: *vcardCache.txt*
To present a comprehensive selection process for the user, **Select Saved Foods** leverages the choose from contacts action in the shortcut. For each saved food, it generates a simple [VCard](https://vcardmaker.com/) that contains the information we would like to display to the user:

```
BEGIN:VCARD
VERSION:3.0
N;CHARSET=UTF-8:Apple
ORG;CHARSET=UTF-8:Presets ⸱ 1 fruit
NOTE;CHARSET=UTF-8:{ "id":1 , "parentFolder": "presets"}
END:VCARD
```

- `N;CHARSET=UTF-8` is the name of the contact, this is the headline text during selection and is therefore used for the food name.
- `ORG;CHARSET=UTF-8` is the organization of the contact, and shows up as a subtitle under the main headline. This is used for additional information, in this case it is the food source and it's serving size
- `NOTE;CHARSET=UTF-8` is a field that is not visible in selection but remains part of the contact. This is used to put information that identifies the selection object e.g. it's selection ID or other information relevant.

The VCards can be compiled into a text and then converted into contacts by setting the name of the text to `vcard.vcf`, and using the `Get Contacts from Input` action. The user can then select the contacts they want, and the notes field is pulled to get the required information.

For this case, the food ID and it's parent folder is stored in the notes field, so that the food file can be retrieved immediately from the appropriate folder.

This contact process is used in almost every place that requires user selection of foods (**Get Recent**, **Edit Saved Foods**, **Make Preset**, **Foods List**, **Log Foods At Different Times** etc.), what each field is used for differs.

Generating the VCards does take some time since we have to open every food file from the *Foods* folder to read their information. This can begin to consume a lot of time as user adds more and more presets.

Since presets and barcoded foods do not change frequently, we can make an optimization to save the generated VCards instead of having to regenerate the cards every time. This saved to *vcardCache.txt* in their respective folders.

If presets or barcoded foods change e.g. addition of a new food, removal of a food etc. The cache is deleted by the shortcut that made the change, and is recreated whenever **Select Saved Foods** is run again.
### Scan Barcode
This allows users to scan a barcode of a product which can be retrieved from their personal database or searched for on OpenFoodFacts.org. This is done using **Barcode Search** with the input parameter `getFood: true`, this tells the shortcut that it is not creating a new food but instead attempting to retrieve one.

If there is a match for the barcode in the users personal database (*Barcodes/Foods*), then the found food is returned. Otherwise, the barcode is used to query OpenFoodFacts.org, after which the user will be given the opportunity to accept, edit or reject the search result.

If the user rejects the search result, they will be given the option to search for the food on the MyFitnessPal database using **Search Algorithm**, or make the food manually with **Make Food Manually**.

In any case where the food is not found in the user's personal database, the created food is added to the user's personal database:
- Barcode is mapped to food in *Barcodes/barcodeCache.json*.
- *vcardCache.txt* is deleted as it will have to be regenerated.

Read more about barcoded foods in [Barcoded Foods](#barcoded-foods).
### Recent Foods
This allows users to select foods from the last 30 logged foods, this is especially useful for search results that need to be accessed again.

Recent meals are saved under *Recents/Foods*, where each food is saved as `food_<food ID>.json`. A user selects one or more recent foods with **Get Recent**, which shows the user their recent foods sorted from latest to earliest. The selection window also shows how long ago the recent food was accessed.

**TODO: PICTURE OF GET RECENTS SELECTION PANE**

This is generated with the use of [Contact VCards](#todo-contact-vcards).
#### Adding New Recent Foods
Foods are added to the recents folder with **Add Recent**, which receives a food object and saves it as `food_<food ID>.json` in the foods folder. Since the ID of a food never changes, adding a food that is already in the folder will overwrite its current file, and update the modified time. This allows **Get Recent** to sort the foods by last modified date for the desired selection order.
### Make Food Manually
If the user has the nutrition label of the food, they can fill the fields in the food object directly using **Make Food Manually**. This shortcut presents the user with a food object dictionary to fill, including the name, serving size and nutrients.

Since vitamins and minerals can either be DV (Daily Value) percentages or exact values, **Make Food Manually** presents users with the option to select one or the other when entering the field values. Since the fields of the food object operate with exact values, a conversion is done within the shortcut if DV percentages are specified.

## Presets

## Barcoded Foods
## Food History

## Food Backlog

## Food Notes

## Nutrition Statistics with Charty

- Searching for food
	- How the MyFitnessPal databse is queried
	- How results are transferred to our own food object format
	- How user can edit the fields in the result
- Recent
	- How recent foods are added or updated (saving the file)
- Presets
	- How presets can be created
		- Make Presets post logging or make presets standalone
	- Editing/Viewing Presets
	- Removing Presets
- Barcoded Foods
	- Making Barcoded Foods
		- Scan and search openFoodfacts.org
		- Fall through to search and then to manual creation
		- Automatically added to database
	- Editing Barcoded Foods
	- Removing Barcoded Foods
