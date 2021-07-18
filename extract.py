import subprocess,json,time,urllib3,os,shutil,argparse
from bs4 import BeautifulSoup
from multiprocessing import cpu_count,Pool

TEMP_FOLDER = os.getcwd() + '/temp/'
TXT_File = os.getcwd() + '/first_gather/url2.txt'
REAL_IMG_FOLDER = os.getcwd() + '/first_gather/after/'
FOLDER = os.getcwd() + '/first_gather/'
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
    img_url = open(FOLDER+'temp.txt','w+')
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
        img_file = open(TEMP_FOLDER+img_name,'wb')
        img_file.write(req.data)
        print(img_name + ' OK')
        img_file.close()
        req.release_conn()
    except :
        print(img_name + ' FAILED')
            
def muti_download():
    url_list = []
    with open(FOLDER+'temp.txt') as url_file:
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
    for img in os.listdir(TEMP_FOLDER):
        #file_list.append(img)
        shutil.copyfile(TEMP_FOLDER+img,FOLDER+'/'+name+'/'+name+'_'+str(NUM)+'.jpg')
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
def arg_parse():
    inp = argparse.ArgumentParser()
    inp.add_argument('--bird',type=str,default='after')
    inp.add_argument('--htm',type=str,default='whatever.htm')
    opt = inp.parse_args()
    return opt
def clear_folder(img_folder):
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    if os.path.exists(FOLDER+img_folder):
        shutil.rmtree(FOLDER+img_folder)
    os.makedirs(TEMP_FOLDER)
    os.makedirs(FOLDER+img_folder)
if __name__ == '__main__':
    subprocess.call('cls',shell=True)
    t0 = time.time()
    cmd_input = arg_parse()
    clear_folder(cmd_input.bird)
    read_html(cmd_input.htm)
    muti_download()
    muti_change(cmd_input.bird)
    print('Time used : %.2f' % (time.time()-t0))