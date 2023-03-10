from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode
import requests
import json
import time
import hashlib
import random

# 학교 정보 파악용 배열
area1=['서울', '서울시', '서울교육청', '서울시교육청', '서울특별시']
area2=['부산', '부산광역시', '부산시', '부산교육청', '부산광역시교육청']
area3=['대구', '대구광역시', '대구시', '대구교육청', '대구광역시교육청']
area4=['인천', '인천광역시', '인천시', '인천교육청', '인천광역시교육청']
area5=['광주', '광주광역시', '광주시', '광주교육청', '광주광역시교육청']
area6=['대전', '대전광역시', '대전시', '대전교육청', '대전광역시교육청']
area7=['울산', '울산광역시', '울산시', '울산교육청', '울산광역시교육청']
area8=['세종', '세종특별시', '세종시', '세종교육청', '세종특별자치시', '세종특별자치시교육청']
area10=['경기', '경기도', '경기교육청', '경기도교육청']
area11=['강원', '강원도', '강원교육청', '강원도교육청']
area12=['충북', '충청북도', '충북교육청', '충청북도교육청']
area13=['충남', '충청남도', '충남교육청', '충청남도교육청']
area14=['전북', '전라북도', '전북교육청', '전라북도교육청']
area15=['전남', '전라남도', '전남교육청', '전라남도교육청']
area16=['경북', '경상북도', '경북교육청', '경상북도교육청']
area17=['경남', '경상남도', '경남교육청', '경상남도교육청']
area18=['제주', '제주도', '제주특별자치시', '제주교육청', '제주도교육청', '제주특별자치시교육청', '제주특별자치도']

level1=['유치원', '유']
level2=['초등학교', '초']
level3=['중학교', '중']
level4=['고등학교', '고']
level5=['특수학교', '특']

# 학교 정보 파악용 함수
def schoolinfo(area,level):
    info={}
    if area in area1:
        schoolcode="01"
        schoolurl="sen"
    if area in area2:
        schoolcode="02"
        schoolurl="pen"
    if area in area3:
        schoolcode="03"
        schoolurl="dge"
    if area in area4:
        schoolcode="04"
        schoolurl="ice"
    if area in area5:
        schoolcode="05"
        schoolurl="gen"
    if area in area6:
        schoolcode="06"
        schoolurl="dje"
    if area in area7:
        schoolcode="07"
        schoolurl="use"
    if area in area8:
        schoolcode="08"
        schoolurl="sje"
    if area in area10:
        schoolcode=10
        schoolurl="goe"
    if area in area11:
        schoolcode=11
        schoolurl="kwe"
    if area in area12:
        schoolcode=12
        schoolurl="cbe"
    if area in area13:
        schoolcode=13
        schoolurl="cne"
    if area in area14:
        schoolcode=14
        schoolurl="jbe"
    if area in area15:
        schoolcode=15
        schoolurl="jne"
    if area in area16:
        schoolcode=16
        schoolurl="gbe"
    if area in area17:
        schoolcode=17
        schoolurl="gne"
    if area in area18:
        schoolcode=18
        schoolurl="jje"
    if level in level1:
        schoollevel=1
    if level in level2:
        schoollevel=2
    if level in level3:
        schoollevel=3
    if level in level4:
        schoollevel=4
    if level in level5:
        schoollevel=5
    info["schoolcode"]=schoolcode
    info["schoollevel"]=schoollevel
    info["schoolurl"]=schoolurl
    return info

# GET, POST 보내기
def web_request(method_name, url, dict_data, is_urlencoded=True):
    """Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
    method_name = method_name.upper() # 메소드이름을 대문자로 바꾼다 
    if method_name not in ('GET', 'POST'):
        raise Exception('method_name is GET or POST plz...')
        
    if method_name == 'GET': # GET방식인 경우
        response = requests.get(url=url, params=dict_data)
    elif method_name == 'POST': # POST방식인 경우
        if is_urlencoded is True:
            response = requests.post(url=url, data=dict_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})
    
    dict_meta = {'status_code':response.status_code, 'ok':response.ok, 'encoding':response.encoding, 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']): # JSON 형태인 경우
        return {**dict_meta, **response.json()}
    else: # 문자열 형태인 경우
        return {**dict_meta, **{'text':response.text}}

# RSA 암호화용 (이름, 생년월일 암호화화)
def rsaEncrypt(n):
    pubkey = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2+SGgEU0aqi5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ8o3FGqMzsMTNxr+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7yDzcfjfBs99K5xJEppHG0qc+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzhwUC8T4G5NclLEWzOQExbQ4oDlZBv8BM/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNNQQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB'
    msg = n
    keyDER = b64decode(pubkey)
    keyPub = RSA.importKey(keyDER)
    cipher = Cipher_PKCS1_v1_5.new(keyPub)
    cipher_text = cipher.encrypt(msg.encode())
    emsg = b64encode(cipher_text)
    return emsg.decode('utf-8')

# SEED 암호 관련 함수들
def tk_sh1prng():
    f = 10325476
    e = 0
    g = ""
    now = time.time()
    Xseed1 = int(now % 60)
    Xseed2 = round(now * 1000)
    a = str(Xseed2) + "1080" + "24" + "1920" + "1032" + str(Xseed1) + str(f) + str(Xseed2)
    if e!=1:
        d = hashlib.sha256(a.encode()).hexdigest()
        e = 1
    XSEEDj = int(now % 60) + round(now * 1000)
    a = str(XSEEDj) + str(d) + str(g) + "1"
    g = hashlib.sha256(a.encode()).hexdigest()
    return g

def tk_getrnd_hex(a):
    b = ""
    if a < 20:
        b = tk_sh1prng();
        b = b[0:a * 2];
        return b
    else:
        for i in range(0,int(a / 20)):
            b += tk_sh1prng()
        if a % 20:
            rand_tmp = tk_sh1prng();
            b += rand_tmp[0:(a % 20) * 2]
    return b

def genKey(a):
    b = a / (8 * 4);
    c = '';
    for i in range(0,int(b)):
        c += tk_getrnd_hex(2)
    return c

def selfcheck(sname, birth, area, pw, schoolname, schoollevel):
    name = rsaEncrypt(sname)
    birth = rsaEncrypt(birth)
    info=schoolinfo(area,schoollevel)
    # 학교 정보 확인
    url = 'https://hcs.eduro.go.kr/v2/searchSchool?lctnScCode='+str(info["schoolcode"])+'&schulCrseScCode='+str(info["schoollevel"])+'&orgName='+schoolname+'&loginType=school'
    response = requests.get(url)
    school_infos = json.loads(response.text)
    if len(school_infos["schulList"])==1: 
        schoolcode=school_infos["schulList"][0]["orgCode"]
    else:
        for i in range(0,len(school_infos["schulList"])):
            print(f'[{i+1}] {school_infos["schulList"][i]["kraOrgNm"]}\n')
        foo = int(input("Select: "))
        schoolcode=school_infos["schulList"][foo-1]["orgCode"]
    searchKey = school_infos['key']
    # 만료 시간 체크
    response = requests.get(url="https://hcs.eduro.go.kr/transkeyServlet?op=getInitTime&1674263524920")
    initTime = response.text.split("'")[1]
    #uuid
    uuid = tk_sh1prng()
    #keyIndex
    a = tk_sh1prng()
    a = a[:8]
    rand_int = int(f'0x{a}', 16)
    allocationIndex=rand_int
    response = requests.post(url=f"https://hcs.eduro.go.kr/transkeyServlet?op=getKeyIndex&name=password&keyType=single&keyboardType=number&fieldType=password&inputName=password&parentKeyboard=false&transkeyUuid={uuid}&exE2E=false&TK_requestToken=0&isCrt=false&allocationIndex={allocationIndex}&keyIndex=&initTime={initTime}&talkBack=true")
    keyIndex = response.text
    #seedkey

    #로그인
    
    response = requests.post(url="https://"+info["schoolurl"]+"hcs.eduro.go.kr/v2/findUser", data=json.dumps(data), headers={'Content-Type': 'application/json'})
    token=response.json()['token']
    
    # 비밀번호
    # headers={'Content-Type': 'application/json', "Authorization": token}
    # data={"password":str(rsaEncrypt(str(pw)))}
    # response = requests.post(url="https://"+info['schoolurl']+"hcs.eduro.go.kr/v2/validatePassword", headers=headers, data=json.dumps(data))
    # token=str(response.json())
    
    #최종 token불러오기 위한 학생정보 확인
    headers={'Content-Type': 'application/json', "Authorization": token}
    response = requests.post(url="https://"+info["schoolurl"]+"hcs.eduro.go.kr/v2/selectUserGroup", headers=headers)
    userPNo = response.json()[0]['userPNo']
    token = response.json()[0]['token']
    #최종 token 발급
    data={"orgCode":schoolcode,"userPNo": userPNo}
    headers={'Content-Type': 'application/json', "Authorization": token}
    response = requests.post(url="https://"+info["schoolurl"]+"hcs.eduro.go.kr/v2/getUserInfo", data=json.dumps(data), headers=headers)
    token=response.json()['token']
    #자가진단 정보 입력
    endpoint = "https://"+info["schoolurl"]+"hcs.eduro.go.kr/registerServey"
    data = {'rspns01':'1','rspns02':'1','rspns03':'1','rspns04':None,'rspns05':None,'rspns06':None,'rspns07':None,'rspns08':None,'rspns09':None,'rspns10':None,'rspns11':None,'rspns12':None,'rspns13':None,'rspns14':None,'rspns15':None,'rspns00':'Y','deviceUuid':'','upperToken':token,'upperUserNameEncpt':sname,'clientVersion':'1.9.22'}
    headers = {'Content-Type': 'application/json;charset=UTF-8',"Authorization": token}
    response=requests.post(endpoint, data=json.dumps(data), headers=headers).json()
    return response