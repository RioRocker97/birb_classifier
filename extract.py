import subprocess,json,time,urllib3,os,shutil
from bs4 import BeautifulSoup
from multiprocessing import cpu_count,Pool

IMG_FOLDER = os.getcwd() + '/TEST/'
TXT_File = os.getcwd() + '/first_gather/url2.txt'
REAL_IMG_FOLDER = os.getcwd() + '/first_gather/after/'
HTTP = urllib3.PoolManager()
NAME = "TEST"
NUM = 1
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
def download(real_url):
    temp = real_url.split('/')
    img_name = temp[len(temp)-1][0:20] + '.jpg'
    try:
        req = HTTP.request('GET',real_url,preload_content=False,timeout=3.0)
        img_file = open(IMG_FOLDER+img_name,'wb')
        img_file.write(req.data)
        print(img_name + ' OK')
        img_file.close()
        req.release_conn()
    except :
        print(img_name + ' FAILED')
            
def muti_download():
    url_list = []
    with open(TXT_File) as url_file:
        for url in url_file.readlines():
            url_list.append(url.split('\n')[0])
    print("URL count :",len(url_list))
    download_pool = Pool(cpu_count())
    download_pool.map(download,url_list)
    download_pool.close()
    download_pool.join()
def muti_change(name):
    global NUM
    #file_list = []
    for img in os.listdir(IMG_FOLDER):
        #file_list.append(img)
        shutil.copyfile(IMG_FOLDER+img,REAL_IMG_FOLDER+name+'_'+str(NUM)+'.jpg')
        print("NEW",name+'_'+str(NUM)+'.jpg',"OK")
        NUM+=1
    #print("File Count :",len(file_list))
    """
    # i will find a way to use shared memory in Pool,somehow...
    change_pool = Pool(cpu_count())
    change_pool.map(change_file,file_list)
    change_pool.close()
    change_pool.join()
    """
#------------------------------------------------------------                
if __name__ == '__main__':
    subprocess.call('cls',shell=True)
    shutil.rmtree(IMG_FOLDER)
    os.mkdir(IMG_FOLDER)
    shutil.rmtree(REAL_IMG_FOLDER)
    os.mkdir(REAL_IMG_FOLDER)
    t0 = time.time()
    muti_download()
    muti_change('TEST')
    #read_html('3.htm')
    #download('green_cheeked_conure')
    print('Time used : %.2f' % (time.time()-t0))
    #single-thread : 1538.7 sec / 1345 pics for grey parrot
    #single-thread : 1652.q sec / 1479 pics for green cheeked
    #Concurrent Pool : 154.26 sec / 1319 pics for green cheeked
    #Concurrent Pool + Copy/change file name : 176.98 sec for 1314 for green cheeked
