# Adiyas job: create send_msg (and the shared dict)

import random
import time

# Shared storage for ALL messages (ID -> data)
message_dict = {}

def send_msg(msg: str, delay: int, units: str):
    """
    Store a message that unlocks after a time delay.

    Args:
        msg (str): the message text
        delay (int): length of the delay
        units (str): one of "seconds", "minutes", "hours"

    Returns:
        int: the randomly generated 6-digit message ID

    Raises:
        Exception: for invalid 'delay' type or invalid 'units' values
    """
    # 1) validate
    if not isinstance(delay, int):
        raise Exception("Delay must be an integer.")
    if units not in ("seconds", "minutes", "hours"):
        raise Exception("Units must be 'seconds', 'minutes', or 'hours'.")

    # 2) convert the delay into sec
    delay_in_seconds = delay
    if units == "minutes":
        delay_in_seconds = delay * 60
    elif units == "hours":
        delay_in_seconds = delay * 3600

    # 3) make random 6-digit id
    msg_id = random.randint(100000, 999999)

    # 4) figure out unlock time 
    unlock_time = time.time() + delay_in_seconds

    # 5) store in global dictionary
    message_dict[msg_id] = {
        "message": msg,
        "unlock_time": unlock_time
    }
    # 6) print and return ID
    print(msg_id)
    return msg_id

# ---- local quick test (run: python3 problem3_code.py) ----
if __name__ == "__main__":
    test_id = send_msg("hey hey from kalos", 3, "seconds")
    print("Stored:", test_id)
