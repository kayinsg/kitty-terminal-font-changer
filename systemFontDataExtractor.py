import subprocess
import re as regex
from dataObjects import FontFamilyTree, FontDetails, FontSelect
from subroutines import eliminateDuplicates, updateLocalFontDatabase, getFontDetails


def getDetailsForFontSelector():
    fontFamilies = FontFamily().groupMembers()
    fontSelectorContainers = list()
    for fontFamily in fontFamilies:
        fontContainerForUser = getFontAncestorWithShortestLengthDescendant(
            fontFamily
        )
        print("")
        print('[ SOURCE ]: ...')
        print('[ INFO ] Font Select')
        print(fontContainerForUser)
        fontSelectorContainers.append(fontContainerForUser)

    return fontSelectorContainers

class FontFamily:
    def __init__(self):
        customFontPaths = CustomFontAddress().get()
        primaryFontNames = FontName().getPrimaryFontNames(customFontPaths)
        fontDetails = getFontDetails(primaryFontNames)
        self.fontDetails = fontDetails

    def groupMembers(self):
        fontFamilies = list()
        for fontFamily in self.getFontFamily():
            fontFamilies.append(fontFamily)
        return fontFamilies

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
            yield (fontFamily)


def getFontAncestorWithShortestLengthDescendant(fontFamily):
    fontsMetadata = list()

    for descendant in fontFamily.descendants:

        fontName = descendant
        lengthOfFontName = len(fontName)

        fontMetadata = (fontName, lengthOfFontName)
        fontsMetadata.append(fontMetadata)

    shortestWord = fontsMetadata[0][0]
    smallest = fontsMetadata[0][1]

    for word, length in fontsMetadata:
        if length < smallest:
            shortestWord = word

    return FontSelect(fontFamily.ancestor, shortestWord)

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


class CustomFontAddress:

    def get(self) -> list[str]:
        listOfFontsAvailable = self.getAllFontAddresses()
        customFontAddresses = self.filterCustomAddresses(listOfFontsAvailable)
        return customFontAddresses

    def getAllFontAddresses(self):
        showSystemFonts = subprocess.run(
            ["fc-list"],
            check=True,
            capture_output=True,
            text=True
        )

        listOfFontsAvailable = showSystemFonts.stdout.splitlines()
        return listOfFontsAvailable

    def filterCustomAddresses(self, listOfFontsAvailable):
        customFontFolder = regex.compile('.*monospace.*')
        customFontAddresses = list()

        for line in listOfFontsAvailable:
            if customFontFolder.search(line):
                customFontAddresses.append(line)
            else:
                pass

        return customFontAddresses


class FontName:

    def getPrimaryFontNames(self, fontAddresses):
        fontNames = self.getAlikeFontNames(fontAddresses)
        primaryFontNames = self.extractFundamentalNames(fontNames)
        return primaryFontNames

    def getAlikeFontNames(self, fontAddresses):
        sample = list()
        for path in fontAddresses:
            filePaths = regex.search(
                r'^(.*?):\s*(.*?)(?::|$)',
                path
            )
            fontGroup = 1
            sample.append(filePaths.groups()[fontGroup])  # type: ignore
        return sample

    def extractFundamentalNames(
        self,
        collectionOfSynonymousFontNames,
    ):
        primaryFontName = regex.compile(r',')
        finalFontNames = list()
        for fileMatch in collectionOfSynonymousFontNames:
            if primaryFontName.search(fileMatch):
                firstFontNameSepartor = primaryFontName.search(
                    fileMatch
                    ).start()  # type: ignore
                finalFontNames.append(fileMatch[0:firstFontNameSepartor])
            else:
                finalFontNames.append(fileMatch)
        return finalFontNames


getDetailsForFontSelector()
