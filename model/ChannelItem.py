__author__ = 'ramdac'


class ChannelItem(object):
    def __init__(self, item_id):
        self._id = item_id

    @property
    def item_youtube_url(self):
        return ''

    @property
    def item_id(self):
        return self._id
