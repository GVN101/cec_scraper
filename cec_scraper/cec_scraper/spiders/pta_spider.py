import scrapy

class PTASpider(scrapy.Spider):
    name = "pta_spider"
    start_urls = ["https://ceconline.edu/about/committees/pta/"]

    def parse(self, response):
        pta_section = response.xpath('//div[contains(@class, "wpb_wrapper")]/div[contains(@class, "pta-section")]')

        if pta_section:
            pta_details = {}
            tables = pta_section.xpath(".//table")

            for table_index, table in enumerate(tables):
                members = []
                rows = table.xpath(".//tr[position()>1]")  # Skip header row
                for row in rows:
                    cols = row.xpath(".//td")
                    if cols:  # Check if the row has any columns at all
                        member = {}
                        try:
                            name_parts = cols[1].xpath(".//text()").getall()
                            member["name"] = "".join(name_parts).strip()
                            member["phone"] = cols[2].xpath(".//text()").get("").strip()
                            member["student_name"] = cols[3].xpath(".//text()").get("").strip() if len(cols) > 3 else "" #handle missing student name
                            members.append(member)
                        except IndexError as e:
                            self.log(f"IndexError in table {table_index + 1}: {e}. Row content: {row.get()}") #log the row content
                            continue #skip to next row
                    else:
                        self.log(f"Empty row found in table {table_index + 1}. Skipping.")

                if members: #only add if there are any members
                    if table_index == 0:
                        pta_details["executive_members"] = members
                    elif table_index == 1:
                        pta_details["faculty_representatives"] = members
                    elif table_index == 2:
                        pta_details["special_invitees"] = members

            if pta_details:
                yield {"pta_details": pta_details}
            else:
                self.log("No PTA data found in tables.")
        else:
            self.log("PTA section not found. Check the XPath.")