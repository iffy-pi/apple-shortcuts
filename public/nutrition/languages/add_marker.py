import json


with open('gui_strings_en.json', 'r') as file:
	dix = json.load(file)


for k in dix.keys():
	dix[k] = '*{}'.format(dix[k])


print(json.dumps(dix, indent=4))