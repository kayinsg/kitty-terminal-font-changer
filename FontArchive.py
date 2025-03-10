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

    def setup(self):
        DatabaseFontTable(self.database).create()

    def getFontsForUserView(self):
        return DatabaseFontInquirer(self.database).retrieveFonts()


class DatabaseFontTable:
    def __init__(self, database):
        self.database= database

    def create(self) -> None:
        databaseInteractor = self.database['cursor']

        self.createStandardFontTable(databaseInteractor)
        self.createCachedFontTable(databaseInteractor)

        self.database['connection'].commit()

    def createStandardFontTable(self, databaseInteractor: sqlite3.Cursor) -> None:
        databaseInteractor.execute(
            """
            CREATE TABLE IF NOT EXISTS Fonts
            (
            FontID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
            ShortenedName UNIQUE,
            FullFontName UNIQUE
            )
            """
        )

    def createCachedFontTable(self, databaseInteractor: sqlite3.Cursor) -> None:
        databaseInteractor.execute(
            """
            CREATE TABLE IF NOT EXISTS CachedFonts
            (
            FontID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
            ShortenedName UNIQUE,
            FullFontName UNIQUE,
            FontSize NULL
            )
            """
        )


class DatabaseFontUpload:
    def __init__(self, database):
        self.database = database

    def uploadFonts(self, listOfFonts):
        self.insertFontsWithinTable(self.database['cursor'], listOfFonts)

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
        return self.flattenCollectionOfFonts(shortenedFonts)

    def fetchFontsForUserView(self, databaseInteractor: sqlite3.Cursor) -> list[tuple]:
        shortenedFontNames = databaseInteractor.execute(
            "SELECT ShortenedName FROM Fonts"
        )
        return shortenedFontNames.fetchall()

    def flattenCollectionOfFonts(self, shortenedFonts):
        return list(
            map(
                lambda shortenedFontName: shortenedFontName[0],
                shortenedFonts
            )
        )
