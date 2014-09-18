from channelitem import ChannelItem

__author__ = 'ramdac'


class VideoItem(ChannelItem):
    def __init__(self, item_id):
        super(VideoItem, self).__init__(item_id)

    @property
    def item_youtube_url(self):
        return 'https://www.youtube.com/watch?v=%s' % self._id