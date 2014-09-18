# Youtube Channel Syncer
Used to sync a list of users or individual youtube channels that are read from config.yaml file.


## Dependencies
 * [PyYaml] (http://pyyaml.org/wiki/PyYAML)
 * [youtube-dl] (https://github.com/rg3/youtube-dl/)
 * [google-api-python-client] (https://developers.google.com/api-client-library/python/)
  

## Usage
 Firstly, Replace the API_KEY with your [own](https://developers.google.com/youtube/v3/getting-started#before-you-start) (or you can follow these instructions in [this](https://github.com/R4md4c/youtube-channel-syncer/wiki/Steps-to-generate-an-API-key-for-the-Youtube-API) wiki page).  
 Secondly, Add the channel or user IDs that you wish to download inside the config.yaml file.  
 Finally, Execute the script using `python2.7 channel-syncer.py`  


## Options
    -h, --help            show this help message and exit
    -c CONFIG_PARAMETER, --config CONFIG_PARAMETER Specify a custom config.yaml file instead of the default one
    -o DOWNLOAD_DIR, --output-dir DOWNLOAD_DIR Specify the destination dir that the video will download to