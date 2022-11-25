# About 

This is a bot to farm MEE6 Discord levels. Please use responsibly, only on spam channels, and do not disrupt other members. 
Respects retry-after response header and backs off requests on failures. Number of requests in default configuration range from 1/s-1/hr.

This project would have probably worked better as a Chrome Extension for Desktop users, however, I don't use Discord often so I created a Python script to run on my Ubuntu VPS. 

Author: [https://alecmaly.com](https://alecmaly.com)


# Install

> <span style='color:indianred; font-weight: bold'>NOTE</span>: You may need to replace 'python' for 'python3'
```bash
# setup python virtual environment
python -m venv venv
./venv/Scripts/activate

pip install -r requirements.txt
```

# Example Usage

```bash
# run against CHANNEL (c) with API_KEY (k)
python ./DiscordMEE6Leveler.py -c 1140732401136273833 -k "XtOi3NS0WtIgXjW4YDAfYDS4.Q7DaQh.UvWZJLODR_Lf6fSmcK5FffqJ2C2_HLC6YTpabc"

# run against CHANNEL (c) with API_KEY (k): MESSAGE (m) = '.'
python ./DiscordMEE6Leveler.py -c 1140732401136273833 -k "XtOi3NS0WtIgXjW4YDAfYDS4.Q7DaQh.UvWZJLODR_Lf6fSmcK5FffqJ2C2_HLC6YTpabc" -m "."

# view help
python ./DiscordMEE6Leveler.py -h
```

## Usage Tips & Tricks: 

(Ubuntu) Detach Process: bot process continues when the terminal is closed. Running with this command allows you to kill your remote session and the bot will persist.

Execute using `nohup` cmd and a trailing `&`.
```bash
nohup python ./DiscordMEE6Leveler.py -c 1140732401136273833 -k "XtOi3NS0WtIgXjW4YDAfYDS4.Q7DaQh.UvWZJLODR_Lf6fSmcK5FffqJ2C2_HLC6YTpabc" &
```

**Note**: This leaves a process running in the background. To kill it you must find & kill the process

```bash
# Step 1: find process PID
sudo ps aux | grep -i -e PID -e DiscordMEE6Leveler --color=none

# Step 2: kill process by PID
sudo kill -9 <PID>
```

# Notes: 
- Jokes pulled from https://raw.githubusercontent.com/daronspence/One-Liners/master/jokes.txt
    - I have not read them all.