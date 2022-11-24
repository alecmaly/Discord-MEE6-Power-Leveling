import argparse
import uuid
import time 
from datetime import datetime, timezone
import json
from os.path import exists
import itertools
import requests
import random

def NewMessage(channel = "1040745201146273833", msg='test'):
    print(f"\nSending message: {msg}")
    url = f"https://discord.com/api/v9/channels/{channel}/messages"

    guid = str(uuid.uuid4())
    body = {
        "content": msg,
        "nonce": guid[0:15],
        "tts": False
    }

    resp = requests.post(url=url, headers=headers, json=body)
    return resp

def DeleteMessage(channel, msgId):
    url = f"https://discord.com/api/v9/channels/{channel}/messages/{msgId}"
    requests.delete(url=url, headers=headers) 

def GenerateRandomMessage(messages=[]):
    # checks if messages exists, is of type list, and is not empty
    msg = random.choice(messages) if messages and type(messages) == list and len(messages) > 0 else WORDLIST_MSG_DEFAULT
    msg = msg.strip()
    return msg if msg and msg != '' else WORDLIST_MSG_DEFAULT


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        prog = 'Discord MEE6 auto-leveler',
                        description = 'Power levels MEE6 on Discord. Uses browser session API which s',
                        usage="testing usage",
                        epilog = 'Author: https://alecmaly.com')
    parser.add_argument('-c', '--channel_id', required=True, help="Get CHANNEL_ID from the URL of discord in browser: https://discord.com/channels/<SERVER_ID>/<CHANNEL_ID>/...")
    parser.add_argument('-k' '--api_key', required=True, help="Pull from browser session using DevTools, proxy, or other method.")
    parser.add_argument('-mx', '--max-sleep-time', help="Max time to sleep, default = 3600 seconds (1 hr)")

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-w', '--message-wordlist', default='./OneLiners.txt', help="Wordlist of message to randomize.")
    group.add_argument('-m', '--message', help="Message to repeat. A short message such as a period '.' is least intrusive to other users.")

    args = parser.parse_args()

    SLEEP_TIME_SECONDS = 1                                                                      # Default MEE6 xp time
    MAX_SLEEP_TIME_SECONDS = int(args.max_sleep_time) if args.max_sleep_time else 60*60         # 60*60 = 60sec/min * 60min/hr = 1 hr sleep time
    WORDLIST_MSG_DEFAULT = '.'

    print("""\n\n**************STARTING BOT**************""")
    print(args)
    print(f"Channel: {args.channel_id}")
    print(f"Key: {args.k__api_key}")
    print(f"Message: {args.message}")
    print(f"Message wordlist: {args.message_wordlist}")
    print(f"Max sleep time: {args.max_sleep_time}")
    print(f"\n\n")

    headers = {
        'Authorization': args.k__api_key,
        'content-type': 'application/json',
        'accept': 'application/json'
    }

    # load wordlist
    if args.message_wordlist and exists(args.message_wordlist):
        message_wordlist = args.message_wordlist
        messages = [msg.strip() for msg in open(message_wordlist, 'r').readlines()]

    # MAIN LOOP
    for i in itertools.count():
        try:
            msg = args.message if args.message else GenerateRandomMessage(messages=messages)

            resp = NewMessage(channel=args.channel_id, msg=msg)
            resp_data = json.loads(resp.text)
            
            if 'retry-after' in resp.headers:
                print(f"[!] Retry after header found, sleeping for {resp.headers['retry-after']} seconds")
                time.sleep(int(resp.headers['retry-after']))
                continue
            
            if resp.status_code != 200:
                raise Exception("Did not receive 200 response from server, pausing.")
            print(f"{i+1} Messages Sent")

            SLEEP_TIME_SECONDS = 1
            time.sleep(SLEEP_TIME_SECONDS)

            DeleteMessage(channel=args.channel_id, msgId=resp_data['id'])
        except Exception as e:
            print(e)
            print(f"[!] Failed ({datetime.now(timezone.utc).astimezone()}): waiting {SLEEP_TIME_SECONDS} second(s) and trying again...")
            time.sleep(SLEEP_TIME_SECONDS)
            SLEEP_TIME_SECONDS = SLEEP_TIME_SECONDS*2 if SLEEP_TIME_SECONDS*2 < MAX_SLEEP_TIME_SECONDS else MAX_SLEEP_TIME_SECONDS
