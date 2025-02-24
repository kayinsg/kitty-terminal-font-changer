import sqlite3


databaseConnection = sqlite3.connect('fonts.db')
cursor = databaseConnection.cursor()
cursor.execute(
            """
            CREATE TABLE Fonts
            (
            FontID INTEGER PRIMARY KEY AUTOINCREMENT,
            ShortenedName,
            FullFontName
            )
            """
)

fontSelects = systemFontDataExtractor.FontSelectorDetails().get()
for fontID, font in enumerate(fontSelects):
    cursor.execute(
        f"""
        INSERT INTO Fonts 
        VALUES
        (
        '{fontID}',
        '{font.shortenedFontName}',
        '{font.standardFontName}'
        """
    )

databaseConnection.commit()
