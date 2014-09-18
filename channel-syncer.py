__author__ = 'ramdac'
import yaml
import os

from youtubeapi import YoutubeAPI
import youtube_dl


def read_yaml_file(config_file_name):
    current_script_dir = os.path.dirname(os.path.realpath(__file__))
    real_file_path = os.path.join(current_script_dir, config_file_name)
    stream = open(real_file_path, 'r')
    return yaml.load(stream)


if __name__ == "__main__":

    config_content = read_yaml_file('config.yaml')
    if config_content['API_KEY'] is None:
        raise AttributeError('Missing API_KEY')


    channels_array = config_content['channels'] if 'channels' in config_content else []
    users_array = config_content['users'] if 'users' in config_content else []

    api = YoutubeAPI(config_content['API_KEY'])
    channel_items_array = []

    try:
        # Collect Channel Items using Channel IDs
        for channel in channels_array:
            channel_item_array = api.list_channel_content(channel)
            print 'Found %s Channel Items Under Channel \'%s\'' % (len(channel_item_array), channel)
            channel_items_array.extend(channel_item_array)

        # Collect Channel Items Using User ID
        for user in users_array:
            user_channel_array = api.list_user_content(user)
            print 'Found %s Channel Items Under User \'%s\'' % (len(user_channel_array), user)
            channel_items_array.extend(user_channel_array)

        # Init the youtube_dl main object to begin download
        youtubeDL = youtube_dl.YoutubeDL()
        youtubeDL.add_default_info_extractors()
        # Go !
        youtubeDL.download([channel_item.item_youtube_url for channel_item in channel_items_array])

    except KeyboardInterrupt:
        print 'KeyboardInterrupt Event Occurred. Leaving ...'

