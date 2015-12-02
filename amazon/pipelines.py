from scrapy.exceptions import DropItem
import json

class EmptyItemPipeline(object):

    def process_item(self, item, spider):
        if not item:
            raise DropItem("Missing value in %s" % item)
        else:
            return item


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
