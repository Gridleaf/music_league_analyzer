from bs4 import BeautifulSoup

html_file = 'musicleague-S02.html'
html_path = f'D:\Desktop\projects\musicLeagueAnalysis\data\{html_file}'


def season_id_scraper():

    with open(html_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    all_links = soup.find_all('a', href=True)
    spotify_links = [link['href'] for link in all_links if "open.spotify.com" in link['href']]
    playlist_id_list = []
    for link in spotify_links:
        playlist_id_list.append(link.replace("https://open.spotify.com/playlist/", ""))
    return playlist_id_list


