import sqlite3

class DatabaseFontUpload:
    def __init__(self, databaseName):
        self.database= self.getDatabaseConnection(databaseName)

    @staticmethod
    def getDatabaseConnection(databaseName) -> dict:
        databaseConnection = sqlite3.connect(databaseName)
        cursor = databaseConnection.cursor()
        return {
            'connection': databaseConnection,
            'cursor': cursor,
        }

    def upload(self, listOfFontSelects) -> None:
        databaseInteractor = self.database['cursor']
        self.createFontTable(databaseInteractor)
        self.insertFontsWithinTable(databaseInteractor, listOfFontSelects)

        self.database['connection'].commit()

    def createFontTable(self, databaseInteractor: sqlite3.Cursor) -> None:
        databaseInteractor.execute(
            """
            CREATE TABLE Fonts
            (
            FontID INTEGER PRIMARY KEY AUTOINCREMENT,
            ShortenedName,
            FullFontName
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
