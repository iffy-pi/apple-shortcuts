import json
import sys
import os
import re

def hasAllVars(line:str, varList):
	if varList is None:
		raise Exception(f'NO variables in var_en.json!')

	for v in varList:
		if line.find(v) == -1:
			return False
	
	return True

def getMissingVars(line:str, varList:list):
	missing = []
	for v in varList:
		if line.find(v) == -1:
			missing.append(v)

	return missing

def hasVars(line:str):
	return line.find('$') != -1

def checkVarPlacement(guiStrings, varJSON):
	for k in guiStrings.keys():
		if not hasVars(guiStrings[k]):
			continue
		if hasAllVars(guiStrings[k], varJSON.get(k)):
			continue
		raise Exception(f'Missing variables in var_en.json for {k}')


def generateToTranslateJSON(guiStringsFile=None):

	if guiStringsFile is None:
		guiStringsFile = os.path.join('..', 'gui_strings_en.json')

	with open(guiStringsFile, 'r') as file:
		guiStrings = json.load(file)

	with open('vars_en.json', 'r') as file:
		varJSON = json.load(file)

	checkVarPlacement(guiStrings, varJSON)

	newls = []

	# then generate the new
	translateStrings = {}
	for k in guiStrings.keys():
		if k.startswith('_'):
			print(f'Skipping {k}')
			continue
		if guiStrings[k].find('\n') != -1:
			newls.append(k)
			continue

		translateStrings[k] = guiStrings[k]

	outputPath = 'to_translate.json'

	with open(outputPath, 'w') as file:
		json.dump(translateStrings, file, indent=4)

	stdout = sys.stdout

	with open('newls.txt', 'w') as file:
		sys.stdout = file
		for k in newls:
			print('============================================================')
			print(f'Key: {k}')
			print('')
			print(guiStrings[k])
			print('============================================================')
		sys.stdout = stdout

	print('Skipped Due To New Lines:')
	for k in newls:
		print(f'   {k}')
	print('Values written to src/newl.txt')
	print('')
	print(f'Generated from {guiStringsFile}')
	print(f'Generated to {outputPath}')


def checkTranslatedJSON(jsonFile, noKeyCheck = False):
	with open('..\\gui_strings_en.json', 'r') as file:
		origGUIStrings = json.load(file)

	with open('vars_en.json', 'r') as file:
		varJSON = json.load(file)

	with open(jsonFile, 'r', encoding='utf-8') as file:
		newGUIStrings = json.load(file)

	# key check
	if not noKeyCheck:
		orgKeys = set(origGUIStrings.keys())
		newKeys = set(newGUIStrings.keys())

		keysNotInOriginal = newKeys - orgKeys
		keysNotInNew = orgKeys - newKeys

		exit = False

		if len(keysNotInOriginal) > 0:
			exit = True
			print('These keys are not in gui_strings_en.json:')
			for k in keysNotInOriginal:
				print(f'   {k}')

		print('')
		if len(keysNotInNew) > 0:
			exit = True
			print('The translated file is missing the following keys')
			for k in keysNotInNew:
				print(f'   {k}')

		if exit:
			return 1

	missingVars = False
	# var check
	for k in newGUIStrings:
		if not hasVars(newGUIStrings[k]):
			continue

		missing = getMissingVars(newGUIStrings[k], varJSON[k])

		if len(missing) == 0:
			continue

		print(f'Missing variables for key: {k}')
		for m in missing:
			print(f'- {m}')

		missingVars = True


	if missingVars:
		return 1

	print('All checks passed!')
	return 0


def jsonifyString(text):
	replacements = [
		('\\', '\\\\'),
		('"', '\\"'),
		('\n', '\\n'),
		('\t', '\\t'),
		#('/', '\\/'),
		('\r', ''),
	]
	for before, after in replacements:
		text = text.replace(before, after)
	return text




def makeJSONKeysFromNewlsFile(newlsFile=None):
	if newlsFile is None:
		 newlsFile = 'newls.txt'

	with open(newlsFile, 'r', encoding='utf-8') as file:
		lines = file.readlines()

	sep = '============================================================'

	
	keyset = []
	
	i = 0
	lineCnt = len(lines)
	while i < lineCnt:
		if lines[i].strip() == sep:
			key = lines[i+1].strip().replace('Key: ', '') 
			
			startLineIdx = i + 3
			itr = startLineIdx
			
			while lines[itr].strip() != sep:
				itr = itr + 1
			
			keyVal = ''.join(lines[startLineIdx: itr]).strip()
			
			keyset.append((key, keyVal))

			# move past the entry
			i = itr + 1

	with open('temp.txt', 'w', encoding='utf-8') as file:
		for key, val in keyset:
			file.write('"{}": "{}",\n'.format(
				key,
				jsonifyString(val)
			))

	print(f'Generated from {newlsFile}')
	print('Generated to temp.txt')
			


def testing(args):
	# with open('newls.txt', 'r', encoding='utf-8') as file:
	# 	text = file.read()
	
	# text = jsonifyString(text)

	# with open('temp.txt', 'w', encoding='utf-8') as file:
	# 	file.write(text)

	makeJSONKeysFromNewlsFile()

def main():
	args = sys.argv[1:]
	argLen = len(args)
	if argLen>0 and args[0] == 'gen':
		jsonFilePath = None
		
		if len(args) > 1:
			jsonFilePath = args[1]

		generateToTranslateJSON(jsonFilePath)
		return 0

	elif argLen>0 and args[0] == 'check':
		js = args[1]
		noKeyCheck = argLen > 2 and args[2] == 'subset'
		checkTranslatedJSON(js, noKeyCheck=noKeyCheck)
		return 0

	elif argLen>0 and args[0] == 'jnewls':
		newlsFile = args[1]
		makeJSONKeysFromNewlsFile(newlsFile = newlsFile)
		return 0

	elif argLen>0 and args[0] == 'format':
		js = args[1]
		with open(js, 'r', encoding='utf-8') as file:
			dix = json.load(file)

		with open(js, 'w', encoding='utf-8') as file:
			json.dump(dix, file, indent=4)

		print('Formatting completed!')
		return 0

	testing(args[1:])



if __name__ == '__main__':
	sys.exit(main())