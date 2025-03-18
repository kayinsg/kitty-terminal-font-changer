import unittest
from FontChanger import FontChanger
from fontDataObjects import KittyTerminal

class TestFontChange(unittest.TestCase):
    def configData(self):
        return """
font_family ZedMono Nerd Font
font_size 13.8

italic_font                  auto
bold_italic_font             auto
allow_remote_control         yes
        """
    def modifiedData(self, fontName, fontSize):
        return f"""
font_family {fontName}
font_size {fontSize}

italic_font                  auto
bold_italic_font             auto
allow_remote_control         yes
        """
    def testFontChange(self):
        configData = self.configData()
        fontChanger = self.fontChanger(configData)
        fontName = "Pragmasevka Nerd Font"
        fontSize = 14

        result = fontChanger.change(fontName, fontSize)

        self.assertEqual(result, self.modifiedData(fontName, fontSize) )

    def fontChanger(self, configData):
       kittyTerminal = TestFontChange.FakeKittyTerminal(configData)
       return FontChanger(kittyTerminal)

    class FakeKittyTerminal(KittyTerminal):
        def __init__(self, data):
            self.path = ""
            self.data = data.split('\n')

        def saveChanges(self, updatedConfigData):
            if updatedConfigData and self.path:
                print("Config Was Changed Successfully")
                return True
            return False

unittest.main()
