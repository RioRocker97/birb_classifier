from time import time
import urllib3,json
from flask import Flask,Response,request
from bird_engine import environ,preload,detect
from google.cloud import firestore
app = Flask(__name__)
HTTP = urllib3.PoolManager()
DB = firestore.Client()
OPENAI_API_KEY = environ['OPENAI_API']
COMMON_HEADER = {
    'Authorization': 'Bearer '+ environ['LINE_TOKEN'],
    'Content-Type': 'application/json'
}
#--- OpenAI stuff
def openai_setup(user_id):
    # the idea about creating a conversation between man and openAI's completion API to make it look like a real chatbot
    # should begin building from GCP's cloud storage to store chat text object
    # then passing given text to openAI's completion api to get res
    # then seperate it into a conversation piece then store it again in GCP's cloud storage
    # should be fine as long as text objects won't be heaping much of the processing time or qurey time
    # should try to experiement exchanging data rapiding to GCP's cloud storage first
    chat_history = DB.collection(str("line_user")).document(str(user_id))
    chat_history.set({
        str("chat"): str("This Helper is an friendly,fun AI that know everything about bird.")
    })
def openai_chat(user_id,text="Human: Hello Helper!"):
    # do stuff that get res from openai's completion api
    chat_history = DB.collection(str("line_user")).document(str(user_id))
    all_chat = ""
    if chat_history.get().exists:
        all_chat = chat_history.get().to_dict().get("chat")
        print(all_chat)
    
    this_header = COMMON_HEADER
    this_header['Authorization'] = 'Bearer ' + OPENAI_API_KEY
    with open('openai-completion-template.json') as data_file:
        data = json.load(data_file)
        data['prompt'] = all_chat+' '+text
        data = json.dumps(data)
    print(type(data))
    rep = HTTP.request('POST','https://api.openai.com/v1/engines/davinci/completions',headers=this_header,body=data)

    if str(rep.status) == '200':
        rep_body = json.loads(rep.data.decode("UTF-8"))
        all_chat+= ' ' + text + ' ' + rep_body['choices'][0]['text']
        print(all_chat)
        chat_history.set({
            str("chat"): str(all_chat)
        })
    else:
        print(rep.data)

    
#--- LINE stuff
def construct_flex_msg(img_url,birb_icon_url,most_likely):
    """
    Build flex message based on my own design flex's template
    """
    with open('./flex_template.json') as flex_file:
        flex_body = json.load(flex_file)
        flex_body['body']['contents'][0]['url'] = img_url
        flex_body['body']['contents'][0]['action']['uri'] = img_url
        flex_body['body']['contents'][1]['contents'][1]['text'] = most_likely
        flex_body['body']['contents'][2]['url'] = birb_icon_url
        
        return flex_body
def get_img(img_id):
    this_header = COMMON_HEADER
    rep = HTTP.request('GET','https://api-data.line.me/v2/bot/message/'+img_id+'/content',headers=this_header)

    if str(rep.status) == '200':
        return rep.data
    else:
        raise Exception("ERROR at Get IMG")
def push_detection_res(user,img_id):
    this_header = COMMON_HEADER
    img_link,img_label=detect(img_id,get_img(img_id))
    data = json.dumps({
        "to":user,
        "messages":[{
            "type":"flex",
            "altText": "Reverse Image search in Flex style",
            "contents": construct_flex_msg(img_link,"https://image.flaticon.com/icons/png/512/3069/3069186.png",img_label)     
        }]
    })
    rep = HTTP.request('POST','https://api.line.me/v2/bot/message/push',headers=this_header,body=data)

    if str(rep.status) == '200':
        print('push reply {',user,'} OK')
    else:
        print(rep.data)
        raise Exception('push reply ERROR')
def text_reply(reply_token,msg="Default Message"):
    this_header = COMMON_HEADER
    data = json.dumps({
        "replyToken": reply_token,
        "messages":[
            {
                "type":"text",
                "text":msg
            }
        ]
    })
    rep = HTTP.request('POST','https://api.line.me/v2/bot/message/reply',
        body = data,headers=this_header)
    
    if str(rep.status) == '200':
        print('Reply OK')
    else :
        print(rep.data)
        print('Reply ERROR')

@app.route('/', methods=['POST'])
def respond():
    line_events = request.json['events']
    for event in line_events:
        if event['type']=='message':
            token = event['replyToken']
            address = event['source']
            payload = event['message']
            if payload['type'] == 'text':
                print("from : ",address['userId'])
                print("Text msg : ",payload['text'])
                text_reply(token)
            if payload['type'] == 'image':
                try:
                    preload()
                    print("Pre-load completed")
                except:
                    print("ERROR pre-loading YOLOv5")
                user_id = address['userId']
                img_id = payload['id']
                text_reply(token,msg="Searching.... Please Wait")
                push_detection_res(user_id,img_id)
                

    return Response(status=200)
@app.route('/',methods=['GET'])
def def_rep():
    return Response(status=200)
if __name__ == "__main__":
    #app.run(debug=True,host='0.0.0.0',port=int(environ['PORT']))
    #openai_setup("69420")
    t0 = time()
    openai_chat("69420","Human: ")
    #print("something")
    print("Time used %.2f" %(time()-t0))