import scrapy

class CecSpider(scrapy.Spider):
    name = 'cec_spider'
    allowed_domains = ['ceconline.edu']
    start_urls = ['https://ceconline.edu/','https://ceconline.edu/administrators/hari/','https://ceconline.edu/board-of-governors/','https://ceconline.edu/about/administration/administrative-staff/']

    def parse(self, response):
        principal_name = response.css('.stm-title.stm-title_sep_bottom::text').extract_first().strip()
        qualification_titles = response.css('.wpb_wrapper ul span::text').getall()
        qualification_details = [q.strip() for q in response.css('.wpb_wrapper ul li::text').getall()]
        qualifications = dict(zip(qualification_titles, qualification_details))
        principal_contact = {}
        contact_details = response.css('.stm-contact-details__items li')

        for detail in contact_details:

            text = detail.css('::text').get().strip()
            key = detail.css('::attr(class)').get().split('_')[-1]
            if text:
                principal_contact[key.replace('-', '')] = text
        positions = response.css('.vc_tta-panel-body ol li::text').getall()
        fields_of_expertise = response.css('.vc_tta-panel-body:contains("LabVIEW") .wpb_wrapper ul li::text').getall()
        # international_journal_publications = []
        # journal_publications_section = response.css('.vc_tta-panel-body:contains("Desiree Juby Vincent & Hari V S")')
        # if journal_publications_section:
        #     journal_publications = journal_publications_section.css('ul li')
        #     for publication in journal_publications:
        #         title = publication.css('::text').getall()[0].strip()
        #         authors = title.split(" & ")[:-1]
        #         date_text = publication.css('::text').getall()[-2].strip()
        #         doi_link = publication.css('a::attr(href)').get()
        #         doi = doi_link.split("/")[-1] if doi_link else None
        #         publication_data = {
        #             'title': title,
        #             'authors': authors,
        #             'date': date_text,
        #             'doi': doi
        #         }
        #         international_journal_publications.append(publication_data)

        # # Extract international conference publications (last 5 years)
        # international_conference_publications = []
        # conference_publications_section = response.css('.vc_tta-panel-body:contains(Aswathy Bhooshan, Hari V S,” Recurrent Neural Netwok)')
        # if conference_publications_section:
        #     conference_publications = conference_publications_section.css('ul li')
        #     for publication in conference_publications:
        #         title = publication.css('::text').getall()[0].strip()
        #         authors = title.split(" & ")[:-1]
        #         date_text = publication.css('::text').getall()[-2].strip()
        #         doi_text = publication.css('::text').re(r'DOI:(\S+)')
        #         doi = doi_text[0] if doi_text else None
        #         publication_data = {
        #             'title': title,
        #             'authors': authors,
        #             'date': date_text,
        #             'doi': doi
        #         }
        #         international_conference_publications.append(publication_data)
        industry_interactions = response.css('.vc_tta-panel-body:contains("Minimization of atomic norm in vibration signals") .wpb_wrapper ul li em::text').getall()
        research_activities = response.css('.vc_tta-panel-body:contains("Incorporated a company Rand Walk Research") .wpb_wrapper ul li p::text').getall()
        books = response.css('.vc_tta-panel-body:contains("Electronics Laboratory Handbook with Simulations using Quite Universal Circuit Simulator (Qucs), Authors Press,New Delhi,ISBN-978-93-5529-048-9") .wpb_wrapper ol li::text').getall()

        yield {
            'principal_name': principal_name,
            'principal\'s-academic-qualifications': qualifications,
            'principal\'s-contact': principal_contact,
            'principal\'s-positions': positions,
            # 'principal\'s-publications': {
            #     'international_journal': international_journal_publications,
            #     'international_conference': international_conference_publications
            # },
            'principal\'s-fields-of-expertise': fields_of_expertise,
            'principal\'s-research': research_activities,
            'principal\'s-industry-interactions': industry_interactions,
            'principal\'s-books-published': books,
        }