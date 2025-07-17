from fontDataObjects import KittyTerminal
import subprocess
import signal
import sys
from os import kill


class ConfigStandardizer:
    def __init__(self, fontConfig):
        self.fontConfig = fontConfig

    def convertInto(self, desiredDataType):
        if desiredDataType == "list":
            return self.transformConfigDataIntoLists()
        else:
            return self.rejoinConfigurationData

    def transformConfigDataIntoLists(self):
        return self.fontConfig.split('\n')

    def rejoinConfigurationData(self, listOfChangedConfigurationLines):
        return '\n'.join(listOfChangedConfigurationLines)


class FontConfigurationModifier:
    def __init__(self, configStandardizer):
        self.configStandardizer = configStandardizer
        self.newLines = []

    def changeFont(self, fontName, fontSize):
        lines = self.configStandardizer.convertInto("list")
        self.changeFontName(fontName, lines)
        self.changeFontSize(fontSize, lines)
        self.includeUnchangedConfigData(lines)
        return self.configStandardizer.convertInto("string")(self.newLines)

    def changeFontName(self, fontName, lines):
        for line in lines:
            if line.startswith("font_family"):
                self.newLines.append(f"font_family                  {fontName}")

    def changeFontSize(self, fontSize, lines):
        for line in lines:
            if line.startswith("font_size"):
                self.newLines.append(f"font_size                    {fontSize}")

    def includeUnchangedConfigData(self, lines):
        for line in lines:
            if not line.startswith("font_family") and not line.startswith("font_size"):
                self.newLines.append(line)


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
