UDPATES AND CHANGES:
- File/Strucutral Changes:
    - JSON Everything
        - All "*dix.txt" files are now converted to JSON,
        - This includes Food files, and any other relevant dictionaries
        - Done with port over to JSON

    - Food IDs
        - Each food is assigned a unique ID to track it within the system
        - The shortcut Generate Food ID is used to generate the food ID
        - ID is tracked with FLS/Other/nextFoodId.txt

    - New backlogging:
        - Backlog is now stored in new format at FLS/Other/backlog.json
        - Backlog is managed in Nutrition function as usual, but is now deleted when it is empty
        - Log algorithm puts stuff in the backlog
        - Storage format:
            {
                backlog: [
                        {
                            Date: '...',
                            Food: ...,
                        },
                        ...
                    ]
            }

    - History Cache
        - Improve logging speeds by adding a history cache
        - Log Algorithm shortcut puts things in cache, and main shortcut clears it at end of execution
        - Makes sure that large size of history file does not slow logging process down
        - History Cache is saved to FLS/History/foodHistoryCache.json,
        - Format:
            {
                cache : [
                    food: ...,
                    servings: ...,
                    cals: ...,
                    date: ...,
                    time: ...,
                    id: ...
                ]
            }

    - Refactored Food History
        - Food history is revamped from FLS/History/foodHistoryDix.txt => FLS/History/foodHistory.json
        - Has new format, see PortOverFoodHistory
        - Used in the main shortcut when clearing cache

    - Environment Variables
        - JSON dictionary stored in FLS/Other/env.json
        - Is formatted:
            {
                '<env var name>' : '<env var value>'
            }
        - Used to contain flags or values that we would like to share between shortcuts:
            - Share hasHealthApp between Nutrition and Log Algorithm

    - New Recents Format
        - Foods are named food_<food ID>.json
        - Foods are now sorted by date when getting recents
        - Shortcut Port Over Recents converts files to new format

    - New Presets Format
        - There is a file presets.json that maintains access times of Presets
            {
                '219' : {
                    'date': '2023-06-09 09:41' # the last time the food was accessed
                },
                < more food IDs>
            }
        - Also have a vcardCache.txt, which is used to cache the vcards used in selecting presets. It is of the format:
            <vcard for food where name=food name, org = serving size, notes = food id>
        - Foods in Presets folder are named in food_<food ID>.json
        - Shortcut Port Over Presets converts files to new format

- Shortcut Changes
    - Conversion Shortcuts
        - Port Over Food History
            - Converts old foodHistoryDix.txt format to foodHistory.json

        - Port Over Foods
            - Updates food files to JSON
            - Adds a unique ID so they can be identified

        - Generate Food ID
            - Generates a unique id for each food object

        - Port Over Recents and Presets
            - Converting to new format for recents and presets

    - Added Shortcuts
        - Generate Food ID
            - Generates a unique id for each food object

    - Removed Shortcuts
        - Get History On
        - Plot Day Summary
        - Plot Week Summary
        - Day Summary
        - Week Summary
        - Add Preset
        - Correct Dictionary
        - 

    - Updated Shortcuts
        - Nutrition
            - Improved methods to check when a device has a health app.
            - Improved backlog clearing
            - Added history cache clearing

        - Log Algorithm
            - Improved logging speeds by minor refactoring of code
            - Implemented history caching using new history cache files

        - Food History
            - Refactored to handle new food history format
            - Other improvements are under the hood

        - Search Algorithm
        - Get Recents
        - Add Recent
        - Get Preset
        - Make Preset
        - Remove Preset
        - Edit Preset


CURRENT STATE:
    - Current file structure (FLS):
        - Presets
            - presetNames.txt : For names of presets
            - Foods
                - Food JSON files in the format of food_{food id}.json

        - Recents:
            - recentNames.txt : For names of recents foods
            - Foods:
                - Food JSON files in the format of food_{food id}.json

        - Barcodes
            - barcodesInfo.json : Maps barcodes to food IDs

            - barcodeDix.txt : Maps barcodes to food names
            - Foods
                - Food JSON files in the format of food_{food id}.json
        
        - History
            - foodHistoryDix.txt => foodHistory.json
            - foodHistoryCache.json

        - Other
            - backlog.txt and backtag.txt => backlog.json
            - nextFoodId.txt : Generates next Unique ID for food
            - lastUpdateCheck: : Date of last checked update
            - nutriKeys.txt : Keys in the food dictionary that are the nutrients
            - env.json : Stores environment variables
            - shortcutNames.json : Stores the name of shortcuts which are used in Run Shortcut actions, ideally should allow user to configure it
                See saved version
                // The porting over shortcuts
                {
                    "Port Over Food History": "Port Over Food History",
                    "Port Over Foods": "Port Over Foods",
                    "Port Over Recents and Presets": "Port Over Recents and Presets",
                }
                // deperectated
                {
                    "Correct Dictionary":"Correct Dictionary",
                    "Number Converter":"Number Converter",
                    "Make Food Item":"Make Food Item",
                    "Save Env Vars": "Save Env Vars",
                    "Add Preset":"Add Preset 1.1",
                }

            - shortcutLinksDix.txt : ? Maps shortcuts to their icloud links

Tutorial: https://github.com/iffy-pi/apple-shortcuts/blob/main/nutrition-shortcut/Tutorial/Tutorial.md