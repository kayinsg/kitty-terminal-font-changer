from dataObjects import FontSelect
import subprocess
import os
from pathlib import Path
from systemFontDataExtractor import getDetailsForFontSelector
import re as regex


workingDirectory = os.getcwd()
temporaryFilePath = Path(workingDirectory).joinpath('temp')

fonts = getDetailsForFontSelector()

def fontPicker(fonts, temporaryFile):
    # temporaryFile = Path(Path(workingDirectory).joinpath('temp')).as_posix()
    with open(temporaryFile , 'w') as file:
        for font in fonts:
                file.writelines(f'{font.ancestor}\n')
    
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

userChosenFont = fontPicker(fonts, temporaryFilePath)


# fontSizeByUser = input("What should the size of the font be? ")


home = os.path.expanduser('~')
kittyConfigPath = os.path.join (home, '.config', 'kitty', 'current_settings')


kittyFontConfig = Path(kittyConfigPath).read_text()


fontFamily = regex.compile(r'(font_family\s*)(\w+)')
fontSize = regex.compile(r'(\bfont_size\s+)(\d+(\.\d+)?)')


# print("")
# print('[ SOURCE ]: ...')
# print('[ INFO ] Kitty Font Config')
# print(kittyFontConfig)


familyMatch = fontFamily.search(kittyFontConfig)
fontFamilyCategory = familyMatch.group(1)
fontName = familyMatch.group(2)
newString = regex.sub(fontFamily, f'{fontFamilyCategory}{userChosenFont}', kittyFontConfig)


fontSizeMatch = fontSize.search(newString)
fontSizeCategory = fontSizeMatch.group(1)
actualFontSize = fontSizeMatch.group(2)
# newString2 = regex.sub(fontSize, f'{fontSizeCategory}{fontSizeByUser}', newString)


# print(newString2)
