from os import getcwd,environ,path,makedirs
from yolo_detect import prepareYolo,runYolo
from google.cloud import storage

BIRB_MODEL = getcwd()+'/birb_model/'
TEMP = getcwd()+'/temp/'
GCP_BUCKET = environ['GCP_B']
GCP_BUCKET_URL = environ['GCP_B_URL']
#LINE_ACCESS_TOKEN = os.environ['LINE_TOKEN']
#BIRB_BUCKET = 0
def preload():
    if not path.exists(BIRB_MODEL):
        makedirs(BIRB_MODEL)
        # do download or update birb model
        #my_progress("Get all model",100000)
    if not path.exists(BIRB_MODEL):
        makedirs(BIRB_MODEL)
        #store image here before detection
    
    #cut to pre-load single model for now...
    prepareYolo(BIRB_MODEL+'bird_first_gather.pt',confidence=0.7)
def upload_img(img_id,data):
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCP_BUCKET)
    blob = bucket.blob(str(img_id)+'.jpg')

    try:
        blob.upload_from_string(data,content_type='image/jpeg')
        print('Imaged Upload !')
        return GCP_BUCKET_URL+str(img_id)+'.jpg'
    except:
        print('ERROR uploading')
        return "ERROR"
def detect(img_file):
    """
        This function should return finished detection image data
    """
    return runYolo(TEMP+img_file)


if __name__ == "__main__":
    pass


