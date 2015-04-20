# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E5020_THLBC_gov"
url = "http://www.towerhamlets.gov.uk/lgsl/800001-800100/800043_transparency/payments_to_suppliers-1.aspx"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
links = soup.findAll('a', href=True)

for link in links:
	url = 'http://www.towerhamlets.gov.uk/' + link['href']
	# title = link.contents[0].encode('ascii')
	title = link.encode_contents(formatter='html').replace('&nbsp;',' ') #  gets rid of erroneous &nbsp; chars
	if title.startswith('Payments for') or title.startswith('Payment for'):
		title = title.strip('\r\n').upper()
		print title
		# create the right strings for the new filename
		csvYr = title.split(' ')[-1]
		csvMth = title.split(' ')[-2][:3]
		csvMth = convert_mth_strings(csvMth);
		filename = entity_id + "_" + csvYr + "_" + csvMth + ".csv"
		todays_date = str(datetime.now())
		scraperwiki.sqlite.save(unique_keys=['l'], data={"l": url, "f": filename, "d": todays_date })
		print filename
