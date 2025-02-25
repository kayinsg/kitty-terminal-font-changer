import sqlite3

class DatabaseFontUpload:
    def __init__(self):
        self.database= self.getDatabaseConnection()

    @staticmethod
    def getDatabaseConnection():
        databaseConnection = sqlite3.connect('fonts.db')
        cursor = databaseConnection.cursor()
        return {
            'connection': databaseConnection,
            'cursor': cursor,
        }

    def upload(self, listOfFontSelects):
        databaseInteractor = self.database['cursor']
        self.createFontTable(databaseInteractor)
        self.insertFontsWithinTable(databaseInteractor, listOfFontSelects)

        self.database['connection'].commit()

    def createFontTable(self, databaseInteractor):
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
    
    def insertFontsWithinTable(self, databaseInteractor, listOfFontSelects):
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
