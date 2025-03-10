from fontDataObjects import KittyTerminal
import subprocess
import re as regex
import signal
import sys
from os import kill


class FontChanger:
    def __init__(self, font, size):
        self.kitty = KittyTerminal()
        self.font = font
        self.size = size

    def applyChanges(self):
        self.changeFontFamily(self.font)
        self.changeFontSize(self.size)
        self.applyChangesToKittyConfig()

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
