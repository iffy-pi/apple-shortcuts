# Using Nutrition
## The Main Menu
The main shortcut for the food logging shortcut is **Nutrition**. Once started, you are provided with a main menu for all relevant actions:
<!-- ![Setting](./images/main_menu.png?raw=true) -->

### Quick Log
`PICHERE: Quick log menu option`

This allows you to log one or more of your recent meals at the current date and time. This option is optimized for speed and is useful for foods you consume frequently.

***Note: If you log foods from a device that does not have the Apple Health app, the foods will be saved to your backlog which will be automatically cleared when you run the shortcut on a device with Apple Health. Read more about the backlog in [Food Backlog](#food-backlog).***

### Log Foods At Time
`PICHERE: menu option`

Log one or more foods at a given date and time. This provides more food sources to log from (recent meals, presets, barcoded foods and even search foods, read more in [Food Sources](#food-sources)).

### Log Foods At Different Times
`PICHERE: menu option`

Log one or more foods at one or more different times. This is useful for cases where foods that were eaten at different times need to be logged. For example, suppose I wish to log:
- A PB Sandwich and Jam at 9 AM
- A Ham Sandwich at 2 PM
- Chicken Noodles at 6 PM

You first select all the foods you wish to log (selection options are from [Food Sources](#food-sources)):

`PICHERE: Picture of foods with foods selected`

Then you can select one or more foods and choose the date and time the selected foods should be logged at. So for the above case, PB sandwich and Jam will be selected:

`PICHERE: Selected PB sandwich and jam`

And I can then apply the 9 AM log time to them:

`PICHERE: Selected 9AM time for pb sandwich and jam`

This process is repeated until all the foods are logged with your selected log time.

### Make Food Note
In the case where you don't have time to log a food, you can save it as a note using the *Make Food Note* option. This allows you to give a short description of the food, along with a date and time for it.

`PICHERE: Ask for food input and select date and time (one pic)`

Food notes will appear at the top when selecting foods and/or logging them, reminding you to log foods you saved.

`PICHERE: Example of food note in the header`

You will be asked if you wish to clear your food notes after logging foods, but if you would like to manually clear it, you can do so by going to *Clear and Other Settings > Clear food notes*

### Saved Foods and Search
This leads to a sub-menu with options for your saved foods and searching for foods on the MyFitnessPal database.

#### Search and View
`PICHERE: Menu option`

This allows you to search for a food from the MyFitnessPal database and view its nutritional contents. You can also choose to log the food, and/or make it a preset.

#### Saved Foods
There are three different types of saved foods:

**Presets**: These are one or more foods that are grouped into a single food for which you can set the name and serving size. Presets are useful for saving meals that are made up of multiple foods. Read more in [Presets](#presets).

`PICHERE: Presets menu option`

**Barcoded Foods**: These are similar presets but also include a barcode for the food. This allows you to scan a barcode and retrieve the food, either from OpenFoodFacts.org or your own personal database. Read more in [Barcoded Foods](#barcoded-foods)

`PICHERE: Barcodes option`

**Recent Meals**: The shortcut saves the last 30 foods that were logged, allowing them to be accessed later. These recent meals are used in [Quick Log](#quick-log) or for making presets. You can view the recent meals through the menu option.

`PICHERE: Menu option`

### History and Stats
This sub-menu provides options to view your Food History or generate statistics based on your logged nutrients.

`PICHERE: Menu options`

#### Statistics with Charty
The application Charty (download [here](https://apps.apple.com/ca/app/charty-for-shortcuts/id1494386093)) is used to generate charts and graphs that break down your nutrient and calorie consumption for dates you select. This gives you an insight on your nutritional diet. Read more in [Nutrition Statistics](#nutrition-statistics).

#### Food History
The shortcut saves a little information about every food you log as your food history. This includes the food name, the servings of the food and the total calories from the meal. The menu option above allows you to access and read the food history. You can read more about the food history is stored in [Your Food History](#your-food-history)

### Clear and Other Settings
This is a sub-menu for miscellaneous options and settings for the shortcut:

`PICHERE: Menu options`

The menu provides options to perform the following actions:
- Clear foods in your backlog, if you are on a device with the Apple Health app (see more in [Food Backlog](#food-backlog)).
- Manually clear your food notes.
- View or rename the storage folder used by the shortcut. Learn more about the shortcut storage in [Storage](#storage)

## Food Sources
When you select foods to log or to make as a preset, there are several sources that can be used to retrieve foods. The **Foods List** shortcut manages the selection of foods from the different sources:

`PICHERE: Foods List menu option`

The shortcut provides an interface to select foods from the different sources available:
- **Search Food**: Search for the food on the MyFitnessPal Database.
- **Get Saved Food(s)**: Select one or more foods from your [Presets](#presets) and [Barcoded Foods](#barcoded-foods).
- **Scan Barcode**: Scan a barcode to retrieve the food from your personal database (see [Barcoded Foods](#barcoded-foods)) or query OpenFoodFacts.org.
- **Get Recent Food(s)**: Select one or more foods from your last 30 foods logged.
- **Make Food Manually**: Fill in the foods nutritional content manually

When foods are selected, you will also be prompted to enter the number of servings for the food. Once this is completed, foods currently in the list will be present at the top of the menu.

`PICHERE: Using bulk entry example`

You can view, edit and/or remove any of the selected foods. When you have completed your selection, you click *Done*.

## Storage
All data used by the shortcut is saved under the storage folder you selected during setup and installation. You can view or rename the storage folder by using the provided options in *Clear and Other Settings*.

**Note: The shortcut knows which folder to access because it saves the folder name in the file Shortcuts/Nutrition_Shortcut_Storage_Folder_Name.txt. If this file is deleted, then the shortcut will not be able to locate the folder until it is recreated.**

## Presets
Presets allow you to combine one or more foods into a single food that will be added to your personal foods. This allows you to save meals you continuously eat. After logging food (with the exception of [Quick Log](#quick-log)), you will have the option to select one or more of the logged foods for making a preset.

Presets are saved in the Presets folder in storage. You can make, view, edit or remove presets with the options provided at *Saved and Search > Presets*:

`PICHERE: Menu options for presets`

## Barcoded Foods
Barcoded foods are similar to presets but also include a barcode, which can be used to retrieve the food immediately. You can add, view, edit or remove barcoded foods with the options provided at *Saved and Search > Barcoded Foods*.

`PICHERE: Menu options for barcodes`

Note: Whenever a barcode is scanned, your personal database (saved in the Barcodes folder in storage) is queried for a match to the scanned barcode. If no match is found, you will be provided the option to search for the barcode on [OpenFoodFacts.org](https://world.openfoodfacts.org/api)or make the food manually.

## Your Food History
Logged foods are saved into your food history with the food name, the number of servings and the total calories they provided. The food history is saved as a JSON file (History/foodHistory.json), where the keys are the different dates, and the values are the different times e.g.

```json
"2020-08-05":{
  "13:30":{
	 "food":"Hashbrowns",
	 "cals":180,
	 "servings":3
  },
  "17:30":[
	 {
		"food":"GV Peanut Butter",
		"cals":238,
		"servings":2.5
	 },
	 {
		"food":"Peanut Butter Sandwich",
		"cals":323,
		"servings":1
	 }
  ],
  "21:40":{
	 "food":"Vegetable Fried Rice",
	 "cals":1158,
	 "servings":4.5
  }
},
```

This storage format makes accessing dates efficient within the Shortcuts framework.

You can view your food history with the options provided at *History and Stats > Food History*

`PICHERE: Menu options for food history`

For queries that span multiple days, each day is returned as an item in the object passed to Quick Look, allowing you to easily scroll through multiple days:

`PICHERE: Example of multiple days in quick look`

## Nutrition Statistics
An additional feature provided by the shortcut is to generate charts and graphs based on your nutrient and calorie consumption. This is done with the use of Charty  (download [here](https://apps.apple.com/ca/app/charty-for-shortcuts/id1494386093)). You can access the statistics from *History and Stats > Statistics with Charty* where you will be provided with the following options:

`PICHERE: Nutrient statistics options`

The **Nutrient Breakdown** generates pie charts that shows how much each nutrient contributes to your overall diet. Two pie charts are generated, one for nutrients measured in grams, and nutrients measured in milligrams. By separating the two, larger nutrients do not overshadow trends in the smaller ones.

`PICHERE: Example pie charts`
![Nutrient Breakdown (Gram Nutrients)](./images/nutr_breakdown_big.png?raw=true)

![Nutrient Breakdown (MilliGram Nutrients)](./images/nutr_breakdown_small.png?raw=true)


Each nutrient is assigned a specific color that is used in every generated pie chart.

You can generate a nutrient breakdown for a specific date, generate them for multiple dates, or generate the average for a given date range.

The **Calorie Breakdown** plots your total daily calories for each day in the date range, along with the calculated average. Calorie breakdowns are included with *Nutrient Breakdown for Dates*, but can be specifically generated with *Calorie Breakdown For Dates*.

`PICHERE: Example calorie breakdown`

## Food Backlog
Sometimes, you may wish to log foods on Apple devices that do not have the Apple Health app e.g. the iPad (though this will change with iOS 17). The shortcut is still functional for these devices, but instead of logging foods directly to Health, they are saved to the backlog.

The backlog is a list of foods along with their date and time (saved to Other/backlog.json) which will be automatically cleared when next on a device with an Apple Health app. This is possible because the backlog is saved in your storage folder which is on iCloud.
