import scrapy

class InternalQualityAssuranceSpider(scrapy.Spider):
    name = "iqac_spider"
    start_urls = ["https://ceconline.edu/about/committees/internal-quality-assurance-cell-or-internal-audit-cell-iqac-iac/#1608789190414-66d69914-5d08"]

    def parse(self, response):
        # Extremely specific XPath using multiple conditions and text content
        iqac_div = response.xpath(
            '//div[contains(@class, "wpb_text_column") and contains(@class, "wpb_content_element")]'
            '/div[contains(@class, "wpb_wrapper")]'
            '/h2/strong[contains(text(), "Internal Quality Assurance Cell")]/ancestor::div[contains(@class,"wpb_wrapper")]' #go to the parent div
        )

        if iqac_div:
           
            text_content = iqac_div.xpath('.//p/text()').get()
            if text_content:
                yield {'iqac_description': text_content.strip()}
            else:
                self.log("No <p> tag or text content found within the IQAC div.")
        else:
            self.log("IQAC div not found. Check the XPath.")