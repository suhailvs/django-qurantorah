import urllib.request
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
parseurl = lambda url: urllib.request.urlopen(url).read()
PATTERNS = {
	'aleph': 'a',
	'beth': 'b',
	'gimel': 'g',
 	'daleth': 'd',
	'he': 'e',
	'vav': 'f', # y
	'zayin': 'z',
	'cheyth': 'h', # heth
 	'teyth': 'j', # teth
	'yowd': 'i', # yodh, j
	'kaph': 'k',
	'lamed': 'l', # lamedh
	'mem': 'm',
	'nuwn': 'n', # nun
	'samek': 'x', # samekh
	'ayin': 'o',
	'phe': 'p', # pe
	'tsadey': 's', # tsade -
	'qowph': 'q', # qoph
	'reysh': 'r', # resh
	'shiyn': 'c', # shin s
	'thav': 't', # taw
}

def soupparser(html_doc):
	soup = BeautifulSoup(html_doc, 'html.parser')
	lines = []
	for i,table in enumerate(soup.find_all('table')):
		if i>2:
			words = []
			for td in table.find_all('td'):				
				contents = td.contents
				try:
					if 'src' in contents[0].attrs: pass
				except: 
					continue
				word = ''
				subline = []
				for content in contents:
					# a full line
					if isinstance(content,Tag):
						if 'src' in content.attrs:
							letter = content.attrs['src'].rstrip('.gif')[1:]
							word+=PATTERNS[letter]
						else:
							# linebreak
							if word:
								subline.append(word)
								word = ''
								subline.reverse()
								# print(subline)
								for l in subline:
									words.append(l)
								subline = []
								
							
					else: 
						# if space
						if word:
							subline.append(word)							
							word = ''
			if words:
				words.reverse()
				lines.append(' '.join(words))
	return lines

# html_doc = parseurl('http://www.hebrewoldtestament.com/B01C001.htm')
#fp =open('html.txt')
#html_doc = fp.read()
v = []
for i in range(1,35):
	html_doc = parseurl('http://www.hebrewoldtestament.com/B05C0%02d.htm'%i)
	v.append(soupparser(html_doc))

data = { 
    "versionTitle": "Paleo Hebrew",
    "language": "ph", 
    "title": "Deuteronomy", 
    "text": v
}
import json
with open('%s.json'%data['title'].lower(), 'w') as outfile:
    json.dump(data, outfile,indent = 4)
