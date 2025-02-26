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

fontDatabaseAlreadyExists = os.path.exists(databasePath(fontDatabaseName))
if fontDatabaseAlreadyExists:
    database = FontRepository(fontDatabaseName)
    userFonts = database.getFontsForUserView()
    userFontName = FontMenu(userFonts).letUserPickFont()
    userFontSize = getFontFromUser()
    FontChanger(userFontName, userFontSize).applyChanges()
    TerminalRestart().execute()
else:
    database = FontRepository(fontDatabaseName)
    fontCollection = FontSelectorDetails().get()
    database.setup(fontCollection)
    userFonts = database.getFontsForUserView()
    userFontName = FontMenu(userFonts).letUserPickFont()
    userFontSize = getFontFromUser()
    FontChanger(userFontName, userFontSize).applyChanges()
    TerminalRestart().execute()
