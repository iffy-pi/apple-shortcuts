import { useState, version } from "react"
import DropDownSelector from "./DropDownSelector"
import ShortcutInfo from "./ShortcutInfo"
import Button from "./Button"
import { apiJSONFetch } from "../basefunctions"


const UpdateShortcuts = ({ updatesPath, updates, issueNo }) => {
    // each object has the shortcut child id, the icloud link and the version
    const [ selectedShortcuts, setShortcuts ] = useState([])
    const [ verMapText, setVerMapText ] = useState('')
    const [ showInstaller, setShowInstaller ] = useState(false)
    const [ version , setVersion ] = useState('')
    const [ link, setLink ] = useState('')
    const [ showRelease, setShowRelease ] = useState(false)
    const [ releaseNotes, setReleaseNotes ] = useState('')


    const addNew = () => {
        setShortcuts([ ...selectedShortcuts, {id:-1, version:'', link:''}])
    }

    const removeFromSelected = (index) => {
        setShortcuts(selectedShortcuts.filter((x, i)=> i != index))
    }

    const editSelectedShortcuts = async () => {
        // API call to:
        // edit the version numbers in the comments of the shortcuts
        // edit shortcut version and update link in the testupdates.json (saving it)
        // returns the childVers dictionary rendered below
        const req = {
            updatesPath: updatesPath,
            shortcuts: selectedShortcuts
        }
        try {
            const res = await apiJSONFetch('edit-shortcuts', 'POST', {}, req)

            if (!res.success ) {
                if ( res.reachedServer ) throw new Error(res.content.message)
                else throw new Error(`Unknown Error: ${res.content}`)
            }
            
            if ( !res.success ) throw new Error('Invalid response: '+res)

            alert('Successfully edited the shortcuts!')
            setVerMapText(res.content.verMap)
        } catch ( error ){
            alert(error.message)
        }
    }

    const updateInstallerPyFile = async () => {
        // API call to:
        // Update the installer python file with the new child version dictionary 
        // Update installer to new verison number
        // Update test updates with the new version and instaler link
        const req = {
            updatesPath: updatesPath,
            version: version,
            link: link
        }
        try {
            const res = await apiJSONFetch('update-installer', 'POST', {}, req)

            if (!res.success ) {
                if ( res.reachedServer ) throw new Error(res.content.message)
                else throw new Error(`Unknown Error: ${res.content}`)
            }
            
            if ( !res.success ) throw new Error('Invalid response: '+res)

            alert('Successfully updated the installer!')
            setShowRelease(true)
        } catch ( error ){
            alert(error.message)
        }
    }

    const updateReleaseNotes = async () => {
        // API call to:
        // Update release notes to the given content
        // Update the release date to the current date
        const req = {
            updatesPath: updatesPath,
            releaseNotes: releaseNotes,
        }
        try {
            const res = await apiJSONFetch('update-release-notes', 'POST', {}, req)

            if (!res.success ) {
                if ( res.reachedServer ) throw new Error(res.content.message)
                else throw new Error(`Unknown Error: ${res.content}`)
            }
            
            if ( !res.success ) throw new Error('Invalid response: '+res)

            alert('Successfully updated the release notes!')
        } catch ( error ){
            alert(error.message)
        }
    }

    return (
        <div className="chat-src-panel">
            <h2>Update Individual Shortcuts</h2>
            {
                selectedShortcuts.map((s, i) => 
                    <ShortcutInfo shortcuts={[{name: 'None Selected', id: -1}, ...updates.children]} selectedShortcuts={selectedShortcuts} 
                    setShortcuts={setShortcuts} index={i} key={i} onRemove={removeFromSelected}/>)
            }
            <Button buttonText="Add" onClick={addNew}/>
            <br></br><br></br>
            <Button buttonText="Edit Shortcut PyFiles and Test Updates" onClick={editSelectedShortcuts}/>
            {
                ( verMapText != '' ) && 
                <div>
                    <h2>Update The Actual Installer Shortcut</h2>
                    <p>The child version mapping is in the text box below</p>
                    <p>Use it to update the dictionary and the version number in the actual installer shortcut</p>
                    <textarea readonly 
                    name="verMap" 
                    rows="5" cols="45" 
                    value={verMapText} />
                    <br></br>
                    <Button buttonText="I've updated the version dictionary and version number in actual installer shortcut" onClick={() => setShowInstaller(true)}/>
                </div>
            }
            <br></br>
            {
                showInstaller && 
                <div>
                    <h2>Update Installer PyFile and Test Updates</h2>
                    <label for="version">New Framework Version:   </label>
                    <input type="text" id="version"
                    value={version} onChange={(e) => setVersion(e.target.value)}/>
                    <br></br>
                    <label for="installer-link">Installer Link:   </label>
                    <input type="text" id="installer-link"
                    value={link} onChange={(e) => setLink(e.target.value)}/>
                    <p>When the button below is clicked, the pyfile will be automatically updated</p>
                    <Button buttonText="Update Installer PyFile and Test Updates" onClick={updateInstallerPyFile}/>
                </div>
            }
            <br></br>
            {
                showRelease &&
                <div>
                    <h2>Update Release Notes and Release Date</h2>
                    <p>Enter Release notes in the text box below</p>
                    <textarea 
                    name="verMap" 
                    rows="10" cols="60" 
                    value={releaseNotes} onChange={(e)=> {setReleaseNotes(e.target.value)}} />
                    <Button buttonText="Update Release Notes" onClick={updateReleaseNotes}/>
                </div>
            }
        </div>
    )
}

export default UpdateShortcuts