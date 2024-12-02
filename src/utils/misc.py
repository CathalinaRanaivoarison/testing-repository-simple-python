def capitalize_name(name: str) -> str:
    return "".join([subname.capitalize() for subname in name.split(" ")])
