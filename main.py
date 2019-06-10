from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import logging
import os
import configparser
import re
import requests

# TODO PROXY

path_to_driver = f'{os.getcwd()}\\geckodriver.exe'
# options = webdriver.FirefoxOptions()
# options.add_argument("start-maximized")
# options.add_argument("--proxy-server=http://85.223.157.204:40329")
driver = webdriver.Firefox(executable_path=path_to_driver) # , firefox_options=options

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("logs.log", 'w', encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
log.addHandler(fh)

def open_main():
	config = configparser.ConfigParser()
	if os.path.isfile('config.ini'):
		config.read('config.ini')
		login = config['EXP']['Login']
		password = config['EXP']['Pass']
	else:
		log.critical('Config file (config.ini) not found')

	driver.implicitly_wait(30)
	log.info('Opening main page...')
	driver.get('https://www.expireddomains.net/login/')
	log.info('Done')
	log.debug('Finding login input...')
	input_login = driver.find_element_by_id('inputLogin')
	log.debug('Login found')
	log.debug('Finding pass input...')
	input_pass = driver.find_element_by_id('inputPassword')
	log.debug('Pass found')
	log.debug('Sending keys...')
	input_login.send_keys(login)
	input_pass.send_keys(password)
	log.debug('Login and Pass keys are sended')
	log.debug('Submitting form after 2 secs...')
	sleep(3)
	# driver.find_element_by_class_name('form-horizontal').submit()
	log.debug('Submitted')

	driver.get('https://member.expireddomains.net/domains/expiredcom/?o=bl&r=d')
	driver.find_element_by_class_name('showfilter').click()
	driver.find_element_by_id('fwhois').click()
	driver.find_element_by_id('fworden').click()
	driver.find_element_by_name('fadult').click()
	driver.find_element_by_name('flast48').click()
	driver.find_element_by_name('fwhoisage').click()
	driver.find_element_by_xpath("//select[@id='fwhoisage']/option[@value='2017']").click()
	driver.find_element_by_name('fabirth_year').click()
	driver.find_element_by_xpath("//select[@id='fabirth_year']/option[@value='2017']").click()
	driver.find_element_by_name('flimit').click()
	driver.find_element_by_xpath("//option[@value='200']").click()
	driver.find_element_by_name('button_submit').click()

def checkonlist():
	hrefs = driver.find_elements_by_xpath('//a[text()="Google Site"]')
	c = 0
	for href in hrefs:
		c += 1
		link = href.get_attribute('href')
		log.debug(f'{c} HREF: {link}')
		driver.execute_script(f"window.open('{link}', 'new window')")
		sleep(1)
		driver.switch_to_window(driver.window_handles[-1])
		log.debug('Finding id div "results stats"...')
		isfound = False
		iscaptcha = False
		try:
			results = driver.find_element_by_id('resultStats')
			log.debug('Found!')
			isfound = True
		except:
			log.debug('Not Found')
			try:
				# driver.find_element_by_class_name('rc-anchor rc-anchor-normal rc-anchor-light')
				driver.find_element_by_id('captcha-form')
				log.debug('Captcha found. Sleep for 90 secs')
				sleep(90)
			except:
				log.debug('Captcha NOT found')
				pass

		if isfound:
				log.debug(results.text)
				count = re.search(r'(\d+)', results.text)
				count = int(count.group(0))
				if count > 100:
					log.info(count)
					search = driver.find_elements_by_class_name('LC20lb')
					greenlinks = driver.find_elements_by_class_name('iUh30')
					for i in range(0, 6):
						log.info(search[i].text)
						log.info(greenlinks[i].text)

		driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
		sleep(1)
		driver.switch_to_window(driver.window_handles[0])
		sleep(10)

def getproxy():
	pass

if __name__ == '__main__':
    try:
        open_main()
        checkonlist()
    finally:
	    log.info('Closed')

