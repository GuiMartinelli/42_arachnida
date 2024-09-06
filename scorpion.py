import argparse
from PIL import Image
from PIL.ExifTags import TAGS

def program_args():
	parser = argparse.ArgumentParser(description="A Python Script that get Metadata from image files")
	parser.add_argument("images", nargs="+", type=str, help="Image files to get Metadata")
	return parser.parse_args()

def open_image(path):
	image = Image.open(path)
	return image

def get_basic_data(image):
	print(f"Format: {image.format}")
	print(f"Size: {image.size}")
	print(f"Mode: {image.mode}")

def get_metadata(image):
	exif_data = image._getexif()
	if exif_data is None:
		print('This image has no exif data.')
	else:
		for tag, value in exif_data.items():
			tag_name = TAGS.get(tag, tag)
			print(f"{tag_name}: {value}")

def main():
	args = program_args()
	for img in args.images:
		try:
			image = open_image(img)
			print("Getting Metadata from " + img)
			get_basic_data(image)
			get_metadata(image)
		except FileNotFoundError:
			print("Error: " + img + " not found")
			continue
	return

if __name__ == "__main__":
	main()
