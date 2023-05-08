import json
import requests
import base64
import io
import sys, getopt
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def main(argv):
    imageurl = ''
    outfile = ''
    
    try:
        opts, args = getopt.getopt(argv,"i:m:o:",["imageurl=","message=","outfile="])
    except getopt.GetoptError:
        print('add-watermark.py -i <imageurl> -m <message> -o <outfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('add-watermark.py -i <imageurl> -m <message> -o <outfile>')
            sys.exit()
        elif opt in ("-i", "--imageurl"):
            imageurl = arg
        elif opt in ("-m", "--message"):
            message = arg
        elif opt in ("-o", "--outfile"):
            outfile = arg

    watermark(input_image_path=imageurl,
                text=message,
                pos=(0, 0), 
                output_image_path=outfile)

    return

def watermark(input_image_path,
                   text, pos, output_image_path):
    # read the image from the URL passed
    photo = Image.open(requests.get(input_image_path, stream=True).raw)
    
    # make the image editable
    drawing = ImageDraw.Draw(photo)
   
    # set the colours red or black
    black = (3, 8, 12)
    red = (255, 40, 3)
    
    # load the font and the colour based on the message
    font = ImageFont.truetype("Roboto-Black.ttf", 80)
    if "Not" in text:
        drawing.text(pos, text, fill=red, font=font)
    else:
        drawing.text(pos, text, fill=black, font=font)
    
    photo.save(output_image_path, format="JPEG")

    return

if __name__ == "__main__":
   main(sys.argv[1:])