import subprocess
import re as regex
from fontDataObjects import FontSelect
from utils import UniqueFonts


class FontSelectorDetails:
    def __init__(self, fontAdresses):
        self.fontAdresses = fontAdresses

    def get(self) -> list[FontSelect]:
        fontFamilies = self.getFontFamilies()
        return self.storeDataInFontSelect(self.ancestorGroupedWithShortestLengthDescendant(fontFamilies))

    def getFontFamilies(self) -> list[dict[str, str | list[str]]]:
        fontAddresses: list[str] = self.fontAdresses.get()
        groupOfRelatedFontNames: list[str] = FontName(fontAddresses).getFontNames()
        fontFamilies: list[dict[str, str | list[str]]] = FontFamily(groupOfRelatedFontNames).groupFontsWithParent()
        return fontFamilies

    def ancestorGroupedWithShortestLengthDescendant(self, fontFamilies: list[dict[str, str | list[str]]]) -> list[dict[str, str]]:
        return list(map(ShortFontPair().getFontAncestorWithShortestLengthDescendant, fontFamilies))

    def storeDataInFontSelect(self, fontContainer: list[dict[str, str]]) -> list[FontSelect]:
        storeInFontSelect = lambda fontContainer: FontSelect(fontContainer['shortestFontName'], fontContainer['fontAncestor'])
        return list(map(storeInFontSelect, fontContainer))


class CustomFontAddress:

    def get(self) -> list[str]:
        listOfFontsAvailable = self.getAllFontAddresses()
        return list(
            filter(
                self.customFontAddress,
                listOfFontsAvailable
            )
        )

    def getAllFontAddresses(self):
        showSystemFonts = subprocess.run(
            ["fc-list"],
            check=True,
            capture_output=True,
            text=True
        )

        return showSystemFonts.stdout.splitlines()

    def customFontAddress(self, line):
        customFontFolder = regex.compile('.*monospace.*')
        if customFontFolder.search(line):
            return True
        return False


class FontName:
    def __init__(self, fontAddresses):
        self.fontAddresses = fontAddresses

    def getFontNames(self):
        relevantFunction = lambda fontAddresses: self.getFirstFontName(self.getFontGroup(fontAddresses))
        uniqueFonts = UniqueFonts(list(map(relevantFunction, self.fontAddresses))).get()
        return uniqueFonts

    def getFontGroup(self, fontAddresses):
        parts = fontAddresses.split(':')
        if len(parts) > 1:
            fontNames = parts[1].strip()
            return fontNames

    def getFirstFontName(self, groupOfRelatedFontNames):
        return groupOfRelatedFontNames.split(',')[0].strip()


class ShortFontPair:

    def get(self, fontFamily):
        return self.getFontAncestorWithShortestLengthDescendant(fontFamily)

    def getFontAncestorWithShortestLengthDescendant(self, fontFamily):
        fontNames = list(map(self.extractFontName, fontFamily['Descendants']))
        fontNameLengths = list(map(self.calculateFontNameLength, fontNames))
        fontsMetadata = list(zip(fontNames, fontNameLengths))
        shortestFontName = self.findShortestFontName(fontsMetadata)
        return {
            'fontAncestor': fontFamily['Ancestor'],
            'shortestFontName': shortestFontName,
        }

    def extractFontName(self, descendant):
        return descendant

    def calculateFontNameLength(self, fontName):
        return len(fontName)

    def findShortestFontName(self, fontsMetadata):
        fontSize = 1
        fontNameLength = lambda fontDetails: fontDetails[fontSize]

        return min(
            fontsMetadata,
            key=fontNameLength
        )[0]


class FontFamily:
    def __init__(self, relatedGroupsOfFontNames):
        self.primaryFontNames = relatedGroupsOfFontNames
        self.ancestors = FontFamily.findFontAncestors(self.primaryFontNames)

    @staticmethod
    def findFontAncestors(fonts):
        extractAncestor = lambda name: name.split()[0]
        ancestors = map(extractAncestor, fonts)
        return UniqueFonts(ancestors).get()

    def groupFontsWithParent(self):
        processFonts = lambda ancestor: self.categorizeFontsAccordingToAncestor(ancestor, self.primaryFontNames)
        return list(
            map(
                processFonts,
                self.ancestors
            )
        )

    def categorizeFontsAccordingToAncestor(self, fontAncestor, listOfFonts):
       return {
           'Ancestor': fontAncestor,
           'Descendants': self.getMatchingFontsRegardingAncestor(fontAncestor, listOfFonts),
       }

    def getMatchingFontsRegardingAncestor(self, fontAncestor:str , listOfFonts: list[str]):
        fontMatchesAncestor = lambda descendant: regex.search(fontAncestor, descendant) is not None
        return list(
            filter(
                fontMatchesAncestor,
                listOfFonts
            )
        )
