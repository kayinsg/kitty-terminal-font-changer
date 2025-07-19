import unittest
from colour_runner.runner import ColourTextTestRunner
from SystemFontExtractor import FontExtractorForFontAddresses, FontFilter, FontSorter, FontBundler, FontChildrenParser
from FontDatabase import Database, UserFontFromDatabase
from FontChanger import ConfigStandardizer, FontConfiguration, KittyTerminal
import sqlite3

class SystemFontDataExtractorTests(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def testShouldShouldShouldGetFontNameForTerminal(self):
        class FakeFontExtractorForFontAddresses(FontExtractorForFontAddresses):
            def getAllFontAddresses(self):
                return (
                    "/usr/share/fonts/ViewCustomFonts/serif/Garamond.ttf: Garamond:style=Regular,Normal,obyčejné,Standard,Κανονικά,Normaali,Normál,Normale,Standaard,Normalny,Обычный,Normálne,Navadno,Arrunta\n"
                    "/usr/share/fonts/ViewCustomFonts/sansSerif/sfDisplay/san francisco pro/SF-Pro-Text-Bold.otf: SF Pro Text:style=Bold\n"
                    "/usr/share/fonts/noto/NotoSerifDevanagari-ExtraCondensedLight.ttf: Noto Serif Devanagari,Noto Serif Devanagari ExtraCondensed Light:style=ExtraCondensed Light,Regular\n"
                    "/usr/share/fonts/ViewCustomFonts/monospace/A - goldFonts/gohu/GohuFont11NerdFont-Regular.ttf: GohuFont 11 Nerd Font:style=Regular"
                )
        def getexpectedFontData():
            return [
                "Garamond",
                "SF Pro Text",
                "Noto Serif Devanagari,Noto Serif Devanagari ExtraCondensed Light",
                "GohuFont 11 Nerd Font"
            ]
        # GIVEN the following preconditions corresponding to the system under test:
        expectedFontData = getexpectedFontData()
        fontExtractor = FakeFontExtractorForFontAddresses()
        # WHEN the following module is executed:
        result = fontExtractor.extract()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(result, expectedFontData)

    def testShouldIgnoreFontsSpecifiedByUser(self):
        def getFontData():
            return [
                "Noto Serif Georgian,Noto Serif Georgian Cn SmBd",
                "Noto Sans Lao Condensed,Noto Sans Lao Condensed Light",
                "Noto Sans Malayalam Condensed,Noto Sans Malayalam Condensed ExtraBold",
                "Lato,Lato Hairline",
                "Noto Sans Thai Looped Condensed,Noto Sans Thai Looped Condensed Light",
                "Noto Serif Display SemiCondensed,Noto Serif Display SemiCondensed Thin",
                "Noto Serif Tamil,Noto Serif Tamil ExtraBold",
                "ZedMono Nerd Font Propo,ZedMono NFP,ZedMono NFP Medium",
                "Noto Sans Arabic UI,Noto Sans Arabic UI Cn",
                "Noto Sans Kannada,Noto Sans Kannada SemiCondensed Black",
                "Georgia",
                "Noto Sans Sinhala UI Condensed,Noto Sans Sinhala UI Condensed ExtraBold",
                "Iosevka Nerd Font,Iosevka NF,Iosevka NF ExtraLight Obl",
                "Noto Serif Ethiopic ExtraCondensed,Noto Serif Ethiopic ExtraCondensed SemiBold",
                "Noto Sans Syloti Nagri"
            ]

        fontData = getFontData()
        fontPatternsToIgnore = ["Noto", "Lato"]
        expectedResult = ["ZedMono Nerd Font Propo,ZedMono NFP,ZedMono NFP Medium", "Georgia", "Iosevka Nerd Font,Iosevka NF,Iosevka NF ExtraLight Obl"]
        fontFilter = FontFilter(fontData)
        result = fontFilter.excludeFontsSpecifiedByUser(fontPatternsToIgnore)
        self.assertEqual(result, expectedResult)


    def testShouldSortListOfFonts(self):
        def getUnsortedFontData():
            return [
                "Adwaita Sans",
                "ZedMono Nerd Font Mono,ZedMono NFM,ZedMono NFM Light",
                "SpaceMono Nerd Font Propo",
                "SourceCodeVF",
                "JetBrainsMonoNL Nerd Font Mono,JetBrainsMonoNL NFM,JetBrainsMonoNL NFM Medium",
                "JetBrainsMonoNL Nerd Font Propo,JetBrainsMonoNL NFP,JetBrainsMonoNL NFP Thin",
                "Source Code Pro",
                "SF Pro Text",
                "MartianMono Nerd Font Propo,MartianMono NFP,MartianMono NFP Med",
                "ZedMono Nerd Font Propo,ZedMono NFP,ZedMono NFP Extd Light",
                "Iosevka Nerd Font,Iosevka NF,Iosevka NF Medium Obl",
                "SourceCodeVF",
                "Iosevka Nerd Font Propo,Iosevka NFP",
                "Source Code Pro",
                "Iosevka Nerd Font Mono,Iosevka NFM,Iosevka NFM ExtraBold Obl"
            ]

        def getsortedFontData():
            return [
                "Adwaita Sans",
                "Iosevka Nerd Font Mono,Iosevka NFM,Iosevka NFM ExtraBold Obl",
                "Iosevka Nerd Font Propo,Iosevka NFP",
                "Iosevka Nerd Font,Iosevka NF,Iosevka NF Medium Obl",
                "JetBrainsMonoNL Nerd Font Mono,JetBrainsMonoNL NFM,JetBrainsMonoNL NFM Medium",
                "JetBrainsMonoNL Nerd Font Propo,JetBrainsMonoNL NFP,JetBrainsMonoNL NFP Thin",
                "MartianMono Nerd Font Propo,MartianMono NFP,MartianMono NFP Med",
                "SF Pro Text",
                "Source Code Pro",
                "Source Code Pro",
                "SourceCodeVF",
                "SourceCodeVF",
                "SpaceMono Nerd Font Propo",
                "ZedMono Nerd Font Mono,ZedMono NFM,ZedMono NFM Light",
                "ZedMono Nerd Font Propo,ZedMono NFP,ZedMono NFP Extd Light"
            ]
        # GIVEN the following preconditions corresponding to the system under test:
        unsortedFontData = getUnsortedFontData()
        sortedFontData = getsortedFontData()
        fontSorter = FontSorter(unsortedFontData)
        # WHEN the following module is executed:
        result = fontSorter.sortFonts()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(sortedFontData, result)

    def testShouldCreateAFontFamilyFromListOfFonts(self):
        def getFonts():
            return [
                "ZedMono Nerd Font Mono,ZedMono NFM",
                "ZedMono Nerd Font Mono,ZedMono NFM,ZedMono NFM Extd",
                "ZedMono Nerd Font Mono,ZedMono NFM,ZedMono NFM Extd ExtBd",
                "ZedMono Nerd Font Mono,ZedMono NFM,ZedMono NFM Extd ExtBd Obl",
                "JetBrainsMono Nerd Font,JetBrainsMono NF,JetBrainsMono NF Light",
                "JetBrainsMono Nerd Font,JetBrainsMono NF,JetBrainsMono NF Medium",
                "JetBrainsMono Nerd Font,JetBrainsMono NF,JetBrainsMono NF SemiBold",
                "JetBrainsMono Nerd Font,JetBrainsMono NF,JetBrainsMono NF Thin",
                "JetBrainsMonoNL Nerd Font Mono,JetBrainsMonoNL NFM",
                "JetBrainsMonoNL Nerd Font Mono,JetBrainsMonoNL NFM,JetBrainsMonoNL NFM ExtraBold",
                "JetBrainsMonoNL Nerd Font Mono,JetBrainsMonoNL NFM,JetBrainsMonoNL NFM ExtraLight",
            ]

        def expectedDataStructureOfFontFamilies():
            return [
                {
                    "Font Family": "ZedMono Nerd Font Mono",
                    "Font Children": [
                        "ZedMono NFM",
                        "ZedMono NFM Extd",
                        "ZedMono NFM Extd ExtBd",
                        "ZedMono NFM Extd ExtBd Obl"
                    ]
                },
                {
                    "Font Family": "JetBrainsMono Nerd Font",
                    "Font Children": [
                        "JetBrainsMono NF",
                        "JetBrainsMono NF Light",
                        "JetBrainsMono NF Medium",
                        "JetBrainsMono NF SemiBold",
                        "JetBrainsMono NF Thin"
                    ]
                },
                {
                    "Font Family": "JetBrainsMonoNL Nerd Font Mono",
                    "Font Children": [
                        "JetBrainsMonoNL NFM",
                        "JetBrainsMonoNL NFM ExtraBold",
                        "JetBrainsMonoNL NFM ExtraLight"
                    ]
                }
            ]
        # GIVEN the following preconditions corresponding to the system under test:
        fonts = getFonts()
        expectedResult = expectedDataStructureOfFontFamilies()
        fontChildrenParser = FontChildrenParser(fonts)
        fontFamily = FontBundler(fontChildrenParser)
        # WHEN the following module is executed:
        result = fontFamily.buildRelationships()
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(result, expectedResult)


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")  # Fake DB (RAM-only)
        self.cursor = self.conn.cursor()

        def getFontFamilies():
            return [
                {
                    'Font Family': 'Intel One Mono',
                    'Font Children': ['Intel One Mono Light', 'Intel One Mono Medium'],
                },
                {
                    'Font Family': 'GohuFont 14 Nerd Font Mono',
                    'Font Children': [],
                }
            ]

        self.fontFamilies = getFontFamilies()

    def tearDown(self):
        self.conn.close()


class DatabaseRelationshipTests(DatabaseTests):
    def testShouldAssignPrimaryKeyToFonts(self):
        def assertThatTableHasPrimaryKey(tableName):
            columns = getTableInfo(tableName)
            self.assertTrue(any(col[5] == 1 for col in columns),
                          f"Table {tableName} has no primary key column")

        def getTableInfo(tableName):
            self.cursor.execute(f"PRAGMA table_info({tableName})")
            return self.cursor.fetchall()

        # GIVEN the test data is already set up in setUp()
        database = Database(self.conn)
        # WHEN the font families are inserted
        database.insertFontsInDatabase(self.fontFamilies)
        # THEN the Fonts table should have a primary key column
        assertThatTableHasPrimaryKey("Fonts")


    def testShouldAssignForeignKeyToFontStyles(self):
        class DataOfficer:
            def __init__(self, cursor, primaryTable):
                self.cursor = cursor
                self.primaryTable = primaryTable

            def assertThatRelationshipBetweenTablesIsVerified(self, foreignTable, foreignKey):
                fkInfo = self._getForeignKeyInfo(foreignTable)
                self._verifyForeignKeyExists(fkInfo)
                self._assertForeignKeyMatches(fkInfo, foreignKey)

            # Worker functions (made private by convention)
            def _getForeignKeyInfo(self, tableName):
                self.cursor.execute(f"PRAGMA foreign_key_list({tableName})")
                return self.cursor.fetchall()

            def _verifyForeignKeyExists(self, fkInfo):
                if not fkInfo:
                    raise AssertionError("No foreign keys found")

            def _assertForeignKeyMatches(self, fkInfo, expectedColumn):
                if fkInfo[0][2] != self.primaryTable:
                    raise AssertionError(
                        f"Incorrect foreign key reference. Expected {self.primaryTable}, "
                        f"got {fkInfo[0][2]}"
                    )
                if fkInfo[0][3] != expectedColumn:
                    raise AssertionError(
                        f"Incorrect foreign key column. Expected {expectedColumn}, "
                        f"got {fkInfo[0][3]}"
                    )
        database = Database(self.conn)
        # WHEN the font families are inserted
        database.insertFontsInDatabase(self.fontFamilies)
        # THEN the FontStyles table should have a foreign key to Fonts
        DataOfficer(self.cursor, "Fonts").assertThatRelationshipBetweenTablesIsVerified("FontStyles", "font_id")

    def testShouldVerifyIntegrityBetweenFontAndStyles(self):
        def assertFontRelationshipsMatch(expectedRelationships):
            self.cursor.execute("""
                SELECT Fonts.name, FontStyles.name
                FROM Fonts
                JOIN FontStyles ON Fonts.id = FontStyles.font_id
                ORDER BY FontStyles.name
            """)
            actual_relationships = self.cursor.fetchall()
            self.assertEqual(actual_relationships, expectedRelationships)

        # GIVEN
        database = Database(self.conn)
        # WHEN
        database.insertFontsInDatabase(self.fontFamilies)
        # THEN
        assertFontRelationshipsMatch([
            ('Intel One Mono', 'Intel One Mono Light'),
            ('Intel One Mono', 'Intel One Mono Medium')
        ])

class DatabaseInsertionTests(DatabaseTests):
    def assertThatRowAndColumnDataIsCorrect(self, tableName, position):
        self.cursor.execute(f"SELECT name FROM {tableName}")
        actualValue = self.cursor.fetchall()[position['row']-1][position['column']-1]
        self.assertEqual(actualValue, position['value'],
                        f"Data mismatch in {tableName} at row {position['row']}, column {position['column']}")

    def testShouldInsertFontFamiliesIntoFontsTable(self):
        database = Database(self.conn)
        database.insertFontsInDatabase(self.fontFamilies)
        self.assertThatRowAndColumnDataIsCorrect("Fonts", {'row': 1, 'column': 1, 'value': 'Intel One Mono'})
        self.assertThatRowAndColumnDataIsCorrect("Fonts", {'row': 2, 'column': 1, 'value': 'GohuFont 14 Nerd Font Mono'})

    def testShouldInsertFontChildrenIntoFontStylesTable(self):
        database = Database(self.conn)
        database.insertFontsInDatabase(self.fontFamilies)
        self.assertThatRowAndColumnDataIsCorrect("FontStyles", {'row': 1, 'column': 1, 'value': 'Intel One Mono Light'})
        self.assertThatRowAndColumnDataIsCorrect("FontStyles", {'row': 2, 'column': 1, 'value': 'Intel One Mono Medium'})

class DatabaseRetrievalTests(DatabaseTests):

    def createFontsTable(self, conn):
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Fonts (name TEXT)")
        fonts = [
            'Intel One Mono',
            'Gohu Font',
            'JetBrains',
            'Iosevka',
            'ZedMono',
            'SpaceMono',
            'SF Mono'
        ]
        for font in fonts:
            cursor.execute("INSERT INTO Fonts VALUES (?)", (font,))
        conn.commit()

    def dropFontsTable(self, conn):
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Fonts")
        conn.commit()

    def testShouldRetrieveFontsRequestedByUserFromTheFontsTable(self):
        # GIVEN the following preconditions corresponding to the system under test:
        self.createFontsTable(self.conn)
        fontRequestedFromUser = "ZedMono"
        database = UserFontFromDatabase(self.conn)
        # WHEN the following module is executed:
        fontReceived = database.getFont(fontRequestedFromUser)
        # THEN the observable behavior should be verified as stated below:
        self.assertEqual(fontReceived, fontRequestedFromUser)
        self.dropFontsTable(self.conn)



class FontChangerTestsTests(unittest.TestCase):

    def testShouldChangeTerminalConfigurationGivenUserSelectedFontNameAndSize(self):
        class FakeKittyTerminal(KittyTerminal):
            def __init__(self, configFilePath):
                self.configFilePath = configFilePath

            def readDataFromConfigFile(self):
                return (
                    "font_family                  Roboto Mono\n"
                    "font_size                    12.5\n"
                    "\n"
                    "italic_font                  auto\n"
                    "bold_italic_font             auto\n"
                    "allow_remote_control         yes\n"
                    "\n"
                    "# #: Keyboard shortcuts\n"
                    "# map ctrl+q close_tab\n"
                    "# map ctrl+t new_tab\n"
                    "# map ctrl+j previous_tab\n"
                    "# map ctrl+k next_tab\n"
                    "# map ctrl+shift+j move_tab_backward\n"
                    "# map ctrl+shift+k move_tab_forward\n"
                    "# map page_up scroll_page_up\n"
                    "# map page_down scroll_page_down\n"
                    "# map ctrl+f2 set_tab_title\n"
                    "\n"
                    "background_opacity 0.8\n"
                    "\n"
                    "map ctrl+shift+f2 unmap"
                )

            def writeDataToConfigFile(self, changedFontConfig):
                if changedFontConfig:
                    self.writeSuccessful = True



        def getExpectedConfigData():
            return (
                "font_family                  JetBrainsMono\n"
                "font_size                    13.5\n"
                "\n"
                "italic_font                  auto\n"
                "bold_italic_font             auto\n"
                "allow_remote_control         yes\n"
                "\n"
                "# #: Keyboard shortcuts\n"
                "# map ctrl+q close_tab\n"
                "# map ctrl+t new_tab\n"
                "# map ctrl+j previous_tab\n"
                "# map ctrl+k next_tab\n"
                "# map ctrl+shift+j move_tab_backward\n"
                "# map ctrl+shift+k move_tab_forward\n"
                "# map page_up scroll_page_up\n"
                "# map page_down scroll_page_down\n"
                "# map ctrl+f2 set_tab_title\n"
                "\n"
                "background_opacity 0.8\n"
                "\n"
                "map ctrl+shift+f2 unmap"
            )
        # GIVEN the following preconditions corresponding to the system under test:
        fontName = "JetBrainsMono"
        fontSize = "13.5"
        kittyTerminal = FakeKittyTerminal("")
        fontChanger = FontConfiguration(kittyTerminal)
        # WHEN the following module is executed:
        fontChanger.changeFont(fontName, fontSize)
        # THEN the observable behavior should be verified as stated below:
        self.assertTrue(kittyTerminal.writeSuccessful)

if __name__ == '__main__':
    unittest.main(testRunner=ColourTextTestRunner(), verbosity=2)
