from bs4 import BeautifulSoup
import requests
from typing import List
import json
import re
import sys

class VideoParser:
    url : str
    description : str
    likes : int
    links : list
    title : str
    author : str
    def __init__(self, url : str)->None:
        # Is the URL valid?
        if not(url.startswith("https://www.youtube.com/watch?v=")):
            raise Exception("L'Url n'est pas valide")

        response = requests.get(url)        
        self.soup = BeautifulSoup(response.text, "html.parser")

        # La vidéo existe?
        if(self.soup.find("meta", itemprop="name") is None):
            raise Exception("Cette vidéo n'existe pas")

        self.url = url
        self.description = None
        self.body = self.soup.find_all("body")[0]
        self.scripts = self.body.find_all("script")
        self.result = json.loads(self.scripts[0].string[30:-1])

    def getTitle(self)->str: 
        self.title = self.result["videoDetails"]["title"]
        return self.title

    def getAuthor(self)->str: 
        self.author = self.result["videoDetails"]["author"]
        return self.author

    def getLikes(self)->int:
        data = re.search(r"var ytInitialData = ({.*?});", self.soup.prettify()).group(1)  
        data_json = json.loads(data)  
        videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
        likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label'] 
        self.likes = int(re.sub(r'[^0-9]', '', likes_label))
        return self.likes
    def getDescription(self)->str:
        self.description = self.result["videoDetails"]["shortDescription"]

        return self.description

    def getLinks(self)->List[str]:
        if(self.description is None):
            self.description = self.getDescription()
        #links
        self.links = re.findall(r"(?P<url>https?://[^\s]+)", self.description)
        #TimeStamps
        self.links += re.findall(r"[0-9]+:[0-9]{2}", self.description)

        return self.links

    def getDict(self)->dict :
        d = {}
        d['Title'] = self.getTitle()
        d['Author'] = self.getAuthor()
        d['NbLikes'] = self.getLikes()
        d['Description'] = self.getDescription()
        d['Links'] = self.getLinks()

        return d
   
#MAIN
if "__main__":
    if(len(sys.argv) != 5):
        raise Exception("Numbers of parameters incorrect. \n Utilisez python3 Scraper.py --input input.json --output output.json")
    # Formatage correct
    if not (sys.argv[2].endswith(".json") and sys.argv[4].endswith(".json")):
        raise Exception("Les fichiers ne sont pas dans le format .json\n Utilisez python3 Scraper.py --input input.json --output output.json")
    if not (sys.argv[1] == "--input" or sys.argv[3] == "--input"):
        raise Exception("Aucun input donné\n Utilisez python3 Scraper.py --input input.json --output output.json")
    if not (sys.argv[1] == "--output" or sys.argv[3] == "--output"):
        raise Exception("Aucun output donné\n Utilisez python3 Scraper.py --input input.json --output output.json")
    
    if (sys.argv[1] == "--input"):
        inputFile, outputFile = sys.argv[2], sys.argv[4]
    else :
        outputFile, inputFile = sys.argv[2], sys.argv[4]
        

    with open(inputFile, 'r') as my_file:
        videosId = json.load(my_file)['videos_id']
    res = {}
    for id in videosId:
        data = VideoParser(f"https://www.youtube.com/watch?v={id}").getDict()
        data['Id'] = id
        res[id]=data

    with open(outputFile, 'w') as f:
        f.write(json.dumps(res, indent=4))
