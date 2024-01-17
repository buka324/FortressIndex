import pandas as pd
import requests
import os
import csv
import FortressAndMatch
from urllib.request import urlretrieve
import difflib
import datetime

leagues_by_api = {"78":"DEU", "61":"FRA", "39":"ENG", "140":"SPA", "135":"ITA", "88":"NED"}


def firstrun(): 
    if not os.path.isdir("data"):
        os.mkdir("data")
        os.chdir("data")
        downlink = "https://www.football-data.co.uk/mmz4281/"
        leagues = ["D1", "F1","E0", "SP1", "I1", "N1"]
        for league in leagues:
            os.mkdir(league)
            curryear = datetime.datetime.now().year
            for year in range(12,curryear-2000): #replace 24 with the current year's last two digits
                urlretrieve(downlink + str(year) + str(year+1) + "/" + league + ".csv", league + "/" + str(year) + str(year+1) + ".csv") # direct these into the league folders
        os.chdir("..")
        headers = {
            "X-RapidAPI-Key": os.environ["FOOTBALL_API_KEY"],
	        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        teams = {}
        index = 0 #I'd love to make a better way to do this, but it's 4am
        for league in leagues_by_api:
            response = requests.get("https://api-football-v1.p.rapidapi.com/v3/teams", headers=headers, params={"league": league})
            data = response.json()
            abbvs = []
            with open("data/" + leagues[index] + "/2324.csv") as csvfile:
                reader = csv.DictReader(csvfile)
                for _item in range(data["response"].len()//2):
                    row = reader.next()
                    abbvs.append(row["HomeTeam"])
                    abbvs.append(row["AwayTeam"])
            for team in data["response"]:
                abbv = difflib.get_close_matches(team["team"]["name"], abbvs, cutoff=0, n=1)[0] #will this let me do this?
                teams[team["team"]["name"]] = (leagues_by_api[league], abbv)
            index += 1
        forts = []
        # forts = pd.DataFrame(columns=["Team", "League", "Fortress Index", "Home PPG", "Home GA PG", "Home Ratio", "Home Matches", "Home Points", "Matches", "Points", "Home GA"])
        for team in teams:
            forts.append(FortressAndMatch.makeFortressFromTeam(team, teams[team][0], teams[team][1]))
            #I need to make checks for missed names. any team with an abbreviation is at risk.
        forts.sort(key=lambda x: x.fortressIndex(), reverse=True)
        with open("data/fortresses.csv", "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["Team", "League", "Fortress Index", "Home PPG", "Home GA PG", "Home Ratio", "Home Matches", "Home Points", "Matches", "Points", "Home GA"])
            writer.writeheader()
            for fortress in forts:
                writer.writerow({"Team": fortress.name, "League": teams[fortress.name][0], "Fortress Index": fortress.fortressIndex(), "Home PPG": fortress.homePPG(), "Home GA PG": fortress.homeGAPG(), "Home Ratio": fortress.homeRatio(), "Home Matches": fortress.homeMatches, "Home Points": fortress.homePoints, "Matches": fortress.matches, "Points": fortress.points, "Home GA": fortress.homeGA})
        return True
    else: return False

def main():
    if firstrun():
        print("First run complete. Please restart the program.")
        exit()
    else:
        os.chdir("data")
        current = datetime.date.today() - datetime.timedelta(days=1)
        #pull the forts file into a dataframe for searching and rewriting.
        headers = {
            "X-RapidAPI-Key": os.environ["FOOTBALL_API_KEY"],
	        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        for league in leagues_by_api:
            response = requests.get("https://api-football-v1.p.rapidapi.com/v3/fixtures"
, headers=headers, params={"date": current.strftime("%Y-%m-%d"), "league": league}).json()
            #use the response to make matches and find forts
    #current date -1
    #do a match request for each league, put into match objects in a list or set
    #pull from database file storing fortresses, put into pandas dataframe
    #for each match, check if its 2 fortresses exists in dataframe
    #if not send None to Match
    #iterate over the set of matches calling addmatch on each
    #overwrite database file with new dataframe 