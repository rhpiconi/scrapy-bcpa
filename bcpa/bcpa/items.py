# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BcpaItem(scrapy.Item):

	site_address = scrapy.Field()
	site_address_link = scrapy.Field()
	property_owner = scrapy.Field()
	mailing_address = scrapy.Field()
	_id = scrapy.Field()
	millage = scrapy.Field()
	use = scrapy.Field()
	abbreviated_legal_description = scrapy.Field()
	url = scrapy.Field()
