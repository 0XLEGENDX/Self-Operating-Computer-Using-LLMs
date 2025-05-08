import boto3
import ctypes
# Initialize client
textract = boto3.client('textract', region_name='us-east-1')


import ctypes


def get_screen_size():
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    return screen_width, screen_height

def fetch_ocr_response(imagePath):
    # Load image
    with open(imagePath, "rb") as document:
        image_bytes = document.read()
    
    response = textract.detect_document_text(Document={'Bytes': image_bytes})
    return response


def extract_text(response):

    text = ""
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + " "

    f = open("temp.txt","w")
    f.write(text)

    return text


def extract_text_location(response, text):
    """
    Returns a list of bounding boxes for all lines in the Textract response that match the given text.
    Each bounding box is in normalized coordinates (Left, Top, Width, Height) from 0 to 1.
    """
    matches = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE' and item['Text'] == text:
            bbox = item['Geometry']['BoundingBox']
            matches.append({
                'Text': item['Text'],
                'BoundingBox': bbox
            })
    
    return matches


def get_click_points_from_matches(matches):
    """
    Given Textract matches with bounding boxes and screen resolution,
    returns a list of (x, y) pixel coordinates suitable for mouse clicks.
    
    Parameters:
        matches (list): List of dicts with 'Text' and 'BoundingBox'. 

    Returns:
        List[Tuple[int, int]]: List of (x, y) click points.
    """

    screen_width, screen_height = get_screen_size()
    print(screen_height,screen_width)
    click_points = []
    
    for match in matches:
        bbox = match['BoundingBox']
        left = bbox['Left'] * screen_width
        top = bbox['Top'] * screen_height
        width = bbox['Width'] * screen_width
        height = bbox['Height'] * screen_height

        center_x = int(left + width / 2)
        center_y = int(top + height / 2)

        click_points.append((center_x, center_y))

    return click_points


if(__name__=="__main__"):
    response = fetch_ocr_response(r"C:\Users\anura\OneDrive\Desktop\test_ocr.png")
    location = extract_text_location(response,"img (2).jpg")
    print(get_click_points_from_matches(location))