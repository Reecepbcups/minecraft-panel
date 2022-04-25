from utils.panel_utils import Panel_Interface
from utils.cosmetics import cprint, cinput


def add(panel: Panel_Interface):
    num1 = cinput("&aInput a number you want to add: ")
    num2 = cinput("&aInput the number you want to add to the first: ")
    cprint(f'&6{int(num1)+int(num2)}')
    panel.feedback.pause_panel()


def subtract(panel: Panel_Interface):
    num1 = cinput("&aInput a number you want to subtract: ")
    num2 = cinput("&aInput the number you want to subtract from the first: ")
    cprint(f'&6{int(num1)-int(num2)}')
    panel.feedback.pause_panel()


choices = {
    '0': ["Add", add],
    '1': ["Subtract", subtract],
}

def on_call(headPanel: Panel_Interface):
    panel = Panel_Interface(choices, "Example", "&6", "An example footnote", "self")
    panel.launch()