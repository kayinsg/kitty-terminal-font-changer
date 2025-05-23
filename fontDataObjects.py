from dataclasses import dataclass
from typing import NamedTuple
from os.path import join, expanduser
from pathlib import Path


@dataclass
class FontSelect:
    standardFontName: str
    shortenedFontName: str


class FontDetails(NamedTuple):
    ancestors: list[str]
    listOfFonts: list[str]


class KittyTerminal:
    def __init__(self):
        self.path = join(expanduser('~'), '.config', 'kitty', 'current_settings')
        self.data = Path(self.path).read_text().split('\n')

    def saveChanges(self, updatedConfigData):
        with open(self.path, "w") as config:
            config.writelines(updatedConfigData)
