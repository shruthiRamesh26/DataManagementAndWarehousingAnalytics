import re
import string

files=['reut2-020.sgm','reut2-021.sgm']

def cleanData(text):
#removce ascii characters
    text.encode('ascii', 'ignore')
    text=text.rstrip()
	#remove all tags
    text=re.sub(r'<[^>]+>',' ',text)
	#remove url
    text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
	#remove non alpha-numeric characters
    text = re.sub(r'([^a-zA-Z0-9\s]|_)+', '', text)
	#remove metacharacter \n
    text=re.sub(r'[\n]', ' ',text)
	#removce non-printable characters like emoticons
    printable = set(string.printable)
    text = list(filter(lambda x: x in printable, text))

    return ''.join(text)


count=1
for file in files:
	#opening reuters files
    fopen = open('./reutFiles/'+file, 'r')
	#reading content of reuter files
    content=fopen.read()
    split=re.split('<TEXT>',content)
    for article in split[1:]:
		#splitting the contebt on <TEXT> & </TEXT> tags
        article=re.split('</TEXT>',article)
        with open("./articles/article" + str(count) + ".txt", "w+") as f:
			#Creating new files with each <TEXT> tag content
            f.write(cleanData(article[0]))
        count += 1




