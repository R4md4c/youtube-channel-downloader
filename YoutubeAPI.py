from model import PlaylistItem

__author__ = 'ramdac'

from apiclient.discovery import build
from model.PlaylistItem import PlaylistItem
from model.VideoItem import VideoItem


class YoutubeAPI(object):
    def __init__(self, api_key):
        self.service = build('youtube', 'v3', developerKey=api_key)

    def list_channel_content(self, channel_id):
        """
        Uses the Youtube Data API to search for a channel using the channel id and returns a list of
        ChannelItem models
        :param channel_id: the channel_id to search for
        :return: a list of either VideoItem model or PlaylistItem according to the 'kind' attribute of the 'id' object
        """
        request = self.service.search().list(part='snippet, id', order='date', maxResults=20, channelId=channel_id)
        response = request.execute()
        items = response['items']
        channel_items_array = []
        for item_dict in items:
            id_item = item_dict['id']
            if "playlist" in id_item['kind']:
                channel_items_array.append(PlaylistItem(id_item['playlistId']))
            elif "video" in id_item['kind']:
                channel_items_array.append(VideoItem(id_item['videoId']))

        return channel_items_array