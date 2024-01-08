notifs = {
	'0': {
		'title': 'Charge Limiting Disabled',
		'body': 'There are no charge limitations'
	},

	'1': {
		'title': 'Charge Limiting Enabled',
		'body': 'Charging will be limited when battery goes above 80%'
	}
}


confirmation = {
	'0': {
		'prompt': 'Charge Limiting is currently enabled. Disable it?',
		'change': 'Disable charge limiting',
		'keep': 'Keep Enabled'
	},

	'1': {
		'prompt': 'Charge Limiting is currently disabled. Enable it?',
		'change': 'Enable charge limiting',
		'keep': 'Keep Disabled'
	},
}

params = Dictionary(ShortcutInput)

# sets the switch value to the params input
if params['set'] is not None:
	switch = Text(params['set'])

# when changeTo key is used, current switch value is compared against the params input
# If they differ, the user is presented with a prompt to change the switch value to the input or keep it as it is
if params['changeTo'] is not None:
	switch = Text(params['changeTo'])
	text = Text(GetFile(From='Shortcuts', 'Charge Limiter/limitedEnabled.txt'))
	if text == switch:
		StopShortcut()

	dix = confirmation[switch]
	Menu(dix['prompt']):
		case f'{dix['change']}':
			# pass through to set switch value
			pass
		case f'{dix['keep']}':
			StopShortcut()

if switch is not None:
	SaveFile(To='Shortcuts', switch, 'Charge Limiter/limiterEnabled.txt', overwrite=True)
	dix = notifs[switch]
	Notification(title=dix['title'], body = dix['body'])
