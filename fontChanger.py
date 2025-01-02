from dataObjects import FontSelect
import subprocess
import os
from pathlib import Path
from systemFontDataExtractor import getDetailsForFontSelector
import re as regex


class FontChanger:
    def __init__(self):
        self.kittyConfigPath = os.path.join(os.path.expanduser('~'), '.config', 'kitty', 'current_settings')
        self.kittyConfigData = Path(self.kittyConfigPath).read_text()


    @classmethod
    def userFontInfo(cls):
        userChosenFont = FontMenu().letUserPickFont()
        fontSizeByUser = input("What should the size of the font be? ")
        return {'name': userChosenFont, 'size': fontSizeByUser}


    def change(self):
        font = self.userFontInfo()
        self.changeFontFamily(font['name'])
        self.changeFontSize(font['size'])
        self.applyChangesToKittyConfig()


    def changeFontFamily(self, userChosenFont):
        fontFamily = regex.compile(r'(font_family\s*)(\w+)')
        familyMatch = fontFamily.search(self.kittyConfigData)
        fontFamilyCategory = familyMatch.group(1)
        fontName = familyMatch.group(2)
        modifiedConfig = regex.sub(fontFamily, f'{fontFamilyCategory}{userChosenFont}', self.kittyConfigData)
        self.kittyConfigData = modifiedConfig


    def changeFontSize(self, userChosenFontSize):
        fontSize = regex.compile(r'(\bfont_size\s+)(\d+(\.\d+)?)')
        fontSizeMatch = fontSize.search(self.kittyConfigData)
        fontSizeCategory = fontSizeMatch.group(1)
        actualFontSize = fontSizeMatch.group(2)
        modifiedConfig = regex.sub(fontSize, f'{fontSizeCategory}{userChosenFontSize}', self.kittyConfigData)
        self.kittyConfigData = modifiedConfig


    def applyChangesToKittyConfig(self):
        with open(self.kittyConfigPath, "w") as config:
            config.writelines(self.kittyConfigData)



class FontMenu:
    def __init__(self):
        self.fonts = getDetailsForFontSelector()
        self.tempFile = os.path.join(os.getcwd(), 'temporaryFile')

    def letUserPickFont(self):
        self.writeFontsToTemporaryFile()
        userSelectedFont = self.fontPicker()
        os.remove(self.tempFile)
        return userSelectedFont

    def writeFontsToTemporaryFile(self):
        with open(self.tempFile , 'w') as file:
            for font in self.fonts:
                    file.writelines(f'{font.ancestor}\n')

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


FontChanger().change()
