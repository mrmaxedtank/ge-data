#!/usr/bin/python3.7

#Fetch data from RSbuddy and OSRS GE database for a defined list of items and present following data in a structured fashion:
#Main (runs periodically):
#Check if GE updated
#If GE updated: add data from osrs API to database, add timestamp of detected update to geupdate table. Launch enrichment function after for adding more accurate pricing information to table.
#If GE not updated: skip OSRS API
#Fetch OSB data
#Check via comparison between md5sum current run and last run if updated
#If updated: add OSB data to database
#
#To do:
#Change parameters to use relative paths, to ease testing.

import os
import sys
import json
import requests
import time
import pymysql
import pymysql.cursors
import logging
import configparser
import functools
import operator
import smtplib
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from datetime import datetime

#Set variables/parameters
#Input
db_conf = '/home/pi/scripts/ge/ge_data/db.conf'
config=configparser.ConfigParser()
config.read(db_conf)
envi = 'prod'
con = pymysql.connect(host = config[envi]['host'], user = config[envi]['user'], password = config[envi]['password'], db = config[envi]['db_name'])
db = config[envi]['db_name']
body = '/tmp/body.txt'
#API
limits_api = 'https://www.osrsbox.com/osrsbox-db/items-json/' # + item_id + .json
url_osb = 'https://rsbuddy.com/exchange/summary.json'
osb_file_path = '/home/pi/scripts/ge/ge_data/summary.json'
osb_file_path_old = '/home/pi/scripts/ge/ge_data/summary.json.OLD'
#osb_data_folder = '/mnt/stack/Scripting/Pythong/GE_data/data/osb_data/'
#wiki_data_folder = '/mnt/stack/Scripting/Python/GE_data/data/wiki_data/'
osb_data_folder = '/mnt/backup/data/osb_data/'
wiki_data_folder = '/mnt/backup/data/wiki_data/'
url_osrs = 'http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item=' # + item_id
url_wiki = 'http://prices.runescape.wiki/api/v1/osrs/5m'
url_wiki_headers = { 'User-Agent' : 'ge_data.py/1.3 MrMaxedTank' }
#Retry
s = requests.Session()
retries = Retry(total=15, backoff_factor=0.2, status_forcelist=[ 400, 401, 402, 404, 500, 502, 503, 504 ])
s.mount('http://', HTTPAdapter(max_retries=retries))
#Mail
tomail = config['ssmtp']['to']
frommail = config['ssmtp']['from']
_mailhub = config['ssmtp']['mailhub']
mailhubport = config['ssmtp']['mailhubport']
mailpass = config['ssmtp']['password']
#Generic
version = '1.3'
updated = False
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def main(args):
	global updated
	updated = False
	if sys.argv[1] == '--rebuild':
		logging.info('Rebuilding limits')
		build_limits()
		logging.info('Limits rebuilt')
	elif sys.argv[1] == '--updated':
		logging.info('Running osrs() as updated')
		updated = True
		osrs()
	elif sys.argv[1] == '--initialize':
		logging.info('Running initization')
		logging.info('Step 1: rebuild limits')
		build_limits()
		updated = True
		logging.info('Step 2: run osrs()')
		osrs()
		logging.info('Step 3: run osb()')
		osb()
	elif sys.argv[1] == '--osrs':
		logging.info('MAIN: osrs: value updated before check_update():' + str(updated))
		updated = check_updated(False)
		logging.info('MAIN: osrs: value updated after check_update():' + str(updated))
		if updated == True:
			logging.info('MAIN: GE updated')
			logging.info('GE updated: running osrs()')
			osrs()
			enrichment()
		else:
			logging.info('MAIN: GE NOT updated')
	elif sys.argv[1] == '--osb':
		logging.info('Running osb()')
		osb()
	elif sys.argv[1] == '--enrich':
		logging.info('Running enrich()')
		enrichment()
	elif sys.argv[1] == '--wiki':
		logging.info('Running wiki()')
		wiki()
	elif sys.argv[1] == '--enrichment_check':
		logging.info('Running enrichment_check()')
		enrichment_check()

def osrs():
#Function for fetching OSRS API data
	logging.info('Function osrs started')
	logging.info('Updated: ' + str(updated))
	if updated == False:
		logging.info('GE not updated, skip function')
	else:
		logging.info('Refresh osrs data')
		try:
			with con.cursor() as cur:
				logging.info('Select ids')
				cur.execute('SELECT id FROM items order by id asc;')
				rows = cur.fetchall()
				#sql_hist = 'INSERT INTO `hist` (`date`, `id`, `overall_average`, `overall_osrs`, `source`) VALUES (%s, %s, %s, %s, %s)'
				sql = 'INSERT INTO `osrs_hist` (`date`, `id`, `current_trend`, `current_price`, `today_trend`, `today_price`, `30day_trend`, `30day_change`, `90day_trend`, `90day_change`, `180day_trend`, `180day_change`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

				for row in rows:
					while True:
						try:
							date = ''
							now = datetime.now()
							id = ''
							osrs = 'osrs'
							current_trend = ''
							current_price = ''
							today_trend = ''
							today_price = ''
							day30_trend = ''
							day30_change = ''
							day90_trend = ''
							day90_change = ''
							day180_trend = ''
							day180_change = ''

							id = int(''.join(map(str, row)))
							address = url_osrs + str(id)
							logging.info(address)
							item_osrs_tmp = s.get(address)
							data = item_osrs_tmp.json()

							current_trend = data['item']['current']['trend']
							current_price = fix_price(data['item']['current']['price'])
							today_trend = data['item']['today']['trend']
							today_price = fix_price(data['item']['today']['price'])
							day30_trend = data['item']['day30']['trend']
							day30_change = data['item']['day30']['change'].replace('%', '')
							day90_trend = data['item']['day90']['trend']
							day90_change = data['item']['day90']['change'].replace('%', '')
							day180_trend = data['item']['day180']['trend']
							day180_change = data['item']['day180']['change'].replace('%', '').replace(',', '')
							date = now.strftime("%Y-%m-%d %H:%M:%S")
							overall_osrs = data['item']['current']['price']

							try:
								cur.execute(sql, (date, id, current_trend, current_price, today_trend, today_price, day30_trend, day30_change, day90_trend, day90_change, day180_trend, day180_change))

								logging.info('Committing data')
								con.commit()
							except:
								error = '''Function OSB() failed to commit data for item: ''' + id + ''' to database''' 
								send_warning(error)
								logging.info('Execution of query failed')
							finally:
								time.sleep(0.5)
						except:
							logging.info('Treatment of item failed, retry (most likely caused by API response)')
							time.sleep(1.0)
							continue
						logging.info('Treatment of item succeeded, next')
						break
		finally:
			logging.info('Closing cursor')
			cur.close()

def osb():
#Detecting if osbuddy API file has changed. If so, insert new data into database)
	logging.info('Function osb() started')
	md5_old = ''
	md5_old_tmp = ''
	md5_new = ''
	md5_new_tmp = ''
	code = ''
	
	code = os.system('wget ' + url_osb + ' -O ' + osb_file_path)
	logging.info('Code: ' + str(code))

	if os.path.isfile(osb_file_path_old) and code == 0:
			logging.info('Json.OLD exists and wget succeeded')
			md5_old_tmp = os.popen('md5sum ' + osb_file_path_old).read()
			md5_new_tmp = os.popen('md5sum ' + osb_file_path).read()

			md5_old = md5_old_tmp.split(' ')[0]
			md5_new = md5_new_tmp.split(' ')[0]
			logging.info('Oude md5 sum: ' + md5_old + '\nNieuwe md5 sum: ' + md5_new)
			if md5_old == md5_new:
					logging.info('Old and new osbuddy files the same, end function')
			else:
					logging.info('New osbuddy file differs from old, start update to database')
					with open(osb_file_path) as f:
							osb_data = json.load(f)

					try:
							with con.cursor() as cur:
									logging.info('Selecting ids')
									cur.execute('SELECT id FROM items where id not in (2, 1391, 2434) order by id asc;')
									rows = cur.fetchall()
									logging.info(rows)
									sql_hist = 'INSERT INTO `osb_updates` (`time`) VALUES (%s)'
									sql = 'INSERT INTO `osb_hist` (`date`, `id`, `buy_average`, `buy_quantity`,  `sell_average`, `sell_quantity`, `overall_average`, `overall_quantity`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

									log_now = datetime.now()
									log_date = log_now.strftime("%Y-%m-%d %H:%M:%S")
									cur.execute(sql_hist, log_date)
									for row in rows:
											id = ''
											buy = ''
											buy_quantity = ''
											sell = ''
											sell_quantity = ''
											overall = ''
											overall_quantity = ''
											overall_check_tmp = ''
											overall_check = ''
											date = ''
											now = datetime.now()

											id = str(int(''.join(map(str, row))))
											buy = osb_data[id]['buy_average']
											buy_quantity = osb_data[id]['buy_quantity']
											sell = osb_data[id]['sell_average']
											sell_quantity = osb_data[id]['sell_quantity']
											overall = osb_data[id]['overall_average']
											overall_quantity = osb_data[id]['overall_quantity']
											date = now.strftime("%Y-%m-%d %H:%M:%S")

											cur.execute('SELECT overall_average FROM osb_hist where id = %s order by date desc limit 1', id)
											overall_check_tmp = cur.fetchone()
											if overall_check_tmp is None:
												overall_check = 0
											else:
												overall_check = int(''.join(map(str, overall_check_tmp)))

											logging.info('-------------' + id + '-------------------------------')
											logging.info('Overall: ' + str(overall))
											logging.info('Overall_check: ' + str(overall_check))

											if overall_quantity == 0:
												logging.info('Overall_quantity = 0')
											elif overall == overall_check:
												logging.info('Old data equals new, skip')
											else:
												cur.execute(sql, (date, id, buy, buy_quantity, sell, sell_quantity, overall, overall_quantity))
												logging.info('Committing data')
												con.commit()
					finally:
							logging.info('Closing cursor')
							cur.close()

					os.system('cp ' + osb_file_path + ' ' + osb_file_path_old)
					osb_data_filename = datetime.now().strftime("%Y%m%d-%H%M%S") + '_osb_data.json'
					os.system('cp ' + osb_file_path + ' ' + osb_data_filename)
					os.system('gzip -9 ' + osb_data_filename)
					os.system('mv ' + osb_data_filename + '.gz ' + osb_data_folder + datetime.now().strftime("%Y") + "/" + datetime.now().strftime("%m") + "/" + osb_data_filename + '.gz')
	else:
		logging.info('Function skipped; osbuddy data not changed or wget failed')

def check_updated(res):
#Function to verify if OSRS GE database has updated or not, first function that's called from main and used to determine which OSRS GE database function to call later during the run. ID of first item in list is used to fetch its properties and compare those to the results of this check during last run. Bear in mind it's important to add new items to the input list at the bottom.
	logging.info('Function check_updated() started')
	logging.info('Res : ' + str(res))
	try:
		with con.cursor() as cur:
			logging.info('Check if last osrs update < 30 minutes ago')
			logging.info('Check timestamp last update')
			cur.execute('SELECT time from ge_updates order by time desc limit 1;')

			if cur.rowcount != 0:
				ts_last_update = cur.fetchone()[0]
				ts_ref = datetime.now()
				diff = ts_ref - ts_last_update
				diff_min = diff.total_seconds() / 60
				logging.info('Minutes since last update: ' + str(diff_min))
				if diff_min < 30:
					logging.info('Last update less than 15 minutes ago, skip')
					return False

			logging.info('Selecting ids for check')
			cur.execute('SELECT id FROM items where id in (2, 1391, 2434);')
			rows_tmp = cur.fetchall()
			logging.info(rows_tmp)
			rows = []
			sql = 'SELECT current_price FROM `osrs_hist` where id = %s order by date desc limit 1'

			for x in rows_tmp:
				item_id = int(''.join(map(str, x))) 
				cur.execute(sql, (item_id))
				#Check if query gave results
				if cur.rowcount == 0:
					logging.info('Problem with cur.fetchone(), using value 0')
					db_osrs_price = 0
				else:
					db_osrs_price = cur.fetchone()[0]

				logging.info('Debug: db_osrs_price: ' + str(db_osrs_price))

				address = url_osrs + str(item_id)
				logging.info('Debug: address: ' + str(address))
				osrs_item_tmp = s.get(address)
				osrs_item_data = osrs_item_tmp.json()
				api_osrs_price = fix_price(osrs_item_data['item']['current']['price'])
				logging.info('Debug: api_osrs_price: ' + str(api_osrs_price))

				if api_osrs_price != db_osrs_price:
					logging.info('GE updated')
					res = True
					break
	finally:
		logging.info('Closing cursor')
		if res == True:
			logging.info('GE updated')
			send_email(db_osrs_price, api_osrs_price)
		else:
			logging.info('GE NOT updated')
		cur.close()

	return res

def build_limits():
#When called rebuilds table limits with fresh data from limits API (osrsbox)
	try:
		with con.cursor() as cur:
			logging.info('Truncating table')
			cur.execute('TRUNCATE limits;')
			con.commit()
			cur.execute('SELECT id FROM items;')
			rows = cur.fetchall()
			sql = 'INSERT INTO `limits` (`id`, `limit`) VALUES (%s, %s)'

			for row in rows:
				id = ''
				limit = ''
				limit_data_tmp = ''
				limit_data_json = ''
				id = int(''.join(map(str, row)))
				limit_data_tmp = s.get(limits_api + str(id) + str('.json'))
				limit_data_json = limit_data_tmp.json()

				limit = limit_data_json['buy_limit']
				cur.execute(sql, (id, limit))
				con.commit()
			logging.info('Table updated')

	finally:
		logging.info('Closing cursor')
		cur.close()

def fix_price(val):
#Recalculates OSRS API data to real integers
    res = ''
    string = str(val)
    tmp_lower = string.lower()

    logging.info('Fix_price: ' + str(tmp_lower))

    if 'k' in tmp_lower:
	#logging.info('Fix_price: ' + str(tmp_lower))
        res = int(tmp_lower.replace('k', '').replace(',', '').replace('.', '').replace(' ', '')) * 100
    elif 'm' in tmp_lower:
        res = int(tmp_lower.replace('m', '').replace(',', '').replace('.', '').replace(' ', '')) * 100000
    elif 'b' in tmp_lower:
        res = int(tmp_lower.replace('b', '').replace(',', '').replace('.', '').replace(' ', '')) * 100000000
    else:
        res = int(tmp_lower.replace(',', '').replace('.', '').replace(' ', ''))

    return res

def send_email(x, y):
#Replace shell script geupdate by this function.
	now = datetime.now()
	date = now.strftime("%Y-%m-%d %H:%M:%S")
	sql = 'INSERT INTO `ge_updates` (`time`) VALUES (%s)'
	logging.info('Function send_mail(x, y) started')
	subject = 'GE has been updated!'
	text = 'Price was %s\n\nPrice is now %s\n\n\n\nChange registered: %s' % (x, y, date)
	message = 'Subject: {}\n\n{}'.format(subject, text)

	try:
		context = ssl.create_default_context()
		with smtplib.SMTP('smtp.gmail.com', 587) as server:
			server.ehlo()
			server.starttls(context=context)
			server.ehlo()
			server.login(frommail, mailpass)
			server.sendmail(frommail, tomail, message)
		logging.info('Email sent!')
	except:
		logging.info('Mail not sent: something went wrong.') 

	try:
		with con.cursor() as cur:
			logging.info('Committing date to database')
			cur.execute(sql, (date))
			con.commit()
	finally:
		logging.info('Closing cursor')
		cur.close()

def send_warning(x):
#Send warning if function of script fails.
	now = datetime.now()
	date = now.strftime("%Y-%m-%d %H:%M:%S")
	logging.info('Function send_warning() started')
	subject = 'Ge_data.py: an error has occured!'
	text = x
	message = 'Subject: {}\n\n{}'.format(subject, text)

	try:
		context = ssl.create_default_context()
		with smtplib.SMTP('smtp.gmail.com', 587) as server:
			server.ehlo()
			server.starttls(context=context)
			server.ehlo()
			server.login(frommail, mailpass)
			server.sendmail(frommail, tomail, message)
			logging.info('Email sent!')
	except:
		logging.info('Mail not sent: something went wrong.')

def enrichment():
#Enriches lines of osrs_hist with more information unavailable to the OSRS API by scraping the itemdb_oldschool pages. Data fetched: precise prices (rather than x.xk or x.xM prices) and quantity of trades recorded. 
	logging.info('Enrichment launched')
	header = '''Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/85.0'''
	base_url = 'https://secure.runescape.com/m=itemdb_rs/viewitem?obj='
	temp_file = '/tmp/osrs_item.html'
	content = ''
	sel_query = 'select id from items where id not in (2, 1391, 2434) order by id asc'
	item_query = 'select `key`, id, date from osrs_hist where id = %s and (enriched = "0" or enriched is null) and date between sysdate() - interval 150 day and sysdate()'
	#Line below for testing purposes
	#item_query = 'select `key`, id, date from osrs_hist where id = %s and date between sysdate() - interval 150 day and sysdate() limit 10'
	update_query = ''
	content_dict = {}

	with con.cursor() as cur:
		logging.info('Running sel_query to select items')
		cur.execute(sel_query)
		items = cur.fetchall()
		#Line below for testing purposes
		#items = cur.fetchone()
		logging.info(items)
		for x in items:
			logging.info('Running item_query to find lines to enrich')
			cur.execute(item_query, x)
			rows = cur.fetchall()
			count = cur.rowcount
			logging.info('Count: ' + str(cur.rowcount))
			if count == 0:
				continue
			price_dict = {}
			quantity_dict = {}
			time.sleep(5)
			#Line below for testing purposes (run 1 item) 
			#os.system('wget --user-agent="%s" https://secure.runescape.com/m=itemdb_oldschool/viewitem?obj=%s -O %s' % (header, x, temp_file))
			os.system('wget --user-agent="%s" https://secure.runescape.com/m=itemdb_oldschool/viewitem?obj=%s -O %s' % (header, str(x[0]), temp_file))
			logging.info('Builing dicts for item ' + str(x[0]))
			with open(temp_file,'r') as file:
				for line in file:
					if 'average180.push' in line:
						date_tmp = line.split("'")[1]
						date = date_tmp.replace("/", "-")
						value = line.split(',')[1].strip()
						price_dict[date] = value
					elif 'trade180.push' in line:
						date_tmp = line.split("'")[1]
						date = date_tmp.replace("/", "-")
						quantity = line.split(',')[1].split(']')
						quantity_dict[date] = quantity[0]
			#logging.info(price_dict)
			#logging.info(quantity_dict)
			logging.info('Dicts built')
			for i in rows:
				key = ''
				id = ''
				date = ''

				key = i[0]
				id = i[1]
				date = i[2]

				if date:
					#logging.info('Date: ' + str(date))
					#logging.info('Date2: ' + date.strftime("%Y-%m-%d"))
					#logging.info('Values to set: ' + price_dict[date.strftime("%Y-%m-%d")] + '&' + quantity_dict[date.strftime("%Y-%m-%d")])
					#print('Updating line')
					try:
						cur.execute('update osrs_hist set enriched_price = %s, enriched_quantity = %s, enriched = 1 where id = %s and substr(date,1,10) = "%s"' % (price_dict[date.strftime("%Y-%m-%d")], quantity_dict[date.strftime("%Y-%m-%d")], id, date.strftime("%Y-%m-%d")))
						con.commit()
						logging.info('Line updated')
						logging.info('---------------------------------------------------')
					except:
						error = '''Function enrichment() failed to enrich data for item: ''' + str(id) + ''' in database for date: ''' + str(date)
						#send_warning(error)
						logging.info('Execution of query failed')


def wiki():
#Function for fetching data from runescape.wiki. Data provided by Runelite users.
	logging.info('Function wiki() started')
	s.headers.update(url_wiki_headers)
	try:
		with con.cursor() as cur:
			logging.info('Select ids')
			cur.execute('SELECT id FROM items where id not in (2, 1391, 2434) order by id asc;')
			rows = cur.fetchall()
			sql = 'INSERT INTO `wiki_hist` (`date`, `id`, `avgHighPrice`, `highPriceVolume`, `avgLowPrice`, `lowPriceVolume`, `json_timestamp`) VALUES (%s, %s, %s, %s, %s, %s, %s)'

			item_wiki_tmp = s.get(url_wiki)
			data = item_wiki_tmp.json()
			date_data = data['timestamp']
			logging.info('Timstamp JSON: ' + str(date_data))

			file_data = item_wiki_tmp.content
			file_date = datetime.now()
			file_name = '/tmp/' + str(file_date.strftime("%Y%m%d-%H%M%S")) + '_wiki_data.json'

			with open(file_name, 'wb') as f:
				f.write(file_data)

			os.system('gzip -9 ' + file_name)
			os.system('mv ' + file_name + '.gz ' + wiki_data_folder + "/" + str(file_date.strftime("%Y")) + "/" + str(file_date.strftime("%m")) + "/"  + file_name.split("/")[2] + '.gz')


			for row in rows:
				date = ''
				now = datetime.now()
				id = ''
				avgHighPrice = ''
				highPriceVolume = 0
				avgLowPrice = ''
				lowPriceVolume = 0
				overall_check_tmp = ''
				overall_check = ''

				id = int(''.join(map(str,row)))

				date = now.strftime("%Y-%m-%d %H:%M:%S")

				for k, v in data['data'].items():
					if k == str(id):
						avgHighPrice = v['avgHighPrice']
						#print(avgHighPrice)
						highPriceVolume = v['highPriceVolume']
						#print(highPriceVolume)
						avgLowPrice = v['avgLowPrice']
						#print(avgLowPrice)
						lowPriceVolume = v['lowPriceVolume']
						#print(lowPriceVolume)

				if lowPriceVolume != 0 or highPriceVolume != 0:
					logging.info('Data available for item, checking if different from last data using json_timestamp')
					cur.execute('SELECT json_timestamp FROM wiki_hist where id = %s order by date desc limit 1', id)
					overall_check_tmp = cur.fetchone()
					if overall_check_tmp is None:
						overall_check = 0
					else:
						overall_check = int(''.join(map(str, overall_check_tmp)))

					if overall_check != date_data:
						try:
							cur.execute(sql, (date, id, avgHighPrice, highPriceVolume, avgLowPrice, lowPriceVolume, date_data))
							logging.info('Committing data')
							con.commit()
						except:
							error = '''Function wiki() failed to commit data for item: ''' + str(id) + ''' to database'''
							send_warning(error)
							logging.info(error)
							logging.info('avgHighPrice: ' + avgHighPrice)
							logging.info('highPriceVolume: ' + highPriceVolume)
							logging.info('avgLowPrice: ' + avgLowPrice)
							logging.info('lowPriceVolume: ' + lowPriceVolume)
							logging.info('Execution of query failed')
					else:
						logging.info('New data equal to last data in database')
	finally:
		logging.info('Closing cursor')
		cur.close()

def enrichment_check():
#Periodical check to see if enrichment has worked properly during last run.
        logging.info('Running enrichment_check()')
        sql_check = 'SELECT distinct(id) from osrs_hist where enriched = 0 and id not in (2, 1391, 2434);'

        try:
                with con.cursor() as cur:
                        logging.info('Check if last osrs update > 60 minutes ago')
                        logging.info('Check timestamp last update')
                        cur.execute('SELECT max(time) from ge.ge_updates;')

                        if cur.rowcount != 0:
                                ts_last_update = cur.fetchone()[0]
                                ts_ref = datetime.now()
                                diff = ts_ref - ts_last_update
                                diff_min = diff.total_seconds() / 60
                                logging.info('Minutes since last update: ' + str(diff_min))
                                if diff_min > 60:
                                        logging.info('Last update more than 60 minutes ago, continue')
                                        try:
                                                cur.execute(sql_check)
                                                logging.info('Rowcount: ' + str(cur.rowcount))
                                                if cur.rowcount != 0:
                                                        count = cur.fetchone()[0]
                                                        logging.info('Count: ' + str(count))
                                                        if count == 0:
                                                                logging.info('Rowcount = 0, exit')
                                                                return
                                                        else:
                                                                logging.info('Records to enrich detected, starting enrichment()')
                                                                enrichment()
                                        except:
                                                error = '''Function enrichment_check() failed to check if there are unenriched items'''
                                                send_warning(error)
        except:
                error = '''Function enrichment_check() failed to check last ge update date'''
                send_warning(error)
        finally:
                logging.info('Check completed')


if __name__ == "__main__":
	main(sys.argv[0:])
