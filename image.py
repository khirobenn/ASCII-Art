from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from os.path import exists
import sys

# a string that contaons the characters from the least dense to the most dense
density = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
lenght_of_density = len(density)
moy = 256//lenght_of_density+1

font_size = 16
my_font = ImageFont.truetype("courier.ttf", font_size)

new_width = 100

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
    if image.width > new_width :
        ratio = image.height / image.width
        image = image.resize((new_width, (int)(new_width*ratio)))
    
    return image

# converting the image to an image with ascii characters
def convert_to_ascii(resized_image, new_image_name, original_image_name):
    new_image = Image.new(mode="RGB", size=(resized_image.width*font_size, resized_image.height*font_size), color=(0, 0, 0))
    draw_in_image = ImageDraw.Draw(new_image)

    for y in range(0, resized_image.height):
        for x in range(0, resized_image.width):
            r, g, b = (0, 0, 0)
            pixel = resized_image.getpixel((x,y))

            # Checking the type of pixel (it can be different from an image to another)
            if type(pixel).__name__ == "tuple" :
                pixel_length = len(pixel)
                # Now we are checking the pixel tuple length, a pixel can be represented by (Red value, Green value, Blue value, Alpha value) or less than that
                if pixel_length == 4: 
                    r, g, b, a = pixel
                    if a == 0:
                        continue # it is transparent we don't have to write anything
                elif pixel_length == 3:
                    r, g, b = pixel
                elif pixel_length == 2:
                    r, g = pixel
            else:
                r = pixel

            average = 0

            if type(pixel).__name__ == "tuple" :
                average = ((r+g+b)//pixel_length)//moy
            else :
                average = r//lenght_of_density

            draw_in_image.text((x*font_size, y*font_size), density[average], font=my_font, fill=(r, g, b))
            
    print(original_image_name + " was converted successfully! "+ new_image_name + " was created.")
    new_image.save(new_image_name)
    print("")


# closing the image
def close_image(image):
    image.close()
    

# Calling main
main()