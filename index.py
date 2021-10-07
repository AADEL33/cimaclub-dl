import enum
from logger import logging
from bs4 import BeautifulSoup
import requests

port = "2096"
cimaclub = f"https://www.cima-club.cc:{port}/"


def get_download_links(url: str):
    """
    :param url: the download link - should be in the form : https://www.cima-club.cc:..../watch/....
    :return: a list of the download links --> watch out, there will be other links in there
    """
    response = requests.get(url)
    content = BeautifulSoup(response.text, "html.parser")
    downloads_links = content.select_one('div[class*="downloads"]')
    if downloads_links is None:
        raise RuntimeError("downloads section not found")
    download_link = ""
    # print(downloads_links.findChildren("a")[0]["href"])
    for i in downloads_links.findChildren("a"):
        if "gvid" in i["href"] or "govid" in i["href"]:
            download_link = i["href"]
            break
    if download_link == "":
        raise RuntimeError("download link not found")  # gvid links not found
    req = requests.get(download_link)
    if not str(req.status_code).startswith("2"):
        logging.error("govid server is unreachable")
        return []
    download_page = BeautifulSoup(req.text, 'html.parser')

    L = []
    for i in download_page.find_all("a"):
        L.append(i["href"])
    return L


class Type(enum.Enum):
    movie = 1
    series = 2


# add a regex validation for season_link
def get_episodes_links(season_link: str):
    if season_link.endswith("/"):
        season_link = season_link[:-1]
    response = requests.get(season_link + "/episodes")
    content = BeautifulSoup(response.text, "html.parser")
    episodes_div = content.select('div[class*="media-block"] > div[class="content-box"]')
    if len(episodes_div) == 0:
        logging.error("could not extract episode links from found season link")
        return []
    episodes_links = [None] * len(episodes_div)
    for i in episodes_div:
        if i.span.em is not None and i.a["href"] is not None:
            episodes_links[int(i.span.em.text) - 1] = i.a["href"]
    while episodes_links[-1] is None:
        episodes_links.pop()
    return episodes_links


def search(title: str, movie_or_series: Type):
    search_result = BeautifulSoup(requests.get(cimaclub + "search", params={"s": title}).text, 'html.parser')
    links = []
    titles = []
    # we will now handle only movies :
    for i in search_result.select('div[class*="media-block"] > div'):
        a = i.find_all('a')[-1]
        if movie_or_series == Type.movie and "series" not in a["href"] and 'season' not in a["href"]:
            links.append(a["href"])
            titles.append(a.text)
        elif movie_or_series == Type.series and ("series" in a["href"] or 'season' in a["href"]):
            links.append(a["href"])
            titles.append(a.text)
    # print(links,titles,sep='\n')
    assert len(links) == len(titles)
    for i in range(len(titles)):
        print(f"({titles[i]} : ({i + 1})")
    chosen = int(input("please choose a title : ")) - 1
    assert 0 <= chosen < len(titles)
    a = links[chosen]
    if movie_or_series == Type.movie:
        a = a.replace("film", "watch")
    elif 'season' in a:
        episodes = get_episodes_links(a)
        for i in episodes:
            if i is not None:
                print(i)
        # add the option to get the whole season
        chosen_episode = int(input(f"please choose an episode : (1-{len(episodes)}) : "))
        assert 0 < chosen_episode < len(episodes)
        a = episodes[chosen_episode-1]
        if a is not None:
            a = a.replace("episode", "watch")
    print(a)
    return a


def main():
    link = search("family guy",Type.series)
    print(get_download_links(link))
    # print(get_episodes_links(
    #     "https://www.cima-club.cc:2096/season/%D9%85%D8%B3%D9%84%D8%B3%D9%84-fbi:-most-wanted-%D9%85%D9%88%D8%B3%D9%85-3"))


if __name__ == "__main__":
    main()
