from html.parser import HTMLParser


class HTMLWorker(HTMLParser):  # class for reconstructing html

    def __init__(self, originServ, proxyServ):
        super().__init__(convert_charrefs=False)  # to prevent double encoding
        self.newHTML = ""
        self.originServ = originServ
        self.proxyServ = proxyServ

    # here needed to process title, alt, value and href tags, but also method can be used it for img caching
    def handle_starttag(self, tag, attrs):
        tagLine = "<" + tag
        for attr in attrs:
            if len(attr) == 1:
                tagLine += ' %s' % attr[0]
            elif len(attr) == 2:
                if attr[0] in ["title", "alt", "value"]:
                    tagLine += ' %s="%s"' % (attr[0], self.processText(attr[1]))
                elif attr[0] == "href":
                    tagLine += ' %s="%s"' % (attr[0],
                                             attr[1].replace(self.originServ.strip("/"), self.proxyServ.strip("/")))
                else:
                    tagLine += ' %s="%s"' % (attr[0], attr[1])

        tagLine += ">"
        self.newHTML += tagLine

    def handle_endtag(self, tag):  # only saving origin
        self.newHTML += "</%s>" % tag

    def handle_entityref(self, name):  # to prevent double encoding smth like &%amp; (&)
        self.newHTML += "&%s;" % name

    def handle_charref(self, name):  # to prevent double encoding smth like &%x27; (/)
        self.newHTML += "&#%s;" % name

    def handle_data(self, data):  # process text nodes
        self.newHTML += self.processText(data)

    @staticmethod
    def processText(txt, splitSymbol=" "):  # adding trademark symbol to words exactly 6 letters long
        words = txt.split(splitSymbol)
        newText = []
        punctuation = "(.,:;?!-)\"'[]{}/\\|\n`~*_\t"
        for word in words:
            # Word can be wrapped in brackets, or be followed by punctuation or
            # have missing whitespaces like word1\nword2, word1,word2, etc.
            # Here is recursive itteration to clear all punctuation and restore it after
            spareSymbol = next((symbol for symbol in punctuation if symbol in word), None)
            if spareSymbol:
                newText.append(HTMLWorker.processText(word, spareSymbol))
                continue
            else:
                # interested only in words. Unfortunately, nicks like }{0ta6 won't be recognised as words
                if len(word) == 6 and word.isalpha():
                    word += "&#8482;"  # trademark html code
                newText.append(word)
        return splitSymbol.join(newText)

    def feed(self, data):
        self.newHTML = ""
        HTMLParser.feed(self, data)
        return self.newHTML
