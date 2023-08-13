import logo from './logo.svg';
import './App.css';
import { useState } from 'react'
import UpdateShortcuts from './components/UpdateShortcuts';
import Button from './components/Button';
import { apiJSONFetch } from './basefunctions';

function App() {
    const [ updatesPath, setUpdatesPath ] = useState('')
    const [ issueNo, setIssueNo ] = useState(0)
    const [ genTest, setGenTest ] = useState(false)
    const [ promote, setPromote ] = useState(false)
    const [ updates, setUpdates ] = useState(null)

    const getUpdatesFile = async () => {
        try {
            const res = await apiJSONFetch('get-updates-file', 'POST', {}, {path: updatesPath})

            if (!res.success ) {
                if ( res.reachedServer ) throw new Error(res.content.message)
                else throw new Error(`Unknown Error: ${res.content}`)
            }
            
            if ( !res.success ) throw new Error('Invalid response: '+res)

            alert('Successfully retrieved updates file')
            setUpdates(res.content)
            setGenTest(true);
            setPromote(false);

        } catch ( error ){
            alert(error.message)
        }
    }

    const doPromotion = async() => {
        try {
            const res = await apiJSONFetch('promotion', 'POST', {}, {updatesPath: updatesPath})

            if (!res.success ) {
                if ( res.reachedServer ) throw new Error(res.content.message)
                else throw new Error(`Unknown Error: ${res.content}`)
            }
            
            if ( !res.success ) throw new Error('Invalid response: '+res)

            alert('Promotion Completed Successfully!')
            setUpdates(res.content)
            setGenTest(true);
            setPromote(false);

        } catch ( error ){
            alert(error.message)
        }
    }

    return (
        <div>
            <h1>Update Tool</h1>
            <label for="updatesjsonpath">Updates.json Path</label>
            <br></br>
            <input type="text" id="updatesjsonpath"
            value={updatesPath} onChange={(e) => setUpdatesPath(e.target.value)} size={Math.max(10, updatesPath.length)}/>
            <br></br>
            <label for="issueno">Issue No.</label><br></br>
            <input type="number" id="issueno"
            value={issueNo} onChange={(e) => setIssueNo(e.target.value)}/><br></br>
            
            <Button buttonText="Generate Test Updates" onClick={() => {
                getUpdatesFile();
            }}/>
            <Button buttonText="Promote Updates" onClick={() => {
                setGenTest(false);
                setPromote(true);
                doPromotion();
            }}/>
            
            { genTest && <UpdateShortcuts updatesPath={updatesPath} updates={updates} issueNo={issueNo} />}
        </div>
    );
}

export default App;
