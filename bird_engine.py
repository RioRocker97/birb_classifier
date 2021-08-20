from os import getcwd,environ,path,makedirs
from yolo_detect import prepareYolo,runYolo
from subprocess import call
from google.cloud import storage

BIRB_MODEL = getcwd()+'/birb_model/'
TEMP = getcwd()+'/temp/'
GCP_BUCKET = environ['GCP_B']
GCP_BUCKET_URL = environ['GCP_B_URL']

def preload():
    """
    pre-load every YOLOv5's asset
    note: Should this function muti-thread ?
    """
    if not path.exists(BIRB_MODEL):
        makedirs(BIRB_MODEL)
        # do download or update birb model
        #my_progress("Get all model",100000)
    if not path.exists(BIRB_MODEL):
        makedirs(BIRB_MODEL)
        #store image here before detection
    
    #cut to pre-load single model for now...
    prepareYolo(BIRB_MODEL+'bird_first_gather.pt',confidence=0.7)
    #prepareYolo(BIRB_MODEL+'yolov5m.pt',confidence=0.7)
def detect(img_id,img_data):
    """
        Begin Deteciton here
        This function should return detected image link url and most likely label
    """
    with open(TEMP+str(img_id)+'.jpg','wb') as temp_img:
        temp_img.write(img_data)
    # Do Detection
    try:
        img_result,label_result = runYolo(TEMP+str(img_id)+'.jpg')
    except:
        print('ERROR Detecting')
    # Do uploading result image after detection completed
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCP_BUCKET)
        blob = bucket.blob(str(img_id)+'.jpg')
        blob.upload_from_string(img_result,content_type='image/jpeg')
        print('Imaged Upload !')
        return GCP_BUCKET_URL+str(img_id)+'.jpg',label_result
    except:
        print('ERROR uploading')



