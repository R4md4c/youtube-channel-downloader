__author__ = 'ramdac'
import yaml
import os

import youtube_dl

from optparse import OptionParser
from youtubeapi import YoutubeAPI


def read_yaml_file(config_file_name):
    if not os.path.isabs(config_file_name):
        real_file_path = os.path.join(os.getcwd(), config_file_name)
    else:
        real_file_path = config_file_name

    try:
        stream = open(real_file_path, 'r')
        return yaml.load(stream)
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, 'Cannot file config.yaml')
        exit()


def setup_parser():
    usage = "usage: %prog [option] arg1"
    parser = OptionParser(usage=usage)
    parser.add_option('-c', '--config', help='Specify a custom config.yaml file instead of the default one', dest='config_path')
    return parser

if __name__ == "__main__":
    parser = setup_parser()
    (options, args) = parser.parse_args()
    if options.config_path is not None:
        file_path = options.config_path
    else:
        file_path = 'config.yaml'

    config_content = read_yaml_file(file_path)
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

