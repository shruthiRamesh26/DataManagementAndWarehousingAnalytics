import json
import os
import math



files=os.listdir('./articles')
to_find=["canada", "halifax","nova scotia"]
to_find=set(to_find)
array={}
data1 = dict()

def wordCount(filename,text):
    data = []
    text=text.split()
    for word in to_find:
        count=text.count(word)
        if count!=0:
            totalWords = text.__len__()
            element = {}
            relFreq=count/totalWords
            element.update({"count": count, "totalwords": totalWords, "filename": filename,"relFreq":relFreq})
            data.append(element)
            if word in data1:
                a=data1[word]
                # append the new number to the existing array at this slot
                a.append(element)
                data1[word]=a
            else:
                # create a new array in this slot
                data1[word]= data



for filename in files:
        with open(os.path.join('./articles', filename)) as f:
            content = f.read()
            if to_find & set(content.split()):
                wordCount(filename,content)
totalFiles=len(files)

for word in to_find:
    if word in data1:
        df=len(data1[word])
        frequency=math.log10(totalFiles / df)
        #term frequency
        print('%s appeared in %i documents with term frequency %f'%(word,len(data1[word]),frequency))

        seq = [x['relFreq'] for x in data1[word]]
        #maximum relative frequency
        print("%s has highest relative frequency of %f for word '%s'"%((max(data1[word], key=lambda x:x['relFreq'])['filename']),(max(data1[word], key=lambda x:x['relFreq'])['relFreq']),word))
#output file
with open('semanticOutput.json', 'w+') as json_file:
    json.dump(data1, json_file)














