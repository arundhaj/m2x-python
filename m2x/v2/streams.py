from m2x.resource import Collection, Item
from m2x.utils import memoize
from m2x.v2.values import Values


class Stream(Item):
    PATH = 'devices/{device_id}/streams/{name}'

    @property
    @memoize
    def values(self):
        return Values(self.api, device_id=self.device_id,
                      stream_name=self.name)

    def update(self, **attrs):
        out = super(Stream, self).update(**attrs)
        if attrs.get('unit_label'):
            self.data['unit']['label'] = attrs['unit_label']
            self.raw_data['unit']['label'] = attrs['unit_label']
        if attrs.get('unit_symbol'):
            self.data['unit']['symbol'] = attrs['unit_symbol']
            self.raw_data['unit']['symbol'] = attrs['unit_symbol']
        return out


class Streams(Collection):
    PATH = 'devices/{device_id}/streams'
    ITEMS_KEY = 'streams'
    ITEM_CLASS = Stream

    def create(self, name, **attrs):
        url = Stream.PATH.format(device_id=self.device_id, name=name)
        stream = self.item(self.api.put(url, data=attrs))
        self.append(stream)
        return stream

    def details(self, name):
        return self.item(self.api.get(self.item_path(name=name)))

    def item(self, entry):
        return self.ITEM_CLASS(self.api, device_id=self.device_id, **entry)

    def item_path(self, **params):
        return super(Streams, self).item_path(device_id=self.device_id,
                                              **params)