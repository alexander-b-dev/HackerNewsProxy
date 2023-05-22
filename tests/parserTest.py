import unittest
from parser import AddTM


class AddTMTest(unittest.TestCase):

    def setUp(self):
        testHTML = """
            <!DOCTYPE html>
            <html>
                <body>
                    <h1>Testing pure text. Circle is a key word</h1>
                    <p>Testing text with punctuation. (Client) is a key word</p>
                    <p>Testing not word value. 123456 is a key sequence</p>
                    <p title="I'm a tooltip. A keyword is coffee">Testing a tooltip.</p>
                </body>
            </html>
        """
        parser = AddTM()
        self.parsedText = parser.feed(testHTML)

    def test_PureText(self):
        self.assertEqual(True, ("Testing pure text. Circle&#8482; is a key word" in self.parsedText))

    def test_Punctuation(self):
        self.assertEqual(True, ("Testing text with punctuation. (Client&#8482;) is a key word" in self.parsedText))

    def test_NotWordValue(self):
        self.assertEqual(True, ("Testing not word value. 123456 is a key sequence" in self.parsedText))

    def test_Tooltip(self):
        self.assertEqual(True, ("I'm a tooltip. A keyword is coffee&#8482;" in self.parsedText))


if __name__ == '__main__':
    unittest.main()
