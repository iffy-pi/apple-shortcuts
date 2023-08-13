import { useState } from "react"

const DropDownSelector = ( {options, onSelect, name, id, className, disabled} ) => {
    // onSelect takes the selected option  index as a parameter
    // first option is always the first selected
    const [ selectedOptId, setSelectedOptId ] = useState(0)

    return (
        <select className={className} name={name} id={id}
        onChange={(e) => {
            setSelectedOptId(e.target.selectedIndex)
            onSelect(e.target.selectedIndex)
        }}
        defaultValue={options[selectedOptId]}
        disabled={disabled}
        >
            {
                options.map( (opt, i) => (
                    // ( i == selectedOptId ) ?
                    // <option value={opt} selected="selected">{opt}</option> :
                    // <option value={opt}>{opt}</option>
                    <option value={opt} key={i}>{opt}</option>
                ))
            }
        </select>
)
}

DropDownSelector.defaultProps = {
    name: 'dropdown',
    id: '',
    className: 'dropdown',
    disabled: false
}

export default DropDownSelector