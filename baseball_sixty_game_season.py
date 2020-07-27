import pandas as pd
import time
import os
import re
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

os.chdir('baseball')
import pickle
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
            time.sleep(seconds_sleep_short)
            print(standings_info)
            print('Standings_info retrieved from site after refresh.')
        # Split on new line
        standings_info = standings_info.text.split('\n')

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
                for month, day in product([6, 7], range(1, monthrange(year, june)[1] + 1)):
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

                    # Retreive team name and team statistics
                    standings_info = [[standings_info[i - 1], standings_info[i]] for i, v in enumerate(standings_info) if
                                      re.match(r'\w{2}\s{1}\w{2}\s{1}\.\w{3}', v)]

                    for index, team_not_sixty in enumerate(teams_to_extract_further, start=1):
                        print(f'{index} - {team_not_sixty}')
                        for team_info in standings_info:
                            if team_info[0] == team_not_sixty:
                                if sum([int(j) for j in [i for i in team_info[1].split(" ")[:2]]]) == 59:
                                    print(f'{team_not_sixty} played their 59th game as of {month, day, year}')
                                    for d in range(int(day) + 1, monthrange(year, june)[1] + 1):
                                        print(f'd: {d}')
                                    # day = int(day) + 1
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

        print("\n")
        print(f'Current information in sixty_game_record ({len(sixty_game_record[year][0::2])} out of the total '
              f'{team_counter} teams for {year})')
        # for i in sixty_game_record[year]:
        #     print(i)

        if set(team_list) != set(sixty_game_record[year][0::2]):
            print(f'Do not have full set of teams for {year} season.')
            continue
        else:
            print(f'Have full set of teams for {year} season.')
            break
