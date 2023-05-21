import re
from html.parser import HTMLParser


class AddTM(HTMLParser):

    def __init__(self):
        super().__init__()
        self.newHTML = ""

    def handle_starttag(self, tag, attrs):
        tagLine = "<" + tag
        for attr in attrs:
            tagLine += ' %s="%s"' % (attr[0], attr[1])
        tagLine += ">"
        self.newHTML += tagLine

    def handle_endtag(self, tag):
        self.newHTML += "</%s>" % tag

    def handle_data(self, data):
        words = data.replace("\n", " ").split(" ")
        newText = ""
        for word in words:
            tmp = word.strip("(.,:;?!)\"'[]{}/\\|\n")
            if re.match(r"^[A-z]{6}$", tmp):
                tmp += "&#8482;"
                newText += " %s" % word.replace(tmp[:-7], tmp)
            else:
                newText += " %s" % word
        self.newHTML += newText

    def feed(self, data):
        self.newHTML = ""
        HTMLParser.feed(self, data)
        return self.newHTML


if __name__ == "__main__":
    html = """ <tr class="spacer" style="height:5px"></tr>
                <tr class="athing" id="36008526">
      <td align="right" valign="top" class="title"><span class="rank">9.</span></td>      <td valign="top" class="votelinks"><center><a id="up_36008526" href="https://news.ycombinator.com/vote?id=36008526&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://axleos.com/">Axle OS</a><span class="sitebit comhead"> (<a href="https://news.ycombinator.com/from?site=axleos.com"><span class="sitestr">axleos.com</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_36008526">147 points</span> by <a href="https://news.ycombinator.com/user?id=mmphosis" class="hnuser">mmphosis</a> <span class="age" title="2023-05-20T01:13:49"><a href="https://news.ycombinator.com/item?id=36008526">9 hours ago</a></span> <span id="unv_36008526"></span> | <a href="https://news.ycombinator.com/hide?id=36008526&amp;goto=news">hide</a> | <a href="https://news.ycombinator.com/item?id=36008526">23&nbsp;comments</a>        </span>
              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class="athing" id="36006626">
      <td align="right" valign="top" class="title"><span class="rank">10.</span></td>      <td valign="top" class="votelinks"><center><a id="up_36006626" href="https://news.ycombinator.com/vote?id=36006626&amp;how=up&amp;goto=news"><div class="votearrow" title="upvote"></div></a></center></td><td class="title"><span class="titleline"><a href="https://praeclarum.org/2023/05/19/webgpu-torch.html">PyTorch for WebGPU</a><span class="sitebit comhead"> (<a href="https://news.ycombinator.com/from?site=praeclarum.org"><span class="sitestr">praeclarum.org</span></a>)</span></span></td></tr><tr><td colspan="2"></td><td class="subtext"><span class="subline">
          <span class="score" id="score_36006626">256 points</span> by <a href="https://news.ycombinator.com/user?id=mighdoll" class="hnuser">mighdoll</a> <span class="age" title="2023-05-19T20:42:43"><a href="https://news.ycombinator.com/item?id=36006626">14 hours ago</a></span> <span id="unv_36006626"></span> | <a href="https://news.ycombinator.com/hide?id=36006626&amp;goto=news">hide</a> | <a href="https://news.ycombinator.com/item?id=36006626">62&nbsp;comments</a>        </span>
              </td></tr>"""

    test = AddTM()
    print(test.feed(html))
