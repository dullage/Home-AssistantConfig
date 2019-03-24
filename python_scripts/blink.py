from requests import get, post
from json import dumps as json_dumps
from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import sleep
from yaml import load as yaml_load, YAMLError
from os import system

########### USER VARIABLES ###########

videoSavePath = "/config/www"
secretsFileLocation = "/config"

goBackMinutes = 1 # Videos created before this many minutes ago will be ignored
waitTimeoutSeconds = 60 # How long to wait for a video before giving up

notifyEntityNames = ["ios_adams_iphone", "ios_leannes_iphone"]
# notifyEntityNames = ["ios_adams_iphone"]

"""
This script also relises on the following entries in the secrets.yaml file.

blinkHassApiBaseURL - e.g. "https://www.myhass.com:8123"
blinkHassApiToken - a Home Assistant long live access token.
blinkUsername - Your Blink username
blinkPassword - Your blink password
"""

######################################

# Load secrets
with open("{0}/secrets.yaml".format(secretsFileLocation), "r") as secretsFile:
    try:
        secret = yaml_load(secretsFile)
    except YAMLError as exc:
        print(exc)

# Get an authentication token from Blink
endpoint = "https://rest-prod.immedia-semi.com/login"

headers = {
    "Host": "prod.immedia-semi.com",
    "Content-Type": "application/json"
}

data = {
    "email": secret["blinkUsername"],
    "password": secret["blinkPassword"], 
    "client_specifier": "iPhone 9.2 | 2.2 | 222"
}

response = post(endpoint, headers=headers, data=json_dumps(data))
token = response.json()["authtoken"]["authtoken"]

# We need to grab the last video but only if it was created recently (goBackMinutes) as the camera may not have finished yet. Grab the current time help with this.
start = datetime.today()
since = (start - relativedelta(minutes=goBackMinutes)).strftime("%Y-%m-%dT%H:%M:%S+00:00")

# Keep refreshing the video list until we have a video from the last minute.
while True:

    # Get a list of videos, assume page 0 has the most recent. Convert the JSON response to a dict.
    responseData = get(
        "https://rest-prde.immedia-semi.com/api/v2/videos/changed?since={0}&page=1".format(since),
        headers={"Host": "rest-prde.immedia-semi.com", "TOKEN-AUTH": token}
    ).json()

    videos = responseData["videos"]

    if len(videos) >= 1:
        latestVideoUrl = videos[0]["address"]
        break
    else:
        if datetime.today() > (start + relativedelta(seconds=waitTimeoutSeconds)):
            latestVideoUrl = None
            elapsedTime = "N/A"
            break
        else:
            # Loop. Wait a second so that we"re not spamming the API too quickly.
            sleep(1)

# If we have a video send it.
if latestVideoUrl is not None:
    # Download the video.
    response = get(
        "https://rest-prde.immedia-semi.com{0}".format(latestVideoUrl),
        headers={"Host": "prod.immedia-semi.com", "TOKEN_AUTH": token}
    )

    # Save it to disk.
    f = open("{0}/BlinkVideo.mp4".format(videoSavePath), "wb")
    f.write(response.content)
    f.close()

    # Extract a still image from the frame at 4s and save that to disk
    system("ffmpeg -y -ss 00:00:04 -i {0}/BlinkVideo.mp4 -vf 'crop=720:720:280:0' -vframes 1 -vcodec png {0}/BlinkImage.png".format(videoSavePath))

    # Send the iOS notification
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer {0}".format(secret['blinkHassApiToken'])
    }

    data = {
        "message": "Doorbell!",
        "data": {
            "attachment": {
                "url": "{0}/local/BlinkVideo.mp4?1=1".format(secret['blinkHassApiBaseURL']),
                "content-type": "mp4"
            }
        }
    }

    for entityName in notifyEntityNames:
        post(
            "{0}/api/services/notify/{1}".format(secret['blinkHassApiBaseURL'], entityName),
            headers=headers,
            data=json_dumps(data)
        )

# If we don"t have a video, just send a message.
else:
    headers = {
        "content-type": "application/json",
        "Authorization": "Bearer {0}".format(secret['blinkHassApiToken'])
    }

    data = {
        "message": "Doorbell!"
    }

    for entityName in notifyEntityNames:
        post(
            "{0}/api/services/notify/{1}".format(secret['blinkHassApiBaseURL'], entityName),
            headers=headers,
            data=json_dumps(data)
        )
