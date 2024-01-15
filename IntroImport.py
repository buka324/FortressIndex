import os
from urllib.request import urlretrieve

def main():
    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)
    os.mkdir("data")
    downlink = "https://www.football-data.co.uk/mmz4281/"
    leagues = ["E0", "F1", "D1", "SP1", "I1", "N1"] # download argentina and brazil later
    os.chdir("data")
    for league in leagues:
        os.mkdir(league)
        for year in range(12,24):
            urlretrieve(downlink + str(year) + str(year+1) + "/" + league + ".csv", league + "/" + str(year) + str(year+1) + ".csv") # direct these into the league folders
    urlretrieve("https://www.football-data.co.uk/new/BRA.csv", "BRA.csv")
    urlretrieve("https://www.football-data.co.uk/new/ARG.csv", "ARG.csv")
main()