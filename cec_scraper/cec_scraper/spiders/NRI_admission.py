import scrapy
from ..items import AdmissionItem
from urllib.parse import urljoin

class AdmissionSpider(scrapy.Spider):
    name = 'nri_admission_spider'
    start_urls = [
        'https://ceconline.edu/b-tech-nri-admission-2024-25/'  # Replace with the actual URL
    ]
    
    def parse(self, response):
        # Using specific data-id attributes to target exact elements
        admission_links = {
            "candidate_details": "//div[@data-id='db33835']//a/@href",
            "original_certificates": "//div[@data-id='7e372bc']//a/@href",
            "admission_schedule": "//div[@data-id='cd4f4f3']//a/@href"
        }
        
        # Get all PDF links
        pdf_links = []
        for key in admission_links:
            link = response.xpath(admission_links[key]).get()
            if link:
                # Convert relative URLs to absolute URLs
                absolute_url = urljoin(response.url, link)
                pdf_links.append(absolute_url)
        
        item = AdmissionItem()
        item['file_urls'] = pdf_links  # FilesPipeline will use this field
        
        # Store the original data as well
        item['candidate_details_link'] = response.xpath(admission_links['candidate_details']).get()
        item['original_certificates_link'] = response.xpath(admission_links['original_certificates']).get()
        item['admission_schedule_link'] = response.xpath(admission_links['admission_schedule']).get()
        
        item['candidate_details_text'] = response.xpath("//div[@data-id='db33835']//a/u/text()").get()
        item['original_certificates_text'] = response.xpath("//div[@data-id='7e372bc']//a/u/text()").get()
        item['admission_schedule_text'] = response.xpath("//div[@data-id='cd4f4f3']//a/u/text()").get()
        
        yield item