def bool_eval(arg: str):
    if arg.lower() == "true":
        return True
    elif arg.lower() == "false":
        return False
    else:
        return None
