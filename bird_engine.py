from os import getcwd,environ,path,makedirs,remove
from yolo_detect import prepareYolo,runYolo
from subprocess import call
from cv2 import imencode
from google.cloud import storage,firestore
BIRB_MODEL = getcwd()+'/birb_model/'
TEMP = getcwd()+'/temp/'
GCP_BUCKET = environ['GCP_B']
GCP_BUCKET_URL = environ['GCP_B_URL']
CONF = float(environ['CONF_VAL'])
def preload():
    """
    pre-load every YOLOv5's asset
    note: Should this function muti-thread ?
    """
    if not path.exists(BIRB_MODEL):
        makedirs(BIRB_MODEL)
    if not path.exists(TEMP):
        makedirs(TEMP)
    
    #cut to pre-load single model for now...
    prepareYolo(BIRB_MODEL+'bird_first_gather.pt',confidence=CONF)
def detect(img_id,img_data):
    """
        Begin Deteciton here
        This function should return detected image link url and most-likely birb label
    """
    with open(TEMP+str(img_id)+'.jpg','wb') as temp_img:
        temp_img.write(img_data)
    # Do Detection
    try:
        img_result,label_result = runYolo(TEMP+str(img_id)+'.jpg')
    except Exception as e:
        print('ERROR Detecting')
        print(e)
    # Do uploading result image after detection is completed
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(GCP_BUCKET)
        blob = bucket.blob(str(img_id)+'.jpg')
        _,buffer = imencode('.jpg',img_result)

        blob.upload_from_string(buffer.tobytes(),content_type='image/jpeg')
        print('Imaged Upload !')
        return GCP_BUCKET_URL+str(img_id)+'.jpg',label_result
    except Exception as e:
        print('ERROR uploading')
        print(e)
    finally:
        remove(TEMP+str(img_id)+'.jpg')

