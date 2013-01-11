#!/usr/bin/python
# -- coding: utf-8 --
import tweepy, os, sys, re, string, HTMLParser
from optparse import OptionParser

########################################
#Function Definitons
########################################
# Break string into multiple lines/paragraphs
def para(text):
    return reduce(lambda line, word, width=50: '%s%s%s' %(line, ' \n'[(len(line)-line.rfind('\n')-1
    + len(word.split('\n',1)[0]) >= 50)], word), text.split(' '))

def tweetReTweet(text):
	if text.find('@')!=-1:
		text=text.partition(': ')[2]
		
	return text

# Convert html entities into Unicode
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text

    return string.replace(re.sub("&#?\w+;", fixup, text)," -", "\n\n-")

########################################
#Main
########################################

parser = OptionParser()
parser.add_option("-u", "--user", dest="username",
                  help="User to Quote", metavar="USER",default="Inspire_Us")

(options, args) = parser.parse_args()

api=tweepy.api

type = api.user_timeline(include_rts=True, screen_name=options.username)
for result in type:
	#Remove advertisements
    if result.text.find('http://')==-1:
        twtu = result.user.screen_name
        twtt = result.text
        print unescape(HTMLParser.HTMLParser().unescape(para(tweetReTweet(twtt.encode('utf-8').strip()))))
        break