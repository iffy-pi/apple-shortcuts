# Functions used within the script that aren't actual shortcuts but instead just a shorthand for the shortcut actions that are used there
def textToContacts(var):
    text = Text(var)
    renamedItem = SetName(var, 'vcard.vcf')
    return GetContacts(renamedItem)

def convertTextFileToJSON():
    GetFile(f"{folder}/{filename}.txt")
    RenameFile(f"{filename}.json")
