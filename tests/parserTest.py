# -*- coding: utf-8 -*-
import unittest

import config
from parser import HTMLWorker


class HTMLWorkerTest(unittest.TestCase):

    def setUp(self):
        testHTML = """
            <!DOCTYPE html>
            <html>
                <body>
                    <h1>Testing pure text. Circle is a key word</h1>
                    <p>Testing text with punctuation. (Client) is a key word</p>
                    <p>Testing not word value. 123456 is a key sequence</p>
                    <p>Testing russian language. Камера is a key word</p>
                    <p>Testing german language. Großes is a key word</p>
                    <p>Testing html codes. '&%amp;#8209; non-breaking hyphen' is a key sequence</p>
                    <p>Testing html codes. 'some&#x27;path' is a key sequence</p>
                    <p title="I'm a tooltip. A keyword is coffee">Testing a tooltip.</p>
                    <a href="https://news.ycombinator.com"></a>
                </body>
            </html>
        """
        parser = HTMLWorker(config.originURL, "http://localhost:5000/")
        self.parsedText = parser.feed(testHTML)

    def test_PureText(self):
        self.assertEqual(True, ("Testing pure text. Circle&#8482; is a key word" in self.parsedText))

    def test_Punctuation(self):
        self.assertEqual(True, ("Testing text with punctuation. (Client&#8482;) is a key word" in self.parsedText))

    def test_NotWordValue(self):
        self.assertEqual(True, ("Testing not word value. 123456 is a key sequence" in self.parsedText))

    def test_Tooltip(self):
        self.assertEqual(True, ("I'm a tooltip. A keyword is coffee&#8482;" in self.parsedText))

    def test_Links(self):
        self.assertEqual(True, ('href="http://localhost:5000"' in self.parsedText))

    def test_Russan(self):
        self.assertEqual(True, ("Testing russian language. Камера&#8482; is a key word" in self.parsedText))

    def test_German(self):
        self.assertEqual(True, ("Testing german&#8482; language. Großes&#8482; is a key word" in self.parsedText))

    def test_entityref(self):
        self.assertEqual(True, ("'&%amp;#8209; non-breaking hyphen&#8482;' is a key sequence" in self.parsedText))

    def test_charref(self):
        self.assertEqual(True, ("'some&#x27;path' is a key sequence" in self.parsedText))


if __name__ == '__main__':
    unittest.main()
