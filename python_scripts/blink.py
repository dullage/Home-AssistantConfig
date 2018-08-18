from requests import get, post
from json import dumps as json_dumps
from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import sleep
from yaml import load as yaml_load, YAMLError

########### USER VARIABLES ###########

videoSavePath = "/config/www"
secretsFileLocation = "/config"

goBackMinutes = 1 # Videos created before this many minutes ago will be ignored
waitTimeoutSeconds = 15 # How long to wait for a video before giving up
timeOffsetHours = 1 # Blinks datetimes were offset by an hour

notifyEntityNames = ["ios_adams_iphone", "ios_leannes_iphone"]
#notifyEntityNames = ["ios_adams_iphone"]

"""
This script also relises on the following entries in the secrets.yaml file.

blinkHassApiBaseURL e.g. "https://www.myhass.com"
blinkHassApiPassword
blinkUsername
blinkPassword
"""

######################################

# Load secrets
with open("{0}/secrets.yaml".format(secretsFileLocation), 'r') as secretsFile:
    try:
        secret = yaml_load(secretsFile)
    except YAMLError as exc:
        print(exc)

# Get an authentication token from Blink
endpoint = "https://rest.prod.immedia-semi.com/login"

headers = {
	"Host":"prod.immedia-semi.com",
	"Content-Type":"application/json"
}

data = {
	"email":secret["blinkUsername"],
	"password":secret["blinkPassword"], 
	"client_specifier":"iPhone 9.2 | 2.2 | 222"
}

response = post(endpoint, headers = headers, data = json_dumps(data))
token = response.json()["authtoken"]["authtoken"]

# We need to grab the last video but only if it was created recently (goBackMinutes) as the camera may not have finished yet. Grab the current time help with this.
start = datetime.today()

# Instantiate a latestVideoTimestamp variable with a very old date.
#latestVideoTimestamp = datetime.utcfromtimestamp(0)

# Keep refreshing the video list until we have a video from the last minute.
while True:
	# Get a list of videos, assume page 0 has the most recent. Convert the JSON response to a dict.
	responseData = get("https://rest-prde.immedia-semi.com/api/v2/videos/page/0", headers = {"Host":"prod.immedia-semi.com", "TOKEN_AUTH":token}).json()
	
	# Assume the first video in the list is the latest. Grab the created datetime.
	latestVideoTimestamp = datetime.utcfromtimestamp(0)
	for video in responseData:
		videoTimestamp = datetime.strptime(video["created_at"], "%Y-%m-%dT%H:%M:%S+00:00") + relativedelta(hours = timeOffsetHours)
		
		if videoTimestamp > latestVideoTimestamp:
			latestVideoTimestamp = videoTimestamp
			latestVideoUrl = video["address"]
	
	# Check to see if it's recent.
	if latestVideoTimestamp > (start - relativedelta(minutes = goBackMinutes)):
		# It's recent, continue.
		elapsedTime = abs(datetime.today() - start).total_seconds()
		break
	else:
		# It's old.
		# If we've been looping longer than the waitTimeoutSeconds, break.
		if datetime.today() > (start + relativedelta(seconds = waitTimeoutSeconds)):
			latestVideoUrl = None
			elapsedTime = "N/A"
			break
		else:
			# Loop. Wait a second so that we're not spamming the API too quickly.
			sleep(1)

# If we have a video send it.
# Message currently includes an elapsedTime for debugging.
if latestVideoUrl != None:
	# Download the video.
	response = get("https://rest-prde.immedia-semi.com{0}".format(latestVideoUrl), headers = {"Host":"prod.immedia-semi.com", "TOKEN_AUTH":token})

	# Save it to disk.
	f = open("{0}/BlinkVideo.mp4".format(videoSavePath), 'wb')
	f.write(response.content)
	f.close()
	
	# Send the iOS notification
	headers = {
		'content-type':'application/json',
		'X-HA-Access':secret["blinkHassApiPassword"]
	}
	
	data = {
		"message": "Doorbell! ({0}s)".format(elapsedTime),
		"data": {
			"attachment": {
				"url": "{0}/local/BlinkVideo.mp4".format(secret["blinkHassApiBaseURL"]),
				"content-type": "mp4"
			}
		}
	}
	
	for entityName in notifyEntityNames:
		post('{0}/api/services/notify/{1}'.format(secret["blinkHassApiBaseURL"], entityName), headers = headers, data = json_dumps(data))

# If we don't have a video, just send a message.
# Message currently includes an elapsedTime for debugging.
else:
	headers = {
		'content-type':'application/json',
		'X-HA-Access':secret["blinkHassApiPassword"]
	}
	
	data = {
		"message": "Doorbell! ({0}s)".format(elapsedTime)
	}
	
	for entityName in notifyEntityNames:
		post('{0}/api/services/notify/{1}'.format(secret["blinkHassApiBaseURL"], entityName), headers = headers, data = json_dumps(data))