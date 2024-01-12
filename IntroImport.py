import os
from urllib.request import urlretrieve

def main():
    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)
    os.mkdir("data")
    downlink = "https://www.football-data.co.uk/mmz4281/"
    leagues = ["E0", "F1", "D1", "SP1", "I1", "N1"]
