import { useState } from "react"
import DropDownSelector from "./DropDownSelector"
import Button from "./Button"

const ShortcutInfo = ({ shortcuts, selectedShortcuts, setShortcuts, index, onRemove }) => {
    const [ version, setVersion ] = useState('')

    const updateVersion = (newVersion) => {
        const newObject = { ...selectedShortcuts[index], version:newVersion}
        setShortcuts([...(selectedShortcuts.filter((x, i) => i != index )), newObject])
    }

    const updateLink = (newLink) => {
        const newObject = { ...selectedShortcuts[index], link:newLink}
        setShortcuts([...(selectedShortcuts.filter((x, i) => i != index)), newObject])
    }

    const updateId = (selectedIndex) => {
        const newObject = { ...selectedShortcuts[index], id:shortcuts[selectedIndex].id, version:shortcuts[selectedIndex].version}
        setShortcuts([...(selectedShortcuts.filter((x,i) => i != index )), newObject])
    }

    return (
        <div className="shortcut-info">
            <label for={"shortcut.dropdown."+index}>Shortcut to Update:   </label>
            <DropDownSelector options={shortcuts.map(x=> x.name)} onSelect={updateId}/>
            <br></br>
            <label for={"shortcut.version."+index}>New Version (Cur={selectedShortcuts[index].version}):   </label>
            <input type="text" id={"shortcut.version."+index}
            value={selectedShortcuts[index].version} onChange={(e) => updateVersion(e.target.value)}/>
            <br></br>
            <label for={"shortcut.link."+index}>New Link:   </label>
            <input type="text" id={"shortcut.link."+index}
            value={selectedShortcuts[index].link} onChange={(e) => updateLink(e.target.value)}/>
            <br></br>
            <Button buttonText="Remove" onClick={() => onRemove(index)}/>
        </div>
    )
}

export default ShortcutInfo