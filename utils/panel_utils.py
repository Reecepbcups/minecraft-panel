from utils.cosmetics import cprint, cfiglet, cinput
import traceback as tback
import sys




class Panel_Feedback:

    def __init__(self, debugmode, feedback, pause):
        self.debugmode = debugmode
        self.feedback = feedback
        self.pause = pause
    

    def print_stack_trace(self, exception: Exception):
        if not self.feedback:
            return

        if self.debugmode:
            self.clear()
            cprint("&4ERROR OCCURED")
            cprint("&4-------------------------")
            tback.print_exc()
            cprint("&4-------------------------")
        else:
            cprint("&4"+str(type(exception).__name__))
            cprint("&4"+str(exception.args))
        self.pause_panel()


    def pause_panel(self):
        if self.pause:
            input("Press Enter To Continue...")


    def clear(self):
        # Time differential on tests
        #os.system("clear") -> 0.0015304088592529297
        #print(\033c) -> 3.075599670410156e-05
        # Using a faster method leads to smoother and quick transitions from panel screen
        print("\033c")


class Panel_Interface():

    def __init__(self, choices: dict, figlet: str="Interface", figletColor: str="&6", footnote: str=None, *args):
        self.feedback: Panel_Feedback = Panel_Feedback(True, True, True)
        self.figlet: str = figlet
        self.figletColor: str = figletColor
        self.footnote: str = footnote
        arglist = list(args)
        if("self" in arglist):
            arglist.insert(arglist.index("self"), self)
            arglist.remove("self")
        self.args = tuple(arglist)
        self.choices = choices


    def launch(self):
        while True:
            self.feedback.clear()

            if self.figlet is not None:
                cfiglet(self.figletColor, self.figlet)

            if self.footnote is not None:
                cprint(self.footnote)
                
            self.print_arguments(self.choices)

            user_in = cinput(">> ")

            try:
                self.choices[user_in][1](*self.args)
            except KeyError as ker:
                if user_in == 'None':
                    sys.exit()
                if user_in == '\x18':
                    return
                self.feedback.print_stack_trace(ker)

            self.feedback.clear()
                
    def close(self):
        self.running = False

        
    def print_arguments(self, index=0):
        for key in self.choices:
            cprint(f'&a[{key}]: {self.choices[key][0]}')
            

class FileInstallException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
