import scrapy

class AICTEFeedbackSpider(scrapy.Spider):
    name = "aicte_feedback_spider"
    start_urls = ["https://ceconline.edu/aicte-feedback/"]

    def parse(self, response):
        notice_div = response.xpath(
            '//div[contains(@class, "wpb_wrapper")]'
            '/h1[contains(text(), "NOTICE")]'
            '/following-sibling::node()' 
        )
        if notice_div:
            feedback_links = {}
            for sibling in notice_div:
                if sibling.xpath('self::p'): #check if the sibling is a p tag
                    links = sibling.xpath(".//a")
                    for link in links:
                        text = link.xpath(".//text()").get()
                        href = link.xpath("@href").get()
                        if text and href:
                            feedback_links[text.strip()] = href.strip()

            if feedback_links:
                yield {'aicte_feedback_links': feedback_links}
            else:
                self.log("No links found within the AICTE feedback notice.")
        else:
            self.log("Notice div 'NOTICE' not found. Check the XPath.")