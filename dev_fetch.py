from flask import Flask,request
from datetime import datetime
from flask_cors import CORS #flaskにCORSを許可
import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime
import json

# python -m flask run で動かす場合このファイルの名前は「app.py」か「wsgi.py」にする

app = Flask(__name__)
CORS(app) #flaskにCORSを許可

def strfilter(string:str)->str:
    #match_object = re.match("[a-zA-Z0-9]+", string)
    match_object = re.fullmatch("[0-9]{4}", string)
    if match_object:
        cleaned = match_object.group(0)
    else:
        cleaned = 'error'
    return cleaned

@app.route('/')
def rootfunc():
    print("do rootfunc")
    return '{"date":"xxxx-xx-xx","o":"0","h":"0","l":"0","c":"0","volume":"0","ca":"0"}'

@app.route('/code/')
@app.route('/code')
def codefunc():
    print("no code")
    return '{"date":"xxxx-xx-xx","o":"0","h":"0","l":"0","c":"0","volume":"0","ca":"0"}'

@app.route('/code/<ticker>/')
@app.route('/code/<ticker>')
def fetch(ticker):
    print("do fetch")
    print(ticker)
    if strfilter(ticker)=="error":
        return '{"date":"xxxx-xx-xx","o":"0","h":"0","l":"0","c":"0","volume":"0","ca":"0"}'
    url = 'https://kabuoji3.com/stock/{}/'.format(ticker)
    soup = BeautifulSoup(requests.get(url,headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}).content,'html.parser')

    tag_tr = soup.find_all('tr')
    head = [h.text for h in tag_tr[0].find_all('th')] #テーブルのヘッドの取得
    col = ['date','o','h','l','c','volume','ca']

    #テーブルの各データの取得
    data = []
    for i in range(1,len(tag_tr)):
        data.append([d.text for d in tag_tr[i].find_all('td')])
        df = pd.DataFrame(data, columns=col)

    #for c in col:
    #    df[c] = df[c].astype(float)
    #df['日付'] = [datetime.strptime(i,'%Y-%m-%d') for i in df['日付']]

    dct=df.loc[0, :].to_dict()
    dct['code_name']=soup.find("span", class_="jp").text
    return json.dumps(dct,ensure_ascii=False)
    #return df.loc[0, :].to_json()

@app.route('/auth/')
@app.route('/auth')
def auth():
    print("do auth")
    head=request.headers.get("authorization")
    #res=requests.get("https://qr1.devmarket.myquick.net/home/member/qrx_func/standard/auth.do",headers={"authorization":head})
    #return str(res.status_code)
    if head=="Basic UUlLQVFDUXh4eHg6UUlLQVFDUXh4eHg=":
        return "200"
    else:
        return "401"
        #return "403"


# python -m flask run ではなくスタンドアロンで走らせたいならこれを書く（この際は任意のファイル名にできる）
if __name__ == "__main__":
    #runメソッドでビルトインサーバーが走る
    app.run(port=5000)