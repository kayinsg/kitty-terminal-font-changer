from fontDataObjects import KittyTerminal
import subprocess
from os import path, remove, getcwd, kill
from pathlib import Path
from systemFontDataExtractor import getDetailsForFontSelector
import re as regex
import signal
import sys


class FontChanger:
    def __init__(self):
        self.kitty = KittyTerminal()

    def change(self):
        font = self.userFontInfo()
        self.changeFontFamily(font.get('name'))
        self.changeFontSize(font.get('size'))
        self.applyChangesToKittyConfig()

    def userFontInfo(self):
        userChosenFont = FontMenu().letUserPickFont()
        fontSizeByUser = input("What should the size of the font be? ")
        return {'name': userChosenFont, 'size': fontSizeByUser}

    def changeFontFamily(self, userChosenFont):
        fontFamily = regex.compile(r'(font_family\s*)(\w+)')
        familyMatch = fontFamily.search(self.kitty.data)
        fontFamilyCategory = familyMatch.group(1)
        fontName = familyMatch.group(2)
        modifiedConfig = regex.sub(fontFamily, f'{fontFamilyCategory}{userChosenFont}', self.kitty.data)
        self.kitty.data = modifiedConfig

    def changeFontSize(self, userChosenFontSize):
        fontSize = regex.compile(r'(\bfont_size\s+)(\d+(\.\d+)?)')
        fontSizeMatch = fontSize.search(self.kitty.data)
        fontSizeCategory = fontSizeMatch.group(1)
        actualFontSize = fontSizeMatch.group(2)
        modifiedConfig = regex.sub(fontSize, f'{fontSizeCategory}{userChosenFontSize}', self.kitty.data)
        self.kitty.data = modifiedConfig

    def applyChangesToKittyConfig(self):
        with open(self.kitty.path, "w") as config:
            config.writelines(self.kitty.data)



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


class TerminalRestart:

    def execute(self):
        kittyProcesses = self.findKittyProcesses()
        self.killKittyProcesses(kittyProcesses)
        self.reopenKittyTerminal()

    def findKittyProcesses(self):
        runningKittyProcesses = subprocess.run(
            ['pgrep kitty'],
            check=True,
            text=True,
            shell=True,
            capture_output=True
        ).stdout.splitlines()
        return runningKittyProcesses

    def killKittyProcesses(self, runningKittyProcesses):
        for process in runningKittyProcesses:
            pid = int(process)
            kill(pid, signal.SIGHUP)

    def reopenKittyTerminal(self):
        subprocess.run("kitty &", shell=True)
        sys.exit(1)

FontChanger().change()
TerminalRestart().execute()
