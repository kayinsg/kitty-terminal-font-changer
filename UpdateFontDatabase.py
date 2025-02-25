import sqlite3

class FontRepository:
    def __init__(self, databaseName):
        self.database = self.getDatabaseConnection(databaseName)

    @staticmethod
    def getDatabaseConnection(databaseName) -> dict:
        databaseConnection = sqlite3.connect(databaseName)
        cursor = databaseConnection.cursor()
        return {
            'connection': databaseConnection,
            'cursor': cursor,
        }

class DatabaseFontUpload:
    def __init__(self, database):
        self.database= database

    def upload(self, listOfFontSelects) -> None:
        databaseInteractor = self.database['cursor']
        self.createStandardFontTable(databaseInteractor)
        self.createCachedFontTable(databaseInteractor)
        self.insertFontsWithinTable(databaseInteractor, listOfFontSelects)

        self.database['connection'].commit()

    def createStandardFontTable(self, databaseInteractor: sqlite3.Cursor) -> None:
        databaseInteractor.execute(
            """
            CREATE TABLE Fonts
            (
            FontID INTEGER PRIMARY KEY AUTOINCREMENT,
            ShortenedName,
            FullFontName,
            )
            """
        )

    def createCachedFontTable(self, databaseInteractor: sqlite3.Cursor) -> None:
        databaseInteractor.execute(
            """
            CREATE TABLE CachedFonts
            (
            FontID INTEGER PRIMARY KEY AUTOINCREMENT,
            ShortenedName,
            FullFontName,
            FontSize NULL
            )
            """
        )

    def insertFontsWithinTable(
        self,
        databaseInteractor: sqlite3.Cursor,
        listOfFontSelects,
    ) -> None:
        for fontID, font in enumerate(listOfFontSelects):
            databaseInteractor.execute(
                f"""
                INSERT INTO Fonts 
                VALUES
                (
                '{fontID}',
                '{font.shortenedFontName}',
                '{font.standardFontName}'
                )
                """
            )

class DatabaseFontInquirer:
    def __init__(self, database):
        self.database = database

    def retrieveFonts(self):
        shortenedFonts = self.fetchFontsForUserView(self.database['cursor'])
        self.flattenCollectionOfFonts(shortenedFonts)

    def fetchFontsForUserView(self, databaseInteractor: sqlite3.Cursor) -> list[tuple]:
        shortenedFontNames = databaseInteractor.execute(
            "SELECT ShortenedName FROM Fonts"
        )
        return shortenedFontNames.fetchall()

    def flattenCollectionOfFonts(self, shortenedFonts):
        flattenedShortenedFontNames = list()
        for fontTuple in shortenedFonts:
            flattenedShortenedFontNames.append(fontTuple[0])
