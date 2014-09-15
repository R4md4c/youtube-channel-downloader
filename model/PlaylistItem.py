from model.ChannelItem import ChannelItem

__author__ = 'ramdac'


class PlaylistItem(ChannelItem):
    def __init__(self, item_id):
        super(PlaylistItem, self).__init__(item_id)

    @property
    def item_youtube_url(self):
        return 'https://www.youtube.com/playlist?list=%s' % self._id
