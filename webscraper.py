from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import json

players = {
    "Novak Djokovic":{},
    "Andrey Rublev":{},
    "Carlos Alcaraz":{},
    "Daniil Medvedev":{},
    "Jannik Sinner":{}
}

for player in players.keys():
    with open(f"{player}.html") as f:
        html_text = f.read()
    soup = BeautifulSoup(html_text, "html.parser")
    table = soup.find("table", {"id": "mcp-return"})
    rows = table.find_all("tr")
    full_table = []
    for row in rows[1:]:
        column_list = row.find_all("td")
        new_column_list = []
        for column in column_list:
            new_column_list.append(column.text.strip())
        full_table.append(new_column_list)
    returns = pd.DataFrame(full_table, columns = ["Match", "Result", "RiP%", "RiP W%", "RetWnr%", "FH/BH", "RDI", "Slice%", "1st:RiP%", "1st:RiP W%", "1st:RetWnr%", "1st:RDI", "1st:Slice%", "2nd:RiP%", "2nd:RiP W%", "2nd:RetWnr%", "2nd:RDI", "2nd:Slice%"])
    returns.drop(columns = ["Match", "Result", "RiP%", "RiP W%", "RetWnr%", "FH/BH", "RDI", "Slice%"], inplace = True)
    returns.replace({'%': '', '-':np.nan}, regex=True, inplace = True)
    returns.dropna(axis = 0, inplace = True)
    returns = returns.astype(float, copy = True)
    final_returns = returns.mean(axis=0)

    table = soup.find("table", {"id": "recent-results"})
    rows = table.find_all("tr")
    full_table = []
    for row in rows[1:]:
        column_list = row.find_all("td")
        new_column_list = []
        for column in column_list:
            new_column_list.append(column.text.strip())
        full_table.append(new_column_list)
    recent_results = pd.DataFrame(full_table, columns = ["Date", "Tournament", "Surface", "Rd" "Rk", "vRk","throw_away_1", "throw_away_2", "Score", "DR", "A%", "DF%", "1stIn", "1st%", "2nd%", "BPSvd", "Time"])
    recent_results.drop(columns = ["Date", "Tournament", "Surface", "Rd" "Rk", "vRk","throw_away_1", "throw_away_2", "Score", "DR", "A%", "BPSvd", "Time"], inplace = True)
    recent_results.replace({'%': '', '-':np.nan}, regex=True, inplace = True)
    recent_results.replace('', np.nan, inplace=True)
    recent_results.dropna(axis = 0, inplace = True)
    recent_results = recent_results.astype(float, copy = True)
    final_results = recent_results.mean(axis=0)

    combined_df = pd.concat([final_returns, final_results], axis=0)
    change_to_decimal = lambda x: x / 100
    combined_df = combined_df.apply(change_to_decimal)

    players[player] = {
        "sw1": combined_df.get("1st%"),
        "sp1": combined_df.get("1stIn"),
        "sw2": combined_df.get("2nd%"),
        "sp2": 1-combined_df.get("DF%")/(1-combined_df.get("1stIn")),
        "rw1": combined_df.get("1st:RiP W%"),
        "rp1": combined_df.get("1st:RiP%"),
        "rw2": combined_df.get("2nd:RiP W%"),
        "rp2": combined_df.get("2nd:RiP%")
    }

with open("players.json", "w") as outfile:
    json.dump(players, outfile)