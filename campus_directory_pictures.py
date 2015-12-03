'''
campus_directory_pictures.py

Simple Python script to download the pictures in the campus directory.
'''

import urllib
from bs4 import BeautifulSoup as BS4
import sys
# import requests
import re
import time
import commands
import os.path

re_image = '/stock/ldapimage.php?\?id=(.*?)&source=campus_directory'
re_name = '<h2>(.*?)</h2>'
re_name_profile = '<h2>[<a href="/profiles/[a-z]+[0-9]?/">]?(.*?)[</a>]*</h2>'
re_person = '<li class="person">(.*?)</li>'

cookie_header = '' # enter when needed.

def main():
    scraper("", 0)

def scraper(m, s):
    for number in range(26):
        print number

        time.sleep(0.1)

        letters = m + chr(97 + number)
        html = commands.getoutput('') # enter when needed --> "curl bla bla bla"
        soup = BS4(html)

        if(soup.find(attrs={"id":"discoErrorNotice"})!=None): continue

        desc = soup.find(attrs={"class":"searchDescription"})
        if 'more than 100 matches' in desc.get_text():
            scraper(letters, s)
        elif 'No exact matcehs' in desc.get_text():
            continue
        else:
            string = html.replace('\n', '')
            for person in re.findall(re_person, string):
                image = re.search(re_image, person)

                if image:
                    image = re.search(re_image, person).group(0)
                    username = image[24:-24]
                    print username

                    image_filename = re.sub(' ', '_', username) + '.jpg'

                    if not os.path.exists(image_filename):
                        urllib.urlretrieve('https://apps.carleton.edu' + image, image_filename)

if __name__ == '__main__':
    main()