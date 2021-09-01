#from time import time
import urllib3,json
from flask import Flask,Response,request
from bird_engine import environ,preload,detect
from line_user import *
from threading import Thread
app = Flask(__name__)
HTTP = urllib3.PoolManager()
OPENAI_API_KEY = environ['OPENAI_API']
COMMON_HEADER = {
    'Authorization': 'Bearer '+ environ['LINE_TOKEN'],
    'Content-Type': 'application/json'
}
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
def muti_reply(reply_token,msg="Default Message"):
    this_header = COMMON_HEADER
    data = json.dumps({
        "replyToken": reply_token,
        "messages":[
            {
                "type":"text",
                "text":msg,
                "quickReply":{
                    "items":[
                        {
                            "type":"action",
                            "imageUrl":"https://image.flaticon.com/icons/png/512/1587/1587565.png",
                            "action":
                            {
                                "type":"postback",
                                "label":"helper-bot",
                                "data":"activate-helper",
                                "displayText":""
                            }
                        },
                        {
                            "type":"action",
                            "imageUrl":"https://image.flaticon.com/icons/png/512/3069/3069186.png",
                            "action":
                            {
                                "type":"postback",
                                "label":"birb-detection",
                                "data":"activate-birb",
                                "displayText":""
                            }
                        }
                    ]
                }
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
def push_text(user,msg,end_chat=False,end_detect=False):
    this_header = COMMON_HEADER
    this_header['Authorization'] = 'Bearer '+ environ['LINE_TOKEN']
    # will try to move JSON object to JSON file for future improvment and easy-to-read code
    raw_data = {
        "to":user,
        "messages":[{
            "type": "text",
            "text": msg,
            "quickReply":{
                "items":[{}]
            }
        }]
    }
    if end_chat:
        raw_data['messages'][0]['quickReply']['items'][0]={
            "type":"action",
            "imageUrl":"https://image.flaticon.com/icons/png/512/1587/1587565.png",
            "action":
            {
                "type":"postback",
                "label":"end helper-bot",
                "data":"deactivate-helper",
                "displayText":""
            }
        }
    elif end_detect:
        raw_data['messages'][0]['quickReply']['items'][0]={
            "type":"action",
            "imageUrl":"https://image.flaticon.com/icons/png/512/3069/3069186.png",
            "action":
            {
                "type":"postback",
                "label":"end birb-detection",
                "data":"deactivate-detect",
                "displayText":""
            }
        }
    data = json.dumps(raw_data)
    rep = HTTP.request('POST','https://api.line.me/v2/bot/message/push',headers=this_header,body=data)

    if str(rep.status) == '200':
        print('push text {',user,'} OK')
    else:
        print("ERROR at PUST TEXT:",rep.data)
        raise Exception('push text ERROR')
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
        push_text(user,"End birb-detection ?",end_detect=True)
    else:
        print(rep.data)
        raise Exception('push reply ERROR')
#--- OpenAI stuff
def openai_setup(user_id):
    # the idea about creating a conversation between man and openAI's completion API to make it look like a real chatbot
    # should begin building from GCP's cloud storage to store chat text object
    # then passing prompt text to openAI's completion api to get res
    # then seperate it into a conversation piece then store it again in GCP's cloud storage
    # should be fine as long as text objects won't be heaping much of memory to be used during processing time or qurey time
    # should try to experiement exchanging data rapidly to GCP's cloud storage first
    set_user_chat(user_id)
def openai_chat(user_id,text="Hello Helper!"):
    # do stuff that get res from openai's completion api
    all_chat = get_user_chat(user_id)
    all_chat += 'Human: '+text+ ' \\nHelper: '
    this_header = COMMON_HEADER
    this_header['Authorization'] = 'Bearer ' + OPENAI_API_KEY
    #print("DEBUG openAI:",this_header)
    with open('openai-completion-template.json') as data_file:
        data = json.load(data_file)
        data['prompt'] = all_chat
        data = json.dumps(data)
    #print(type(data))
    rep = HTTP.request('POST','https://api.openai.com/v1/engines/davinci/completions',headers=this_header,body=data)

    if str(rep.status) == '200':
        # maybe i should divide these process into muti-thread
        rep_body = json.loads(rep.data.decode("UTF-8"))
        all_chat+= rep_body['choices'][0]['text']
        #print("Text Generation completed! Saving to firesore...")
        try:
            sub_task1 = Thread(target=set_user_chat,args=(user_id,all_chat))
            sub_task2 = Thread(target=push_text,args=(user_id,rep_body['choices'][0]['text'],True,False))
            sub_task1.start()
            sub_task2.start()
        except Exception as e:
            print("ERROR at muti-Thread openai_chat")
            print(e)
        #set_user_chat(user_id,chat=all_chat)
        #push_text(user_id,rep_body['choices'][0]['text'],end_chat=True)
    else:
        print("ERROR:",rep.data)
#---- webhook routing
@app.route('/', methods=['POST'])
def respond():
    line_events = request.json['events']
    for event in line_events:
        if event['type']=='message':
            token = event['replyToken']
            payload = event['message']
            user_id = event['source']['userId']
            if payload['type'] == 'text':
                print("from : ",user_id)
                print("Text msg : ",payload['text'])
                if get_user_bot(user_id) :
                    openai_chat(user_id,payload['text'])
                else:
                    muti_reply(token,"Select New Task")
            elif payload['type'] == 'image':
                if get_user_detect(user_id):   
                    try:
                        preload()
                        print("Pre-load completed")
                    except:
                        print("ERROR pre-loading YOLOv5")
                    img_id = payload['id']
                    text_reply(token,msg="Searching.... Please Wait")
                    push_detection_res(user_id,img_id)
                else:
                    muti_reply(token,"Select New Task")
        elif event['type']=='postback':
            token = event['replyToken']
            user_id = event['source']['userId']
            postback = event['postback']['data']
            print("From:",user_id)
            print("Postback-Request:",postback)
            if postback == 'activate-helper':
                set_user_bot(user_id,True)
                set_user_detect(user_id,False)
                text_reply(token,"Helper is up ! begin to chat now !!!")
            elif postback == 'deactivate-helper':
                set_user_bot(user_id,False)
                set_user_chat(user_id)
                text_reply(token,"Helper is gone ! see you later !!!")
            elif postback == 'activate-birb':
                set_user_bot(user_id,False)
                set_user_detect(user_id,True)
                text_reply(token,"Birb-Detection is up ! send pic to begin detection !!!")
            elif postback == 'deactivate-detect':
                set_user_detect(user_id,False)
                text_reply(token,"Birb-Detection is gone !")      
        elif event['type'] == 'follow':
            user_id = event['source']['userId']
            token = event['replyToken']
            print("!!! NEW USER !!! {%s}" %user_id)
            generate_initial_user_data(user_id)
            muti_reply(token,"Select Task")
        elif event['type'] == 'unfollow':
            user_id = event['source']['userId']
            print("!!! USER{%s} is leaving !!! " %user_id)
            delete_user_data(user_id)

    return Response(status=200)
@app.route('/',methods=['GET'])
def def_rep():
    return Response(status=200)
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(environ['PORT']))