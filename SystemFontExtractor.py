import subprocess
import re as regex
from fontDataObjects import FontSelect


class FontSelectorDetails:

    def get(self) -> list[FontSelect]:
        fontFamilies = FontFamily().groupFontsWithParent()
        return self.getDetailsForFontSelector(fontFamilies)

    def getDetailsForFontSelector(self, fontFamilies):
        fontContainers = map(
            ShortFontPair().get,
            fontFamilies
        )

        return list(map(
            self.storeDataInFontSelect,
            fontContainers
        ))

    def storeDataInFontSelect(self, fontContainer):
        return FontSelect(
            fontContainer['shortestFontName'],
            fontContainer['fontAncestor']
        )


class ShortFontPair:

    def get(self, fontFamily):
        return self.getFontAncestorWithShortestLengthDescendant(fontFamily)

    def getFontAncestorWithShortestLengthDescendant(self, fontFamily):
        fontNames = list(map(self.extractFontName, fontFamily.descendants))
        fontNameLengths = list(map(self.calculateFontNameLength, fontNames))
        fontsMetadata = list(zip(fontNames, fontNameLengths))
        shortestFontName = self.findShortestFontName(fontsMetadata)
        return {
            'fontAncestor': fontFamily.ancestor,
            'shortestFontName': shortestFontName,
        }

    def extractFontName(self, descendant):
        return descendant

    def calculateFontNameLength(self, fontName):
        return len(fontName)

    def findShortestFontName(self, fontsMetadata):
        return min(fontsMetadata, key=lambda x: x[1])[0]


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
