import scrapy

class CollegeInfoSpider(scrapy.Spider):
    name = "college_info_spider"
    start_urls = ["https://ceconline.edu/contact-us/"]

    def parse(self, response):
        contact_items = response.xpath('//div[contains(@class, "stm-map__content")]//ul[@class="stm-contact-details__items"]/li')
        contacts = {}
        for item in contact_items:
            detail_text = item.xpath('.//text()').get().strip()
            detail_type = item.xpath('@class').get()
            if detail_type:
                detail_type = detail_type.split("_")[-1]
                contacts[detail_type] = detail_text
            else:
                pass  

        location_section = response.xpath('//div[contains(@class, "entry-content")]//div[@class="wpb_wrapper"]')
        if location_section:
            location_details = {}
            main_description = location_section.xpath('./p[1]/text()').get("").strip()
            if main_description:
                location_details["main_description"] = main_description

            transit_details = {}
            transit_paragraphs = location_section.xpath('./p[position() > 1]')
            for p in transit_paragraphs:
                strong_text = p.xpath('./strong/text()').get("").strip()
                if strong_text:
                    rest_of_text = "".join(p.xpath('./text()[not(ancestor::strong)]').getall()).strip()
                    transit_details[strong_text.replace(":", "").strip()] = rest_of_text.strip()
            if transit_details:
                location_details["transit_distances"] = transit_details

        google_maps_info = {}
        google_maps_card = response.xpath('//div[contains(@class, "place-card") and contains(@jsaction, "placeCard.directions")]')

        if google_maps_card:
            google_maps_info = {}
            link = google_maps_card.xpath('.//a[contains(@class, "navigate-link")]/@href').get()
            if link:

                google_maps_info["college_name"] = link.split("+")[0].replace("College+of+Engineering+", "").strip()

        yield {
            "contact_details": contacts,
            "location_details": location_details,
            "google_maps_info": google_maps_info if google_maps_info else None  
        }
         