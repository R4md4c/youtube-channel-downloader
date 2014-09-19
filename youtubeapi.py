

__author__ = 'ramdac'

from apiclient.discovery import build
from model.playlistitem import PlaylistItem
from model.videoitem import VideoItem

class YoutubeAPI(object):
    def __init__(self, api_key, max_videos_download):
        self.service = build('youtube', 'v3', developerKey=api_key)
        self.max_videos_download = max_videos_download

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
            if self._array_reached_max(channel_items_array):
                break
            if "playlist" in id_item['kind']:
                channel_items_array.append(PlaylistItem(id_item['playlistId']))
            elif "video" in id_item['kind']:
                channel_items_array.append(VideoItem(id_item['videoId']))

        return channel_items_array

    def list_user_content(self, user_name):
        channel_items_array = []
        self._list_user_content(user_name, channel_items_array)
        return channel_items_array

    def _list_user_content(self, user_name, channel_items_array, next_page_token=None):
        if self._array_reached_max(channel_items_array):
            return

        request = self.service.search().list(part='id', order='date',
                                             maxResults=50, type='channel', q=user_name, pageToken=next_page_token)

        response = request.execute()

        items = response['items']
        for item_dict in items:
            id_item = item_dict['id']
            if self._array_reached_max(channel_items_array):
                break
            if "channel" in id_item['kind']:
                channel_contents = self.list_channel_content(id_item['channelId'])
                if len(channel_contents) + len(channel_items_array) <= self.max_videos_download:
                    channel_items_array.extend(channel_contents)

        if 'nextPageToken' in response and len(channel_items_array) < self.max_videos_download:
            self._list_user_content(user_name, channel_items_array, response['nextPageToken'])

    def _array_reached_max(self, array):
        return len(array) >= self.max_videos_download




