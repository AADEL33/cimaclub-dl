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
        if "gvid" in i["href"]:
            download_link = i["href"]
            break
    if download_link == "":
        raise RuntimeError("download link not found") # gvid links not found

    download_page = BeautifulSoup(requests.get(download_link).text, 'html.parser')
    L = []
    for i in download_page.find_all("a"):
        L.append(i["href"])
    return L


def search(title: str):
    # we will now handle only movies :
    search_result = BeautifulSoup(requests.get(cimaclub + "search", params={"s": title}).text, 'html.parser')
    links = []
    titles = []
    # print(search_result.select('div[class*="media-block"] > div'))
    for i in search_result.select('div[class*="media-block"] > div'):
        a = i.find_all('a')[-1]
        if "series" not in a["href"] and 'season' not in a["href"]:
            links.append(a["href"])
            titles.append(a.text)
    # print(links,titles,sep='\n')
    assert len(links) == len(titles)
    for i in range(len(titles)):
        print(f"({titles[i]} : ({i + 1})")
    chosen = int(input("please choose a title : ")) - 1
    assert 0 <= chosen < len(titles)
    a = links[chosen]
    a = a.replace("film", "watch")
    print(a)
    return a


def main():
    link = search("happy")
    print(get_download_links(link))

if __name__ == "__main__":
    main()
