from google.cloud import firestore
DB = firestore.Client().collection('line_user')
#--- userData stuff
# maybe i should put these in Class for future-development
# but i'm fking lazy to do so
def generate_initial_user_data(user_id):
    try:
        DB.document(user_id).set({
            str('chat'): str("Helper is a friendly,fun AI that know everything about bird."),
            str("is_bot_active"): False,
            str("is_detection_active"): False
        })
        print("{%s} is created!" % user_id)
    except Exception as e:
        print("ERROR at Initial-User-Data")
        print(e)
def delete_user_data(user_id):
    try:
        DB.document(user_id).delete()
        print("{%s} is deleted!" % user_id)
    except Exception as e:
        print("ERROR at Delete-User-Data")
        print(e)
def get_user_bot(user_id):
    try:
        data = DB.document(user_id)
        if data.get().exists:
            return data.get().to_dict().get("is_bot_active")
        else:
            print("data for {%s} not found" % user_id)
    except Exception as e:
        print("ERROR at Set-User-Bot")
        print(e)
def get_user_detect(user_id):
    try:
        data = DB.document(user_id)
        if data.get().exists:
            return data.get().to_dict().get("is_detection_active")
        else:
            print("data for {%s} not found" % user_id)
    except Exception as e:
        print("ERROR at Set-User-Bot")
        print(e)
def get_user_chat(user_id):
    try:
        data = DB.document(user_id)
        if data.get().exists:
            return data.get().to_dict().get("chat")
        else:
            print("data for {%s} not found" % user_id)
    except Exception as e:
        print("ERROR at Set-User-Bot")
        print(e)
def set_user_bot(user_id,set_bot):
    try:
        data = DB.document(user_id)
        if data.get().exists:
            new_data = data.get().to_dict()
            new_data.update({str("is_bot_active"):set_bot})
            data.set(new_data)
        else:
            print("data for {%s} not found" % user_id)
    except Exception as e:
        print("ERROR at Set-User-Bot")
        print(e)
def set_user_detect(user_id,set_detect):
    try:
        data = DB.document(user_id)
        if data.get().exists:
            new_data = data.get().to_dict()
            new_data.update({str("is_detection_active"):set_detect})
            data.set(new_data)
        else:
            print("data for {%s} not found" % user_id)
    except Exception as e:
        print("ERROR at Set-User-Detect")
        print(e)
def set_user_chat(user_id,chat="DEFAULT"):
    try:
        data = DB.document(user_id)
        if data.get().exists:
            if chat == "DEFAULT":
                new_data = data.get().to_dict()
                new_data.update({str("chat"):str("Helper is a friendly,fun AI that know everything about bird.")})
                data.set(new_data)
            else:
                new_data = data.get().to_dict()
                new_data.update({str("chat"):str(chat)})
                data.set(new_data)
        else:
            print("data for {%s} not found" % user_id)
    except Exception as e:
        print("ERROR at Set-User-chat")
        print(e)
