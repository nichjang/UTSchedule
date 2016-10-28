import requests
import re
import csv
from bs4 import BeautifulSoup

classContentArray = []

def parseData(siteURL, level="L", next=False):
    if next != True:
        siteURL += '&level=' + level
        #print('added level')

    #for classID in classAbrev:
    #print(siteURL)
    r = requests.post(siteURL, cookies=cookies, data=payload)

    soup = BeautifulSoup(r.content)
        
    classContent = soup.find_all("tr")
    if len(classContent) > 1:
        for content in classContent:
            local = []
            try:
                tds = content.find_all('td')
                for td in tds:
                    local.append(td.text.strip())
                classContentArray.append(local)
            except AttributeError:
                pass
        next = soup.find('a', id='next_nav_link')

        if next is not None:
            for item in match:
            pattern = r'level=([A-Z])&|level=([A-Z])$'
            match = re.findall(pattern, next["href"])
            #print(next['href'])
                if len(item) == 1:
                    level = item
            #print(level + " next block hit")
            siteURLTemp = "https://utdirect.utexas.edu/apps/registrar/course_schedule/20172/results/" + next['href']
            parseData(siteURLTemp,level,True)
    # hit this when blank page or no more nexts
    # check current level, and increment by "1" if level != "G"
    if level != "G":
        #print('up level')
        if level == "L":
            level = "U"
        else:
            level = "G"
        # remove out the current level and any next unique
        pattern = r'fos_fl=([A-Z].*[A-Z])&|fos_fl=([A-Z].*)$'
        match = re.findall(pattern, siteURL)
        # print(siteURL)
        # print(match)
        match = match[0]
        if len(match[0]) > 0:
            course = str(match[0])
            #print(str(match[0]))
        else:
            course = str(match[1])
        # regex out the fos_fl= value see above regex for example
        siteURL = "https://utdirect.utexas.edu/apps/registrar/course_schedule/20172/results/?search_type_main=FIELD&fos_fl=" + course 
        # get string up to ?
        # append to string search_type_main=FIELD
        # append fos_fl=value

        parseData(siteURL, level)
    # else return



session = requests.session()

#IDToken1 is your ut eid
#IDToken2 is your password for your account 
payload = {'IDToken1': '', 'IDToken2': ''}
url = 'https://login.utexas.edu/login/cdcservlet?goto=https%3A%2F%2Futdirect.utexas.edu%3A443%2Fapps%2Fregistrar%2Fcourse_schedule%2F20172&RequestID=831877453&MajorVersion=1&MinorVersion=0&ProviderID=https%3A%2F%2Futdirect.utexas.edu%3A443%2Famagent%3FRealm%3D%2Fadmin%2Futdirect-realm&IssueInstant=2016-10-23T00%3A04%3A28Z'
r = requests.get(url)
# get all form fields from response other than IDToken
soup = BeautifulSoup(r.content)
hidden_tags=soup.find_all("input",type="hidden")
for tag in hidden_tags:
	# append to payload those fields with values
	payload[tag["name"]] = tag["value"]

# make post request
r = requests.post(url, data=payload)
# set cookies explicitly
cookies = r.cookies
#submit LARES
soup = BeautifulSoup(r.content)
LARES = soup.find_all("input", type="hidden")
name = ""
value = ""
for tag in LARES:
	name = tag["name"]
	value = tag["value"]
payload = {}
payload[name] = value
r = requests.post("https://utdirect.utexas.edu:443/apps/registrar/course_schedule/20172", cookies=cookies, data=payload)
cookies = r.cookies

soup = BeautifulSoup(r.content)
classContainer = soup.find("select", id = "fos_fl")
classContainer = classContainer.find_all("option")
classAbrev = []

for title in classContainer:
	classAbrev.append(title['value'])

del classAbrev[0]


for classID in classAbrev:
    siteURL = "https://utdirect.utexas.edu/apps/registrar/course_schedule/20172/results/?ccyys=20172&search_type_main=FIELD&fos_fl="
    siteURL += classID
    value = parseData(siteURL)

    #print("next ID")
#print(classContentArray)
s = ','
for item in classContentArray:
    s.join(item)


with open('test4.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
        quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # write headers
    headers = ['name', 'uniqueId', 'date','time', 'location', 'prof', 'status', 'flags']
    writer.writerow(headers)
    classTitle = ''

    if (len(classContentArray[0]) == 1):
        classTitle = classContentArray[0]

    for schedule in classContentArray:
        if len(schedule) > 1:
            writer.writerow(classTitle + schedule)
        elif len(schedule) == 1:
            classTitle = schedule
print("completed")



print (classContentArray)
exit()
