import pyfiglet

color_dict = {
    '&1': '\u001b[38;5;4m',
    '&2': '\u001b[38;5;2m',
    '&3': '\u001b[38;5;6m',
    '&4': '\u001b[38;5;1m',
    '&5': '\u001b[38;5;5m',
    '&6': '\u001b[38;5;3m',
    '&7': '\u001b[38;5;7m',
    '&8': '\u001b[38;5;8m',
    '&0': '\u001b[38;5;0m',
    '&a': '\u001b[38;5;10m',
    '&b': '\u001b[38;5;14m',
    '&c': '\u001b[38;5;9m',
    '&d': '\u001b[38;5;13m',
    '&e': '\u001b[38;5;11m',
    '&f': '\u001b[38;5;15m',
    '&r': '\u001b[0m',
}

def color(text):
    '''
    Translates the color codes in text to teh color codes in colors
    '''
    text = text.replace("§", "&")
    formatted = ""
    i = 0
    while i in range(0, len(text)):
        if text[i:i+2] in color_dict:
            formatted += color_dict[text[i:i+2]]
            i += 1
        else:
            formatted += text[i]
        i += 1
    return formatted + color_dict['&r']


def cfiglet(clr, figlet):
    print(color(clr+pyfiglet.figlet_format(figlet)))


def cprint(text):
    print(color(text))

def cinput(text):
    try:
        return input(color(str(text)))
    except KeyboardInterrupt:
        return str("None")