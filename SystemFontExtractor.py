import subprocess
import re as regex
from fontDataObjects import FontDetails, FontSelect
from utils import sanitizeFontNames


class FontSelectorDetails:

    def get(self) -> list[FontSelect]:
        fontFamilies = FontFamily().groupMembers()
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

    def __init__(self):
        customFontPaths = CustomFontAddress().get()
        self.primaryFontNames = sanitizeFontNames(FontName().getPrimaryFontNames(customFontPaths))
        self.ancestors = FontFamily.findFontAncestors(self.primaryFontNames)

    @staticmethod
    def findFontAncestors(fonts):
        firstWordOfFullFontName = 0
        ancestors = set(map(lambda font: font.split()[firstWordOfFullFontName], fonts))
        return sorted(list(ancestors))

    def groupMembers(self):
        processFonts = lambda ancestor: self.categorizeFontsAccordingToAncestor(ancestor, self.primaryFontNames)
        return list(map(processFonts, self.ancestors))

    def categorizeFontsAccordingToAncestor(self, fontAncestor, listOfFonts):
       return {
           'Ancestor': fontAncestor,
           'Descendants': self.getMatchingFontsRegardingAncestor(fontAncestor, listOfFonts),
       }

    def getMatchingFontsRegardingAncestor(self,fontAncestor, listOfFonts):
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

    def getPrimaryFontNames(self, fontAddresses):
        fontNames = list(map(self.getFontNames, fontAddresses))
        return list(map(self.getFirstFontNameInGroup, fontNames))

    def getFontNames(self, fontAddress):
        filePaths = regex.search(
            r'^(.*?):\s*(.*?)(?::|$)',
            fontAddress
        )
        fontGroup = 1
        return filePaths.groups()[fontGroup]

    def getFirstFontNameInGroup(self, relatedFontNames):
        separatorMatch = regex.search(',', relatedFontNames)

        if separatorMatch:
            separatorIndex = separatorMatch.start()
            firstFontInGroupOfFonts = relatedFontNames[:separatorIndex]

        return firstFontInGroupOfFonts
