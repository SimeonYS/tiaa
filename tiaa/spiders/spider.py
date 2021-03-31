import scrapy
from scrapy.loader import ItemLoader
from ..items import TiaaItem
from itemloaders.processors import TakeFirst
import json
from w3lib.html import remove_tags

class TiaaSpider(scrapy.Spider):
	name = 'tiaa'
	start_urls = ['https://www.tiaabank.com/public/services/newsarticle?pageSize=0&page=1']

	def parse(self, response):

		data = json.loads(response.text)
		for index in range(len(data['data'])):
			date = data['data'][index]['name']
			title = data['data'][index]['title']
			content = remove_tags(data['data'][index]['article']).strip().replace('\n','')

			item = ItemLoader(item=TiaaItem(), response=response)
			item.default_output_processor = TakeFirst()

			item.add_value('title', title)
			item.add_value('link', response.url)
			item.add_value('content', content)
			item.add_value('date', date)

			yield item.load_item()
