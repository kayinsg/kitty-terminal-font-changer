import subprocess


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


class UniqueFonts:
    def __init__(self, fonts):
        self.fonts = fonts

    def get(self):
        unique_fonts = []
        seen_fonts = set()

        for font in self.fonts:
            if font not in seen_fonts:
                unique_fonts.append(font)
                seen_fonts.add(font)

        return unique_fonts
