# Flickrwall

This script helps you to change automatically your desktop wallpaper using the photos that you have stored in Flickr.
You can specify varios settings in the configuration file, such as rotation time, tags, number of screens and so on.
Note that the script currently works only in Mac OSX.

------------
<h2>Configuration</h2>

The main script read various settings from `config.py` that need to be properly set.
Below the important configuration settings are described. 

<h4>Authentication Settings</h4>

The file `sample-config.py` need to be renamed to `config.py` and then it requires the following settings.
* `key`
* `secret`
* `username`

To get your Flickr key/secret values, visit [Flickr API](https://www.flickr.com/services/api/auth.howto.web.html).

Once you run for the first time Flickrwall, it will help you through your API activation, just follow the prompt in the terminal and then it will store your details in the `auth_file` specified (I would suggest to change the permissions to 600 after its creation). 

<h4>General Settings</h4>

* `time_seconds`, rotation time in seconds of each wallpaper
* `number_of_screens`, the number of screens attached to your computer. Note that the scripts use different methods to communicate with the OSX if you have 1 or multiple screens.
* `photos_folder`, the folder where the photos will be temporary stored

<h4>General Settings</h4>

* `accepted_tags`, list of tags that are used to retrieve photos from your profile
* `min_taken_date` and `max_taken_date` describe the time range from which pick your photos


------------
<h2>Script Execution</h2>

Once you have updated the configuration file you can run the script simply typing 
``` 
python Flickrwall.py
```
A log file will be generated following the name and path specified in the configuration file.


------------
<h2>Notes</h2>

Once the script is running the configuration file can be modified because it will be reloaded at each iteration (after the seconds specified in `time_seconds`).