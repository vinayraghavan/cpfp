from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import urllib2
from bs4 import BeautifulSoup
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
    total_pages = 0
    has_code = []; no_code = []
    for i in links:
        link = str(i.get('href'))
        if main_url in link:
            total_pages = total_pages + 1
            ga_code = get_ga_code(html_content)
            if ga_code:
                has_code.append([link, ga_code])

            else:
                no_code.append(link)
    return (has_code, no_code, total_pages)



def spider(url):
    plain_url = re.compile(r'(http[:][/][/])|(www[.])').sub('', url) #removes 'http' and 'www'
    #plain_url = re.compile(re.escape(".  ")+'.*').sub('', plain_url1)   #removes everything after (and including) '.' (e.g. .com)
    level1 = {}; level2 = {};
    
    temp = get_all_codes(url, plain_url)
    level1['has_code'] = temp[0]
    level1['no_code'] = temp[1]
    total_pages = temp[2]
    #level2['has_code'] = []; level2['no_code'] = [];
    #for url in level1['has_code']:
        #codes = get_all_codes(url[0], plain_url)
        #level2['has_code'].append(codes[0])
        #level2['no_code'].append(codes[1])
    #for url in level1['no_code']:
        #codes = get_all_codes(url[0], plain_url)
        #level2['has_code'].append(codes[0]);
        #level2['no_code'].append(codes[1])
    return (level1, level2, total_pages)                
        
@csrf_exempt
def home(request):
    if request.method == "POST":
        url = str(request.POST.get('url', ''))
        if not url.startswith('http'):
            url = "http://"+url
        if url[-1] == '/':
            url = url[:-1]
        try:
            url_content = urllib2.urlopen(url)
        except:
            return render_to_response('error_occured.html')
        html_content = url_content.read()
        ga_code = get_ga_code(html_content)

        if ga_code:
            all_levels = spider(url)
            level1 = all_levels[0]
            level2 = all_levels[1]
            pages = all_levels[2]
            return render_to_response('uses_google_analytics.html',{'url':url, 'level1':level1, 'level2':level2, 'pages':pages,})
        else:
            return render_to_response('no_google_analytics.html',{'url':url,})
    else:
        return render_to_response('home_page.html')
