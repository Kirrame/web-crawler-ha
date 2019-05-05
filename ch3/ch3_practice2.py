import requests
from bs4 import BeautifulSoup

home_page = 'https://movies.yahoo.com.tw/'
this_week = home_page+'movie_thisweek.html'


def get_request(url):
    req = requests.get(url)
    if req.status_code == 200:
        return req
    else:
        return None

# Check if next page exist or not. If not return None
def get_next_page(url):
    html = get_request(url).text
    soup_nexturl = BeautifulSoup(html, 'html5lib')

    try:
        next_url = soup_nexturl.find('li',{'class':'nexttxt'}).find('a').get('href')
        #print(next_url)

    except:
        next_url = None
        #print("No more next page.")

    return next_url


def soup_init(html):
    soup_init = BeautifulSoup(html, 'html5lib')

    return soup_init


def main():
    this_week_html = get_request(this_week).text

    # Find all next page list
    url_list = [this_week]
    chk_next = 1
    next_url = this_week   # Start from main page
    while chk_next == 1:
        next_url = get_next_page(next_url)

        if next_url is None:
            chk_next = 0
        else:
            url_list.append(next_url)
    print(url_list)

    movie_list_html = []
    #Get the html for all url_list
    for url in url_list:
        soup = soup_init(get_request(url).text)
        movie_list_html = movie_list_html + soup.find('ul', {'class': 'release_list'}).findChildren('li')

    #Get context for each movie
    movie_list = []
    for m in movie_list_html:
        cn = m.find('div', {'class':'release_movie_name'}).a.text.strip()
        en = m.find('div', {'class':'en'}).text.strip()
        link = m.find('div', {'class':'release_movie_name'}).find('a').get('href').strip()

        # Get content
        content_soup = soup_init(get_request(link).text)
        content = content_soup.find('div',{'class':'gray_infobox_inner'}).span.text.strip()

        movie_dict = {'cn': cn, 'en': en, 'link': link, 'content': content}

        movie_list.append(movie_dict)

    return movie_list

if __name__ == '__main__':
    movie_list = main()

    for movie in movie_list:
        print('======='+ movie['cn']+'\\'+movie['en']+'========')
        print(movie['content']+"\n\n")

