import scrapy

class AntiRaggingSpider(scrapy.Spider):
    name = "antiragging_spider"
    start_urls = ["https://ceconline.edu/about/committees/anti_ragging/"]

    def parse(self, response):
        # More robust XPath using contains()
        antiragging_section = response.xpath(
            '//div[contains(@class, "wpb_text_column") and contains(@class, "wpb_content_element") and contains(@class,"vc_custom_")]'
        )

        if antiragging_section:
            details = {}
            functions = []
            for li in antiragging_section.xpath('.//ul/li'):
                function_text = li.xpath('.//text()').get("").strip()
                if function_text:
                    functions.append(function_text)
            if functions:
                details["functions"] = functions
                yield {"details_about_anti_ragging_cell": details}
            else:
                self.log("No functions found within the anti-ragging section.")
        else:
            self.log("Anti-ragging section not found. Check the XPath.")