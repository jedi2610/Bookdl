from bs4 import BeautifulSoup
import requests
from book import books
from selenium import webdriver
import time
import re


def search(book_name,book):
    url = "https://www.pdfdrive.com/search?q={}".format(book_name)
    source = requests.get(url)
    soup = BeautifulSoup(source.content, 'html5lib')
    results = soup.findAll('a', attrs = {'class': 'ai-search'})
    i = 1
    for result in results:
        title = result.find('h2').text
        link = result['href']
        book.add(i,title,link)
        i += 1
    return book.get_results()

def download(title,url):
    url = ("https://www.pdfdrive.com"+url)
    source = requests.get(url)
    soup = BeautifulSoup(source.content,'html5lib')
    results = soup.find('a',attrs = {'id':'download-button-link'})
    link = results['href']
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/usr/lib/chromium/chromedriver", options=chrome_options)
    driver.get("https://www.pdfdrive.com"+link)
    html = driver.page_source
    soup = BeautifulSoup(html,'html5lib')
    button = soup.find('a',attrs = {'onclick':re.compile('AiD(.*)')})
    try:
        link = re.findall('http://(.*)',button['href'])
        pdf = "http://"+link[0]
    except:
        pdf = "https://www.pdfdrive.com"+button['href']
    try:
        book = requests.get(pdf, allow_redirects=True)
        open('/home/kaushalp/Books/{}.pdf'.format(title), 'wb').write(book.content)
    except:
        print("Link not found!")
    

if __name__ == '__main__':
    obj = books()
    book_name = input("Enter book name")
    result = search(book_name,obj)
    i = 1
    while(i < 4):
        obj.show_results(i)
        response = input("Select:")
        if(response != '0'):
            url = obj.get_url(int(response))
            title = obj.get_title(int(response))
            download(title,url)
            break
        else:
            i = i+1