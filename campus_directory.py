import requests
from bs4 import BeautifulSoup as BS4
import csv
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def scraper(m, s):
    for number in range(26):

        letters = m + chr(97 + number)
        # HOW TO LOG IN? NEED TO DO THAT TO GET ALL INFORMATION FROM SITE.
        search_result = requests.get(campus_directory % letters)
        soup = BS4(search_result.content)

        if(soup.find(attrs={"id":"discoErrorNotice"})!=None): continue

        desc = soup.find(attrs={"class":"searchDescription"})
        if 'more than 100 matches' in desc.get_text():
            scraper(letters, s)
        elif 'No exact matches' in desc.get_text():
            continue
        else:
            for person in soup.find_all(attrs={"class":"person"}):
                print count
                count = count + 1

                name = ""
                year = ""
                major = ""
                residence_hall = ""
                email = ""
                telephone = ""
                tags = ""
                urls = ""
                home_address = ""
                status = ""

                valid = True
                info_groups = person.find(attrs={"class":"info groups"})
                if info_groups != None:
                    groupA = info_groups.find(attrs={"class":"groupA"})
                    if groupA != None:
                        if groupA.find(attrs={"class":"title"}) != None:
                            valid = False
                        if valid != False:
                            if groupA.p != None:
                                if groupA.p.get_text() == "Off Campus Program":
                                    # status = groupA.find({"class":"status"}).get_text()
                                    residence_hall = "Off Campus Program"
                                elif groupA.p.get_text() == "Early Finish":
                                    residence_hall = "Early Finish"
                                else: 
                                    location = groupA.find(attrs={"class":"location"})
                                    if location != None:
                                        if location.a != None:
                                            residence_hall = location.a.get_text()
                                        elif location.find({"class":"location"}) != None:
                                            residence_hall = location.find({"class":"location"}).get_text()
                                        elif location.get_text() != None:
                                            for br in location.find_all('br'):
                                                br.replace_with(" ")
                                            residence_hall = location.get_text()
                    if valid == True:
                        groupB = info_groups.find(attrs={"class":"groupB"})
                        if groupB != None:
                            mail = groupB.find(attrs={"class":"email"})
                            if mail != None:
                                # print "Mail: " + str(mail)
                                if mail.get_text() != None:
                                    email = mail.get_text()
                            tele = groupB.find(attrs={"class":"telephone"})
                            if tele != None:
                                if status != "":
                                    telephone = tele.a.get("href")[4:]
                                if status == "Off Campus Program":
                                    telephone = tele.get_text()
                                    residence_hall = "Off Campus Program"
                                else:
                                    telephone = tele.get_text()
                            tags_info = groupB.find(attrs={"class":"tags"})
                            if tags_info != None:
                                inner = tags_info.find(attrs={"class":"inner"})
                                if inner != None:
                                    tag_list = []
                                    for tag in inner:
                                        tag_list.append(tag.a.get_text())
                                    tags = tag_list
                            url_info = groupB.find(attrs={"class":"urls"})
                            if url_info != None:
                                url_list = []
                                for url in url_info.find_all("a"):
                                    url_list.append((url.get_text(), url.get("href")))
                        groupC = info_groups.find(attrs={"class":"groupC"})
                        if groupC != None:
                            personal = groupC.find(attrs={"class":"personal"})
                            if personal != None:
                                address = personal.find(attrs={"class":"homeAddress"})
                                for br in address.find_all('br'):
                                    br.replace_with(" ")
                                home_address = address.get_text()

                if valid == True:
                    heading_groups = person.find(attrs={"class":"heading "})
                    if heading_groups != None:
                        group1 = heading_groups.find(attrs={"class":"group1"})
                        if group1 != None:
                            name = group1.h2.get_text()
                            year = group1.find(attrs={"class":"affiliation"}).get_text()
                            majors = group1.find(attrs={"class":"majors"})
                            if majors != None:
                                cross_ref = majors.find(attrs={"class":"crossRef"})
                                if cross_ref != None:
                                    major = cross_ref.find(attrs={"class":"major"}).get_text()
                    else:
                        heading_groups = person.find(attrs={"class":"heading groups"})
                        if heading_groups != None:
                            group1 = heading_groups.find(attrs={"class":"group1"})
                            if group1 != None:
                                name = group1.h2.get_text()
                                year = group1.find(attrs={"class":"affiliation"}).get_text()
                                majors = group1.find(attrs={"class":"majors"})
                                if majors != None:
                                    major = group1.find(attrs={"class":"major"}).get_text()

                    # print "PERSON:"
                    # print name
                    # print year
                    # print major
                    # print residence_hall
                    # print email
                    # print telephone
                    # print tags
                    # print urls
                    # print home_address

                    person_stats = (name, year, major, residence_hall, email, telephone, tags, urls, home_address)

                    if person_stats not in person_dict:
                        person_dict[person_stats] = 1

person_dict = {}
count = 0

if len(sys.argv) != 3:
    print "$ <username> <password>"

campus_directory = "https://apps.carleton.edu/campus/directory/?first_name=%s&search_for=student"
# Use 'with' to ensure the session context is closed after use.
payload = {"username" : sys.argv[1], "password" : sys.argv[2]}
with requests.Session() as s:
    CARLETONedu = Xx # Enter
    CARLETONpass = Xx # Enter
    auth = (CARLETONedu, CARLETONpass)
    s.post("https://apps.carleton.edu/login/", auth=auth)
    # print the html returned or something more intelligent to see if it's a successful login page.

    # An authorised request.
    scraper("", s)

############## MORE HERE #########

csv_list = []
csv_list.append(["Name", "Year", "Major", "Residence Hall", "Email", "Telephone", "Home Address", "Tags", "Urls"])
for index in person_dict:
    info_bloc = [index[0], index[1], index[2], index[3], index[4], index[5], index[8], index[6], index[7]]
    csv_list.append(info_bloc)

if len(csv_list) != 1:
    filename = "TEST_CAMPUS_DOWNLAOD"
    myfile = open(filename + "-unfinished.csv", 'wb')
    wr = csv.writer(myfile, dialect='excel', quotechar='"', quoting=csv.QUOTE_ALL)
    wr.writerows(csv_list)
    myfile.close()

    open(filename + ".csv", "w").write("sep=,\n" + open(filename + "-unfinished.csv").read())
    os.remove(filename + "-unfinished.csv")
else:
    print "Failed to collect any information."

print "Done!"

####################### START #####
# if EXISTS:
#     READ FILE INTO DICT
#     for index in person_dict:
#         if index not in file_dict:
#             file_dict[index] = 1
#     person_dict = file_dict
####################### END #####


# get personal phone
# base64 encoding fro authentication?
# get image
# get student profile






