__author__ = 'ramdac'
import yaml

from YoutubeAPI import YoutubeAPI
import youtube_dl


def read_yaml_file(file):
    stream = open(file, 'r')
    return yaml.load(stream)


if __name__ == "__main__":
    config_content = read_yaml_file('config.yaml')
    if config_content['API_KEY'] is None:
        raise AttributeError('Missing API_KEY')
    if config_content['channels'] is None or not isinstance(config_content['channels'], list):
        raise AttributeError('No Channel Array is Found')

    api = YoutubeAPI(config_content['API_KEY'])
    channel_items_array = []
    for channel in config_content['channels']:
        channel_items_array.extend(api.list_channel_content(channel))

    # Init the youtube_dl main object to begin download
    youtubeDL = youtube_dl.YoutubeDL()
    youtubeDL.add_default_info_extractors()
    # Go !
    youtubeDL.download([channel_item.item_youtube_url for channel_item in channel_items_array])

