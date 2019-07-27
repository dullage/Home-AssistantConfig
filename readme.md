# My Setup
I currently run [Home Assistant](http://homeassistant.io/) version 0.94.3 in a docker container on a Raspberry Pi 3. Details of my docker setup can be found in the [docker folder](https://github.com/Dullage/Home-AssistantConfig/tree/master/docker).

Currently there is very little in terms of in-configuration comments but if anyone has any questions I'm happy to answer.

# Presence Detection
I use 2 platforms for presence detection with a good success rate:

1. [Home Assistant iOS App](https://www.home-assistant.io/docs/ecosystem/ios/)
2. [Ubiquiti Wifi](https://www.home-assistant.io/components/device_tracker.unifi/)

The Ubiquiti tracking is slow to see you leave so I don't use it in the person groups, instead I just have an automation that steps in on the odd occasion the Home Assistant app fails to see us arrive (or is just slow). See [locationCleanup.yaml](https://github.com/Dullage/Home-AssistantConfig/blob/master/automations/locationCleanup.yaml).

# Highlights
Some highlights of our setup in no particular order:

* Google Home Minis / Google Home Hub for voice control and voice notifications (Google Cast) in most areas of the house.
* Chromecast Audios for whole house audio.
* Most house lights controllable via Home Assistant (a mix of Hue, Sonoff and WS2812 LED strips).
* Nest Thermostat.
* Broadlink RM Mini IR blaster for AV control.
* Motion detection for some lighting effects (Xiaomi Motion Sensors).
* The heating turns itself off as we go to bed ([bedtime.yaml](/automations/bedtime.yaml)).
* All lights turn off if everyone leaves the house. Lights turn on (at night) when someone comes home ([locationLights.yaml](/automations/locationLights.yaml)).
* ESP8266 controlled ceiling lights (see [this forum post](https://community.home-assistant.io/t/esp8266-sonoff-controlled-ceiling-lights/24141)).
* Double toggle a wall switch to perform a special function e.g. turn off every light on that floor (see [this repo](https://github.com/Dullage/SwitchedSonoffSimple) and [switchDoubleToggles.yaml](/automations/switchDoubleToggles.yaml)).
* iOS notifications when the doorbell is pressed ([doorbell.yaml](/automations/doorbell.yaml)). These include a video of the person walking up the path (see [this forum post](https://community.home-assistant.io/t/blink-camera-as-video-doorbell/65844)).
* iOS notifications if we both leave the house but a door or window is left open ([locationDoorWarning.yaml](/automations/locationDoorWarning.yaml)).
* Wall mounted Amazon Fire Tablet to display HADashboard.
* Smart Microwave! See [this forum post](https://community.home-assistant.io/t/making-my-microwave-smart-ish/89843) and [this automation](/automations/microwave.yaml).
* Google Assistant integrated with the Shopping List via IFTTT so I can say "Hey Google, add beer to my shopping list".
* iOS notification to send me the shopping list when I go near a local supermarket. Follow-up notification when I leave the supermarket offering to clear the shopping list.

# Entity Counts
| Type             | Count                          |
| ---------------- | ------------------------------ |
| Automations      | 103     |
| Binary Sensors   | 22  |
| Cameras          | 5         |
| Climate Controls | 1        |
| Device Trackers  | 8 |
| Groups           | 15          |
| Input Booleans   | 8  |
| Input Numbers    | 7   |
| Input Selects    | 5   |
| Input Text       | 2     |
| Lights           | 17          |
| Media Players    | 11   |
| Scenes           | 7          |
| Scripts          | 39         |
| Sensors          | 61         |
| Switches         | 2         |

# Screenshots
Here are some screenshots from the front end and HA Dashboard:

## Main Tab
![Main Tab](docs/main_tab.png)

## Climate Tab
![Climate Tab](docs/climate_tab.png)

## AV Tab
![AV Tab](docs/av_tab.png)

## Miscellaneous Tab
![Miscellaneous Tab](docs/miscellaneous_tab.png)

## Camera Tab
![Camera Tab](docs/camera_tab.png)

## Admin Tab
![Admin Tab](docs/admin_tab.png)

## HADashboard
![HADashboard](docs/hadashboard.png)