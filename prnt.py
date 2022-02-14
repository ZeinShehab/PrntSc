from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from io import BytesIO
from PIL import Image
import random
import sys
import os


OS = sys.platform
PATH = "geckodriver" if OS == "win32" else "/usr/bin/geckodriver"

CHARS = "abcdefghijklmnopqrtsuvwxyz0123456789"
XPATH = "/html/body/div[3]/div/div/img"

EXCLUDE_PATH = "exclude/"
DOWNLOAD_PATH = "images/"
BLACKLIST_FILE = "blacklist.txt"

op = Options()
op.headless = True
service = Service(PATH)
driver = webdriver.Firefox(service=service, options=op)


def get_url() -> str:
	url = "https://prnt.sc/"
	image = "".join(random.sample(CHARS, 6))

	blacklist = open(BLACKLIST_FILE, 'r').readlines()
	if url + image in blacklist:
		print("Found in blacklist: " + url + image)
		get_url();

	return url + image


def get_img() -> bytes:
	try:
		image = driver.find_element(By.XPATH, XPATH).screenshot_as_png
	except:
		image = False
	return image


def download_image(image, file_name) -> None:
	file_path = DOWNLOAD_PATH + file_name

	with open(file_path, "wb") as f:
		f.write(image)


def find_dup(img, dir_path):
	if img:
		img = Image.open(BytesIO(img))
	else:
		return False

	for image_path in os.listdir(dir_path):
		img2 = Image.open(dir_path+image_path)
	
		if list(img.getdata()) == list(img2.getdata()):
			return True
	return False


def blacklist(url):
	with open(BLACKLIST_FILE, "a") as blacklist:
		blacklist.write(url + "\n")


def main(check_dups=False):
	print("[*] IMAGES IN EXCLUDED FOLDER WILL NOT BE SAVED")

	if check_dups:
		print("[*] DUPLICATE IMAGES WILL NOT BE SAVED\n")
	else:
		print("[*] DUPLICATE IMAGES WILL BE SAVED\n")

	count = 1
	while count <= N_IMAGES:
		excluded = False
		duplicate = False

		url = get_url()
		driver.get(url)

		image = get_img()	
		file_name = f"index_{count}.png"
		
		excluded = find_dup(image, EXCLUDE_PATH)
		if check_dups:
			duplicate = find_dup(image, DOWNLOAD_PATH)

		if excluded:
			blacklist(url)
			print(f"[-] IMAGE IS EXCLUDED. SKIPPING...")

		elif duplicate:
			print(f"[-] IMAGE IS DUPLICATE. SKIPPING...")

		elif not image:
			print("[-] IMAGE NOT FOUND. RETRYING...")

		else:
			download_image(image, file_name)
			print(f"[+] IMAGE {count} DOWNLOADED SUCCESSFULLY")
			count += 1

	driver.close()


def show_help():
	print("Missing argument: number of images")
	print("Please enter number of images you want to download")
	print("\nUSAGE: python3 prntsc.py <number_of_images> <check_duplicates>")


if __name__ == '__main__':
	if len(sys.argv) >= 2:
		N_IMAGES = int(sys.argv[1])
	else:
		show_help()
		sys.exit()


	if len(sys.argv) == 3 and sys.argv[2] == "True":
		main(True)
	else:
		main()