import csv
import os
#download the league tables (all available

class Fortress:
    def __init__(self, name):
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

def makeFortressFromTeam(club, league):
    fort = Fortress(club)
    os.chdir("data")
    if league in ["ARG", "BRA"]:
        with open (league + ".csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["League"] != "Copa de la Liga Profesional":
                    if row["HomeTeam"] == club:
                        fort.homepoints += pointsFromResult(row["FTR"], "H")
                        fort.points += pointsFromResult(row["FTR"], "H")
                        fort.homematches += 1
                        fort.matches += 1
                        fort.homeGA += int(row["FTAG"])
                    elif row["AwayTeam"] == club:
                        fort.points += pointsFromResult(row["FTR"], "A")
                        fort.matches += 1
    else:
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
                        if row["HomeTeam"] == club:
                            fort.homepoints += pointsFromResult(row["FTR"], "H")
                            fort.points += pointsFromResult(row["FTR"], "H")
                            fort.homematches += 1
                            fort.matches += 1
                            fort.homeGA += int(row["FTAG"])
                        elif row["AwayTeam"] == club:
                            fort.points += pointsFromResult(row["FTR"], "A")
                            fort.matches += 1
        os.chdir("..")
        os.chdir("..")
    return fort
def addMatch(home, away, match): #home and away are Fortresses. score is an int double (home first). This will be used later to update created fortresses
    