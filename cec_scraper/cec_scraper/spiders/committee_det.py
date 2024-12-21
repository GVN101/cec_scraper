import scrapy

class CommitteeSpider(scrapy.Spider):
    name = "committee_spider"
    start_urls = ["https://ceconline.edu/about/committees/rti/"]

    def parse(self, response):
        committees_xpath = response.xpath(
            '//div[contains(@class, "vc_column-inner")]'
            '/div[contains(@class, "wpb_wrapper")]'
            '/div[contains(@class, "wpb_text_column") and contains(@class, "wpb_content_element")]'
        )

        committee_details = []
        for committee_section in committees_xpath:
            committee_title = committee_section.xpath(".//h3/strong/text()").get().strip()
            if committee_title:
                details = {"name": committee_title, "officers": []} 
                officer_info = committee_section.xpath(".//p")
                for officer in officer_info:
                    text_parts = officer.xpath(".//span/text()").getall() 
                    if text_parts:
                        name = text_parts[0].strip()
                        designation = text_parts[1].strip() if len(text_parts)>1 else None
                        contact= None
                        if officer.xpath('.//a/@href').get():
                            contact = officer.xpath('.//a/@href').get()
                        details["officers"].append({
                            "name": name,
                            "designation": designation,
                            "contact": contact,
                        })

                committee_details.append(details)

        if committee_details:
            yield {"committee_details": committee_details}
        else:
            self.log("No committee sections found. Check the XPath.")