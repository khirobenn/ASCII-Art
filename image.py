from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from os.path import exists
import sys

# a string that contaons the characters from the least dense to the most dense
density = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
lenght_of_density = len(density)
moy = 256//lenght_of_density+1

font_size = 32

my_font = ImageFont.truetype("courier.ttf", size=font_size)

def main():
    if len(sys.argv) < 2 :
        print("Invalid arguments! (please put path of images you want to convert)")
        return
    
    for i in range(1, len(sys.argv)):
        indice = str(i) # number of the image
        image = load_image(sys.argv[i])  
        if image != -1 :

            file_name_array = sys.argv[i].split(".")
            extention = file_name_array[-1]
            file_name_array[-1] = "_ASCII"
            file_name = "".join(file_name_array) + "." + extention

            convert_to_ascii(image, file_name, sys.argv[i])
            close_image(image)

    return

# loading the image if it exists
def load_image(image_file):
    if not exists(image_file) :
        print(image_file + " doesn't exist, please make sure to put the right path to the image.")
        return -1
    image = Image.open(image_file)

    # resize the image
    new_width = 100 # You can choose the new width as you want and you can uncomment all the code below to return the original image
    if image.width > new_width :
        ratio = image.height / image.width
        image = image.resize((new_width, (int)(new_width*ratio)))
    
    return image

# converting the image to an image with ascii characters
def convert_to_ascii(resized_image, new_image_name, original_image_name):
    new_image = Image.new(mode="RGB", size=(resized_image.width*font_size, resized_image.height*font_size), color=(0, 0, 0))
    # new_image = Image.new(mode="RGB", size=(resized_image.width*font_size, resized_image.height*font_size), color=(255, 255, 255))
    draw_in_image = ImageDraw.Draw(new_image)

    for y in range(0, resized_image.height):
        for x in range(0, resized_image.width):
            pixel = resized_image.getpixel((x,y))
            average = (sum(pixel)//len(pixel))//moy
            draw_in_image.text((x*font_size, y*font_size), density[average], font=my_font, fill=(pixel[0], pixel[1], pixel[2]))

    print(original_image_name + " was converted successfully! "+ new_image_name + " was created.")
    new_image.save(new_image_name)
    print("")


# closing the image
def close_image(image):
    image.close()
    

# Calling main
main()
