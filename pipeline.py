import cv2
import easyocr

from bs4 import BeautifulSoup as bs

reader = easyocr.Reader(['en'])

# Extracts text from an image and returns 
def extract_text(image_path: str) -> list[str]:
    image = cv2.imread(image_path)

    # Preprocess image
    gray         = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text_results = reader.readtext(gray)

    print(text_results)

    # Find and group text
    lines = []
    for (bbox, word, conf) in text_results:
        if len(lines) == 0:
            lines.append([(bbox, word, conf)])
            continue

        
        for l in lines:
            




def process_annotations(image_path: str, url_link: str):
    # load image

    # process and return relevant information (image, text)


        # extract text and sort into categories, position on page, overall topic
            # beautifulsoup scrape web page for text
            

        # locate and identify annotations
            # TO-DO: self-trained or pretrained+finetuned

    pass

extract_text('test.png')