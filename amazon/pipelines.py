from scrapy.exceptions import DropItem
import json

with open('review.jl', 'r') as json_file:
	json_data = json.load(json_file)

class EmptyItemPipeline(object):

    def process_item(self, item, spider):
        if not item:
            raise DropItem("Missing value in %s" % item)
        else:
            return item


class RepeatedItemPipeline(object):
    	def process_item(self, item, spider):
		data = dict(item)
        	if data in json_data:
            		raise DropItem("Missing value in %s" % item)
        	else:
            		return item
