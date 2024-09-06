import argparse, requests, os, re
from pathlib import Path
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

downloaded_pages = set()

def program_args():
	parser = argparse.ArgumentParser(description="A Python Script that donwload files")
	parser.add_argument("url", type=str, help="The URL to download")
	parser.add_argument("-r", "--recursive", action="store_true", help="recursively downloads the images in a URL received as a parameter")
	parser.add_argument("-l", "--layers", type=int, default=5, help="indicates the maximum depth level of the recursive download. If not indicated, it will be 5.")
	parser.add_argument("-p", "--path", type=str, default="./data/", help=": indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.")
	return parser.parse_args()


def create_path_dir(path):
	Path(path).mkdir(parents=True, exist_ok=True)


def download_page(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
	}
	try:
		html = requests.get(url, headers=headers, timeout=10)
		return html
	except:
		print("Could not download data from " + url)
		return SyntaxError()


def download_images(page_html, path):
	soup = BeautifulSoup(page_html, 'html.parser')
	image_extensions = re.compile(r'.*\.(png|jpeg|jpg|gif|bmp)$')

	for img in soup.find_all('img'):
		img_src = img.get('src')
		if img_src and image_extensions.match(img_src):
			image_name = os.path.basename(img_src)
			try:
				print("\tDownloading img" + image_name + " from " + img_src)
				urlretrieve(img_src, (path + image_name))
			except:
				print("\tCould not download img" + image_name + " from " + img_src)
				continue
	print("Finished downloading images from page")


def extract_inner_urls(page_html):
	soup = BeautifulSoup(page_html, 'html.parser')
	image_extensions = re.compile(r'.*\.(png|jpeg|jpg|gif|bmp)$')

	links = []
	for a in soup.find_all('a', href=True):
		href = a['href']
		if not image_extensions.match(href):
			links.append(href)
	return links


def extract_images(url, args, layer):
	print("Extracting images from: " + url)
	try:
		response = download_page(url)
		if response.status_code == 200:
			downloaded_pages.add(url)
			download_images(response.text, args.path)
			urls = extract_inner_urls(response.text)
			if (args.recursive and layer > 0):
				for inner_url in urls:
					if (inner_url not in downloaded_pages):
						extract_images(inner_url, args, (layer - 1))
			else:
				return
		else:
			print("Error Downloading Page: " + str(response.status_code) + " " + response.reason)
	except:
		return


def main():
	args = program_args()
	create_path_dir(args.path)
	extract_images(args.url, args, args.layers)


if __name__ == "__main__":
	main()
