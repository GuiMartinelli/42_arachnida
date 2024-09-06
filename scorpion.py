import argparse, os.path, time
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
	print(f"\tCreation date: {time.ctime(os.path.getctime(image))}")
	print(f"\tModification date: {time.ctime(os.path.getmtime(image))}")
	print(f"\tSize file: {(os.path.getsize(image))}")


def print_info(info):
	for key, value in info.items():
		if key != 'exif':
			print(f"\t{key}: {value}")

def get_metadata(image):
	print_info(image.info)
	exif_data = image._getexif()
	if exif_data is None:
		print('\tThis image has no EXIF metadata.')
	else:
		for tag, value in exif_data.items():
			tag_name = TAGS.get(tag, tag)
			print(f"\t{tag_name}: {value}")


def main():
	args = program_args()
	for img in args.images:
		try:
			image = open_image(img)
			print("\nGetting Metadata from " + img)
			get_basic_data(img)
			get_metadata(image)
		except FileNotFoundError:
			print("Error: " + img + " Not Found")
			continue
	return


if __name__ == "__main__":
	main()
