import scrapy

class FacilitiesSpider(scrapy.Spider):
    name = "facilities_spider"
    start_urls = ["https://ceconline.edu/about/facilities/"]

    def parse(self, response):
        # Target the paragraph directly and extract text
        facility_description = response.xpath('//h2[text()="Facilities"]/following-sibling::div//p/text()').get()
        if facility_description:
            yield {"facility_description": facility_description.strip()}
        else:
            self.log("Facility description not found.")