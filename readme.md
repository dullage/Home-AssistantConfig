# My Setup
I run [Home Assistant](http://homeassistant.io/) in a docker contatiner on a Raspberry Pi 3. Details of my docker setup can be found in the docker folder.

Currently there is very little in terms of in-configuration comments but if anyone has any questions I'm happy to answer.

# Presence Detection
After a lot of trial and error I have found the following setup works very well for me with little lag or error rate.

I use 3 platforms for presence detection:

1. [Locative iOS App](https://www.home-assistant.io/components/device_tracker.locative/)
2. [Home Assistant iOS App](https://www.home-assistant.io/docs/ecosystem/ios/)
3. [Ubiquiti Wifi](https://www.home-assistant.io/components/device_tracker.unifi/)

I use the 3 platforms with the following logic:

* For each household member the Locative and the Home Assistant iOS App devices are combined into a group. This group is what I use to trigger automations etc.
* If either of the app devices changes to "away" an automation will also set the other device to "away" so that the group is also changed to "away". _Note: I don't need to do the same for a change to "home" as only 1 device in the group needs to show as "home" for the group to show as "home"._
* If the Unifi device changes to "home" an automation sets both of the app devices as "home" (thus also changing the group to "home"). This is the only way I use the Unifi device tracker as the change to "away" is both slow and un-reliable.

The logic for the automations mentioned above can be found in the automation file [locationCleanup.yaml](https://github.com/Dullage/Home-AssistantConfig/blob/master/automations/locationCleanup.yaml).

# Screenshots
Here are some screenshots from the front end:

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
