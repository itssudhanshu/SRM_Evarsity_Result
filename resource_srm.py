try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import time
import requests
from bs4 import BeautifulSoup


UPLOAD_FOLDER = 'static/uploads/'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

captcha_url="https://evarsity.srmist.edu.in/srmwebonline/Captcha"
name=int(round(time.time() * 1000))        


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


def getCaptcha():
    captcha=requests.get(captcha_url)
    with open(UPLOAD_FOLDER+str(name)+'.jpg', 'wb') as test:
        test.write(captcha.content)
    cap=ocr_core(UPLOAD_FOLDER +str(name)+'.jpg')
    print(cap)
    cook=captcha.cookies['JSESSIONID']
    del captcha
    return cook,cap

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




