import json


with open('gui_strings_en.json', 'r') as file:
	dix = json.load(file)


for k in dix.keys():
	dix[k] = '__{}'.format(dix[k])


print('Done')
with open('temp.json', 'w') as file:
	json.dump(dix, file, indent=4)