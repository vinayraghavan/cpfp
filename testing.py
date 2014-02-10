from bs4 import BeautifulSoup
import urllib2
import re



def get_ga_code(html_content):
    soup = BeautifulSoup(html_content)
    scripts = soup.find_all('script')
    ga_code = ''	
    for i in scripts:
        if '"UA-' in str(i) or "'UA-" in str(i):
            ga_code = str(i)
            for j in ga_code.split("'"):
               if "UA-" in j:
                   return j



def get_all_codes(url, main_url):
    if not url.startswith('http'):
        url = "http://"+url
    if url[-1] == '/':
        url = url[:-1]
    try:
        url_content = urllib2.urlopen(url)
    except:
        return ([], [])
    html_content = url_content.read()
    soup = BeautifulSoup(html_content)
    links = soup.find_all('a')
    has_code = []; no_code = []
    for i in links:
        link = str(i.get('href'))
        if main_url in link:
            ga_code = get_ga_code(html_content)
            if ga_code:
                has_code.append([link, ga_code])

            else:
                no_code.append(link)
    return (has_code, no_code)



def spider(url):
    plain_url = re.compile(r'(http[:][/][/])|(www[.])').sub('', url) #removes 'http' and 'www'
    #plain_url = re.compile(re.escape(".  ")+'.*').sub('', plain_url1)   #removes everything after (and including) '.' (e.g. .com)
    level1 = {}; level2 = {};
    
    temp = get_all_codes(url, plain_url)
    level1['has_code'] = temp[0]
    level1['no_code'] = temp[1]
    level2['has_code'] = []; level2['no_code'] = [];
    for url in level1['has_code']:
        codes = get_all_codes(url[0], plain_url)
        level2['has_code'].append(codes[0])
        level2['no_code'].append(codes[1])
    for url in level1['no_code']:
        codes = get_all_codes(url[0], plain_url)
        level2['has_code'].append(codes[0]);
        level2['no_code'].append(codes[1])
    return level1, level2
                

spider('http://imorph.com')
