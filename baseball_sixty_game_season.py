import pandas as pd
import time
import os
import re
import pickle
import yaml
from calendar import monthrange
from selenium import webdriver
from more_itertools import unique_everseen
from itertools import product
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

season_ending_list = []
for year in range(1994, 2020):
    # Define Chrome webdriver for site
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
    al_divison_moniker = standings_info[0]
    al_wild_card_moniker = list(set([x for x in standings_info if 'al wild card' in x.lower()]))[0]
    nl_divison_moniker = al_divison_moniker.replace('AL', 'NL')
    nl_wild_card_moniker = al_wild_card_moniker.replace('AL', 'NL')

    # AL Divison Winners
    # print(standings_info[[i for i, x in enumerate(standings_info) if x == '>.500'][0]+1: [i for i, x in
    #     enumerate(standings_info) if x == al_divison_moniker][1]])
    season_ending_list.append(standings_info[[i for i, x in enumerate(standings_info) if x == '>.500'][0]+1: [i for i, x in
        enumerate(standings_info) if x == al_divison_moniker][1]])

    # AL Wild Card Winner(s)
    # print(standings_info[[x for x in [i for i, x in enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
    #     enumerate(standings_info) if x == al_wild_card_moniker][0]][0]+1: [x for x in [i for i, x in
    #     enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
    #     enumerate(standings_info) if x == al_wild_card_moniker][0]][0]+4])
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

    # NL Divison Winners
    # print(standings_info[[x for x in [i for i, x in enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
    #     enumerate(standings_info) if x == nl_divison_moniker][0]][0]+1:[i for i, x in enumerate(standings_info) if
    #     x == nl_divison_moniker][1]])
    season_ending_list.append(standings_info[[x for x in [i for i, x in enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
        enumerate(standings_info) if x == nl_divison_moniker][0]][0]+1:[i for i, x in enumerate(standings_info) if
        x == nl_divison_moniker][1]])

    # NL Wild Card Winner(s)
    # print(standings_info[[x for x in [i for i, x in enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
    #     enumerate(standings_info) if x == nl_wild_card_moniker][0]][0]+1: [x for x in [i for i, x in
    #     enumerate(standings_info) if x == '>.500'] if x > [i for i, x in
    #     enumerate(standings_info) if x == nl_wild_card_moniker][0]][0]+4])
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

# # Save season ending standings
# with open("season_ending_list.txt", "wb") as season_ending_list_txt:
#     pickle.dump(season_ending_list, season_ending_list_txt)

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
divisons_by_year_teams = {}
# Define dictionary that will capture full team name for each year
teams_city_name = {}
# Define dictionary to retrieve each team's record at 60 games
sixty_game_record = {}
seconds_sleep_short, seconds_sleep_long = 5, 20

for year in range(1994, 2020):
    print('f')
    for month, day in product([6, 7], range(1, monthrange(year, june)[1] + 1)):
        print('e')
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
        if year not in divisons_by_year_teams.keys():
            print(f'{year} not in divisons_by_year_teams.')
            team_index_locator = []
            for value in unique_everseen([i for i in standings_info if "AL " in i or "NL " in i or "W Wins" in i]):
                team_index_locator.extend([i for i, x in enumerate(standings_info) if x == value])
            team_index_locator = team_index_locator[1:]
            divisons_by_teams = []
            for i, j in zip(team_index_locator[0::2], team_index_locator[1::2]):
                divisons_by_teams.append(standings_info[i:j])

            divisons_by_year_teams[year] = divisons_by_teams
            print(f'{year} is now in divisons_by_year_teams.')

            team_counter = 0
            team_list = []
            for i in range(len(divisons_by_year_teams[year])):
                team_counter += len(divisons_by_year_teams[year][i][1:])
                team_list.extend(divisons_by_year_teams[year][i][1:])

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
                    print('d')
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

# # Save divisons by years with teams
# with open("divisons_by_year_teams.txt", "wb") as divisons_by_year_teams_txt:
#     pickle.dump(divisons_by_year_teams, divisons_by_year_teams_txt)
#
# # Save teams with their full city and names
# with open("teams_city_name.txt", "wb") as teams_city_name_txt:
#     pickle.dump(teams_city_name, teams_city_name_txt)
#
# # Save 60 game records
# with open("sixty_game_record.txt", "wb") as sixty_game_record_txt:
#     pickle.dump(sixty_game_record, sixty_game_record_txt)







# Load in 60 game records
with open("sixty_game_record.txt", "rb") as handle:
    sixty_game_record = pickle.load(handle)

# Load in season ending information
with open("season_ending_list.txt", "rb") as handle:
    season_ending_list = pickle.load(handle)

# Load in divisons_by_year_teams
with open("divisons_by_year_teams.txt", "rb") as handle:
    divisons_by_year_teams = pickle.load(handle)

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

# Add divison each team played in for that year
for year in sixty_game_record.keys():
    print(year)
    for index, team in enumerate(sixty_game_record[year]):
        print('\n')
        print(team)
        for divisons in divisons_by_year_teams[year]:
            print(divisons)
            for divison in divisons:
                if team[0] in divison:
                    print(index, team[0], divisons[0])
                    sixty_game_record[year][index] = sixty_game_record[year][index] + [divisons[0]]
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
                    print('Divison Winner')
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

# Fill None values
# all_info.fillna("-")

# Create Sorted Dataframe
all_info = all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                                          ascending=[True, False, True])



# Standings at 60 game mark
for year in all_info.index.levels[0]:
    print('*'*60)
    print(f'Year: {year}')
    print(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                                         ascending=[True, False, True]))
    print('\n' * 1)
    print(f'AL {year} standings at 60 games')
    # Only 1 wildcard team up until 2011
    if year <= 2011:
        # AL Divisions for particular year
        al_divisions_at_sixty = [x for x in all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                    ascending=[True, False, True]).groupby('division').head(1)['division'] if x[0:2] == "AL"]
        # AL Division leaders at 60 game mark
        al_sixty_best = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).loc[all_info.loc[year].
                             sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).division.isin(al_divisions_at_sixty), 'full_team'])
        # AL Wild Card winning percentage at 60 games
        al_wild_card_at_sixty_winning_percentage = list(all_info.loc[(year,)].query("(division in @al_divisions_at_sixty) &"
                                    " (full_team not in @al_sixty_best)").sort_values(by='sixty_game_win_percentage',
                                    ascending=False).head(1)['sixty_game_win_percentage'])
        # Print AL standings at 60 game mark
        print(all_info.loc[(year,)].query("full_team in @al_sixty_best").sort_values(by='division').
              append(all_info.loc[(year,)].query("(division in @al_divisions_at_sixty) & (full_team not in @al_sixty_best) &"
                                                 " (sixty_game_win_percentage in @al_wild_card_at_sixty_winning_percentage)")))

        print('\n' * 1)
        print(f'NL {year} standings at 60 games')
        # NL Divisions for particular year
        nl_divisions_at_sixty = [x for x in all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                    ascending=[True, False, True]).groupby('division').head(1)['division'] if x[0:2] == "NL"]
        # NL Division leaders at 60 game mark
        nl_sixty_best = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).loc[all_info.loc[year].
                             sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).division.isin(nl_divisions_at_sixty), 'full_team'])
        # NL Wild Card winning percentage at 60 games
        nl_wild_card_at_sixty_winning_percentage = list(all_info.loc[(year,)].query("(division in @nl_divisions_at_sixty) &"
                                     " (full_team not in @nl_sixty_best)").sort_values(by='sixty_game_win_percentage',
                                     ascending=False).head(1)['sixty_game_win_percentage'])
        # Print NL standings at 60 game mark
        print(all_info.loc[(year,)].query("full_team in @nl_sixty_best").sort_values(by='division').
              append(all_info.loc[(year,)].query("(division in @nl_divisions_at_sixty) & (full_team not in @nl_sixty_best) &"
                                                 " (sixty_game_win_percentage in @nl_wild_card_at_sixty_winning_percentage)")))
        print('\n' * 2)
    # 2 wildcard teams after 2011
    else:
        # AL Divisions for particular year
        al_divisions_at_sixty = [x for x in all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                    ascending=[True, False, True]).groupby('division').head(1)['division'] if x[0:2] == "AL"]
        # AL Division leaders at 60 game mark
        al_sixty_best = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).loc[all_info.loc[year].
                             sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).division.isin(al_divisions_at_sixty), 'full_team'])
        # AL Wild Card winning percentage at 60 games
        al_wild_card_at_sixty_winning_percentage = list(all_info.loc[(year,)].query("(division in @al_divisions_at_sixty) &"
                                    " (full_team not in @al_sixty_best)").sort_values(by='sixty_game_win_percentage',
                                    ascending=False).head(2)['sixty_game_win_percentage'])
        # Print AL standings at 60 game mark
        print(all_info.loc[(year,)].query("full_team in @al_sixty_best").sort_values(by='division').
              append(all_info.loc[(year,)].query("(division in @al_divisions_at_sixty) & (full_team not in @al_sixty_best) &"
                                        " (sixty_game_win_percentage in @al_wild_card_at_sixty_winning_percentage)").
                                        sort_values(by='sixty_game_win_percentage', ascending=False)))

        print('\n' * 1)
        print(f'NL {year} standings at 60 games')
        # NL Divisions for particular year
        nl_divisions_at_sixty = [x for x in all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                    ascending=[True, False, True]).groupby('division').head(1)['division'] if x[0:2] == "NL"]
        # NL Division leaders at 60 game mark
        nl_sixty_best = list(all_info.loc[year].sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).loc[all_info.loc[year].
                             sort_values(by=['division', 'sixty_game_win_percentage', 'season_result'],
                ascending=[True, False, True]).groupby('division').head(1).division.isin(nl_divisions_at_sixty), 'full_team'])
        # NL Wild Card winning percentage at 60 games
        nl_wild_card_at_sixty_winning_percentage = list(all_info.loc[(year,)].query("(division in @nl_divisions_at_sixty) &"
                                       " (full_team not in @nl_sixty_best)").sort_values(by='sixty_game_win_percentage',
                                       ascending=False).head(2)['sixty_game_win_percentage'])
        # Print AL standings at 60 game mark
        print(all_info.loc[(year,)].query("full_team in @nl_sixty_best").sort_values(by='division').
              append(all_info.loc[(year,)].query("(division in @nl_divisions_at_sixty) & (full_team not in @nl_sixty_best) &"
                                                 " (sixty_game_win_percentage in @nl_wild_card_at_sixty_winning_percentage)").
                                                 sort_values(by='sixty_game_win_percentage', ascending=False)))
        print('\n' * 2)