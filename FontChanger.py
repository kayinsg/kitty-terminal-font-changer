import subprocess
import signal
import sys
import os

class FontConfiguration:
    def __init__(self, terminal):
        self.terminal = terminal
        self.newLines = []

    def changeFont(self, fontName, fontSize):
        configData = self.terminal.readDataFromConfigFile()
        config = ConfigDataType(configData)
        modifiedConfig = ModifiedConfig(config).change(fontName, fontSize)
        self.terminal.writeDataToConfigFile(modifiedConfig)


class KittyTerminal:
    def __init__(self, configFilePath):
        self.configFilePath = configFilePath

    def readDataFromConfigFile(self):
        with open(self.configFilePath, 'r') as file:
            return file.read()

    def writeDataToConfigFile(self, changedFontConfig):
        with open(self.configFilePath, 'w') as file:
            file.write(changedFontConfig)


class ModifiedConfig:
    def __init__(self, config):
        self.config = config
        self.newLines = []

    def change(self, fontName, fontSize):
        configData = self.config.convertInto("list")
        self.changeFontName(configData, fontName)
        self.changeFontSize(configData, fontSize)
        self.includeUnchangedConfigData(configData)
        return self.config.convertInto("string")(self.newLines)

    def changeFontName(self,configData, fontName):
        for line in configData:
            if line.startswith("font_family"):
                self.newLines.append(f"font_family                  {fontName}")

    def changeFontSize(self, configData, fontSize):
        for line in configData:
            if line.startswith("font_size"):
                self.newLines.append(f"font_size                    {fontSize}")

    def includeUnchangedConfigData(self, configData):
        for line in configData:
            if not line.startswith("font_family") and not line.startswith("font_size"):
                self.newLines.append(line)


class ConfigDataType:
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
            os.kill(pid, signal.SIGHUP)

    def reopenKittyTerminal(self):
        subprocess.run("kitty &", shell=True)
        sys.exit(1)
