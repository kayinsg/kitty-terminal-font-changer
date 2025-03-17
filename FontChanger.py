from fontDataObjects import KittyTerminal
import subprocess
import signal
import sys
from os import kill


class FontChanger:
    def __init__(self, kitty: KittyTerminal):
        self.kitty = kitty

    def change(self, newFontName, newFontSize):
        linesInKittyConfig = self.kitty.data
        newFontProperties = {'FontName': newFontName, 'FontSize': newFontSize}
        updatedConfig= self.getModifiedConfig(linesInKittyConfig, newFontProperties)

        self.kitty.saveChanges(updatedConfig)

        return updatedConfig

    def getModifiedConfig(self, originalConfig, newFontProperties):
        return ModifiedConfig(originalConfig, newFontProperties).get()


class ModifiedConfig:
    def __init__(self, originalConfig: list[str], newFontProperties: dict):
        self.originalConfig = originalConfig
        self.newFontProperties = newFontProperties

    @staticmethod
    def joinConfigLinesTogether(updatedConfig):
        return '\n'.join(updatedConfig)

    def get(self):
        return ModifiedConfig.joinConfigLinesTogether(self.updatedConfigData())

    def updatedConfigData(self):
        updatedFontSize = list(map(
            lambda line: self.changeFontName(line, self.newFontProperties['FontName']),
            self.originalConfig
        ))
        updatedConfigFontSize = list(map(
            lambda line: self.changeFontSize(line, self.newFontProperties['FontSize']),
            updatedFontSize
        ))
        return updatedConfigFontSize

    def changeFontName(self, line, fontName):
        if line.strip().startswith('font_family'):
            return f"font_family {fontName}"
        return line

    def changeFontSize(self, line, fontSize):
        if line.strip().startswith('font_size'):
            return f"font_size {fontSize}"
        return line


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
