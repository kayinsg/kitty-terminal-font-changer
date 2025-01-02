from dataObjects import FontSelect
import subprocess
import os
from pathlib import Path
from systemFontDataExtractor import getDetailsForFontSelector
import re as regex

def fontPicker(temporaryFile):
    fontMenu = subprocess.run(
        ['cat', temporaryFile],
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
    os.remove(temporaryFile)
    return userFont


def getTemporaryFilePath():
    workingDirectory = os.getcwd()
    temporaryFilePath = os.path.join(workingDirectory, 'temporaryFile')
    return temporaryFilePath

def writeFontsToTemporaryFile(fonts, temporaryFilePath):
    with open(temporaryFilePath , 'w') as file:
        for font in fonts:
                file.writelines(f'{font.ancestor}\n')


def getKittyConfigPath():
    home = os.path.expanduser('~')
    kittyConfigPath = os.path.join (home, '.config', 'kitty', 'current_settings')
    return kittyConfigPath


def getKittyConfigData(kittyConfigPath):
    return Path(kittyConfigPath).read_text()



def changeFontFamily(kittyConfigData):
    fontFamily = regex.compile(r'(font_family\s*)(\w+)')
    familyMatch = fontFamily.search(kittyConfigData)
    fontFamilyCategory = familyMatch.group(1)
    fontName = familyMatch.group(2)
    modifiedConfig = regex.sub(fontFamily, f'{fontFamilyCategory}{userChosenFont}', kittyConfigData)
    return modifiedConfig


def changeFontSize(kittyConfigData):
    fontSize = regex.compile(r'(\bfont_size\s+)(\d+(\.\d+)?)')
    fontSizeMatch = fontSize.search(kittyConfigData)
    fontSizeCategory = fontSizeMatch.group(1)
    actualFontSize = fontSizeMatch.group(2)
    modifiedConfig = regex.sub(fontSize, f'{fontSizeCategory}{fontSizeByUser}', kittyConfigData)
    return modifiedConfig


def applyChangesToKittyConfig(modifiedKittyData, kittyConfigPath):
    with open(kittyConfigPath, "w") as config:
        config.writelines(modifiedKittyData)


fonts = getDetailsForFontSelector()
temporaryFilePath = getTemporaryFilePath()
writeFontsToTemporaryFile(fonts, temporaryFilePath)

kittyConfigPath = getKittyConfigPath()
kittyConfigData = getKittyConfigData(kittyConfigPath)

modifiedFontFamily = changeFontFamily(kittyConfigData)
modifiedFontSize = changeFontSize(modifiedFontFamily)

applyChangesToKittyConfig(modifiedFontSize, kittyConfigPath)



userChosenFont = fontPicker(temporaryFilePath)
fontSizeByUser = input("What should the size of the font be? ")
