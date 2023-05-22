import re
from html.parser import HTMLParser


class AddTM(HTMLParser):  # class for reconstructing html

    def __init__(self):
        super().__init__()
        self.newHTML = ""

    # here needed to process title and alt tag, but also method can be used it for img caching
    def handle_starttag(self, tag, attrs):
        tagLine = "<" + tag
        for attr in attrs:
            if len(attr) == 1:
                tagLine += ' %s' % attr[0]
            elif len(attr) == 2:
                if attr[0] in ["title", "alt"]:
                    tagLine += ' %s="%s"' % (attr[0], self.processText(attr[1]))
                else:
                    tagLine += ' %s="%s"' % (attr[0], attr[1])

        tagLine += ">"
        self.newHTML += tagLine

    def handle_endtag(self, tag):  # only saving origin
        self.newHTML += "</%s>" % tag

    def handle_data(self, data):  # process text nodes
        self.newHTML += self.processText(data)

    @staticmethod
    def processText(txt):  # adding trademark symbol to words exactly 6 letters long
        words = txt.replace("\n", " ").split(" ")  # sometimes \n occures in html, there no sence in them
        newText = ""
        for word in words:
            tmp = word.strip("(.,:;?!)\"'[]{}/\\|\n")  # word can be wrapped in brackets, or be followed by punctuation
            # regexp for word contains only letters and exactly 6 letters long,
            # to prevent adding symbol to all other staff
            if re.match(r"^[A-z]{6}$", tmp):
                tmp += "&#8482;"  # trademark html code
                newText += " %s" % word.replace(tmp[:-7], tmp)
            else:
                newText += " %s" % word
        return newText

    def feed(self, data):
        self.newHTML = ""
        HTMLParser.feed(self, data)
        return self.newHTML
