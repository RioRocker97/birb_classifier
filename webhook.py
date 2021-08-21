import urllib3,json
from flask import Flask,Response,request
from bird_engine import environ,preload,detect
app = Flask(__name__)
HTTP = urllib3.PoolManager()
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
    """
    try:
        preload()
        print("Pre-load completed")
    except:
        print("ERROR pre-loading YOLOv5")
    """
    app.run(debug=True,host='0.0.0.0',port=int(environ['PORT']))