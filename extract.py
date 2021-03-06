import subprocess,json,time,urllib3,os,shutil,argparse
from bs4 import BeautifulSoup
from multiprocessing import cpu_count,Pool

TEMP_FOLDER = os.getcwd() + '/temp/'
FOLDER = os.getcwd() + '/image_data/'
HTTP = urllib3.PoolManager()
NUM = 1

"""
    Extract image data from Yandex.com's image search Full HTM file
    typically, yandex.com search result will always have starting image result at 30 pics
    To extract more than that , you need to scroll down to the end of that search result page 
    SO you could get like 1000+ pics
    #### HOW to use ########
    there are 4 flags
    --bird for naming bird folder and file accordingly
    --htm for using THAT HTM file to extract image URL
    --change-only for only time you just want to change file accordingly
    --add-num for that time when you want specific starting number of file for bird images
"""
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
        #req.release_conn()
    except :
        print(img_name + ' FAILED')
def muti_download(worker=cpu_count()):
    url_list = []
    with open(FOLDER+'temp.txt') as url_file:
        for url in url_file.readlines():
            url_list.append(url.split('\n')[0])
    print("URL count :",len(url_list))
    # oh yeah , just add more workers . NoThInG cOuLd gO wRoNg.
    download_pool = Pool(worker)
    download_pool.map(download,url_list)
    download_pool.close()
    download_pool.join()
def muti_change(name,add_num=0):
    global NUM
    #file_list = []
    NUM+=add_num
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
    inp.add_argument('--change-only',action='store_true')
    inp.add_argument('--add-num',type=int,default=0)
    opt = inp.parse_args()
    return opt
def clear_folder(img_folder,htm_folder):
    print(FOLDER+htm_folder.split('.htm')[0]+"_files")
    time.sleep(3)
    if os.path.exists(FOLDER+htm_folder.split('.htm')[0]+"_files"):
        shutil.rmtree(FOLDER+htm_folder.split('.htm')[0]+"_files")
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    if os.path.exists(FOLDER+img_folder):
        shutil.rmtree(FOLDER+img_folder)
    os.makedirs(TEMP_FOLDER)
    os.makedirs(FOLDER+img_folder)
def clear_temp():
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    os.makedirs(TEMP_FOLDER)
#-----------------------------------------------------------
def yandex_static_download(bird_name="wanker",htm_file="whatever.htm",only_change_file_name=False,starting_file_number=0,worker=cpu_count()):
    #export extract.py into one simeple-to-use function
    # will try to make it colorful in CMD usage later
    t0=time.time()
    print("============Download from yandex's static htm==============")
    if only_change_file_name:
        muti_change(bird_name,starting_file_number)
    else:
        clear_folder(bird_name,htm_file)
        read_html(htm_file)
        muti_download(worker)
        muti_change(bird_name,starting_file_number)
    clear_temp()
    print('=====================Time used : %.2f======================' % (time.time()-t0))
    print("============Download from yandex's static htm==============")
if __name__ == '__main__':
    subprocess.call('cls',shell=True)
    t0 = time.time()
    cmd_input = arg_parse()
    if cmd_input.change_only :
        muti_change(cmd_input.bird,cmd_input.add_num)
    else :
        clear_folder(cmd_input.bird,cmd_input.htm)
        read_html(cmd_input.htm)
        muti_download(cpu_count()*2)
        muti_change(cmd_input.bird,cmd_input.add_num)
    clear_temp()
    print('Time used : %.2f' % (time.time()-t0))