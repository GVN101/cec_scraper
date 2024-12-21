from urllib.parse import urljoin
import scrapy

class NoticeSpider(scrapy.Spider):
    name = 'notice_spider'
    start_urls = ['https://ceconline.edu/notifications-2/']
    
    def parse(self, response):
        notice_identifiers = {
            'semester_registration_revised': 'Revised notice for  Semester Registration',
            'semester_registration': 'Semester Registration for B.Tech  and MCA',
            'fees_payment': 'Fees Payment for Semester registration',
            'induction_programme': 'Student Induction Programme 2024',
            'btech_documents': 'B.Tech Documents To Be Submitted',
            'ladies_hostel': 'Ladies Hostel List',
            'answer_book': 'Purchase Of Main Answer Book'
        }
        
        for notice_id, notice_text in notice_identifiers.items():
            notice_element = response.xpath(
                f"//div[contains(@class, 'elementor-widget-container')]"
                f"//h2[contains(@class, 'elementor-heading-title')]"
                f"//a[contains(., '{notice_text}')]"
            )
            
            if notice_element:
                link = notice_element.attrib.get('href', '')
                text = notice_element.css('u::text').get('').strip()
                
                if not text:
                    text = notice_element.get().strip()
                
                if link.startswith('/'):
                    link = urljoin(response.url, link)
                    
                doc_type = self.get_document_type(link)
                yield {
                    'data_type': 'notice',  
                    'id': notice_id,
                    'title': text,
                    'url': link,
                    'type': doc_type,
                    'matched_text': notice_text
                }
                
                if doc_type == 'pdf':
                    yield scrapy.Request(
                        url=link,
                        callback=self.save_pdf,
                        meta={
                            'title': text,
                            'notice_id': notice_id
                        },
                        errback=self.handle_error
                    )
    
    def get_document_type(self, url):
        if url.endswith('.pdf'):
            return 'pdf'
        elif 'onlinesbi.sbi' in url:
            return 'payment_portal'
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