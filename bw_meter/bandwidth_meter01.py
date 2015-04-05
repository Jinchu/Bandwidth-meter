# Simple network monitoring script made by
# Panu Simolin for learning, fun and profit.
#
# Downloads a test file according to given 
# configuration and logs the download speed.
# Bugs and questions can be send to 
# p.simolin[atlf]gmail.com

import json
import sys
import time
import urllib.request

class config:
	def __init__(self):
		f = open("bw_config", 'r')
		conffile = f.read()
		json_conf = json.loads(conffile)
		self.version = json_conf["version"]
		self.url = json_conf["url"]
		self.log_path = json_conf["log_path"]
		self.interval = json_conf["mins_between_tests"]
		f.close()
	
	def print_all(self):
		print("url: ", self.url)
		print("interval: ", self.interval)
		print("log_path: ", self.log_path)
		
def download_test_file(url):
	response = urllib.request.urlopen(url)
	total = int(response.headers['content-length'])
	
	file = response.read()
	del file
	return total


def calculate_speed(size, time):
	speed = size / time
	
	if (speed < 0):
		return "error"
	elif (speed == 0):
		return "0 kb/s"
	elif (speed < 1000):
		return ("%.1f"%speed + " B/s")
	
	speed = speed / 1000
	if (speed < 1000):
		return ("%.1f"%speed + " kB/s")
	
	speed = speed / 1000
	return ("%.2f"%speed + " MB/s")
        
def add_to_log(entry, path):
	f = open(path, "a")
	f.write(entry + "\n")
	f.close
	return
		
def measurement_loop():
	conf = config()
	running = 3
	
	while (running == 3):
		if conf.version == 1:
			start = time.clock()
			file_size = download_test_file(conf.url)
			time_used = time.clock() - start
			result = calculate_speed(file_size, time_used)
			log_entry = (time.ctime() + "     ---   " + result)
			add_to_log(log_entry, conf.log_path)
			
			seconds = conf.interval * 60
			time.sleep(seconds)
			
		else:
			print('Unsupported configuration')
			running = 0
		
	return

def main():
	measurement_loop()
	
main()
