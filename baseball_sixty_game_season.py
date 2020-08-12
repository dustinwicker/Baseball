import pandas as pd
import numpy as np
import time
import os
import re
import pickle
import yaml
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import colors
from calendar import monthrange
from selenium import webdriver
from collections import Counter
from more_itertools import unique_everseen
from itertools import product, chain
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Increase maximum width in characters of columns - will put all columns in same line in console readout
pd.set_option('expand_frame_repr', False)
# Be able to read entire value in each column (no longer truncating values)
pd.set_option('display.max_colwidth', None)
# Increase number of rows printed out in console
pd.set_option('display.min_rows', 200)

# Change current working directory to main directory
def main_directory(directory):
    # Load in .yml file to retrieve location of heart disease directory
    info = yaml.load(open("info.yml"), Loader=yaml.FullLoader)
    os.chdir(os.getcwd() + info[directory])
main_directory(directory="baseball_directory")

# Webdriver options
options = Options()
# options.add_argument('--headless')
# Define Chrome webdriver for site
driver = webdriver.Chrome(options=options)
# Define url
url = "https://www.mlb.com/standings/wild-card"

# Retreive season ending standings for playoff teams
season_ending_list = []
for year in range(1994, 2020):
    print(year)
    driver.get(url=url+f'/{year}')
    print(driver.current_url)
    time.sleep(60)
    print('\n')
    if 'wild-card' not in driver.current_url:
        driver.find_elements(By.XPATH, value="//li[contains(@class, 'wildCard')]")[0].click()
        time.sleep(30)
    standings_info = driver.find_element(by='xpath', value="//section[@class='g5-component g5-component--"
                                                           "baseball-standings g5-component--baseball-standings-"
                                                           "initiated g5-component--mlb g5-component--is-en g5-"
                                                           "component--is-visible']")
    standings_info = standings_info.text.split('\n')
    al_division_moniker = standings_info[0]
    al_wild_card_moniker = list(set([x for x in standings_info if 'al wild card' in x.lower()]))[0]
    nl_division_moniker = al_division_moniker.replace('AL', 'NL')
    nl_wild_card_moniker = al_wild_card_moniker.replace('AL', 'NL')

    season_ending_list.append(standings_info[[i for i, x in enumerate(standings_info) if x == '>.500'][0]+1: [i for i, x in
        enumerate(standings_info) if x == al_division_moniker][1]])

    if year <= 2011:
        season_ending_list.append(standings_info[[x for x in [i for i, x in enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
            enumerate(standings_info) if x == al_wild_card_moniker][0]][0]+1: [x for x in [i for i, x in
            enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
            enumerate(standings_info) if x == al_wild_card_moniker][0]][0]+4])
    else:
        season_ending_list.append(standings_info[[x for x in [i for i, x in enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
            enumerate(standings_info) if x == al_wild_card_moniker][0]][0]+1: [x for x in [i for i, x in
            enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
            enumerate(standings_info) if x == al_wild_card_moniker][0]][0]+7])

    season_ending_list.append(standings_info[[x for x in [i for i, x in enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
        enumerate(standings_info) if x == nl_division_moniker][0]][0]+1:[i for i, x in enumerate(standings_info) if
        x == nl_division_moniker][1]])

    if year <= 2011:
        season_ending_list.append(standings_info[[x for x in [i for i, x in enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
            enumerate(standings_info) if x == nl_wild_card_moniker][0]][0]+1: [x for x in [i for i, x in
            enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
            enumerate(standings_info) if x == nl_wild_card_moniker][0]][0]+4])
    else:
        season_ending_list.append(standings_info[[x for x in [i for i, x in enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
            enumerate(standings_info) if x == nl_wild_card_moniker][0]][0]+1: [x for x in [i for i, x in
            enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
            enumerate(standings_info) if x == nl_wild_card_moniker][0]][0]+7])

# Save season ending standings
with open("season_ending_list.txt", "wb") as season_ending_list_txt:
    pickle.dump(season_ending_list, season_ending_list_txt)

# Retrieve standings at 60 game mark
# Webdriver options
options = Options()
# Open tab onto second monitor
options.add_argument("--window-position=2000,0")
# options.add_argument('--headless')
# Define Chrome webdriver for site
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# Define url
url = "https://www.mlb.com/standings"
# Define shorter month of June and July
june = 6
# Define months
month = [6, 7]

# Define dictionary that will capture teams that make up each division for each year
divisions_by_year_teams = {}
# Define dictionary that will capture full team name for each year
teams_city_name = {}
# Define dictionary to retrieve each team's record at 60 games for each year
sixty_game_record = {}
seconds_sleep_short, seconds_sleep_long = 5, 20

for year in range(1994, 2020):
    for month, day in product([6, 7], range(1, monthrange(year, june)[1] + 1)):
        if len(str(day)) == 1:
            day = str(day).zfill(2)
        print('\n'*2)
        print('-' * 60)
        print('Begin')
        print('-' * 60)
        print(f'Year, Month, Day: {year, month, day}')
        # Define Chrome webdriver for site
        driver.get(url + f'/{year}' + '-' f'{month:02}' + '-' + f'{day}')
        print(f'Current URL: {driver.current_url}')
        if 'standings' + f'/{year}' + '-' f'{month:02}' + '-' + f'{day}' not in driver.current_url:
            print('Current URL is not correct.')
            driver.find_elements(By.XPATH, value="//li[contains(@class, 'regularSeason')]")[0].click()
            print(f'Current URL: {driver.current_url}')
            time.sleep(seconds_sleep_long) #30
        # Retrieve standings and team statistics
        try:
            team_statistics_element = wait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                   "//section[@class='g5-component g5-component--"
                                                                   "baseball-standings g5-component--baseball-standings-"
                                                                   "initiated g5-component--mlb g5-component--is-en g5-"
                                                                   "component--is-visible']")))
            standings_info = driver.find_element(By.XPATH, value="//section[@class='g5-component g5-component--"
                                                                   "baseball-standings g5-component--baseball-standings-"
                                                                   "initiated g5-component--mlb g5-component--is-en g5-"
                                                                   "component--is-visible']")
            time.sleep(seconds_sleep_short)
            # Split on new line
            standings_info = standings_info.text.split('\n')

            print(standings_info)
            if standings_info == []:
                print('standings_info got returned, and after text splitting it is an empty list. Will pull it again.')
                time.sleep(seconds_sleep_short)
                standings_info = driver.find_element(By.XPATH, value="//section[@class='g5-component g5-component--"
                                                                 "baseball-standings g5-component--baseball-standings-"
                                                                 "initiated g5-component--mlb g5-component--is-en g5-"
                                                                 "component--is-visible']")
                time.sleep(seconds_sleep_short)
                # Split on new line
                standings_info = standings_info.text.split('\n')
            if standings_info != []:
                print('Standings_info retrieved from site.')
        except (NoSuchElementException, TimeoutException):
            print('Error here.')
            driver.refresh()
            print('Page refreshed.')
            team_statistics_element = wait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                   "//section[@class='g5-component g5-component--"
                                                                   "baseball-standings g5-component--baseball-standings-"
                                                                   "initiated g5-component--mlb g5-component--is-en g5-"
                                                                   "component--is-visible']")))
            standings_info = driver.find_element(By.XPATH, value="//section[@class='g5-component g5-component--"
                                                                   "baseball-standings g5-component--baseball-standings-"
                                                                   "initiated g5-component--mlb g5-component--is-en g5-"
                                                                   "component--is-visible']")
            time.sleep(seconds_sleep_short)
            # Split on new line
            standings_info = standings_info.text.split('\n')
            print(standings_info)
            print('Standings_info retrieved from site after refresh.')

        # Make dictionary of teams that make up each division for each year
        if year not in divisions_by_year_teams.keys():
            print(f'{year} not in divisions_by_year_teams.')
            team_index_locator = []
            for value in unique_everseen([i for i in standings_info if "AL " in i or "NL " in i or "W Wins" in i]):
                team_index_locator.extend([i for i, x in enumerate(standings_info) if x == value])
            team_index_locator = team_index_locator[1:]
            divisions_by_teams = []
            for i, j in zip(team_index_locator[0::2], team_index_locator[1::2]):
                divisions_by_teams.append(standings_info[i:j])

            divisions_by_year_teams[year] = divisions_by_teams
            print(f'{year} is now in divisions_by_year_teams.')

            team_counter = 0
            team_list = []
            for i in range(len(divisions_by_year_teams[year])):
                team_counter += len(divisions_by_year_teams[year][i][1:])
                team_list.extend(divisions_by_year_teams[year][i][1:])

            if team_counter != len([[standings_info[i - 1], standings_info[i]] for i, v in
                                    enumerate(standings_info) if re.match(r'\w{1,2}\s{1}\w{1,2}\s{1}\.\w{3}', v)]):
                print('Not all teams were extracted from standings_info or another error occurred.')
                break

            # Get full team names
            # Open new tab
            driver.execute_script('''window.open("https://www.google.com/","_blank");''')
            # Make new tab current URL
            driver.switch_to.window(driver.window_handles[1])
            driver.get(f"https://www.mlb.com/stats/team/{year}")
            print(f'Current URL: {driver.current_url}')
            try:
                team_info_element = wait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                       "//div[@class='table-wrapper-3-qU3HfQ']")))
                team_info = driver.find_element(By.XPATH, value="//div[@class='table-wrapper-3-qU3HfQ']").text.split('\n')
                time.sleep(seconds_sleep_short)
                print(team_info)
                # print(standings_info.text)
                print('team_info retrieved from site.')
            except (NoSuchElementException, TimeoutException, KeyError):
                print('Error here.')
                driver.refresh()
                print('Page refreshed.')
                team_info_element = wait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                                            "//div[@class='table-wrapper-3-qU3HfQ']")))
                team_info = driver.find_element(By.XPATH, value="//div[@class='table-wrapper-3-qU3HfQ']").text.split('\n')
                time.sleep(seconds_sleep_short)
                print(team_info)
                # print(standings_info.text)
                print('team_info retrieved from site after refresh.')
            # Create key:value for each year as key with full team names as value
            for i in team_info:
                for j in team_list:
                    if j[0:2] == "NY":
                        j = j.replace("NY", "New York")
                    elif j[0:2] == "LA":
                        j = j.replace("LA", "Los Angeles")
                    elif j[0:3] == "Chi":
                        j = j.replace("Chi", "Chicago")
                    if j in i:
                        while True:
                            try:
                                teams_city_name[year].extend([i])
                            except KeyError:
                                teams_city_name[year] = []
                                continue
                            break
            if team_counter != len(teams_city_name[year]):
                print("Not all full team names were extracted from team info or another error occurred.")
                break
            print(f'Number of full team names acquired for {year}: {len(teams_city_name[year])}')
            print(f'Full team names for {year}')
            print(teams_city_name[year])
            # Close current tab
            driver.close()
            # Switch tabs
            driver.switch_to.window(driver.window_handles[0])
            print(f'Current URL: {driver.current_url}')
        # Retrive team name and team statistics
        standings_info = [[standings_info[i-1], standings_info[i]] for i, v in enumerate(standings_info) if
                          re.match(r'\w{2}\s{1}\w{2}\s{1}\.\w{3}', v)]

        # Print maximum number of games played by team (make use as boundary condition)
        print(f'Maximum number of games played: '
              f'{max([sum(k) for k in [[int(j) for j in i] for i in [i[1].split(" ")[:2] for i in standings_info]]])}')
        print(f'Minimum number of games played: '
              f'{min([sum(k) for k in [[int(j) for j in i] for i in [i[1].split(" ")[:2] for i in standings_info]]])}')
        if max([sum(k) for k in [[int(j) for j in i] for i in [i[1].split(" ")[:2] for i in standings_info]]]) < 60:
            continue

        # Account for double header (team played 60th and 61st game on same day, i.e. Boston in 2006)
        try:
            if (set(team_list) != set(sixty_game_record[year][0::2])) &\
                    (min([sum(k) for k in [[int(j) for j in i] for i in [i[1].split(" ")[:2] for i in standings_info]]]) > 60):
                teams_to_extract_further = list(set(team_list).difference(set(sixty_game_record[year][0::2])))
                print(f'{teams_to_extract_further} has not had their 60 game '
                      f'record recorded and more than 60 games have been played for each team.')
                # for month, day in product([6, 7], range(1, monthrange(year, june)[1] + 1)):
                for month, day in zip(pd.date_range(start="5/24/" + str(year), end="7/31/" + str(year)).month,
                                      pd.date_range(start="5/24/" + str(year), end="7/31/" + str(year)).day):
                    if set(team_list) == set(sixty_game_record[year][0::2]):
                        break
                    if len(str(day)) == 1:
                        day = str(day).zfill(2)
                    print('\n'*2)
                    print('-' * 60)
                    print('Begin')
                    print('-' * 60)
                    print(f'Year, Month, Day: {year, month, day}')
                    # Define Chrome webdriver for site
                    driver.get(url + f'/{year}' + '-' f'{month:02}' + '-' + f'{day}')
                    print(f'Current URL: {driver.current_url}')
                    if 'standings' + f'/{year}' + '-' f'{month:02}' + '-' + f'{day}' not in driver.current_url:
                        print('Current URL is not correct.')
                        driver.find_elements(By.XPATH, value="//li[contains(@class, 'regularSeason')]")[0].click()
                        print(f'Current URL: {driver.current_url}')
                        time.sleep(seconds_sleep_long) #30
                    # Retrieve standings and team statistics
                    try:
                        team_statistics_element = wait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                               "//section[@class='g5-component g5-component--"
                                                                               "baseball-standings g5-component--baseball-standings-"
                                                                               "initiated g5-component--mlb g5-component--is-en g5-"
                                                                               "component--is-visible']")))
                        standings_info = driver.find_element(By.XPATH, value="//section[@class='g5-component g5-component--"
                                                                               "baseball-standings g5-component--baseball-standings-"
                                                                               "initiated g5-component--mlb g5-component--is-en g5-"
                                                                               "component--is-visible']")
                        time.sleep(seconds_sleep_short)
                        print(standings_info)
                        # print(standings_info.text)
                        print('Standings_info retrieved from site.')
                    except (NoSuchElementException, TimeoutException):
                        print('Error here.')
                        driver.refresh()
                        print('Page refreshed.')
                        team_statistics_element = wait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                               "//section[@class='g5-component g5-component--"
                                                                               "baseball-standings g5-component--baseball-standings-"
                                                                               "initiated g5-component--mlb g5-component--is-en g5-"
                                                                               "component--is-visible']")))
                        standings_info = driver.find_element(By.XPATH, value="//section[@class='g5-component g5-component--"
                                                                               "baseball-standings g5-component--baseball-standings-"
                                                                               "initiated g5-component--mlb g5-component--is-en g5-"
                                                                               "component--is-visible']")
                        print(standings_info)
                        print('Standings_info retrieved from site after refresh.')
                    # Split on new line
                    standings_info = standings_info.text.split('\n')

                    # Retrieve team name and team statistics
                    standings_info = [[standings_info[i - 1], standings_info[i]] for i, v in enumerate(standings_info) if
                                      re.match(r'\w{2}\s{1}\w{2}\s{1}\.\w{3}', v)]

                    for index, team_not_sixty in enumerate(teams_to_extract_further, start=1):
                        print(f'{index} - {team_not_sixty}')
                        for team_info in standings_info:
                            if team_info[0] == team_not_sixty:
                                if sum([int(j) for j in [i for i in team_info[1].split(" ")[:2]]]) == 59:
                                    print(f'{team_not_sixty} played their 59th game as of {month, day, year}')
                                    for d in range(int(day) + 1, monthrange(year, month)[1] + 1):
                                        print(f'd: {d}')
                                        if len(str(d)) == 1:
                                            d = str(d).zfill(2)
                                        driver.get("https://www.mlb.com/scores" + f'/{year}' + '-' f'{month:02}' + '-' + f'{d}')
                                        print(f'Current URL: {driver.current_url}')
                                        try:
                                            games_element = wait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                                "//div[@id='gridWrapper']")))
                                            games = driver.find_element(By.XPATH, value="//div[@id='gridWrapper']").text.split('\n')
                                            time.sleep(seconds_sleep_short)
                                            # print(team_info)
                                            # print(standings_info.text)
                                            print('games retrieved from site.')
                                        except (NoSuchElementException, TimeoutException):
                                            print('Error here.')
                                            driver.refresh()
                                            print('Page refreshed.')
                                            games_element = wait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                                                "//div[@id='gridWrapper']")))
                                            games = driver.find_element(By.XPATH, value="//div[@id='gridWrapper']").text.split('\n')
                                            time.sleep(seconds_sleep_short)
                                            # print(team_info)
                                            # print(standings_info.text)
                                            print('games retrieved from site after refresh.')
                                        try:
                                            if [i for i in teams_city_name[year] if team_not_sixty in
                                                i][0][len(team_not_sixty):].strip() in games:
                                                for i in [i for i, v in enumerate(games) if v == [i for i in teams_city_name[year]
                                                     if team_not_sixty in i][0][len(team_not_sixty):].strip()]:
                                                    print([i for i in teams_city_name[year] if team_not_sixty in
                                                        i][0][len(team_not_sixty):].strip())
                                                    if sum([int(i.strip()) for i in games[i + 1].split("-")]) == 60:
                                                        sixty_game_record[year].extend([[j for j in teams_city_name[year] if
                                                                games[i] in j][0][:-len(games[i])].strip(), games[i + 1]])
                                                        print(f'{[[j for j in teams_city_name[year] if games[i] in j][0][:-len(games[i])].strip(), games[i                                                  + 1]]} added to sixty_game_record for {year}')
                                                        print(f'Number of teams in sixty_game_record for {year}: '
                                                              f'{len(sixty_game_record[year][0::2])}')
                                                        print(set(team_list) == set(sixty_game_record[year][0::2]))
                                                        break
                                                break
                                        except IndexError:
                                            if [i for i in teams_city_name[year] if team_not_sixty.replace("NY", "New York").
                                                replace("LA", "Los Angeles").replace("Chi", "Chicago") in i][0].replace("New York",
                                                "").replace("Los Angeles", "").replace("Chicago", "").strip() in games:
                                                for i in [i for i, v in enumerate(games) if v == [i for i in teams_city_name[year] if
                                                    team_not_sixty.replace("NY", "New York").replace("LA",
                                                    "Los Angeles").replace("Chi", "Chicago") in i][0].replace("New York",
                                                    "").replace("Los Angeles", "").replace("Chicago", "").strip()]:
                                                    print('h')
                                                    if sum([int(i.strip()) for i in games[i + 1].split("-")]) == 60:
                                                        sixty_game_record[year].extend([[j.replace("New York",
                                                               "NY").replace("Los Angeles", "LA").replace("Chicago", "Chi")
                                                               for j in teams_city_name[year] if games[i] in j][0], games[i + 1]])
                                                        print(f'{[[j.replace("New York","NY").replace("Los Angeles", "LA").replace("Chicago", "Chi") for j in teams_city_name[year] if games[i] in j][0], games[i + 1]]} added to sixty_game_record for {year}')
                                                        print(f'Number of teams in sixty_game_record for {year}: '
                                                              f'{len(sixty_game_record[year][0::2])}')
                                                        print(set(team_list) == set(sixty_game_record[year][0::2]))
                                                        break
                                                break
                                break
        except KeyError:
            pass
        # Retrieve teams that have played 60 games
        sixty_games_indices = [i for i, v in enumerate([sum(k) for k in [[int(j) for j in i] for i in [i[1].split(" ")[:2] for
                                                                                                   i in standings_info]]]) if v == 60]
        print(f'Number of teams retrieved for particular run: {len(sixty_games_indices)}')


        for i in sixty_games_indices:
            print(i, standings_info[i])
            while True:
                try:
                    if standings_info[i][0] not in sixty_game_record[year][0::2]:
                        sixty_game_record[year].extend(standings_info[i])
                except KeyError:
                    sixty_game_record[year] = []
                    continue
                break

        if year not in sixty_game_record.keys():
            print(f'{year} is not a key in sixty_game_record yet. This might be an indication no teams have recorded '
                  f'their 60 game record as of {month, day, year}.')
            continue
        elif (set(team_list) != set(sixty_game_record[year][0::2])) & (year in sixty_game_record.keys()):
            print("\n")
            print(f'Do not have full set of teams for {year} season.')
            print(f'Current information in sixty_game_record ({len(sixty_game_record[year][0::2])} out of the total '
                  f'{team_counter} teams for {year})')
            continue
        else:
            print(f'Have full set of teams for {year} season.')
            break

# Save divisions by years with teams
with open("divisions_by_year_teams.txt", "wb") as divisions_by_year_teams_txt:
    pickle.dump(divisions_by_year_teams, divisions_by_year_teams_txt)

# Save teams with their full city and names
with open("teams_city_name.txt", "wb") as teams_city_name_txt:
    pickle.dump(teams_city_name, teams_city_name_txt)

# Save 60 game records
with open("sixty_game_record.txt", "wb") as sixty_game_record_txt:
    pickle.dump(sixty_game_record, sixty_game_record_txt)


# Retrieve World Series champions for years of analysis
# Webdriver options
options = Options()
# options.add_argument('--headless')
# Define Chrome webdriver for site
driver = webdriver.Chrome(options=options)
# Define url
url = "https://en.wikipedia.org/wiki/List_of_World_Series_champions"
# Go to URL
driver.get(url)
# Retrieve data
try:
    world_series_element = wait(driver, 120).until(EC.presence_of_element_located((By.XPATH,
                                                    "//div[@class='mw-parser-output']"
                                                    "//table[@class='wikitable sortable plainrowheaders "
                                                    "jquery-tablesorter']")))
    world_series_info = driver.find_element(By.XPATH, value="//div[@class='mw-parser-output']//"
                                                       "table[@class='wikitable sortable plainrowheaders "
                                                       "jquery-tablesorter']")
    driver.close()
except (NoSuchElementException, TimeoutException):
    print('Error here.')

# Split on new line
world_series_info = world_series_info.text.split('\n')
# world_series_info.text.split('\n')[0:1] ['Year Winning team Manager Games Losing team Manager Ref.']

# Remove years before 1995
world_series_info = world_series_info[[index for index, value in enumerate(world_series_info) if '1994' in value[0:4]][0]+1:]

# Retrieve year, world series winner, and world series loser
world_series_winner_loser = {}
for i in range(len(world_series_info)):
    world_series_winner_loser[int(world_series_info[i][0:4])] = \
        [world_series_info[i][world_series_info[i].index(" "):[index for index, value in
            enumerate(world_series_info[i]) if value == "("][0]].strip(),
        world_series_info[i][world_series_info[i].index(re.findall(r"\d{1}–\d{1}",
            world_series_info[i])[1])+3:[index for index, value in enumerate(world_series_info[i]) if value == "("][1]].strip()]

# Clean up values
for year in world_series_winner_loser.keys():
    for index, team in enumerate(world_series_winner_loser[year]):
        if '[' in team:
            world_series_winner_loser[year][index] = world_series_winner_loser[year][index].split('[')[0]

# Save world series info
with open("world_series_winner_loser.txt", "wb") as world_series_winner_loser_txt:
    pickle.dump(world_series_winner_loser, world_series_winner_loser_txt)


### Begin data cleanup and exploration
# Load in 60 game records
with open("sixty_game_record.txt", "rb") as handle:
    sixty_game_record = pickle.load(handle)

# Load in season ending information
with open("season_ending_list.txt", "rb") as handle:
    season_ending_list = pickle.load(handle)

# Load in divisions_by_year_teams
with open("divisions_by_year_teams.txt", "rb") as handle:
    divisions_by_year_teams = pickle.load(handle)

# Load in teams_city_name
with open("teams_city_name.txt", "rb") as handle:
    teams_city_name = pickle.load(handle)

# Clean up results returned for each team
for year in sixty_game_record.keys():
    sixty_game_record[year] = [re.match(r'\w{2}\s{1}\w{2}\s{1}\.\w{3}', i).group(0) if re.match(r'\w{2}\s{1}\w{2}\s{1}\.\w{3}', i)
                                                                        is not None else i for i in sixty_game_record[year]]

# Group teams with their team information (the next value in the starting list) and then split wins, losses, and
# winning percentage for each team
for year in sixty_game_record.keys():
    sixty_game_record[year] = [sixty_game_record[year][i:i+2] for i in range(0,len(sixty_game_record[year]), 2)]
    for index, team_info in enumerate(sixty_game_record[year]):
        if re.match(r'\w{2}\s{1}\w{2}\s{1}\.\w{3}', team_info[1]) is not None:
            sixty_game_record[year][index] = sixty_game_record[year][index] + team_info[1].split(" ")
        else:
            sixty_game_record[year][index] = sixty_game_record[year][index] + \
                                             [x.strip() for x in team_info[1].split("-")] + ['NA']

# Check to make sure all teams for each year have the right number of values
# for year in sixty_game_record.keys():
#     for i in sixty_game_record[year]:
#         if len(i) != 5:
#             print(i)

# Add division each team played in for that year
for year in sixty_game_record.keys():
    print(year)
    for index, team in enumerate(sixty_game_record[year]):
        print('\n')
        print(team)
        for divisions in divisions_by_year_teams[year]:
            print(divisions)
            for division in divisions:
                if team[0] in division:
                    print(index, team[0], divisions[0])
                    sixty_game_record[year][index] = sixty_game_record[year][index] + [divisions[0]]
                    break


# Clean up list
season_ending_list = [[value for value in season if value not in ['w', 'y', 'z']] for season in season_ending_list]
season_ending_list = [[re.match(r'\w{2,3}\s{1}\w{2}\s{1}\.\w{3}', i).group(0) if re.match(r'\w{2,3}\s{1}\w{2}\s{1}\.\w{3}', i)
                                is not None else i for i in season] for season in season_ending_list]

# print(int(len(season_ending_list)/len(range(1994,2020))) == 4)
for index, season_end in enumerate(season_ending_list):
    if re.match(r'\w{2,3}\s{1}\w{2}\s{1}\.\w{3}', season_end[-1]) == None:
        season_ending_list[index] = season_ending_list[index][:-1]
season_ending_list = [[value.split('-')[1] if "-" in value else value for value in season] for season in season_ending_list]

# Create dict from list of lists
season_ending_dict = {}
for year, season_result in zip(range(1994, 2020),
                               [season_ending_list[i:i + 4] for i in range(0, len(season_ending_list), 4)]):
    season_ending_dict[year] = season_result

# Add division winner and wild card teams for each year
for year in sixty_game_record.keys():
    print('\n')
    print(year)
    for team_index, team in enumerate(sixty_game_record[year]):
        for result_index, result in enumerate(season_ending_dict[year]):
            if team[0] in result[0::2]:
                print('\n')
                if result_index in [0, 2]:
                    sixty_game_record[year][team_index] = sixty_game_record[year][team_index] + [
                        result[result.index(team[0]):result.index(team[0]) + 2][1], 'Division Winner']
                    print(year, team[0], index, result, result[result.index(team[0]):result.index(team[0]) + 2][1])
                    print('Division Winner')
                    print(team_index)
                elif result_index in [1, 3]:
                    sixty_game_record[year][team_index] = sixty_game_record[year][team_index] + [
                        result[result.index(team[0]):result.index(team[0]) + 2][1], 'Wild Card Winner']
                    print(year, team[0], index, result, result[result.index(team[0]):result.index(team[0]) + 2][1])
                    print('Wild Card Winner')
                    print(team_index)

for year in sixty_game_record.keys():
    for index, team_info in enumerate(sixty_game_record[year]):
        # Length of 8 signifies team is a Division or Wild Card Winner
        if len(sixty_game_record[year][index]) == 8:
            sixty_game_record[year][index] = sixty_game_record[year][index] + sixty_game_record[year][index][-2].split(" ")

# Get maximum list length
max_length_of_list = []
for year in sixty_game_record.keys():
    max_length_of_list.append(len(max(sixty_game_record[year], key=len)))
max_length_of_list = max(max_length_of_list)

# Make each list same length
for year in sixty_game_record.keys():
    for index, team_info in enumerate(sixty_game_record[year]):
        if len(sixty_game_record[year][index]) < max_length_of_list:
            sixty_game_record[year][index] = sixty_game_record[year][index] + [None] * (
                        max_length_of_list - len(sixty_game_record[year][index]))

# Get full team names
for year in sixty_game_record.keys():
    print('\n')
    print(year)
    for index, team in enumerate(sixty_game_record[year]):
        for full_team_name in teams_city_name[year]:
            if team[0].replace("NY", "New York").replace("Chi", "Chicago").replace("LA",
                                                                                   "Los Angeles") in full_team_name:
                print(team[0], full_team_name)
                sixty_game_record[year][index] = sixty_game_record[year][index] + [full_team_name]

# Update season result with world series outcome
for year in sixty_game_record.keys():
    try:
        print('\n')
        print(year)
        for index, team in enumerate(sixty_game_record[year]):
            if team[-1] == world_series_winner_loser[year][0]:
                sixty_game_record[year][index][-5] = 'World Series Winner'
            elif team[-1] == world_series_winner_loser[year][1]:
                sixty_game_record[year][index][-5] = 'World Series Loser'
    except KeyError:
        pass


# Create DataFrame of combined results
all_info = pd.concat({key: pd.DataFrame(value) for key, value in sixty_game_record.items()}, axis=0)

# Rename columns
all_info = all_info.rename(columns={0: 'team', 1: 'sixty_game_stats', 2: 'sixty_game_wins', 3: 'sixty_game_losses',
                         4: 'sixty_game_win_percentage', 5: 'division', 6: 'season_stats', 7: 'season_result',
                         8: 'season_wins', 9: 'season_losses', 10: 'season_winning_percentage', 11: 'full_team'})

# Reorder columns
all_info = all_info[['team', 'full_team', 'division', 'season_result', 'sixty_game_stats', 'season_stats',
                     'sixty_game_wins', 'sixty_game_losses', 'sixty_game_win_percentage', 'season_wins',
                     'season_losses', 'season_winning_percentage']]

# Convert from object to numeric
all_info[['sixty_game_wins', 'sixty_game_losses', 'sixty_game_win_percentage', 'season_wins', 'season_losses',
          'season_winning_percentage']] = all_info[['sixty_game_wins', 'sixty_game_losses', 'sixty_game_win_percentage',
                                                    'season_wins', 'season_losses',
                                                    'season_winning_percentage']].apply(pd.to_numeric, errors='coerce')

# Fill in sixty game winning percentage for teams without one (likely played double header so only their
# 60 game W-L record was pulled)
all_info.loc[all_info.sixty_game_win_percentage.isnull(), 'sixty_game_win_percentage'] = \
    all_info.loc[all_info.sixty_game_win_percentage.isnull(), 'sixty_game_wins'] / \
    (all_info.loc[all_info.sixty_game_win_percentage.isnull(), 'sixty_game_wins'] +
     all_info.loc[all_info.sixty_game_win_percentage.isnull(), 'sixty_game_losses'])

# Drop the 1994 year - strike shortened season
all_info = all_info.drop(1994)

# Sort Dataframe
# all_info = all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
#                                           ascending=[True, False, True])

# List of None value to use in df.query
none_values = [None]

al_teams_in_playoff_contention_sixty_game_wins_win_percentage = {}
al_teams_in_division_lead_sixty_game_wins_win_percentage = {}
al_teams_in_wild_card_contention_sixty_game_wins_win_percentage = {}

al_teams_in_playoffs_sixty_game_wins_win_percentage_season_wins_win_percentage = {}
al_teams_division_winners_sixty_game_wins_win_percentage_season_wins_win_percentage = {}
al_teams_wild_card_winners_sixty_game_wins_win_percentage_season_wins_win_percentage = {}

nl_teams_in_playoff_contention_sixty_game_wins_win_percentage = {}
nl_teams_in_division_lead_sixty_game_wins_win_percentage = {}
nl_teams_in_wild_card_contention_sixty_game_wins_win_percentage = {}

nl_teams_in_playoffs_sixty_game_wins_win_percentage_season_wins_win_percentage = {}
nl_teams_division_winners_sixty_game_wins_win_percentage_season_wins_win_percentage = {}
nl_teams_wild_card_winners_sixty_game_wins_win_percentage_season_wins_win_percentage = {}

al_contention_playoff_in_in_in_out_out_in = {}
nl_contention_playoff_in_in_in_out_out_in = {}

# Check if divisions are same every year or unique each year
divisions_same_each_year = []
for year in all_info.groupby(level=0)['division'].unique().index[1:]:
    divisions_same_each_year.extend([set(all_info.groupby(level=0)['division'].unique()[1995]) == set(
        all_info.groupby(level=0)['division'].unique()[year])])
if set(divisions_same_each_year) == {True}:
    print("Divisions each year are the same in both leagues and lists containing AL and NL divisions have been created.")
    # Create list of AL divisions
    al_divisions = [x for x in all_info.groupby(level=0)['division'].unique()[year] if x[0:2] == "AL"]
    # Create list of NL divisions
    nl_divisions = [x for x in all_info.groupby(level=0)['division'].unique()[year] if x[0:2] == "NL"]
else:
    print("Divisions each year are not the same in both leagues")


# Standings at 60 game mark
for year in all_info.index.get_level_values(0).unique():
    print('*'*100)
    print(f'Year: {year}')
    print(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                                         ascending=[True, False, True]))
    print('\n' * 1)
    print(f'AL {year} standings')
    print('-'*60)

    # Only 1 wildcard team up until 2011
    if year <= 2011:
        # AL Division leaders at 60 game mark
        al_sixty_best = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).loc[all_info.loc[year].
                             sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).division.isin(al_divisions), 'full_team'])
        # AL Wild Card winning percentage at 60 games
        al_wild_card_at_sixty_winning_percentage = list(all_info.loc[(year,)].query("(division in @al_divisions) &"
                                    " (full_team not in @al_sixty_best)").sort_values(by='sixty_game_win_percentage',
                                    ascending=False).head(1)['sixty_game_win_percentage'])
        # Print AL standings at 60 game mark
        print('60 game standings:')
        al_standings_sixty_game_mark = all_info.loc[(year,)].query("full_team in @al_sixty_best").sort_values(by='division').\
            append(all_info.loc[(year,)].query("(division in @al_divisions) & (full_team not in @al_sixty_best) &"
                                                 " (sixty_game_win_percentage in @al_wild_card_at_sixty_winning_percentage)"))
        print(al_standings_sixty_game_mark)
        al_teams_in_playoff_contention_sixty_game_wins_win_percentage[year] = \
            [list(al_standings_sixty_game_mark['sixty_game_wins']),
             list(al_standings_sixty_game_mark['sixty_game_win_percentage'])]

        al_teams_in_division_lead_sixty_game_wins_win_percentage[year] = \
            [list(al_standings_sixty_game_mark['sixty_game_wins'][:len(al_divisions)]),
             list(al_standings_sixty_game_mark['sixty_game_win_percentage'][:len(al_divisions)])]

        al_teams_in_wild_card_contention_sixty_game_wins_win_percentage[year] = \
            [list(al_standings_sixty_game_mark['sixty_game_wins'][len(al_divisions):]),
             list(al_standings_sixty_game_mark['sixty_game_win_percentage'][len(al_divisions):])]

        print('\n' * 1)
        # Print AL final standings
        print('Final standings:')
        al_final_standings = all_info.loc[(year,)].query("(division in @al_divisions) &"
                                " (season_result not in @none_values)").sort_values(by=['season_result',
                                                                            'division'], ascending=[True, True])
        print(al_final_standings)

        al_teams_in_playoffs_sixty_game_wins_win_percentage_season_wins_win_percentage[year] =\
            [list(al_final_standings['sixty_game_wins']), list(al_final_standings['sixty_game_win_percentage']),
             list(al_final_standings['season_wins']), list(al_final_standings['season_winning_percentage'])]

        al_teams_division_winners_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(al_final_standings['sixty_game_wins'][:len(al_divisions)]),
             list(al_final_standings['sixty_game_win_percentage'][:len(al_divisions)]),
             list(al_final_standings['season_wins'][:len(al_divisions)]),
             list(al_final_standings['season_winning_percentage'][:len(al_divisions)])]

        al_teams_wild_card_winners_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(al_final_standings['sixty_game_wins'][len(al_divisions):]),
             list(al_final_standings['sixty_game_win_percentage'][len(al_divisions):]),
             list(al_final_standings['season_wins'][len(al_divisions):]),
             list(al_final_standings['season_winning_percentage'][len(al_divisions):])]

        al_contention_playoff_in_in_in_out_out_in[year] = len(al_standings_sixty_game_mark), len(al_final_standings),\
                                set(al_standings_sixty_game_mark['full_team']) & set(al_final_standings['full_team']), \
                                set(al_standings_sixty_game_mark['full_team']) - set(al_final_standings['full_team']), \
                                set(al_final_standings['full_team']) - set(al_standings_sixty_game_mark['full_team'])

        print('\n' * 1)
        print(f'NL {year} standings')
        print('-'*60)
        # NL Division leaders at 60 game mark
        nl_sixty_best = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).loc[all_info.loc[year].
                             sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).division.isin(nl_divisions), 'full_team'])
        # NL Wild Card winning percentage at 60 games
        nl_wild_card_at_sixty_winning_percentage = list(all_info.loc[(year,)].query("(division in @nl_divisions) &"
                                     " (full_team not in @nl_sixty_best)").sort_values(by='sixty_game_win_percentage',
                                     ascending=False).head(1)['sixty_game_win_percentage'])
        # Print NL standings at 60 game mark
        print('60 game standings:')
        nl_standings_sixty_game_mark = all_info.loc[(year,)].query("full_team in @nl_sixty_best").sort_values(by='division').\
              append(all_info.loc[(year,)].query("(division in @nl_divisions) & (full_team not in @nl_sixty_best) &"
                                                 " (sixty_game_win_percentage in @nl_wild_card_at_sixty_winning_percentage)"))
        print(nl_standings_sixty_game_mark)

        nl_teams_in_playoff_contention_sixty_game_wins_win_percentage[year] = \
            [list(nl_standings_sixty_game_mark['sixty_game_wins']),
             list(nl_standings_sixty_game_mark['sixty_game_win_percentage'])]

        nl_teams_in_division_lead_sixty_game_wins_win_percentage[year] = \
            [list(nl_standings_sixty_game_mark['sixty_game_wins'][:len(nl_divisions)]),
             list(nl_standings_sixty_game_mark['sixty_game_win_percentage'][:len(nl_divisions)])]

        nl_teams_in_wild_card_contention_sixty_game_wins_win_percentage[year] = \
            [list(nl_standings_sixty_game_mark['sixty_game_wins'][len(nl_divisions):]),
             list(nl_standings_sixty_game_mark['sixty_game_win_percentage'][len(nl_divisions):])]

        print('\n' * 1)
        # Print NL final standings
        print('Final standings:')
        nl_final_standings = all_info.loc[(year,)].query("(division in @nl_divisions) & (season_result not in @none_values)").\
            sort_values(by=['season_result', 'division'], ascending=[True, True])
        print(nl_final_standings)

        nl_teams_in_playoffs_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(nl_final_standings['sixty_game_wins']), list(nl_final_standings['sixty_game_win_percentage']),
             list(nl_final_standings['season_wins']), list(nl_final_standings['season_winning_percentage'])]

        nl_teams_division_winners_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(nl_final_standings['sixty_game_wins'][:len(nl_divisions)]),
             list(nl_final_standings['sixty_game_win_percentage'][:len(nl_divisions)]),
             list(nl_final_standings['season_wins'][:len(nl_divisions)]),
             list(nl_final_standings['season_winning_percentage'][:len(nl_divisions)])]

        nl_teams_wild_card_winners_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(nl_final_standings['sixty_game_wins'][len(nl_divisions):]),
             list(nl_final_standings['sixty_game_win_percentage'][len(nl_divisions):]),
             list(nl_final_standings['season_wins'][len(nl_divisions):]),
             list(nl_final_standings['season_winning_percentage'][len(nl_divisions):])]

        nl_contention_playoff_in_in_in_out_out_in[year] = len(nl_standings_sixty_game_mark), len(nl_final_standings),\
                                set(nl_standings_sixty_game_mark['full_team']) & set(nl_final_standings['full_team']), \
                                set(nl_standings_sixty_game_mark['full_team']) - set(nl_final_standings['full_team']), \
                                set(nl_final_standings['full_team']) - set(nl_standings_sixty_game_mark['full_team'])

        print('\n' * 2)
    # 2 wildcard teams after 2011
    else:
        # AL Division leaders at 60 game mark
        al_sixty_best = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).loc[all_info.loc[year].
                             sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).division.isin(al_divisions), 'full_team'])
        # AL Wild Card winning percentage at 60 games
        al_wild_card_at_sixty_winning_percentage = list(all_info.loc[(year,)].query("(division in @al_divisions) &"
                                    " (full_team not in @al_sixty_best)").sort_values(by='sixty_game_win_percentage',
                                    ascending=False).head(2)['sixty_game_win_percentage'])
        # Print AL standings at 60 game mark
        print('60 game standings:')
        al_standings_sixty_game_mark = all_info.loc[(year,)].query("full_team in @al_sixty_best").sort_values(by='division').\
              append(all_info.loc[(year,)].query("(division in @al_divisions) & (full_team not in @al_sixty_best) &"
                                        " (sixty_game_win_percentage in @al_wild_card_at_sixty_winning_percentage)").
                                        sort_values(by='sixty_game_win_percentage', ascending=False))
        print(al_standings_sixty_game_mark)

        al_teams_in_playoff_contention_sixty_game_wins_win_percentage[year] = \
            [list(al_standings_sixty_game_mark['sixty_game_wins']),
             list(al_standings_sixty_game_mark['sixty_game_win_percentage'])]

        al_teams_in_division_lead_sixty_game_wins_win_percentage[year] = \
            [list(al_standings_sixty_game_mark['sixty_game_wins'][:len(al_divisions)]),
             list(al_standings_sixty_game_mark['sixty_game_win_percentage'][:len(al_divisions)])]

        al_teams_in_wild_card_contention_sixty_game_wins_win_percentage[year] = \
            [list(al_standings_sixty_game_mark['sixty_game_wins'][len(al_divisions):]),
             list(al_standings_sixty_game_mark['sixty_game_win_percentage'][len(al_divisions):])]

        print('\n' * 1)
        # Print AL final standings
        print('Final standings:')
        al_final_standings = all_info.loc[(year,)].query("(division in @al_divisions) & (season_result not in @none_values)").\
            sort_values(by=['season_result', 'division'], ascending=[True, True])
        print(al_final_standings)

        al_teams_in_playoffs_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(al_final_standings['sixty_game_wins']), list(al_final_standings['sixty_game_win_percentage']),
             list(al_final_standings['season_wins']), list(al_final_standings['season_winning_percentage'])]

        al_teams_division_winners_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(al_final_standings['sixty_game_wins'][:len(al_divisions)]),
             list(al_final_standings['sixty_game_win_percentage'][:len(al_divisions)]),
             list(al_final_standings['season_wins'][:len(al_divisions)]),
             list(al_final_standings['season_winning_percentage'][:len(al_divisions)])]

        al_teams_wild_card_winners_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(al_final_standings['sixty_game_wins'][len(al_divisions):]),
             list(al_final_standings['sixty_game_win_percentage'][len(al_divisions):]),
             list(al_final_standings['season_wins'][len(al_divisions):]),
             list(al_final_standings['season_winning_percentage'][len(al_divisions):])]

        al_contention_playoff_in_in_in_out_out_in[year] = len(al_standings_sixty_game_mark), len(al_final_standings),\
                                set(al_standings_sixty_game_mark['full_team']) & set(al_final_standings['full_team']), \
                                set(al_standings_sixty_game_mark['full_team']) - set(al_final_standings['full_team']), \
                                set(al_final_standings['full_team']) - set(al_standings_sixty_game_mark['full_team'])


        print('\n' * 1)
        print(f'NL {year} standings')
        print('-'*60)
        # NL Division leaders at 60 game mark
        nl_sixty_best = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).loc[all_info.loc[year].
                             sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).division.isin(nl_divisions), 'full_team'])
        # NL Wild Card winning percentage at 60 games
        nl_wild_card_at_sixty_winning_percentage = list(all_info.loc[(year,)].query("(division in @nl_divisions) &"
                                       " (full_team not in @nl_sixty_best)").sort_values(by='sixty_game_win_percentage',
                                       ascending=False).head(2)['sixty_game_win_percentage'])
        # Print NL standings at 60 game mark
        print('60 game standings:')
        nl_standings_sixty_game_mark = all_info.loc[(year,)].query("full_team in @nl_sixty_best").sort_values(by='division').\
              append(all_info.loc[(year,)].query("(division in @nl_divisions) & (full_team not in @nl_sixty_best) &"
                                                 " (sixty_game_win_percentage in @nl_wild_card_at_sixty_winning_percentage)").
                                                 sort_values(by='sixty_game_win_percentage', ascending=False))
        print(nl_standings_sixty_game_mark)

        nl_teams_in_playoff_contention_sixty_game_wins_win_percentage[year] = \
            [list(nl_standings_sixty_game_mark['sixty_game_wins']),
             list(nl_standings_sixty_game_mark['sixty_game_win_percentage'])]

        nl_teams_in_division_lead_sixty_game_wins_win_percentage[year] = \
            [list(nl_standings_sixty_game_mark['sixty_game_wins'][:len(nl_divisions)]),
             list(nl_standings_sixty_game_mark['sixty_game_win_percentage'][:len(nl_divisions)])]

        nl_teams_in_wild_card_contention_sixty_game_wins_win_percentage[year] = \
            [list(nl_standings_sixty_game_mark['sixty_game_wins'][len(nl_divisions):]),
             list(nl_standings_sixty_game_mark['sixty_game_win_percentage'][len(nl_divisions):])]


        print('\n' * 1)
        # Print NL final standings
        print('Final standings:')
        nl_final_standings = all_info.loc[(year,)].query("(division in @nl_divisions) & (season_result not in @none_values)").\
            sort_values(by=['season_result', 'division'], ascending=[True, True])
        print(nl_final_standings)

        nl_teams_in_playoffs_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(nl_final_standings['sixty_game_wins']), list(nl_final_standings['sixty_game_win_percentage']),
             list(nl_final_standings['season_wins']), list(nl_final_standings['season_winning_percentage'])]

        nl_teams_division_winners_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(nl_final_standings['sixty_game_wins'][:len(nl_divisions)]),
             list(nl_final_standings['sixty_game_win_percentage'][:len(nl_divisions)]),
             list(nl_final_standings['season_wins'][:len(nl_divisions)]),
             list(nl_final_standings['season_winning_percentage'][:len(nl_divisions)])]

        nl_teams_wild_card_winners_sixty_game_wins_win_percentage_season_wins_win_percentage[year] = \
            [list(nl_final_standings['sixty_game_wins'][len(nl_divisions):]),
             list(nl_final_standings['sixty_game_win_percentage'][len(nl_divisions):]),
             list(nl_final_standings['season_wins'][len(nl_divisions):]),
             list(nl_final_standings['season_winning_percentage'][len(nl_divisions):])]

        nl_contention_playoff_in_in_in_out_out_in[year] = len(nl_standings_sixty_game_mark), len(nl_final_standings),\
                                set(nl_standings_sixty_game_mark['full_team']) & set(nl_final_standings['full_team']), \
                                set(nl_standings_sixty_game_mark['full_team']) - set(nl_final_standings['full_team']), \
                                set(nl_final_standings['full_team']) - set(nl_standings_sixty_game_mark['full_team'])
        print('\n' * 2)

al_teams_expanded_playoffs_actual_playoff_teams_actual_division_actual_wild_card = {}
nl_teams_expanded_playoffs_actual_playoff_teams_actual_division_actual_wild_card = {}

# Account for 2020 playoff modification - 1st and 2nd place teams in each division plus two wild card teams from
# each league will make playoffs
for year in all_info.index.get_level_values(0).unique():
    print('*'*100)
    print(f'Year: {year}')
    print(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                                         ascending=[True, False, True]))
    print('\n' * 1)
    print(f'AL {year} standings')
    print('-'*60)
    # AL Division leaders at 60 game mark
    al_sixty_best_corona = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                                ascending=[True, False, True]).groupby('division').head(2).loc[all_info.loc[year].
                                sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                                     ascending=[True, False, True]).groupby('division').head(2).division.isin(
                                 al_divisions), 'full_team'])
    # AL Wild Card winning percentage at 60 games
    al_wild_card_at_sixty_winning_percentage_corona = list(all_info.loc[(year,)].query("(division in @al_divisions) &"
                                " (full_team not in @al_sixty_best_corona)").sort_values(by='sixty_game_win_percentage',
                                ascending=False).head(2)['sixty_game_win_percentage'])
    # Print AL standings at 60 game mark
    print('60 game standings:')
    al_standings_sixty_game_mark_corona = all_info.loc[(year,)].query("full_team in @al_sixty_best_corona").\
        sort_values(by=['division', 'sixty_game_win_percentage'], ascending=[True, False]). \
        append(all_info.loc[(year,)].query("(division in @al_divisions) & (full_team not in @al_sixty_best_corona) &"
                                           " (sixty_game_win_percentage in @al_wild_card_at_sixty_winning_percentage_corona)").
               sort_values(by='sixty_game_win_percentage', ascending=False))
    print(al_standings_sixty_game_mark_corona)

    print('\n' * 1)
    print(f'NL {year} standings')
    print('-'*60)
    # NL Division leaders at 60 game mark
    nl_sixty_best_corona = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
            ascending=[True, False, True]).groupby('division').head(2).loc[all_info.loc[year].
                         sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
            ascending=[True, False, True]).groupby('division').head(2).division.isin(nl_divisions), 'full_team'])
    # NL Wild Card winning percentage at 60 games
    nl_wild_card_at_sixty_winning_percentage_corona = list(all_info.loc[(year,)].query("(division in @nl_divisions) &"
                                   " (full_team not in @nl_sixty_best_corona)").sort_values(by='sixty_game_win_percentage',
                                   ascending=False).head(2)['sixty_game_win_percentage'])
    # Print NL standings at 60 game mark
    print('60 game standings:')
    nl_standings_sixty_game_mark_corona = all_info.loc[(year,)].query("full_team in @nl_sixty_best_corona").\
        sort_values(by=['division', 'sixty_game_win_percentage'], ascending=[True, False]).\
          append(all_info.loc[(year,)].query("(division in @nl_divisions) & (full_team not in @nl_sixty_best_corona) &"
                                             " (sixty_game_win_percentage in @nl_wild_card_at_sixty_winning_percentage_corona)").
                                             sort_values(by='sixty_game_win_percentage', ascending=False))
    print(nl_standings_sixty_game_mark_corona)

    al_teams_expanded_playoffs_actual_playoff_teams_actual_division_actual_wild_card[year] = \
        (len(al_standings_sixty_game_mark_corona.loc[al_standings_sixty_game_mark_corona.season_result.notnull()]),
        len(al_standings_sixty_game_mark_corona.loc[al_standings_sixty_game_mark_corona.season_result == "Division Winner"]),
        len(al_standings_sixty_game_mark_corona.loc[al_standings_sixty_game_mark_corona.season_result == "Wild Card Winner"]))
    nl_teams_expanded_playoffs_actual_playoff_teams_actual_division_actual_wild_card[year] = \
        (len(nl_standings_sixty_game_mark_corona.loc[nl_standings_sixty_game_mark_corona.season_result.notnull()]),
        len(nl_standings_sixty_game_mark_corona.loc[nl_standings_sixty_game_mark_corona.season_result == "Division Winner"]),
        len(nl_standings_sixty_game_mark_corona.loc[nl_standings_sixty_game_mark_corona.season_result == "Wild Card Winner"]))

### Descriptive, statistical analysis, and visualizations ###

# Set colors
lineplot_colors = {"american_league": "#EE0A46", "national_league": "#0E4082"}

# Confirm keys (i.e. playoff years) in AL and NL dict are same
if al_contention_playoff_in_in_in_out_out_in.keys() == nl_contention_playoff_in_in_in_out_out_in.keys():
    playoff_years = nl_contention_playoff_in_in_in_out_out_in.keys()
else:
    print('AL and NL dicts do not have same playoff years. Need to check this out.')

# Traditional season
# Create DataFrame of percentage of teams that were in playoff contention at 60 games and made playoffs at end of year
percentage_in_in_df = pd.DataFrame(data=[list(playoff_years),
                          list(map(lambda playoff_years:  len(al_contention_playoff_in_in_in_out_out_in[playoff_years][2])/
                            al_contention_playoff_in_in_in_out_out_in[playoff_years][1], playoff_years)),
                          list(map(lambda playoff_years: len(nl_contention_playoff_in_in_in_out_out_in[playoff_years][2]) /
                            nl_contention_playoff_in_in_in_out_out_in[playoff_years][1], playoff_years))]).T.set_index([0])
# Use years for index
percentage_in_in_df.index = pd.to_datetime(percentage_in_in_df.index.values.astype('int'), format='%Y').year
# Set column names
percentage_in_in_df = percentage_in_in_df.rename(columns={1:'american_league', 2:'national_league'})
# Create DataFrame from wide to long
percentage_in_in_df_melt = pd.melt(percentage_in_in_df)
# Repeat index twice (AL and NL values have correct years)
percentage_in_in_df_melt.index = list(percentage_in_in_df.index)*2

# Expanded playoff season analysis (i.e. what they are doing for the 2020 playoff season)
# Create DataFrame of percentage of teams, at the 60-game mark, that were playoffs teams at seasons end with expanded format
expanded_percentage_playoff_teams_captured_df = pd.DataFrame(data=[list(playoff_years),
                          list(map(lambda playoff_years:
                                   al_teams_expanded_playoffs_actual_playoff_teams_actual_division_actual_wild_card[playoff_years][0]/
                            al_contention_playoff_in_in_in_out_out_in[playoff_years][1], playoff_years)),
                          list(map(lambda playoff_years:
                                   nl_teams_expanded_playoffs_actual_playoff_teams_actual_division_actual_wild_card[playoff_years][0]/
                            nl_contention_playoff_in_in_in_out_out_in[playoff_years][1], playoff_years))]).T.set_index([0])
# Use years for index
expanded_percentage_playoff_teams_captured_df.index = \
    pd.to_datetime(expanded_percentage_playoff_teams_captured_df.index.values.astype('int'), format='%Y').year
# Set column names
expanded_percentage_playoff_teams_captured_df = expanded_percentage_playoff_teams_captured_df.\
    rename(columns={1:'american_league', 2:'national_league'})
# Create DataFrame from wide to long
expanded_percentage_playoff_teams_captured_df_melt = pd.melt(expanded_percentage_playoff_teams_captured_df)
# Repeat index twice (AL and NL values have correct years)
expanded_percentage_playoff_teams_captured_df_melt.index = list(expanded_percentage_playoff_teams_captured_df.index)*2

## Plot of percentage of teams that were in playoff contention at 60 games and made playoffs at end of year -
# Traditional and Expanded
fig, axes = plt.subplots(nrows=1, ncols=2, sharey=True)
# fig.subplots_adjust(left=0.05, right=.99, top=0.90, bottom=0.04)
# fig.suptitle('Distributions with Kernel Density Estimation (KDE) Overlaid ', fontweight='bold', fontsize=26)
# fig.subplots_adjust(left=0.19, right=0.83, top=0.90, bottom=0.12, hspace=0.7, wspace = 0.25)

# Set common parameters for each plot
line_width = 3
marker_width = 10
years = np.arange(min(percentage_in_in_df_melt.index), max(percentage_in_in_df_melt.index)+1, 1)
rotation_angle = 45
xtick_labels_fontsize = 22
# ytick_labels_fontsize = 22
subplot_title_fontsize = 22

sns.lineplot(ax=axes[0], y=percentage_in_in_df_melt.value, x=percentage_in_in_df_melt.index,
             hue=percentage_in_in_df_melt.variable, palette=lineplot_colors, style=percentage_in_in_df_melt.variable,
             markers=True, dashes=False, linewidth=line_width, markersize=marker_width)
# Set xticks to display each year
axes[0].set_xticks(years)
axes[0].set_xticklabels(labels=axes[0].get_xticks(), rotation=rotation_angle, fontdict ={'fontweight': 'bold',
                                                                                         'fontsize': xtick_labels_fontsize})
axes[0].set_ylabel("")
axes[0].set_title("Traditional Playoff Format", fontdict ={'fontweight': 'bold', 'fontsize': subplot_title_fontsize})

sns.lineplot(ax=axes[1], y=expanded_percentage_playoff_teams_captured_df_melt.value,
             x=expanded_percentage_playoff_teams_captured_df_melt.index,
             hue=expanded_percentage_playoff_teams_captured_df_melt.variable,
             palette=lineplot_colors, style=expanded_percentage_playoff_teams_captured_df_melt.variable,
             markers=True, dashes=False, linewidth=line_width, markersize=marker_width)
axes[1].set_xticks(years)
axes[1].set_xticklabels(labels=axes[0].get_xticks(), rotation=rotation_angle, fontdict ={'fontweight': 'bold',
                                                                                         'fontsize': xtick_labels_fontsize})
axes[1].set_title("Expanded Playoff Format", fontdict ={'fontweight': 'bold', 'fontsize': subplot_title_fontsize})
fig.suptitle('Percentage of Teams in Playoff Position at Sixty-Game Mark and Made Playoffs at End of Year',
             fontweight= 'bold', fontsize= 26)
axes[0].set_yticklabels(labels=axes[0].get_yticks(), fontdict ={'fontweight': 'bold', 'fontsize': 22})
axes[0].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
axes[0].get_legend().remove()
axes[1].get_legend().remove()
handles, legends = axes[1].get_legend_handles_labels()
legends_spelled_out_dict = {'variable': "Legend",'american_league': "American League", 'national_league': "National League"}
fig.legend(handles, legends_spelled_out_dict.values(), loc='upper left', bbox_to_anchor=(0.77, 1.0),
           prop={'weight': 'bold', 'size': 14})
# handles, legends = axes[1].get_legend_handles_labels()
# legends_spelled_out_dict = {'american_league': "American League", 'national_league': "National League"}
# fig.legend(handles[1:], legends_spelled_out_dict.values(), loc='upper left', bbox_to_anchor=(0.77, 1.0),
#            prop={'weight': 'bold', 'size': 14})

# fig.text(0.5, 0.04, 'Year', ha='center')

len(percentage_in_in_df.loc[(percentage_in_in_df.american_league==1.0) & (percentage_in_in_df.national_league==1.0)])
len(percentage_in_in_df.loc[(percentage_in_in_df.american_league==1.0) & (percentage_in_in_df.national_league==1.0)])/len(percentage_in_in_df)
percentage_in_in_df['american_league'].mean()
percentage_in_in_df['national_league'].mean()





# Swarmplot detailing each team's 60 game winning percentage and their season outcomes
# Set colors
swarmplot_colors = {"Did Make Playoffs": "#EE0A46", "World Series Winner": "#EE0A46", "Did Not Make Playoffs": "#0E4082",
                    "vertical_line": "#D3D3D3"}
# Tuple of season result values not to replace
season_results_not_to_replace = ("World Series Winner", "Did Not Make Playoffs")

# American League
al_sixty_game_win_percentage_season_result = all_info.query("(division in @al_divisions)")[["season_result",
                            "sixty_game_win_percentage"]].fillna("Did Not Make Playoffs")

# Replace all season results that are not 'Did Not Make Playoffs' or 'World Series Winner'
for value in [x for x in list(al_sixty_game_win_percentage_season_result['season_result'].unique())
              if x not in season_results_not_to_replace]:
    al_sixty_game_win_percentage_season_result['season_result'] = \
        al_sixty_game_win_percentage_season_result['season_result'].replace(value, "Did Make Playoffs")
fig, axes = plt.subplots(nrows=1, ncols=1)
# fig.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.12, hspace=0.7, wspace = 0.25)
sns.swarmplot(x= al_sixty_game_win_percentage_season_result.index.get_level_values(0),
              y=al_sixty_game_win_percentage_season_result.sixty_game_win_percentage,
              hue=al_sixty_game_win_percentage_season_result.season_result, palette=swarmplot_colors)
# Verticl line between years to separate
for xtick in axes.get_xticks()[:-1]:
    plt.axvline(x=xtick + 0.5, ymin=0.05, ymax=0.95, color=swarmplot_colors['vertical_line'])
# Place stars on World Series winners
for year_index, year in enumerate(al_sixty_game_win_percentage_season_result.index.get_level_values(0).unique()):
    if 'World Series Winner' in al_sixty_game_win_percentage_season_result.loc[year]['season_result'].values:
        for point_index, point in enumerate(axes.get_children()[year_index].get_offsets()):
            if round(point[1],3) == round(al_sixty_game_win_percentage_season_result.loc[year].\
                  query("season_result == 'World Series Winner'")['sixty_game_win_percentage'].values[0],3):
                if colors.to_hex(axes.get_children()[year_index].get_facecolors()[point_index]).upper() == swarmplot_colors['World Series Winner']:
                    axes.plot(point[0], al_sixty_game_win_percentage_season_result.loc[year].
                              query("season_result == 'World Series Winner'")['sixty_game_win_percentage'].values[0],
                              marker='*', markersize=12, color=swarmplot_colors["World Series Winner"])
                    break


# National League
nl_sixty_game_win_percentage_season_result = all_info.query("(division in @nl_divisions)")[["season_result",
                            "sixty_game_win_percentage"]].fillna("Did Not Make Playoffs")
# Replace all season results that are not 'Did Not Make Playoffs' or 'World Series Winner'
for value in [x for x in list(nl_sixty_game_win_percentage_season_result['season_result'].unique())
              if x not in season_results_not_to_replace]:
    nl_sixty_game_win_percentage_season_result['season_result'] = \
        nl_sixty_game_win_percentage_season_result['season_result'].replace(value, "Did Make Playoffs")

fig, axes = plt.subplots(nrows=1, ncols=1)
fig.subplots_adjust(left=0.05, right=0.95, top=0.90, bottom=0.12, hspace=0.7, wspace = 0.25)
nl_swarm_plot = sns.swarmplot(x= nl_sixty_game_win_percentage_season_result.index.get_level_values(0),
              y=nl_sixty_game_win_percentage_season_result.sixty_game_win_percentage,
              hue=nl_sixty_game_win_percentage_season_result.season_result, palette=swarmplot_colors)
# Verticl line between years to separate
for xtick in nl_swarm_plot.get_xticks()[:-1]:
    plt.axvline(x=xtick + 0.5, ymin=0.05, ymax=0.95, color=swarmplot_colors['vertical_line'])
# Place stars on World Series winners
for year_index, year in enumerate(nl_sixty_game_win_percentage_season_result.index.get_level_values(0).unique()):
    if 'World Series Winner' in nl_sixty_game_win_percentage_season_result.loc[year]['season_result'].values:
        for point_index, point in enumerate(axes.get_children()[year_index].get_offsets()):
            if round(point[1],3) == round(nl_sixty_game_win_percentage_season_result.loc[year].\
                  query("season_result == 'World Series Winner'")['sixty_game_win_percentage'].values[0],3):
                if colors.to_hex(axes.get_children()[year_index].get_facecolors()[point_index]).upper() == swarmplot_colors['World Series Winner']:
                    world_series_marker = plt.plot(point[0], nl_sixty_game_win_percentage_season_result.loc[year].
                              query("season_result == 'World Series Winner'")['sixty_game_win_percentage'].values[0],
                              marker='*', markersize=12, color=swarmplot_colors["World Series Winner"], drawstyle=None)
                    break
world_series_marker[0].set_linestyle('None')
handles, legends = axes.get_legend_handles_labels()
handles[-1] = world_series_marker[0]
fig.legend(handles, legends, loc='upper left', bbox_to_anchor=(0.77, 1.0),
           prop={'weight': 'bold', 'size': 14})




# T-test on two related samples - paired t-test for dependent groups
# Question: Do teams "in the playoffs" at 60 games, on average, have a higher winning percentage at that point in the
# season than the season ending winning percentage of teams that make the playoffs?
# Null hypothesis: Equal average winning percentages

# Sixty game winning percentage of all MLB "60 game playoff teams"
mlb_teams_in_playoff_contention_sixty_game_win_percentage = []
for year in al_teams_in_playoff_contention_sixty_game_wins_win_percentage.keys():
    print(year)
    if year <= 2011:
        mlb_teams_in_playoff_contention_sixty_game_win_percentage.extend(
            al_teams_in_playoff_contention_sixty_game_wins_win_percentage[year][1][:4])
    else:
        mlb_teams_in_playoff_contention_sixty_game_win_percentage.extend(
            al_teams_in_playoff_contention_sixty_game_wins_win_percentage[year][1][:5])
for year in nl_teams_in_playoff_contention_sixty_game_wins_win_percentage.keys():
    print(year)
    if year <= 2011:
        mlb_teams_in_playoff_contention_sixty_game_win_percentage.extend(
            nl_teams_in_playoff_contention_sixty_game_wins_win_percentage[year][1][:4])
    else:
        mlb_teams_in_playoff_contention_sixty_game_win_percentage.extend(
            nl_teams_in_playoff_contention_sixty_game_wins_win_percentage[year][1][:5])

# Final winning percentage of all MLB playoff teams
mlb_teams_in_playoffs_sixty_game_win_percentage = list(chain(*[values[-1] for keys, values in
        al_teams_in_playoffs_sixty_game_wins_win_percentage_season_wins_win_percentage.items()])) + \
        list(chain(*[values[-1] for keys, values in nl_teams_in_playoffs_sixty_game_wins_win_percentage_season_wins_win_percentage.items()]))

print(len(mlb_teams_in_playoff_contention_sixty_game_win_percentage) == len(mlb_teams_in_playoffs_sixty_game_win_percentage))


# Determine 'strong' alpha value based on sample size (AA 501, 3 - More Complex ANOVA Regression)
sample_size_one, strong_alpha_value_one = 100, 0.001
sample_size_two, strong_alpha_value_two = 1000, 0.0003
slope = (strong_alpha_value_two - strong_alpha_value_one)/(sample_size_two - sample_size_one)
strong_alpha_value = slope * (len(mlb_teams_in_playoff_contention_sixty_game_win_percentage) - sample_size_one) + strong_alpha_value_one
print(f"The alpha value for use in hypothesis tests is {strong_alpha_value}.")

# Differences between two groups
win_percentage_differences = [i - j for i, j in zip(mlb_teams_in_playoff_contention_sixty_game_win_percentage,
                                                    mlb_teams_in_playoffs_sixty_game_win_percentage)]

# Check for normality
# Histogram with KDE overlaid
sns.distplot(a = win_percentage_differences)
plt.figure()
# Boxplot
sns.boxplot(x = win_percentage_differences)
# Skewness and kurtosis
stats.describe(win_percentage_differences)

# Test for normality
stats.normaltest(a = win_percentage_differences)[1] < strong_alpha_value
stats.shapiro(x = win_percentage_differences)[1] < strong_alpha_value
stats.anderson(x = win_percentage_differences, dist='norm')

stats.ttest_rel(a=mlb_teams_in_playoff_contention_sixty_game_win_percentage,
          b=mlb_teams_in_playoffs_sixty_game_win_percentage)















box = plt.boxplot(x = mlb_teams_in_playoff_contention_sixty_game_win_percentage)

for outlier in box['fliers'][0].get_ydata():
    if outlier in mlb_teams_in_playoff_contention_sixty_game_win_percentage:
        mlb_teams_in_playoff_contention_sixty_game_win_percentage.remove(outlier)

sample_size_one, strong_alpha_value_one = 100, 0.001
sample_size_two, strong_alpha_value_two = 1000, 0.0003
slope = (strong_alpha_value_two - strong_alpha_value_one)/(sample_size_two - sample_size_one)
strong_alpha_value = slope * (len(mlb_teams_in_playoff_contention_sixty_game_win_percentage) - sample_size_one) + strong_alpha_value_one
print(f"The alpha value for use in hypothesis tests is {strong_alpha_value}.")

sns.distplot(a = mlb_teams_in_playoff_contention_sixty_game_win_percentage)
plt.figure()
sns.boxplot(x = mlb_teams_in_playoff_contention_sixty_game_win_percentage)








plt.figure()
sns.distplot(a = mlb_teams_in_playoffs_sixty_game_win_percentage)
plt.figure()
sns.boxplot(x = mlb_teams_in_playoffs_sixty_game_win_percentage)

# Determine 'strong' alpha value based on sample size (AA 501, 3 - More Complex ANOVA Regression)
sample_size_one, strong_alpha_value_one = 100, 0.001
sample_size_two, strong_alpha_value_two = 1000, 0.0003
slope = (strong_alpha_value_two - strong_alpha_value_one)/(sample_size_two - sample_size_one)
strong_alpha_value = slope * (len(mlb_teams_in_playoffs_sixty_game_win_percentage) - sample_size_one) + strong_alpha_value_one
print(f"The alpha value for use in hypothesis tests is {strong_alpha_value}.")

normaltest(a = mlb_teams_in_playoffs_sixty_game_win_percentage)[1] < strong_alpha_value
shapiro(x = mlb_teams_in_playoffs_sixty_game_win_percentage)

box = plt.boxplot(x = mlb_teams_in_playoffs_sixty_game_win_percentage)

for outlier in box['fliers'][0].get_ydata():
    if outlier in mlb_teams_in_playoffs_sixty_game_win_percentage:
        mlb_teams_in_playoffs_sixty_game_win_percentage.remove(outlier)

plt.figure()
sns.distplot(a = mlb_teams_in_playoffs_sixty_game_win_percentage)
plt.figure()
sns.boxplot(x = mlb_teams_in_playoffs_sixty_game_win_percentage)

# Determine 'strong' alpha value based on sample size (AA 501, 3 - More Complex ANOVA Regression)
sample_size_one, strong_alpha_value_one = 100, 0.001
sample_size_two, strong_alpha_value_two = 1000, 0.0003
slope = (strong_alpha_value_two - strong_alpha_value_one)/(sample_size_two - sample_size_one)
strong_alpha_value = slope * (len(mlb_teams_in_playoffs_sixty_game_win_percentage) - sample_size_one) + strong_alpha_value_one
print(f"The alpha value for use in hypothesis tests is {strong_alpha_value}.")

normaltest(a = mlb_teams_in_playoffs_sixty_game_win_percentage)[1] < strong_alpha_value



sns.distplot(a = list(chain(*[values[1] for keys, values in
                                        al_teams_in_playoff_contention_sixty_game_wins_win_percentage.items()])))

sns.distplot(a = list(chain(*[values[0] for keys, values in
                                        al_teams_in_division_lead_sixty_game_wins_win_percentage.items()])))

sns.distplot(a = list(chain(*[values[0] for keys, values in
                                        al_teams_in_wild_card_contention_sixty_game_wins_win_percentage.items()])))

sns.scatterplot(x = list(chain(*[values[0] for keys, values in
                                        al_teams_in_division_lead_sixty_game_wins_win_percentage.items()])),
                y = list(chain(*[values[0] for keys, values in
                                        nl_teams_in_division_lead_sixty_game_wins_win_percentage.items()])))

sns.distplot(a = list(chain(*[values[0] for keys, values in
                                        nl_teams_in_playoff_contention_sixty_game_wins_win_percentage.items()])))

al_in_in_teams = []
for year in al_contention_playoff_in_in_in_out_out_in.keys():
    for team in al_contention_playoff_in_in_in_out_out_in[year][2]:
        al_in_in_teams.extend([team])
print(Counter(al_in_in_teams).most_common())

nl_in_in_teams = []
for year in nl_contention_playoff_in_in_in_out_out_in.keys():
    for team in nl_contention_playoff_in_in_in_out_out_in[year][2]:
        nl_in_in_teams.extend([team])
print(Counter(nl_in_in_teams).most_common())