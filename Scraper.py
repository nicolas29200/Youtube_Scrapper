
import sys
import json

from Youtube_scraper import VideoParser
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