
import datetime

def get_msg(id:int):

    # make sure the id points to a real msg
    if id in message_dict:
        msg_info = message_dict[id] # will return {msg : messagestring, open_time : datetime}

        rn = datetime.now()

        if rn >= msg_info["delay"]:
            print(msg_info["msg"])
            return True
        else:
            print ("cannot retrieve your message. The message may not exist or more time may need to pass.")
            return False

    # if the id does not exist in the dictionary, kill the program
    else: 
        raise KeyError("There is no message associated with the ID provided.")



