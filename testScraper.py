import pytest

from Youtube_scraper import VideoParser

class TestVideoParser:

    def testUrlValid(self):
        v = VideoParser("https://www.youtube.com/watch?v=OY-dBg3slzM")
        assert(v.description is None) is True

    def testVideoDoesntExist(self):
        with pytest.raises(Exception, match=r"Cette vidéo n'existe pas"):
            v = VideoParser("https://www.youtube.com/watch?v=kldjfmqlksf")

    def testgetTitle(self):
        v = VideoParser("https://www.youtube.com/watch?v=pAnld0aOxfQ")
        assert(v.getTitle() == "Plato, le robot fran\u00e7ais qui va vous servir au restaurant") is True

    def testgetAuthor(self):
        v = VideoParser("https://www.youtube.com/watch?v=pAnld0aOxfQ")
        assert(v.getAuthor() == "Le Parisien") is True

    def testgetLikes(self):
        v = VideoParser("https://www.youtube.com/watch?v=AjeReBve-Ow")
        assert(v.getLikes() == 1) is True
    
    def testgetNoLink(self):
        v = VideoParser("https://www.youtube.com/watch?v=pAnld0aOxfQ")
        assert(len(v.getLinks()) == 0) is True

    def testgetLinks(self):
        v = VideoParser("https://www.youtube.com/watch?v=UBDY5mjtuNE")
        assert(len(v.getLinks()) == 12) is True

    def testgetSpecificLinks(self):
        v = VideoParser("https://www.youtube.com/watch?v=UBDY5mjtuNE")
        assert(v.getLinks()[0] == "https://www.youtube.com/watch?v=k16zhsMI9dM") is True

    def testDescription(self):
        v = VideoParser("https://www.youtube.com/watch?v=pAnld0aOxfQ")
        desc = "Plato est un robot \"passe plat\", con\u00e7u en France pour accompagner les serveurs dans leurs service."
        assert(v.getDescription() == desc) is True
