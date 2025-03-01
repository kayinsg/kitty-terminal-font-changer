from os import path, remove, getcwd
import subprocess

class FontMenu:
    
    @staticmethod
    def getTemporaryFile():
        return str(path.join(getcwd(), 'temporaryFile'))

    def __init__(self, fontCollection):
        self.fonts = fontCollection
        self.temporaryFile = FontMenu.getTemporaryFile()
        self.interface = FZFInterface(self.temporaryFile)

    def letUserPickFont(self):
        self.writeFontsToTemporaryFile()
        userSelectedFont = self.interface.fontPicker()
        remove(self.temporaryFile)
        return userSelectedFont

    def writeFontsToTemporaryFile(self):
        with open(self.temporaryFile , 'w') as file:
            for font in self.fonts:
                    file.writelines(f'{font}\n')

class FZFInterface:
    def __init__(self, temporaryFile):
        self.temporaryFile = temporaryFile

    def fontPicker(self):
       FZFInput = self.getTemporaryFileOutput()
       fontChosenByUser = self.displayFZFMenuToUser(FZFInput) 
       return fontChosenByUser

    def getTemporaryFileOutput(self):
        return subprocess.run(
            ['cat', self.temporaryFile],
            check=True,
            text=True,
            stdout=subprocess.PIPE
        ).stdout

    def displayFZFMenuToUser(self, FZFInput):
        try:
            return subprocess.run(
                ['fzf'],
                input = FZFInput,
                check=True,
                capture_output=True,
                text=True
            ).stdout.strip()
        except subprocess.CalledProcessError as FZFError:
            print("[ ERROR ] No Fonts Were Selected")
            print("Full Error Info Is Found Below")
            print(FZFError)
