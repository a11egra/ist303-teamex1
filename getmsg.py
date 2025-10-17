# Team Kalos, problem 3.1
# Allegra's task: implement send_msg

import datetime

def get_msg(id:int):
    '''
    Finds message info based on message ID.
    Checks if current time meets the wait time criteria for the message.
    Returns message and True if the wait time is fulfilled, else returns
       error message and False.
    '''

    # make sure the id points to a real msg
    if id in message_dict:
        msg_info = message_dict[id] # will return {msg : messagestring, unlock_time : datetime}

        rn = datetime.now()

        if rn >= msg_info["unlock_time"]:
            print(msg_info["msg"])
            return True
        else:
            print ("cannot retrieve your message. The message may not exist or more time may need to pass.")
            return False

    # if the id does not exist in the dictionary, kill the program
    else: 
        raise KeyError("There is no message associated with the ID provided.")