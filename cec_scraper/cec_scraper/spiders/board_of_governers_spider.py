import scrapy

class BoardOfGovernorsSpider(scrapy.Spider):
    name = "bog"
    start_urls = ['https://ceconline.edu/board-of-governors/']
    
    def parse(self, response):
        table = response.xpath('//div[@class="wpb_wrapper"]//table[contains(., "Board of Governors")]')
        rows = table.xpath('.//tr[td]') 

        for row in rows:
            # sl_no = row.xpath('td[1]/strong/text()').get()
            name_designation = row.xpath('td[2]/strong/text()').get()
            designation = row.xpath('td[3]/strong/text()').get()
            role = row.xpath('td[4]/strong/text()').get()
            if  name_designation and designation:
                yield {
                    # 'Sl.No': sl_no.strip(),
                    'Name and Designation': name_designation.strip(),
                    'Designation': designation.strip(),
                    'Role': role.strip() if role else '',
                }
