import scrapy, json
from bcpa.items import BcpaItem

class bcpaSpider(scrapy.Spider):
		
	name = "bcpa"
	DOWNLOAD_DELAY = 0.20

	def start_requests(self):

		subdivisions = [
		"1","2","3","4","5","6","7","8","9","0"
		]

		for subdivision in subdivisions:
			
			form_data = {"LongSubDivisionNumber":subdivision}

			headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate',
			'Accept-Language':'pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',
			'Content-Type':'application/x-www-form-urlencoded',
			'Host':'www.bcpa.net',
			'Origin':'http://www.bcpa.net',
			'Referer':'http://www.bcpa.net/RecSub.asp',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36}'
			}

			yield scrapy.FormRequest('http://www.bcpa.net/RecSubDivision.asp', 
				method="POST",
				formdata=form_data,
				headers= headers
			)
				   
	def parse(self, response):


		table = response.xpath("""//*[@id="Table8"]""")

		if table:

			urls = response.xpath("""//*[@id="Table8"]//tr/td[1]//a/@href""").extract()
			
			for url in urls:
				
				yield scrapy.Request(url="http://www.bcpa.net/"+url, callback=self.extract)

			next_page = response.xpath("""//*[@id="Table9"]//b/a[contains(text(),'Next')]/@href""").extract_first()

			if (next_page):

				yield scrapy.Request(url="http://www.bcpa.net/"+next_page)

	def extract(self, response):

		self.log('GETTING URL: %s'% response.url)

		item = BcpaItem()

		item["site_address_link"] = response.xpath("""//table//tr[contains(.,'Site Address')]/td[2]//a/@href""").extract_first()

		site_address = response.xpath("""//table//tr[contains(.,'Site Address')]/td[2]//text()[normalize-space()]""").extract()
		if site_address : item["site_address"] = site_address[0].replace("\r\n\t\t\t","").strip()	

		property_owner = response.xpath("""//table//tr[contains(.,'Property Owner')]/td[2]//text()[normalize-space()]""").extract()
		if property_owner : item["property_owner"] = ''.join(property_owner).replace("\u00a0","").strip()

		mailing_address = response.xpath("""//table//tr[contains(.,'Mailing Address')]/td[2]//text()[normalize-space()]""").extract()
		if mailing_address : item["mailing_address"] = ''.join(mailing_address).replace("\u00a0","").strip()
		
		abbreviated_legal_description = response.xpath("""//table//tr[contains(.,'Abbreviated Legal Description')]/td[2]//text()[normalize-space()]""").extract()
		if abbreviated_legal_description : item["abbreviated_legal_description"] = ''.join(abbreviated_legal_description).replace("\u00a0","").strip()
		
		_id = response.xpath("""//table//tr[contains(.,'ID #')]/td[2]//text()[normalize-space()]""").extract()		
		if _id : item["_id"] = ''.join(_id).replace("\u00a0","").strip()

		millage = response.xpath("""//table//tr[contains(.,'Millage')]/td[2]//text()[normalize-space()]""").extract()
		if millage : item["millage"] = ''.join(millage).replace("\u00a0","").strip()

		use = response.xpath("""//table//tr[contains(.,'Use')]/td[2]//text()[normalize-space()]""").extract()
		if use : item["use"] = ''.join(use).replace("\u00a0","").strip()

		item["url"] = response.url

		yield item
	 