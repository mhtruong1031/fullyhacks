import cv2
import easyocr

from pix2text import Pix2Text

reader = easyocr.Reader(['en'])
p2t    = Pix2Text()

# Extract LaTeX
def extract_latex_items(image_path: str) -> list[dict]:
    return p2t.recognize_text_formula(image_path, resized_shape=768, return_text=False)

# Extracts text from an image and returns 
def extract_text(image_path: str) -> list[str]:
    image = cv2.imread(image_path)

    # Preprocess image
    gray         = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text_results = reader.readtext(gray)

    # Find and group text
    lines   = [] # Lines with metadata
    for result in text_results:
        bbox, word, conf = result
        word             = word.lower()

        w_upper, w_lower = bbox[0][1], bbox[2][1] # Current word y_value bounds
        found = False

        for line in lines:
            l_bbox           = line[0][0]
            l_lower, l_upper = l_bbox[0][1], l_bbox[2][1] # Line bounds

            if l_lower <= w_lower <= l_upper or l_lower <= w_upper <= l_upper: # Test for overlap
                line.append((bbox, word, conf))
                found = True
                break

        if not found:
            lines.append([(bbox, word, conf)])

    lines_w = [] # Lines with only words
    for line in lines:
        line.sort(key=lambda x: x[0][0][0]) # Sort by left to right
        words = [word[1] for word in line] # Grab only words

        lines_w.append(words)
    
    return [" ".join(line) for line in lines_w]