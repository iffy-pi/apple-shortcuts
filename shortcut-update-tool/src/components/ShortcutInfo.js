import { useState } from "react"
import DropDownSelector from "./DropDownSelector"
import Button from "./Button"

const ShortcutInfo = ({ shortcuts, selectedShortcuts, setShortcuts, index, onRemove }) => {
    const [ version, setVersion ] = useState('')

    const updateShortcutInList = (newObject) => {
        setShortcuts([...(selectedShortcuts.slice(0, index)), newObject, ...(selectedShortcuts.slice(index+1))]);
    }

    const updateVersion = (newVersion) => {
        const newObject = { ...selectedShortcuts[index], version:newVersion}
        updateShortcutInList(newObject);
    }

    const updateLink = (newLink) => {
        const newObject = { ...selectedShortcuts[index], link:newLink}
        updateShortcutInList(newObject);
    }

    const updateId = (selectedIndex) => {
        const newObject = { ...selectedShortcuts[index], id:shortcuts[selectedIndex].id, version:shortcuts[selectedIndex].version}
        updateShortcutInList(newObject);
        setVersion(shortcuts[selectedIndex].version)
    }

    return (
        <div className="shortcut-info">
            <label for={"shortcut.dropdown."+index}>Shortcut to Update:   </label>
            <DropDownSelector options={shortcuts.map(x=> x.name)} onSelect={updateId}/>
            <br></br>
            <label for={"shortcut.version."+index}>New Version (Cur={version}):   </label>
            <input type="text" id={"shortcut.version."+index}
            value={selectedShortcuts[index].version} onChange={(e) => updateVersion(e.target.value)}/>
            <br></br>
            <label for={"shortcut.link."+index}>New Link:   </label>
            <input type="text" id={"shortcut.link."+index}
            value={selectedShortcuts[index].link} onChange={(e) => updateLink(e.target.value)} size={Math.max(20, selectedShortcuts[index].link.length)}/>
            <br></br>
            <Button buttonText="Remove" onClick={() => onRemove(index)}/>
        </div>
    )
}

export default ShortcutInfo