import requests
from bs4 import BeautifulSoup
import pandas
import xlrd
import os
import csv
import pandas as pd
import numpy as np

def grabData(region, resort):
	print(resort)
	## SCRAPES DATA FROM ON THE SNOW FOR THE RESORT AND REGION FROM 2009 to 2017
	## OUTPUTS DATA FORMATTED ONTO A CSV FILE
	i = 2009
	year = 2018
	while i < year:
		try:
			page = requests.get("http://www.onthesnow.com/" + region + "/" + resort + "/historical-snowfall.html?&y=" + str(i) + "&v=list")
			soup = BeautifulSoup(page.content, "lxml")

			headers = [c.get_text() for c in soup.find('tr').find_all('td')[0:4]]
			data = [[cell.get_text(strip=True) for cell in row.find_all('td')[0:4]]
				for row in soup.find_all("tr", class_=True)]

			for entry in data:
				masterCSV = open("LOCATION OF DESTINATION CSV FILE", 'a')
				masterWriter = csv.writer(masterCSV, delimiter=",")

				date = str(entry).replace('[', '')
				date = date.replace(']', '')
				date = date.replace("'", '')
				date = date.replace(',', '')
				final = date.replace('u', '@')

				if final != "":
					dayIndex = final.find('@', 1)
					tfHourIndex = final.find('@', dayIndex + 1)
					seasonIndex = final.find('@', tfHourIndex + 1)

					day = final[:dayIndex]
					tfHour = final[dayIndex:tfHourIndex - 1]
					season = final[tfHourIndex:seasonIndex - 1]
					depth = final[seasonIndex:]

					day = getMDYString(day)
					tfHour = trim(tfHour)
					season = trim(season)
					depth = trim(depth)			

					masterWriter.writerow([resort, region, day, tfHour, season, depth])
					masterCSV.close()
			i += 1;

		except:
			fail = open("LOCATION OF TXT FILE WITH NAME OF FAILURES", "a")
			fail.write(resort + "\n")
			fail.close()
			print("fail")
			return('fail')
	return('good')


def grabRegions():
	fields = ['region']
	## TAKES IN REGIONS FROM RESORTREGION EXCEL FILE
	regions = pandas.read_excel('resortRegion.xlsx', usecols=fields)
	return(regions)

def grabResorts():
	fields = ['resort']
	## TAKES IN RESORTS FROM RESORTREGION EXCEL FILE
	resorts = pandas.read_excel('resortRegion.xlsx', usecols=fields)
	return(resorts)

def trim(string):
	## TRIMS THE STRING PARAMETER OF UNNECESSARY CHARACTERS
	newString = string.replace('in.', '')
	newString = newString.replace(' ', '')
	newString = newString.replace('@', '')
	return(newString)

def getMDYString(string):
	## CONVERTS STRING DATA (JAN 1 2009") INTO MMDDYYYY FORMAT
	newString = string.replace('@', "")
	newString = newString.replace(' ', '')
	final = ""
	if newString[:3] == 'Jan':
		final += "01"
	elif newString[:3] == 'Feb':
		final += "02"
	elif newString[:3] == 'Mar':
		final += "03"
	elif newString[:3] == 'Apr':
		final += "04"
	elif newString[:3] == 'May':
		final += "05"
	elif newString[:3] == 'Jun':
		final += "06"
	elif newString[:3] == 'Jul':
		final += "07"
	elif newString[:3] == 'Aug':
		final += "08"
	elif newString[:3] == 'Sep':
		final += "09"
	elif newString[:3] == 'Oct':
		final += "10"
	elif newString[:3] == 'Nov':
		final += "11"
	elif newString[:3] == 'Dec':
		final += "12"
	else:
		final = final
	if len(newString) < 9:
		final += '0'
	final += newString[3:]
	#final = final.replace(" ", '')
	return(final)

#MAIN MAIN MAIN MAIN MAIN

## CREATES HEADERS OF THE CSV FILE
masterCSV = open("LOCATION OF DESTINATION CSV FILE", 'a')
masterWriter = csv.writer(masterCSV, delimiter=",")
masterWriter.writerow(["resort", "region", "snowdate", "snownew", "snowannual", "snowbase"])
masterCSV.close()

## SCRAPES AND WRITES DATA FOR ALL REGIONS
regions = grabRegions()
resorts = grabResorts()
failures = 0
## 0 IS THE INDEX OF THE FIRST RESORT AND 388 THE LAST
for i in range (0, 388):
        print(i)
	if grabData(regions.region[i], resorts.resort[i]) == 'fail':
		failures += 1
		print(failures)
