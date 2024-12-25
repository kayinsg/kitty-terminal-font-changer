import subprocess
from dataObjects import FontDetails


def eliminateDuplicates(originalListOfLines):
    unduplicatedLines = list()
    for line in originalListOfLines:
        if line not in unduplicatedLines:
            unduplicatedLines.append(line)
        else:
            pass
    return unduplicatedLines


def updateLocalFontDatabase():
    try:
        updateFonts = subprocess.run(
            ["fc-cache", "-f"],
            check=True,
        )
        updateFonts.check_returncode()
    except subprocess.CalledProcessError:
        exit(1)
