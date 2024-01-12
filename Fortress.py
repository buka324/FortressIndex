import csv
#download the league tables (all available



class Fortress:
    def __init__(self, name, points, homepoints, matches, homematches, ga):
        self.name = name
        self.points = points
        self.homepoints = homepoints
        self.matches = matches
        self.homematches = homematches
        self.homeGA = ga
    def homePPG(self):
        return float(self.homepoints)/float(self.homematches)
    def homeGAPG(self):
        return float(self.homeGA)/float(self.homematches)
    def homeRatio(self):
        ppg = float(self.points)/float(self.matches)
        return self.homePPG()/ppg
    def fortressIndex(self): return self.homePPG*self.homeRatio/self.homeGAPG

def makeFortressFromTeam(club, league):
    if league in ["ARG", "BRA"]:
        # Download individual CSV
    else:
        match league:
            case "ENG": 
            case "DEU":
            case "ITA":
            case "SPA":
            case "FRA":
            case "NED":

def addMatch(home, away, score): #home and away are Fortresses. score is an int double (home first)
