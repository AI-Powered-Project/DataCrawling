from bs4 import BeautifulSoup
import requests
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk import Text
import matplotlib.pyplot as plt
from nltk import FreqDist
from wordcloud import WordCloud
from collections import Counter

class CheckDataLink():
    def __init__(self):
        pass
    def getTargetList(self, searchWord):
        result = []
        for pagenum in range(1,6):
            # checking target list from craigslist
            url = f'https://sfbay.craigslist.org/search/hhh?query={searchWord}#search=1~gallery~{pagenum}~0'
            response = requests.get(url)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                # print(soup)
                titles = soup.select('.cl-static-search-result')
                # print(titles)
                for title in titles:        
                    a = title.select_one('a')   
                    result.append(a.attrs['href'])
            else : 
                print(response.status_code)
        return result
    def getTargetData(self, targetUrl):
        # get target data from craigslist
        response = requests.get(targetUrl)
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # print(soup)
            main = soup.select_one('#postingbody').get_text()
            # print(titles)
            return main[30:]
        else : 
            print(response.status_code)
    def wordFilter(self, targetList):
        result = []
        lm = WordNetLemmatizer()
        lenoflist = len(targetList)
        count = 1
        for maintext in targetList:
            tokenised = word_tokenize(maintext)
            for token in tokenised:
                target = pos_tag([token])
                if (target[0][1][0] == 'N' or target[0][1][0] == 'J') and len(target[0][0]) > 1:
                    result.append(lm.lemmatize(token))
            print(str(count) +'/' +str(lenoflist) + 'is done')
            count += 1
        return result
    def countWords(self, targetList):
        # counting words
        return 1
    def openJson(self, name):
        # opening json file
        with open(name, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data
    def saveJson(self, listForJson, name):
        # saving json file
        with open(name, 'w', encoding='utf-8') as file:
            json.dump(listForJson, file, ensure_ascii=False, indent='\t')
        print('saved')

def crawlingandSaveJson():
    mainText = []
    checkDataLink = CheckDataLink()
    targetUrlList = checkDataLink.getTargetList('roommate')
    count = 0
    lenoflist = len(targetUrlList)
    for targetUrl in targetUrlList:
        mainText.append(checkDataLink.getTargetData(targetUrl))
        print(str(count) +'/' +str(lenoflist) + 'is done')
        count += 1

    checkDataLink.saveJson(mainText,'crawlingResult.json')
def filterWords():
    checkDataLink = CheckDataLink()
    targetList = checkDataLink.openJson('crawlingResult.json')
    filterdWord = checkDataLink.wordFilter(targetList)
    checkDataLink.saveJson(filterdWord,'filterdWord.json')
def countWords():
    checkDataLink = CheckDataLink()
    targetList = checkDataLink.openJson('filterdWord.json')
    count = checkDataLink.countWords(targetList)
    checkDataLink.saveJson(count,'countWord.json')
def resultGraph():
    checkDataLink = CheckDataLink()
    targetList = checkDataLink.openJson('filterdWord.json')
    text = Text(targetList)
    text.plot(50)
    plt.show()
def wordCloud():
    checkDataLink = CheckDataLink()
    targetList = checkDataLink.openJson('filterdWord.json')
    counts = Counter(targetList)
    tags = counts.most_common(200) 
    wc = WordCloud(width=1000, height=1000, background_color="white", random_state=0)
    plt.imshow(wc.generate_from_frequencies(dict(tags)))
    plt.axis("off")
    plt.show()
def main():
    pass
if __name__ == '__main__':
    main()