from fontDataObjects import KittyTerminal
import subprocess
import signal
import sys
from os import kill


class FontChanger:
    def __init__(self, kitty: KittyTerminal):
        self.kitty = kitty
        self.fileWriter = ConfigFileWriter()

    def change(self, newFontName, newFontSize):
        linesInKittyConfig = self.kitty.data
        newFontProperties = {'FontName': newFontName, 'FontSize': newFontSize}
        updatedConfig= self.getModifiedConfig(linesInKittyConfig, newFontProperties)
        finalConfig = self.joinConfigLinesTogether(updatedConfig)

        self.fileWriter.saveChangesToKittyConfig(self.kitty.path, finalConfig)

        return finalConfig

    def getModifiedConfig(self, originalConfig, newFontProperties):
        return ModifiedConfig(originalConfig, newFontProperties).get()

    def joinConfigLinesTogether(self, updatedConfig):
        return '\n'.join(updatedConfig)

class ConfigFileWriter:

    def saveChangesToKittyConfig(self, filePath, configData):
        with open(filePath, "w") as config:
            config.writelines(configData)

class ModifiedConfig:
    def __init__(self, originalConfig: list[str], newFontProperties: dict):
        self.originalConfig = originalConfig
        self.newFontProperties = newFontProperties

    def get(self):
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
