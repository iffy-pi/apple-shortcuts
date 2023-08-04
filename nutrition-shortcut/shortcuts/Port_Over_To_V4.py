shortcuts = {
    'PFS': 'Port Over Saved Foods To v4',
    'PFH': 'Port Over Food History To v4'
}

Menu("You'll need to install the helper shortcuts"):
    case 'Get Install Links':
        text = f'''
            ...
        '''# installation links
        note = CreateNote(note)
        OpenNote(note)
        StopShortcut()
    case "I've installed the shortcuts":
        pass

Menu("The conversion process is automated...")
    case "Open Settings":
        OpenApp("Settings")
        StopShortcut()
    case "I've set the settings":
        pass

Alert("Conversion progress is not automated...")

Notification("0/5 Steps Completed")

RunShortcut(shortcuts['PFS'])

Notification("3/5 Steps Completed")

RunShortcut(shortcuts['PFH'])

Notification("4/5 Steps Completed")

dix = Dictionary(Text(...)) # shortcutNames.json
SaveFile(dix, "FLS/Other/shortcutNames.json", overwrite=True)

delete = [
    "Other/shortcutDix.txt",
    "Other/backlog.txt",
    "Other/backtag.txt",
    "Other/Backlog.txt",
    "Other/shortcutLinksDix.txt",
    "History/foodHistoryDix.txt",
    "History/foodHistory.txt",
    "History/HistoryIDs.txt"
]

for d in delete:
    file = GetFile(f"FLS/{d}", errorIfNotFound=False)
    DeleteFile(file)

SaveFile("FLS", "Nutrition_Shortcut_Storage_Folder_Name.txt", overwrite=True)

Notification("5/5 Steps Completed")

