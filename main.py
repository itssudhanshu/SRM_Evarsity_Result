from flask import Flask
from flask import request as rq
from flask import Response
import requests
import resource_srm
import json


UPLOAD_FOLDER = 'static/uploads/'
result_url = "https://evarsity.srmist.edu.in/srmwebonline/exam/onlineResult.jsp"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
    "Keep-Alive": "300",
    "Referer": "https://evarsity.srmist.edu.in/srmwebonline/exam/onlineResult.jsp",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "114",
    "Connection": "keep-alive",
    "Origin": "https://evarsity.srmist.edu.in",
    "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91" sec-ch-ua-mobile: ?0',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"
}

app = Flask(__name__)


@app.route('/')
def home():
    json_o = {"status": "success",
              "msg": "*** SRM EXAMINATION RESULT API WITH PYTHON *** By Sudhashu Kushwaha"}
    json_o = json.dumps(json_o)
    return json_o


@app.route('/result', methods=['GET', 'POST'])
def Result():
    if 'regno' in rq.args and 'date' in rq.args and 'month' in rq.args and 'year' in rq.args:
        cookiee, captcha = resource_srm.getCaptcha()
        headers["Cookie"] = "JSESSIONID="+str(cookiee)
    

        frmdate, txtFromDate, selMonth, txtYear = resource_srm.genfrmDate(
            rq.args.get('date'), rq.args.get('month'), rq.args.get('year'))
        print("Trying date: " + frmdate)

        data = {
            "frmdate": frmdate,
            "iden": "1",
            "txtRegisterno": rq.args.get('regno'),
            "txtFromDate": txtFromDate,
            "selMonth": selMonth,
            "txtYear": txtYear,
            "txtvericode": captcha.replace(" ", "")
        }

        caperror = "Invalid Verification Code"
        bdayerror = "Given Date of Birth is Incorrect"
        regnoerror = "Given Register Number" + \
            rq.args.get('regno')+" not available"

        
        result = requests.post(result_url, data=data, headers=headers)
        if caperror in result.text:
            response = {"status": "error",
                                "msg": "Invalid Verification Code!!"}
            response = json.dumps(response)
            response = Response(
                        response, status=200, mimetype='application/json')
            return response

        elif bdayerror in result.text:
            response = {"status": "error",
                                "msg": "Given Date of Birth is Incorrect!!"}
            response = json.dumps(response)
            response = Response(
                        response, status=200, mimetype='application/json')
            return response

        elif regnoerror in result.text:
            response = {"status": "error",
                                "msg": "Given Registration Number " +
                                rq.args.get('regno')+" is not available!!"}
            response = json.dumps(response)
            response = Response(
                        response, status=200, mimetype='application/json')
            return response
                   
        else:
            student = resource_srm.getDetails(result)
            results = resource_srm.generateResult(result)
            # print(results)
            response = {"student": student,"result": results}
            response = json.dumps(response)
            response = Response(
                        response, status=200, mimetype='application/json')
            return response
    else:
        response = {"status": "error", "msg": "Error in Input Parameters"}
        response = json.dumps(response)
        response = Response(response, status=200, mimetype='application/json')
        return response


if __name__ == '__main__':
    app.run(debug=True)
