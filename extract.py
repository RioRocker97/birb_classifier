import subprocess,json,time,urllib3,os
from bs4 import BeautifulSoup
subprocess.call('cls',shell=True)

IMG_FOLDER = os.getcwd() + '/img2/'
TXT_File = 'url2.txt'
def read_data():
    file = open('data-pem.txt')
    IMG_URL = 15
    SPLIT = '&quot;'
    txt = file.read()

    num =0
    print('===============================')
    for word in txt.split('&quot;'):
        if num == IMG_URL:
            print("%i : %s" %(num,word))
        num+=1
    print('===============================')
def read_html(htm_file):
    file = open(htm_file,encoding='UTF-8')
    img_url = open(TXT_File,'w+')
    html = BeautifulSoup(file.read())
    print(len(html.find_all('div',{'class':'serp-item_type_search'})))
    #print(html.find_all('div',{'class':'serp-item_type_search'})[0]['data-bem'])
    for img in html.find_all('div',{'class':'serp-item_type_search'}) :
        data = json.loads(img['data-bem'])
        #data = json.loads(html.find_all('div',{'class':'serp-item_type_search'})[0]['data-bem'])
        img_url.write(data['serp-item']['preview'][0]['url'] + '\n')
    
    img_url.close()
    file.close()
def download(name):
    http = urllib3.PoolManager()
    num=0
    with open(TXT_File) as url_file:
        for url in url_file.readlines():
            real_url = url.split('\n')[0]
            try:
                req = http.request('GET',real_url,preload_content=False,timeout=3.0)
            except Exception as msg:
                print(msg,'. Passing...')
                req.release_conn()
                pass
            img_name = name+'_'+str(num)+'.jpg'
            try:
                img_file = open(IMG_FOLDER+img_name,'wb')
                img_file.write(req.data)
                print(img_name + ' OK')
                num+=1
            except Exception as msg:
                print(msg)
                print(img_name + ' FAILED')
            finally:
                img_file.close()
                req.release_conn()
                

t0 = time.time()
read_html('3.htm')
download('green_cheeked_conure')
print('Time used : %.2f' % (time.time()-t0))
#single-thread : 1538.7 sec / 1345 pics for grey parrot
#single-thread : 1652.q sec / 1479 pics for green cheeked