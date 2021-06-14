from bs4 import BeautifulSoup

def genfrmDate(date,month,year):
    month=str(month).zfill(2)
    date=str(date).zfill(2)
    return str(str(year)+"-"+str(month)+"-"+str(date)),date,month,year

def generateResult(result):
    results = []
    temp_sub = {}
    soup = BeautifulSoup(result.content, 'html5lib') 
    table = soup.find('table', attrs = {'id':'table1'}) 
    for tr in table.findAll('tr')[1:]:
        td = tr.findAll('td')
        temp_sub['sno'] = td[0].text
        temp_sub['semester'] = td[1].text
        temp_sub['course_code'] = td[2].text
        temp_sub['course_name'] = td[3].text
        temp_sub['credit'] = td[4].text
        temp_sub['marks'] = td[7].text
        temp_sub['max_marks'] = td[8].text
        temp_sub['grade'] = td[9].text
        temp_sub['result'] = td[10].text

        temp = temp_sub.copy()
        results.append(temp)
        temp_sub.clear()
    
    return results

def getDetails(result):
    details = {}
    soup = BeautifulSoup(result.content, 'html5lib') 
    table = soup.find('table', attrs = {'class':'dynaColorTR2'})
    for tr in table.findAll('tr'):
        td = tr.findAll('td')
        details[td[0].text] = td[1].text
    
    return details




