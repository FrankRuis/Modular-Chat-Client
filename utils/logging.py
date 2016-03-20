def log(msg, *args):
    if not isinstance(msg, str):
        print(msg)
    else:
        print(msg.format(*args))
