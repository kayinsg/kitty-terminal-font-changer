from os import path, remove, getcwd
import subprocess

class FontMenu:
    def __init__(self, fontCollection):
        self.fonts = fontCollection
        self.tempFile = path.join(getcwd(), 'temporaryFile')

    def letUserPickFont(self):
        self.writeFontsToTemporaryFile()
        userSelectedFont = self.fontPicker()
        remove(self.tempFile)
        return userSelectedFont

    def writeFontsToTemporaryFile(self):
        with open(self.tempFile , 'w') as file:
            for font in self.fonts:
                    file.writelines(f'{font}\n')

    def fontPicker(self):
        fontMenu = subprocess.run(
            ['cat', self.tempFile],
            check=True,
            text=True,
            stdout=subprocess.PIPE
        )
        userFont = subprocess.run(
            ['fzf'],
            input = fontMenu.stdout,
            check=True,
            capture_output=True,
            text=True
        ).stdout.strip()
        return userFont

