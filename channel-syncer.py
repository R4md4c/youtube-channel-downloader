import argparse

__author__ = 'ramdac'
import yaml
import os

import youtube_dl

from argparse import ArgumentParser
from youtubeapi import YoutubeAPI

ARCHIVE_FILE = 'video_dl.cache'
DEFAULT_CONFIG_FILE = 'config.yaml'
DEFAULT_MAX_VIDEOS_DOWNLOAD = 100


def read_yaml_file(config_file_name):
    if not config_file_name:
        real_file_path = os.path.join(os.path.dirname(__file__), DEFAULT_CONFIG_FILE)
    elif not os.path.isabs(config_file_name):
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
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', help='Specify a custom config.yaml file instead of the default one',
                        default='', dest='config_parameter')
    parser.add_argument('-o', '--output-dir', help='Specify the destination dir that the video will download to',
                        default='', dest='download_dir')
    parser.add_argument('-m', '--max-videos-download',
                        help="Specify the max number of downloads for each user or channel, the downloads are ordered by date",
                        default=DEFAULT_MAX_VIDEOS_DOWNLOAD, dest='max_videos_download', type=int)
    return parser


if __name__ == "__main__":
    parser = setup_parser()
    options = vars(parser.parse_args())

    config_content = read_yaml_file(options['config_parameter'])

    if config_content['API_KEY'] is None:
        raise AttributeError('Missing API_KEY')

    channels_array = config_content['channels'] if 'channels' in config_content else []
    users_array = config_content['users'] if 'users' in config_content else []

    api = YoutubeAPI(config_content['API_KEY'], options['max_videos_download'])
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
        youtubeDL = youtube_dl.YoutubeDL({
            'outtmpl': os.path.join(options['download_dir'], youtube_dl.DEFAULT_OUTTMPL),
            'download_archive': ARCHIVE_FILE,
            # Compute max downloads for all supplied channels and users
            'max_downloads': options['max_videos_download'] * (
            len(channels_array) if len(channels_array) > 0 else 1) * (len(users_array) if len(users_array) > 0 else 1),
            'continuedl': True
        })

        youtubeDL.add_default_info_extractors()

        # Go !
        youtubeDL.download([channel_item.item_youtube_url for channel_item in channel_items_array])

    except KeyboardInterrupt:
        print 'KeyboardInterrupt Event Occurred. Leaving ...'

