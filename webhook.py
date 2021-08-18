import urllib3,json
from flask import Flask,Response,request
from bird_engine import *
app = Flask(__name__)
HTTP = urllib3.PoolManager()
COMMON_HEADER = {
    'Authorization': 'Bearer '+ environ['LINE_TOKEN']
}
def push_text_msg(user,flex_body):
    this_header = COMMON_HEADER
    this_header['Content-Type'] = 'application/json'
    data = json.dumps({
        "to":user,
        "messages":[{
            "type":"flex",
            "altText": "Reverse Image search in Flex style",
            "contents": flex_body     
        }]
    })
    rep = HTTP.request('POST','https://api.line.me/v2/bot/message/push',headers=this_header,body=data)

    if str(rep.status) == '200':
        print('push reply {',user,'} OK')
    else:
        print(rep.data)
        raise Exception('push reply ERROR')
def text_reply(reply_token,msg="Another One Webhook"):
    this_header = COMMON_HEADER
    this_header['Content-Type'] = 'application/json'
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
                user_id = address['userId']
                img_id = payload['id']
                print("LINE image ID : ",img_id)
                text_reply(token,msg="Searching.... Please Wait")

    return Response(status=200)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=80)