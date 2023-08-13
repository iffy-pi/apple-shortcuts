const API = 'http://localhost:5000'


// returns true if file is a good upload and false if not
const goodChatFileUpload = (file) => {
    if ( file.type === "" || !file.type.startsWith('text/') ) return false
    return true
}

const readFileToText = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.addEventListener('load', () => resolve(reader.result))
    reader.addEventListener('error', () => reject('Reading file failed'))
    reader.readAsText(file)
})

/*
    Returns a Response object for a given API call, repsonse object is of the format:
    {
        success: true or false based on result of call
        status: http status for the call
        content: contains JSON for success call or client side error call, contains text for other failures
    }
*/
async function apiJSONFetch(apiPath, method, headers, body ) {

    const request = {
        method: method
    }

    if ( headers !== null && headers !== {} ){
        request.headers = headers
    }

    if ( body !== null ){
        if ( request.headers['content-type'] === undefined ){
            request.headers['content-type'] = 'application/json'
            request.body = JSON.stringify(body)
        }
    }
    // Make the request
    const res = await fetch(
        `${API}/${apiPath}`,
        request
    )

    const response = {
        success: true,
        reachedServer: true,
        status: res.status
    }

    // grpStatus to check status range
    const statusGrp = Math.floor( res.status / 100)

    if ( statusGrp !== 2 ){

        // something happened
        response.success = false

        if ( statusGrp === 4 || statusGrp === 5 ) {
            // Client side and server side errors mean the server gave us a response
            // Server always responds in specific JSON error format, so we can accurately pull the information

            response.content = await res.json()

        } else {
            // We dont know what happened, just pull the text if we can
            response.reachedServer = false
            response.content = await res.text() 
        }
        return response
    }

    // check if we have json which we should have
    response.content = await res.json()

    return response
}

// Parse the text into the json format
const chatTextToChatJSON = ( transcriptText ) => {
    const lines = transcriptText.split('\n')

    const parties = []
    const messages = []
    let partiesFound = null
    let curParty = null
    let curPartyID = -1

    for ( let i=0; i < lines.length; i++ ) {
        const line = lines[i].trim()
        if ( line === '' ) continue;

        // get the party that sent the message if it is a party identifier line
        partiesFound = line.match(/^[a-zA-z][a-zA-z]*:/) 
        if ( partiesFound != null  ) {
            // Removing colon from party name
            curParty = partiesFound[0].substring(0, partiesFound[0].length-1)

            curPartyID = parties.indexOf(curParty)

            if ( curPartyID === -1 ) {
                curPartyID = parties.length
                parties.push(curParty)
            }
            continue;
        }

        if ( curPartyID === -1) throw new Error('No sender labels found. See expected format.')

        // Add to messages if it is not already present
        messages.push({
            id: messages.length,
            pid: curPartyID,
            text: line
        })
        
    }

    if ( messages.length === 0 ) throw new Error('No messages found in the transcript')

    // if ( parties.length > 2 ) throw new Error('Chat summarization is only supported for two parties!')

    const partiesObj = []
    parties.forEach((p, i) => { partiesObj.push({ id: i, name: p })})

    const parsedChat = {
        config: {
            parties: partiesObj
        },
        messages: messages
    }

    return parsedChat

}

const ContentStates = {
    unset: 0,
    loading: 1,
    set: 2
}

const InputOptions = {
    def: 0,
    file: 1,
    text: 2
}


export {
    goodChatFileUpload,
    readFileToText,
    apiJSONFetch,
    chatTextToChatJSON,
    ContentStates,
    InputOptions
}