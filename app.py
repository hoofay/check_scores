import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import streamlit as st

df = pd.DataFrame({'Home': ['',''], 'HG': ['',''], 'AG': ['',''], 'Away': ['',''], 'Date_Time': ['','']})

my_links = [f'https://onefootball.com/en/competition/premier-league-9/fixtures',
f'https://onefootball.com/en/competition/efl-championship-27/fixtures',
f'https://onefootball.com/en/competition/efl-league-one-42/fixtures',
f'https://onefootball.com/en/competition/efl-league-two-43/fixtures']

for comp in my_links:
    link = comp
    
    # getting data
    source = requests.get(link).text
    # scraping the data
    page = bs(source, 'lxml')
    
    # searching for the date and time
    dateTime = page.find_all('div', class_='SimpleMatchCard_simpleMatchCard__matchContent__prwTf')
    date_time = []
    
    for i in range(len(dateTime)):
        date_time.append(dateTime[i].text.strip())
    
    #  searching for the teams
    team = page.find_all('span',  class_='SimpleMatchCardTeam_simpleMatchCardTeam__name__7Ud8D')
    teams = []
    for i in range(len(team)):
        teams.append(team[i].text.strip())
    
    # separating the teams
    home = []
    for i in teams[0::2]:
        home.append(i)

    away = []
    for i in teams[1::2]:
        away.append(i)
    
    # searching for the scores data
    score = page.find_all('span', class_='SimpleMatchCardTeam_simpleMatchCardTeam__score__UYMc_')
    scores = []
    for i in range(len(score)):
        scores.append(score[i].text.split())
        
    # separating the scores
    home_scores = []
    away_scores = []

    for i in scores[0::2]:
        if len(i)>0:
            home_scores.append(i[0])
        else:
            home_scores.append('-')

    for i in scores[1::2]:
        if len(i)>0:
            away_scores.append(i[0])
        else:
            away_scores.append('-')
    
    df = pd.concat([df,pd.DataFrame({'Home': home, 'HG': home_scores, 'AG': away_scores, 'Away': away, 'Date_Time':date_time})],ignore_index=True)

live_games = df[df['Date_Time'].str.contains("'") | df['Date_Time'].str.contains("Half time")] # live games

st.header('Check Live Football Scores')
st.info('Check the latest scores of live games in English leagues')

if len(live_games.Home)>0:
    live_teams = pd.concat([live_games.Home,live_games.Away])

    team = st.multiselect('Choose teams to display',live_teams)

    if len(team)>0:
        team_select = live_games[(live_games.Home.isin(team)) | (live_games.Away.isin(team))]
    else:
        team_select = live_games

    st.markdown(team_select.style.hide_index().to_html(), unsafe_allow_html=True)

    st.write('')
    st.button('Refresh')
else:
    st.write('No games to display')

