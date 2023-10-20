# Import all required directries
import base64
import datetime
import os
import pytesseract
import cv2
from pyzbar.pyzbar import decode
from dbFunctionsItem import add_item, db_get_item_id
from textprocessing import get_dates, format_dates

# Setting pytesseract path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# -----------------------------------------------image functions
# to transform the image into black and white color code
def get_image(image_path):
    return cv2.imread(image_path)

def get_image_base64(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        image_url = f'/api/get_image/{os.path.basename(image_path)}'
    return image_data, image_url

def get_image_uri(image_path):
    return f'/api/get_image/{os.path.basename(image_path)}'

# to transform the image into black and white color code
def gray_image(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# function to rotate the image by 90 degree
def rotate_image(image):
    return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

def image_adaptive_treshold(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 23, 0)

def image_adaptive_treshold(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# function to fetch data from image
def get_text_pytesseract(gray_product_image):
    return pytesseract.image_to_string(gray_product_image, lang='eng' ,config='--psm 6') # Perform text extraction

def show_image(image):
    cv2.imshow('sample image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_barcode(image_path):
    image = cv2.imread(image_path) # Read the image
    barcodes = decode(image) # Decode barcodes
    barcode_info = [] # Extract barcode information
    for barcode in barcodes:
        data = barcode.data.decode('utf-8')
        barcode_info.append(data)
    return barcode_info

def crop_image(image, num_rows, num_cols):
    height, width = image.shape # Get dimensions of the image
    if height > width:
        temp = num_rows
        num_rows = num_cols
        num_cols = temp
    part_height = height // num_rows # Calculate the height and width of each part
    part_width = width // num_cols
    cropped_parts = [] # Initialize a list to store cropped parts and their coordinates
    for i in range(num_rows): # Loop through the image and crop into parts
        for j in range(num_cols):
            y_start = i * part_height # Calculate coordinates for cropping
            y_end = (i + 1) * part_height
            x_start = j * part_width
            x_end = (j + 1) * part_width
            part = image[y_start:y_end, x_start:x_end] # Crop the part
            cropped_parts.append(part) # Append the cropped part and its coordinates to the list
    return cropped_parts   

# Process each cropped part with OCR
def get_text_from_images_pytesseract(cropped_parts):
    combined_text = ""
    for part in cropped_parts:
        part_text = pytesseract.image_to_string(part)
        combined_text += part_text + "\n"
    # print("Combined Text: ",combined_text)
    return combined_text

# -----------------------------------------------
# -----------------------------------------------
# scan image and get expiry date main Algorithm
def scan_image_and_get_expiry_date(cursor, user_id, front_image_path, back_image_path):
    expiry_date = '2000-10-21'
    max_rotations = 4
    formatted_dates = None
    image = get_image(back_image_path)
    image = gray_image(image)
    # print("outside the loop")
    for _ in range(max_rotations):
        text = get_text_pytesseract(image)
        dates = get_dates(text)
        print('dates', dates)
        formatted_dates = format_dates(dates)
        print('formatted_dates', formatted_dates)
        # print("inside the loop", _)
        if not formatted_dates:
            print("No valid date found in the image, croping the image and trying again.")
            cropped_image = crop_image(image, 3, 2)
            text = get_text_from_images_pytesseract(cropped_image)
            dates = get_dates(text)
            formatted_dates = format_dates(dates)
            # print("if one", _)
        if not formatted_dates:
            print("No valid date found in the image, rotating the image by 90 degree and trying again.", _)
            image = rotate_image(image)
            # print("if two", _)
        else:
            print('Identified dates: ', formatted_dates)
            break
    # try:
    print('before max date.')
    if formatted_dates:
        expiry_date = max(formatted_dates)
    print("Calling add_time with ", expiry_date)
        # time.sleep(5)
    add_item(cursor, user_id, front_image_path, back_image_path, expiry_date)
    print("Came back from add_item.")
    item_id = db_get_item_id(cursor, back_image_path)
        # time.sleep(5)
    print("Item_id values has been assigned.")

    # except:
        # print("No valid date identified in the image.")    
    
    return expiry_date, item_id    

# ----------------------------
