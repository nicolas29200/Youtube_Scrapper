from bs4 import BeautifulSoup
import requests
from typing import List
import json
import re


class VideoParser:
    url : str
    description : str
    likes : int
    links : list
    title : str
    author : str
    def __init__(self, url : str)->None:

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
