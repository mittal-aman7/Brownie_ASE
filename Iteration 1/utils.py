def format_value_to_uint256(value):
    """Format a value (hex or int) to be uint256 compatible."""
    
    if isinstance(value, int):
        hex_string = hex(value)[2:]  # Convert integer to hex and strip off the "0x"
    elif isinstance(value, str) and value.startswith("0x"):
        hex_string = value[2:]  # Strip off the "0x" if present
    else:
        raise ValueError(f"Unsupported value type: {value}")
    
    return "0x" + hex_string.rjust(64, '0')


def call_contract_function(contract, function_name, *args):
    formatted_args = [
        format_value_to_uint256(arg) if isinstance(arg, (int, str)) and (isinstance(arg, int) or arg.startswith("0x")) else arg 
        for arg in args
    ]
    contract_function = getattr(contract, function_name)
    return contract_function(*formatted_args)
