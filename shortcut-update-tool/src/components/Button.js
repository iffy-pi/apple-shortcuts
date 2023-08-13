const Button = ({buttonText, onClick, className}) => {
    return (
        <button
        onClick={onClick}
        className={className}>
            {buttonText}
        </button>
    )
}

Button.defaultProps = {
    buttonText: "Click Me!",
    onClick: () => alert("I've been clicked!"),
    className: ""
}

export default Button