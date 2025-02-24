import sqlite3

databaseConnection = sqlite3.connect('fonts.db')
cursor = databaseConnection.cursor()
cursor.execute(
    "CREATE TABLE Fonts(FontID INTEGER PRIMARY KEY AUTOINCREMENT, InterfaceFontName, FullFontName)"
)
fontSelects = systemFontDataExtractor.FontSelectorDetails().get()
for fontID, font in enumerate(fontSelects):
    cursor.execute(
        f"""
        INSERT INTO Fonts 
        VALUES
        (
        '{fontID}',
        '{font.standardFontName}',
        '{font.externalInterfaceValue}'
        )
        """
    )

databaseConnection.commit()
