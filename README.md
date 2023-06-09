# apple-shortcuts
A repository for handling the updates and versioning of my apple shortcuts, and also draft versions.

**NEXT SHORTCUT ID:**
```
4
```

## Creating a Versioned Shortcut
1. Create a folder in `versioning/` for the shortcut, e.g. `myshortcut`
2. Implement versioning system within the shortcut (see [Configuring Update System In Shortcut](#configuring-update-system-in-shortcut)). If new, set initial version to be 1.0.
3. Copy the shortcut's icloud link.
4. Create a post on routinehub.co for the shortcut. Publish using version 0.0
5. Create the `updates.json` and `history.json` in the `versioning/myshortcut` (see [Configuring Versioning System For Shortcut](#configuring-versioning-system-for-shortcut)).
6. Push JSON files to remote.
7. Publish new version of shortcut on routinehub with the version 1.0


## Udpating a Version Shortcut
1. Make changes in shortcut
2. Update version number in shortcut
3. Write out the changelog for this new update somewhere (will need it later)
4. Copy shortcut's icloud link
5. Create new version with the new version number on RoutineHub, use the changelog wrtten earlier.
6. Copy the current version of the shortcut's `updates.json`, and prepend it to the list in `history.json`.
7. Update the shortcut's `updates.json`
	- `version` should match the new shortcut version
	- Update shortcut link
	- Update release notes (use changelog and replace newlines with `\\n`)
	- Update release time
8. Run shortcut to double check update mechanism
	- Revert to shortcut previous version and test that the update has been deployed

**If there are shortcut bugs, simply fix them and then update the icloud links in the RoutineHub version and the GHP version**.

## Configuring Versioning System For Shortcut
The version system works with two files under `versioning/myshortcut`. `updates.json` contains the latest version of the shortcut, while `history.json` contains the previous versions of the shortcut. 

### `updates.json`

The format for `updates.json` varies based on the shortcut type: Independent and Framework. Independent shortcuts are shortcuts that only run and manage themselves. This means that they do not have any helper or inner shortcuts that they use and that need to be tracked.

Framework shortcuts have inner shortcuts and helper shortcuts. For framework shortcuts, there will always be an updater shortcut which will contain the updating system for the shortcuts in the framework. The updater shortcut handles versioning for all shortcuts in the framework.

Independent shortcuts use the format:

```json
{
	// Remember to remove the comment and update the fields when copy pasting!
	"id": "<id>",
	"version": 3.24,
	"name": "My Shortcut",
	"type": "independent",
	"link": "<icloud link>",
	"rhub": "https://routinehub.co/shortcut/15515",
	"updateLink": "https://iffy-pi.github.io/apple-shortcuts/versioning/myshortcut/updates.json",
	"releaseNotes": "...",
	"releaseTime": "2023-06-09"
}
```

- `id`           : The versioning ID of the shortcut, which is pulled from the ID counter above.
- `version`      : The version number for the shortcut and is at most a double e.g. `1.11`.
- `name`         : The actual shortcut name.
- `type`         : The shortcut type, which is set to independent.
- `link`         : The icloud link for the shortcut.
- `rhub`         : The RoutineHub link (**without the ending forward slash**).
- `updateLink`	 : The link to updates for the shortcut.
- `releaseNotes` : The notes for the current release, these can be multiple lines separated by an escaped newline character `\\n`.
- `releaseTime`  : The date for the release, using ISO 8601 formatting (`YYYY-MM-DD`).

Update Links are always of the format:
```
https://iffy-pi.github.io/apple-shortcuts/versioning/<SHORTCUT FOLDER NAME>/updates.json
```


Framework shortcuts have a similar format but introduces new fields:

```json
{
	// Remember to remove the comment and update the fields when copy pasting!
	"id": "<id>",
	"version": 3.24,
	"name": "<framework name>",
	"type": "framework",
	"rhub": "https://routinehub.co/shortcut/15515",
	"link": "<updater shortcut icloud link>",
	"updateLink": "https://iffy-pi.github.io/apple-shortcuts/versioning/myshortcut/updates.json",
	"releaseNotes": "...",
	"releaseTime": "2023-06-09",
	"children": [
		{
			"id": "<id>",
			"version": 1.24,
			"name": "name",
			"link": "<icloud link>",
			"type": "child",
		},
		// ...
		// can have multiple children for shortcut frameworks
		// compare ids of children if major version has changed
	]

}
```

The key differences are:
- The type is now `framework` instead of independent.
- `link` is now the updater shortcut's icloud link.
- It has the key `children`, which contains the other shortcuts in the framework.

`children` is a list of dictionaries, where each dictionary contains the information for a shortcut in the framework:
- `id` : The shortcuts ID from the ID counter.
- `version` : The shortcuts current version.
- `name` : The shortcut name.
- `link` : The shortcut link.
- `type` : Set to `child` to indicate the shortcut is a part of a framework.

The idea in this case is that the updater shortcut will use the information contained in `children` to determine what shortcuts need updating. For children, the `id` is essential, as it allows for efficient storing of data in dictionaries and such.

### `history.json`
This is used to maintain version history, and is simply just a JSON list of previous `updates.json` dictionaries. This helps track changes overtime.

```json
[
	// Most recent updates first
	{
		// updates.json object
		// ...
	},
	// ...
]
```

## Configuring Update System In Shortcut
Shortcuts will store their current version and a link to their updates page in a simple dictionary. At the end of execution, the shortcut queries the updates page and compares its version to the posted version. If it is less than the posted version, then the update process can begin.

Independent shortcuts only need to do this with themselves. Framework shortcuts will have the updater shortcut query the versions for each child shortcut to determine which shortcuts needs to change.

The pseudocode for the process can be experessed in shortcut-ish python.

### Independent Shortcut:
```python
# done at the beginning or end of the shortcut, which ever is preferred

updateInfo = {
	'updateLink' : '<updateLink from updates.json>',
	'version' : 1.02
}

updateRes = GetContentsOfURL(updateInfo['updateLink'])

if Number(UpdateRes['version']) > updateInfo['version']:
	date = Date(updateRes['releaseTime'])
	splitText = SplitText(updateRes['releaseNotes'], '\\n')
	
	text = f"""
		{updateRes['name']} Shortcut Update
		An update is available for this shortcut:
		{updateInfo['version']} ➡️ {updateRes['version']}

		🕦 Released:
		{date}

		✅ Install:
		{updateRes['link']}

		📝 Release Notes:
		{splitText}

		📬 Developer:
		Reddit: iffythegreat

		📚 Full Update History:
		{updateRes['rhub']}/changelog
	"""

	note = CreateNote(text)
	OpenNote(note)

```

### Framework Updater Shortcut:
```python
# Put in updater
'''
	Suppose we have two shortcuts in the framework
	ShortcutA at v1.8, id=41
	ShortcutB at v2.6, id=42
'''

updateInfo = {
	'updateLink' : '<updateLink from updates.json>',
	'version' : 1.02
}

updateRes = GetContentsOfURL(updateInfo['updateLink'])

# also now includes information about the children
childVers = {
	# just map ids to their versions
	'41': 1.8,
	'42': 2.6,
}

if Number(UpdateRes['version']) > updateInfo['version']:
	# collate information about the changed children
	newChildren = UpdateRes['children']

	updateText = []
	updateLinks = []

	# updater shorcut needs to be updated
	updateText.append(f"Updater Shortcut: {updateInfo['version']} ➡️ {updateRes['version']}")
	updateLinks.append(f"Updater Shortcut: {updateRes['link']}\n")

	for child in newChildren:
		curVer = childVers[ child['id'] ]
		if Number(child['version']) > curVer:
			updateText.append(f"{child['name']}: {curVer} ➡️ {child['version']}")
			updateLinks.append(f"{child['name']}: {child['link']}\n")

	date = Date(updateRes['releaseTime'])
	splitText = SplitText(updateRes['releaseNotes'], '\\n')
	
	text = f"""
		{updateRes['name']} Shortcut Update
		Updates are available for shortcuts:
		{updateText}

		🕦 Released:
		{date}

		✅ Install:
		{updateLinks}

		📝 Release Notes:
		{splitText}

		📬 Developer:
		Reddit: iffythegreat

		📚 Full Update History:
		{updateRes['rhub']}/changelog
	"""

	note = CreateNote(text)
	OpenNote(note)

```

### Actual Shortcut Examples
- Independent Shortcut:
- Framework Updater Shortcut: 

# Other Information
## Action Pipeline
- Shortcut versions are stored in versioning folder
- Configured static HTML github workflow to deploy on changes to contents of versioning folder
- Versioning folder contains JSONs