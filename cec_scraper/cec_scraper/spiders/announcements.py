from urllib.parse import urljoin
import scrapy

class AnnounceSpider(scrapy.Spider):
    name = 'announce_spider'
    start_urls = ['https://ceconline.edu/announcements/']
    
    def parse(self, response):
        # Dictionary mapping element IDs to notice identifiers and texts
        notice_mapping = {
            '0fa72ab': {
                'id': 'btech_registration',
                'text': 'Registration Form - B.Tech Admission 2024'
            },
            '7089465': {
                'id': 'btech_fee',
                'text': 'B.Tech  Fee Structure 2024-25'
            },
            '2099742': {
                'id': 'nri_fee',
                'text': 'NRI Fee Structure'
            },
            'd2d9dc9': {
                'id': 'let_fee',
                'text': 'LET Fee Structure'
            },
            '4b5f897': {
                'id': 'mca_fee',
                'text': 'MCA Fee Structure'
            }
        }
        
        for element_id, info in notice_mapping.items():
            notice_element = response.xpath(
                f"//div[contains(@class, 'elementor-element-{element_id}')]"
                "//div[contains(@class, 'elementor-widget-container')]"
                "//h2[contains(@class, 'elementor-heading-title')]"
                "//a"
            ).get() 
            
            if notice_element:
                notice_selector = scrapy.Selector(text=notice_element)
                link = notice_selector.xpath('//a/@href').get('')
                text = notice_selector.css('u::text').get('')
                
                if not text: 
                    text = notice_selector.xpath('//a/text()').get('').strip()
                if link and link.startswith('/'):
                    link = urljoin(response.url, link)
                    
                if link:  
                    doc_type = self.get_document_type(link)
                    
                    yield {
                        'data_type': 'notice',
                        'id': info['id'],
                        'title': text,
                        'url': link,
                        'type': doc_type,
                        'element_id': element_id,
                        'matched_text': info['text']
                    }
                    
                    if doc_type == 'pdf':
                        yield scrapy.Request(
                            url=link,
                            callback=self.save_pdf,
                            meta={
                                'title': text,
                                'notice_id': info['id']
                            },
                            errback=self.handle_error
                        )
    
    def get_document_type(self, url):
        if url.endswith('.pdf'):
            return 'pdf'
        elif 'forms.gle' in url:
            return 'google_form'
        elif url.startswith('http') or url.startswith('https'):
            return 'external_link'
        return 'other'
    
    def save_pdf(self, response):
        notice_id = response.meta['notice_id']
        filename = f"pdfs/{notice_id}.pdf"
        
        try:
            with open(filename, 'wb') as f:
                f.write(response.body)
            yield {
                'data_type': 'status',
                'status': 'success',
                'message': f'PDF saved: {filename}',
                'notice_id': notice_id
            }
        except Exception as e:
            yield {
                'data_type': 'status',
                'status': 'error',
                'message': f'Failed to save PDF: {str(e)}',
                'notice_id': notice_id
            }
    
    def handle_error(self, failure):
        yield {
            'data_type': 'status',
            'status': 'error',
            'message': f'Request failed: {str(failure.value)}',
            'url': failure.request.url
        }

# from urllib.parse import urljoin
# import scrapy
# import os

# class AnnounceSpider(scrapy.Spider):
#     name = 'announce_spider'
#     start_urls = ['https://ceconline.edu/announcements/']
    
#     def __init__(self, *args, **kwargs):
#         super(AnnounceSpider, self).__init__(*args, **kwargs)
#         os.makedirs('pdfs', exist_ok=True)
    
#     def parse(self, response):
#         notice_mapping = {
#             '0fa72ab': {
#                 'id': 'btech_registration',
#                 'text': 'Registration Form - B.Tech Admission 2024'
#             },
#             '7089465': {
#                 'id': 'btech_fee',
#                 'text': 'B.Tech  Fee Structure 2024-25'
#             },
#             '2099742': {
#                 'id': 'nri_fee',
#                 'text': 'NRI Fee Structure'
#             },
#             'd2d9dc9': {
#                 'id': 'let_fee',
#                 'text': 'LET Fee Structure'
#             },
#             '4b5f897': {
#                 'id': 'mca_fee',
#                 'text': 'MCA Fee Structure'
#             }
#         }
        
#         for element_id, info in notice_mapping.items():
#             notice_element = response.xpath(
#                 f"//div[contains(@class, 'elementor-element-{element_id}')]"
#                 "//div[contains(@class, 'elementor-widget-container')]"
#                 "//h2[contains(@class, 'elementor-heading-title')]"
#                 "//a"
#             ).get() 
            
#             if notice_element:
#                 notice_selector = scrapy.Selector(text=notice_element)
#                 link = notice_selector.xpath('//a/@href').get('')
#                 text = notice_selector.css('u::text').get('')
                
#                 if not text: 
#                     text = notice_selector.xpath('//a/text()').get('').strip()
#                 if link and link.startswith('/'):
#                     link = urljoin(response.url, link)
                    
#                 if link:  
#                     doc_type = self.get_document_type(link)
                    
#                     yield {
#                         'data_type': 'notice',
#                         'id': info['id'],
#                         'title': text,
#                         'url': link,
#                         'type': doc_type,
#                         'element_id': element_id,
#                         'matched_text': info['text']
#                     }
                    
#                     if doc_type == 'pdf':
#                         yield scrapy.Request(
#                             url=link,
#                             callback=self.save_pdf,
#                             meta={
#                                 'title': text,
#                                 'notice_id': info['id']
#                             },
#                             errback=self.handle_error
#                         )
    
#     def get_document_type(self, url):
#         if url.endswith('.pdf'):
#             return 'pdf'
#         elif 'forms.gle' in url:
#             return 'google_form'
#         elif url.startswith('http') or url.startswith('https'):
#             return 'external_link'
#         return 'other'
    
#     def save_pdf(self, response):
#         notice_id = response.meta['notice_id']
#         filename = f"pdfs/{notice_id}.pdf"
        
#         try:
#             # Make sure the directory exists (in case it was deleted after spider initialization)
#             os.makedirs('pdfs', exist_ok=True)
            
#             with open(filename, 'wb') as f:
#                 f.write(response.body)
#             yield {
#                 'data_type': 'status',
#                 'status': 'success',
#                 'message': f'PDF saved: {filename}',
#                 'notice_id': notice_id
#             }
#         except Exception as e:
#             yield {
#                 'data_type': 'status',
#                 'status': 'error',
#                 'message': f'Failed to save PDF: {str(e)}',
#                 'notice_id': notice_id,
#                 'error_type': type(e).__name__  # Added for better error tracking
#             }