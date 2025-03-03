import os
from SystemFontExtractor import FontSelectorDetails
from FontArchive import FontRepository
from UserFontPicker import FontMenu
from FontChanger import FontChanger, TerminalRestart

fontDatabaseName = 'fonts.db'

def databasePath(fontDatabaseName):
    workingDirectory = os.getcwd()
    return os.path.join(workingDirectory, fontDatabaseName)

def getFontFromUser():
    return input("What should the size of the font be? ")

database = FontRepository(fontDatabaseName)
fontCollection = FontSelectorDetails().get()
database.setup()
userFonts = database.getFontsForUserView()
userFontName = FontMenu(userFonts).letUserPickFont()
userFontSize = getFontFromUser()
FontChanger(userFontName, userFontSize).applyChanges()
TerminalRestart().execute()
