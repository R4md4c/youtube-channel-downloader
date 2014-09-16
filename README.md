# Youtube Channel Syncer
Used to sync a list of users or individual youtube channels that are read from config.yaml file.


## Dependencies
 * [PyYaml] (http://pyyaml.org/wiki/PyYAML)
 * [youtube-dl] (https://github.com/rg3/youtube-dl/)
 * [google-api-python-client] (https://developers.google.com/api-client-library/python/)
  

## Usage
 Replace the API_KEY with your [own](https://developers.google.com/youtube/v3/getting-started#before-you-start) then add the channel or user IDs that you wish to download inside the config.yaml file, finally execute `python2.7 channel-syncer.py`

## Limitations
 Since this is the first version of the script, so I am sorry to tell that it 
 does not track the downloaded videos or playlists, in other words if the syncing failed or stopped you will have to start all over again.