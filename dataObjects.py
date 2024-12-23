from dataclasses import dataclass
from typing import NamedTuple


@dataclass
class FontSelectDetails:
    ancestor: str
    fontForClipboard: str


@dataclass
class FontFamilyTree:
    ancestor: str
    descendants: list[str]


class FontDetails(NamedTuple):
    ancestors: list[str]
    listOfFonts: list[str]
