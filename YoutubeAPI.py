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
        request = self.service.search().list(part='snippet, id', order='date', maxResults=50, channelId=channel_id)
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

    def list_user_content(self, user_name):
        channel_items_array = []
        self._list_user_content(user_name, channel_items_array)
        return channel_items_array

    def _list_user_content(self, user_name, channel_items_array, next_page_token = None):
        request = self.service.search().list(part='id', order='date',
                                             maxResults=50, type='channel', q=user_name, pageToken=next_page_token)
        response = request.execute()

        items = response['items']
        for item_dict in items:
            id_item = item_dict['id']
            if "channel" in id_item['kind']:
                channel_items_array.extend(self.list_channel_content(id_item['channelId']))

        if 'nextPageToken' in response:
            self._list_user_content(user_name, channel_items_array, response['nextPageToken'])




