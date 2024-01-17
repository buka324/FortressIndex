import csv
import os
import pandas as pd

class Fortress:
    def __init__(self, name, league):
        self.name = name
        self.points = 0
        self.homepoints = 0
        self.matches = 0
        self.homematches = 0
        self.homeGA = 0
    def homePPG(self):
        return float(self.homepoints)/float(self.homematches)
    def homeGAPG(self):
        return float(self.homeGA)/float(self.homematches)
    def homeRatio(self):
        ppg = float(self.points)/float(self.matches)
        return self.homePPG()/ppg
    def fortressIndex(self): return self.homePPG*self.homeRatio/self.homeGAPG

def pointsFromResult(result, team):
    if result == team: return 3
    elif result == "D": return 1
    else: return 0

def makeFortressFromTeam(club, league, abbv):
    fort = Fortress(club, league)
    os.chdir("data")
    match league:
        case "ENG":
            os.chdir("E0")
        case "DEU":
            os.chdir("D1")
        case "ITA":
            os.chdir("I1")
        case "SPA":
            os.chdir("SP1")
        case "FRA":
            os.chdir("F1")
        case "NED":
            os.chdir("N1")
        case default:
            print("Invalid league")
            os.chdir("..")
            exit()
    for file in os.listdir():
        if file.endswith(".csv"):
            with open(file) as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    fort.matches += 1
                    if row["HomeTeam"] == abbv: # may need to use regex here instead
                        fort.homepoints += pointsFromResult(row["FTR"], "H")
                        fort.points += pointsFromResult(row["FTR"], "H")
                        fort.homematches += 1
                        fort.homeGA += int(row["FTAG"])
                    elif row["AwayTeam"] == abbv:
                        fort.points += pointsFromResult(row["FTR"], "A")
        os.chdir("..")
    os.chdir("..")
    return fort

class Match:
    def __init__(self, jsonMatch):
        self.home = jsonMatch["teams"]["home"]["name"]
        self.away = jsonMatch["teams"]["away"]["name"]
        self.score = jsonMatch["score"]["fulltime"]
        if self.score["home"] > self.score["away"]: 
            self.result = "H"
        elif self.score["home"] < self.score["away"]: 
            self.result = "A"
        else: 
            self.result = "D"

def addMatch(home, away, match): #home and away are Fortresses. score is an int double (home first). This will be used later to update created fortresses
    if home != None:
        home.matches += 1
        home.homematches += 1
        home.points += pointsFromResult(match.result, "H")
        home.homepoints += pointsFromResult(match.result, "H")
        home.homeGA += match.score["away"]
    if away != None:
        away.matches += 1
        away.points += pointsFromResult(match.result, "A")
    