import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

main_url = 'https://tw.dictionary.search.yahoo.com/search?p='


def get_req(url):
    try:
        req = requests.get(url)
        return req

    except:
        return None



def get_html(req):
    soup = BeautifulSoup(req.text,'html5lib')

    typo_msg= '很抱歉，字典找不到您要的資料喔！'
    suggest_pre = '你是不是要查'

    div_web = soup.find('div', {'id': 'web'})
    ol_list = div_web.find_all('ol')
    ol1_text = ol_list[0].text

    #Result1: Typo and return suggestion
    if typo_msg in ol1_text and suggest_pre in ol1_text :
        #Find the suggest word
        typo_msg_index = ol1_text.find(typo_msg)
        suggest_pre_len = len(suggest_pre)

        sugg = ol1_text[suggest_pre_len:typo_msg_index].strip()

        return None, None, sugg
    #Result2: Typo, no suggestion
    elif typo_msg in ol1_text:
        return None, None, None

    #Result3: Correct word
    else:
        #Title
        title = soup.find('div', {'class':'compTitle mt-25 ml-25 mb-10'}).text

        #Description
        li_list = soup.find('div', {'class':'compList mb-25 ml-25 p-rel'}).find_all('li')
        desc_list =[]
        for e in li_list:
            desc_list.append(e.text)

        return title, desc_list, None



if __name__ == '__main__':

    try_ind = True

    #If it is unable to get result, try again
    while try_ind == True:
        search_string = input('Enter the word ready to search:')
        url_keyword = main_url + urllib.parse.quote_plus(search_string)
        #url_keyword = 'rrrr'
        request = get_req(url_keyword)

        if request == None:
            print('url error, plz check again')
        elif request.status_code == 200:
            print('URL:', url_keyword)

            # Get content
            result = get_html(request)


            if not any(result):                   #Result2
                print('Typo, plz check again')
                continue
            elif result[2] is not None:           #Result1
                print('Typo, suggestion:',result[2])
                continue
            else:                                 #Result3
                print('================Search Result================')
                print('Title:', result[0])
                print('Description:')
                for e in result[1]:
                    print('* ', e)

                try_ind = False

        else:
            print(request.status_code)
            print('URL:', url_keyword)




