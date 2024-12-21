# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CecScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

from scrapy.item import Item, Field

class AdmissionItem(Item):
    file_urls = Field()
    files = Field()
    candidate_details_link = Field()
    original_certificates_link = Field()
    admission_schedule_link = Field()
    candidate_details_text = Field()
    original_certificates_text = Field()
    admission_schedule_text = Field()
