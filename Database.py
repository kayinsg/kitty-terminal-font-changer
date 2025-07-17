class Database:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def insertFontsInDatabase(self, fontFamilies):
        self.createTables()
        self.insertDataIntoDatabase(fontFamilies)

    def createTables(self):
        DatabaseTableCreator(self.cursor).createTables()

    def insertDataIntoDatabase(self, fontFamilies):
        DatabaseDataInsert(self.conn, self.cursor).insertDataIntoTables(fontFamilies)

    def getFontFromDatabase(self, fontRequestedByUser):
        return DatabaseRetriever(self.conn).getFont(fontRequestedByUser)


class DatabaseTableCreator:
    def __init__(self, cursor):
        self.cursor = cursor

    def createTables(self):
        commands = [
            self.createFontsTable(),
            self.createFontStylesTable()
        ]
        self.createTablesForFonts(commands)

    def createFontsTable(self):
        return "CREATE TABLE IF NOT EXISTS Fonts (id INTEGER PRIMARY KEY, name TEXT)"

    def createFontStylesTable(self):
        return """
            CREATE TABLE IF NOT EXISTS FontStyles (
                id INTEGER PRIMARY KEY,
                name TEXT,
                font_id INTEGER,
                FOREIGN KEY(font_id) REFERENCES Fonts(id)
            )
        """

    def createTablesForFonts(self, sqlCommands):
        list(map(lambda command: self.cursor.execute(command), sqlCommands))


class DatabaseDataInsert:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def insertDataIntoTables(self, fontFamilies):
        self.assignPrimaryKeyToFonts(fontFamilies)
        self.assignForeignKeyToFontStyles(fontFamilies)

    def assignPrimaryKeyToFonts(self, fontFamilies):
        for family in fontFamilies:
            self.cursor.execute(
                "INSERT INTO Fonts (name) VALUES (?)",
                (family['Font Family'],)
            )
        self.conn.commit()

    def assignForeignKeyToFontStyles(self, fontFamilies):
        fontId = 1
        for family in fontFamilies:
            for child in family['Font Children']:
                self.cursor.execute(
                    "INSERT INTO FontStyles (name, font_id) VALUES (?, ?)",
                    (child, fontId)
                )
            fontId += 1
        self.conn.commit()


class DatabaseRetriever:
    def __init__(self, conn):
        self.conn = conn

    def getFont(self, fontRequestedFromUser):
        commandExecutor = self.getCommandExecutor()
        return self.selectUserSelectedFontFromDatabase(commandExecutor, fontRequestedFromUser)

    def getCommandExecutor(self):
        return self.conn.cursor()

    def selectUserSelectedFontFromDatabase(self, cursor, fontRequestedFromUser):
        cursor.execute("SELECT name FROM Fonts WHERE name = ?", (fontRequestedFromUser,))
        return cursor.fetchone()[0]
