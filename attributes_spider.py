import scrapy

class AttributesSpider(scrapy.Spider):
    name = "attributes"
    start_urls = ['https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes']

    def parse(self, response):
        for row in response.xpath('//article/table/tbody/tr'):
            experimental = row.xpath('td[1]/span/i/@class').get() == 'icon-beaker'
            if experimental:
                continue
            attributes = set()
            attributes.add(row.xpath('td[1]/code/a[contains(@href, "Attributes")]/text()').get())
            attributes.add(row.xpath('td[1]/code/a[contains(@href, "Global_attributes")]/text()').get())
            attributes.add(row.xpath('td[1]/code/a/text()').get())
            attributes.add(row.xpath('td[1]/a/code/text()').get())
            attributes.add(row.xpath('td[1]/code/text()').get())
            attributes.add(row.xpath('td[1]/text()').get())
            attributes.remove(None)

            tags = row.xpath('td[2]/a[contains(@href, "Element")]/code/text()').getall()
            global_attribute = row.xpath('td[2]/a[contains(@href, "Global_attributes")]/text()').get() == "Global attribute"
            yield {
                    'name': attributes.pop(),
                    'tags': [tag.replace('<','').replace('>','') for tag in tags],
                    'is_global': global_attribute
                    }

