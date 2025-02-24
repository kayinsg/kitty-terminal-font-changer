import subprocess
import re as regex
from fontDataObjects import FontFamilyTree, FontDetails, FontSelect
from subroutines import eliminateDuplicates


class FontSelectorDetails:

    def get(self):
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
            fontContainer['fontAncestor'],
            fontContainer['shortestFontName']
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
        primaryFontNames = FontName().getPrimaryFontNames(customFontPaths)
        fontDetails = getFontDetails(primaryFontNames)
        self.fontDetails = fontDetails

    def groupMembers(self):
        return list(map(lambda x: x, list(self.getFontFamily())))

    def getFontFamily(self):
        for fontAncestor in self.fontDetails.ancestors:
            fontFamily = FontFamilyTree(fontAncestor, [""])
            for font in self.fontDetails.listOfFonts:
                descendantOfTheFontFamilyHasBeenFound = regex.search(
                    fontAncestor,
                    font
                )
                if descendantOfTheFontFamilyHasBeenFound:
                    fontFamily.descendants.append(font)
                else:
                    pass

            fontFamily.descendants = fontFamily.descendants[1::]
            yield fontFamily


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

    def getFirstFontNameInGroup(self, fontName):
        primaryFontName = regex.compile(r',')
        if primaryFontName.search(fontName):
            firstFontNameSepartor = primaryFontName.search(
                fontName
                ).start()  # type: ignore
            return fontName[0:firstFontNameSepartor]
        return fontName


def getFontDetails(fontNames):
    cleanedListOfFonts = sanitizeFontNames(fontNames)
    ancestors = getFontAncestorFromName(cleanedListOfFonts)
    return FontDetails(ancestors, cleanedListOfFonts)


def sanitizeFontNames(primaryFontNames):
    alphabeticallyOrderedList = sorted(
        primaryFontNames,
        key=lambda x: x[0]
    )
    nonDuplicatedListOfFonts = eliminateDuplicates(
        alphabeticallyOrderedList
    )
    return nonDuplicatedListOfFonts


def getFontAncestorFromName(nonDuplicatedListOfFonts):
    words = list()
    for font in nonDuplicatedListOfFonts:
        letters = list()
        for currentCharacter in font[0::]:
            characterIsNotACapitalLetter = currentCharacter.islower() is True
            characterIsNotASpace = currentCharacter != " "
            if characterIsNotASpace or characterIsNotACapitalLetter:
                letters.append(currentCharacter)
            else:
                break
        words.append(''.join(letters))
    return eliminateDuplicates(words)

print(FontSelectorDetails().get())
