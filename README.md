# apple-shortcuts
A repository for handling the updates and versioning of my apple shortcuts

## Action Pipeline
- Shortcut versions are stored in versioning folder
- Configured static HTML github workflow to deploy on changes to contents of versioning folder
- Versioning folder contains JSONs

## Other Information

- Update JSONs
	- See formats provided below
	- In that case, naming can be simple legible names e.g. pushbullet.json, pullbullet.json
	- Shortcut frameworks
		- Will have a main/root shortcut which contains information required for versioning
		- Each shortcut in the framework will have a unique ID within the framework
		- Root shortcut will contain:
			- Dictionary that maps unique ID to shortcut name
			- Dictionary that maps unique ID to shortcut version
		- Root shortcut can then query its update json
		- Check if major version number has been updated
		- If updated, then cross reference to identify which inner shortcut version needs to be updated and aggregate the information which is shown at end of the shortcut
		- Can even make it some sort of weekly or monthly check per se
- JSON format?

We know which shortcuts are framework and which shortcuts are independent and sicne we are the ones writing the shortcut, we will know what fields to access.

Therefore we can have two JSON formats and just note which type is being used for maintenance

Independent shortcuts:

```json
{
	// indie shortcuts dont really need an ID as they are the only one of their kind, but its good practice incase they become part of a framework
	"id": "id",
	"version": { 
		"str" : "3.2.4",
		// number version allows for efficient comparison
		// grouped with version to allow for efficient comparisons
		"num" : 324
	},
	"name": "My Shortcut",
	"type": "independent",
	"link": "<icloud link>",
	"release_logs": "release logs",
	"release_time": "some date time format"
}
```

Framework shortcuts

```json
{
	// major version number is just used to manage checks
	// shortcut only cross refs children if 
	// root shortcut has framework verison
	"version": { 
		"str" : "3.2.4",
		// number version allows for efficient comparison
		// grouped with version to allow for efficient comparisons
		"num" : 324
	},
	
	"name": "<framework name>",
	"type": "framework",
	// framework types will always have a list of children
	"children": [
		{
			// id is required for framework shortcuts
			// root shortcut will have a dictionary that maps ids to vcomps and shortcut names
			"id": "<id>",
			"version": { 
				"str" : "3.2.4",
				// number version allows for efficient comparison
				// grouped with version to allow for efficient comparisons
				"num" : 324
			},
			"name": "name",
			"link": "<icloud link>",
			"type": "child", // helps identify what type of object this is
			"release_logs": "Some information about the current release",
			"release_time": "some date time format"
		},
		// ...
		// can have multiple children for shortcut frameworks
		// compare ids of children if major version has changed
	]
}
```

What about documenting the history of updates?

Keep it separate from the update JSON, so that it doesn't bog down latency.

Could use a specific naming format for the update JSON and the history json
- well since each shortcut has their own folder, we can give them the standard names `updates.json` and `history.json`.

Format of history json:

```json
[
	// each object is an update object
	{},
]
```
