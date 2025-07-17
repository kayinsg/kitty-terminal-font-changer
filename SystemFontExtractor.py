import subprocess

def main():
    fontData = FontExtractorForFontAddresses().extract()
    excludedFonts = ["Lato", "Noto", "System", "Bitstream", "Liberation"]
    filteredFontData = FontFilter(fontData).excludeFontsSpecifiedByUser(excludedFonts)
    sortedFontData = FontSorter(filteredFontData).sortFonts()
    fontChildrenParser = FontChildrenParser(sortedFontData)
    return FontBundler(fontChildrenParser).buildRelationships()


class FontExtractorForFontAddresses:
    def extract(self):
        fontAddresses = self.getAllFontAddresses()
        listOfFontAddresses = self.transformFontAddressesIntoLists(fontAddresses)
        return list(map(self.extractFontNameFromAddress, listOfFontAddresses))

    def getAllFontAddresses(self):
        return subprocess.run(
            ["fc-list", ":spacing=mono"],
            check=True,
            capture_output=True,
            text=True
        ).stdout

    def transformFontAddressesIntoLists(self, fontAddresses):
        return fontAddresses.split('\n')

    def extractFontNameFromAddress(self, fontAddress):
        if fontAddress and ":" in fontAddress:
            return fontAddress.split(':')[1].split(':')[0].strip()


class FontFilter:
    def __init__(self, fontData):
        self.fontData = fontData

    @staticmethod
    def removeEmptyEntriesFromFonts(fonts):
        return list(filter(lambda font: font is not None, fonts))

    def excludeFontsSpecifiedByUser(self, fontPatternsToIgnore):
        fontData = self.removeEmptyEntriesFromFonts(self.fontData)
        acceptedFonts = list(filter(
            lambda font: self.determineIfFontShouldBeIgnored(font, fontPatternsToIgnore),
            fontData
        ))
        deduplicatedFonts = self.removeDuplicates(acceptedFonts)
        return self.removeEmptyEntriesFromFonts(deduplicatedFonts)

    def determineIfFontShouldBeIgnored(self, font, patterns):
        return not any(map(lambda pattern: pattern in font, patterns))

    def removeDuplicates(self, fonts):
        listOfSeenFonts = []
        for currentFont in fonts:
            isFontAlreadySeen = currentFont in listOfSeenFonts
            if isFontAlreadySeen == False:
                listOfSeenFonts.append(currentFont)
        return listOfSeenFonts


class FontSorter:
    def __init__(self, fontData):
        self.fontData = fontData

    def sortFonts(self):
        preparedFonts = list(map(self.createHashTableWithOriginalFontsAndSortingKey, self.fontData))
        tempSorted = self.sortOriginalListOfFontsAccordingToSortKey(preparedFonts)
        return self.getOriginalListOfFontsInSortedOrder(tempSorted)

    def createHashTableWithOriginalFontsAndSortingKey(self, font):
        firstCommaPart = font.split(',')[0]
        firstWord = firstCommaPart.split(' ')[0]
        firstWordLower = firstWord.lower()
        return {
            'original': font,
            'sortKey': firstWordLower
        }

    def sortOriginalListOfFontsAccordingToSortKey(self, preparedFonts):
        tempSorted = sorted(preparedFonts, key=lambda x: x['original'])
        tempSorted.sort(key=lambda x: x['sortKey'])
        return tempSorted

    def getOriginalListOfFontsInSortedOrder(self, fontsTable):
        return list(map(lambda font: font['original'], fontsTable))


class FontChildrenParser:
    def __init__(self, listOfFonts):
        self.listOfFonts = listOfFonts

    def parse(self):
        separatedFonts = self.separateElementsByCommas()
        return list(map(self.parseSingleFontString, separatedFonts))

    def separateElementsByCommas(self):
        return list(map(lambda fontString: fontString.split(","), self.listOfFonts))

    def parseSingleFontString(self, fontString):
        primaryFont = fontString[0]
        variantFonts = fontString[1:]
        return (primaryFont, variantFonts)


class FontBundler:
    def __init__(self, fontChildrenParser):
        self.fontChildrenParser = fontChildrenParser
        self.families = {}

    def buildRelationships(self):
        parsedFonts = self.fontChildrenParser.parse()
        list(map(self.updateSingleFamily, parsedFonts))
        return self.finalizeFamilies()

    def updateSingleFamily(self, entry):
        familyName, variants = entry
        self.createNewFamilyIfParentFontDoesNotExist(familyName)
        self.families[familyName].update(variants)

    def createNewFamilyIfParentFontDoesNotExist(self, familyName):
        fontIsAlreadyRegistered = familyName in self.families
        if fontIsAlreadyRegistered:
            pass
        else:
            self.families[familyName] = set()

    def finalizeFamilies(self):
        extractFontFamilyAndChildren = lambda item: {
            "Font Family": item[0],
            "Font Children": sorted(list(item[1]))
        }
        return list(map(extractFontFamilyAndChildren, self.families.items()))

main()
