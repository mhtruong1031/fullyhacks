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

def process_annotations(image_path: str, scale_factor: float = 1):
    latex_extract = extract_latex_items(image_path)
    text_clusters = cluster_p2t_output(latex_extract, scale_factor = scale_factor)

    prompts_list: list[str] = clusters_to_text(text_clusters)

    return prompts_list

# Returns center y_value
def get_position_center(position_array):
    return (position_array[2][1] + position_array[0][1]) / 2

def get_box_height(position_array):
    return abs(position_array[2][1] - position_array[0][1])

def cluster_p2t_output(p2t_output: list[dict], k: int = 2, scale_factor: float = 1):
    clusters = []

    p2t_output = sorted(p2t_output, key=lambda item: get_position_center(item['position']))

    # cluster shit
    for i, item in enumerate(p2t_output):
        self_position = item['position']
        y_center      = get_position_center(self_position)

        # Sort by y
        p2t_output = sorted(p2t_output, key=lambda x: get_position_center(x['position']))

        neighbors   = p2t_output[max(0, i - k): i + k + 1]
        h_neighbors = [get_box_height(neighbor['position']) for neighbor in neighbors] # includes self
        h_local     = sum(h_neighbors) / len(h_neighbors)

        threshold = h_local * scale_factor
        placed     = False

        for cluster in clusters:
            cluster_y = get_position_center(cluster[-1]['position'])

            if abs(y_center - cluster_y) < threshold:
                cluster.append(item)
                placed = True
                break

        if not placed:
            clusters.append([item])

    return clusters

def clusters_to_text(clusters: list[dict]) -> list[str]:
    texts = []

    for cluster in clusters:
        sorted_output = sorted(
            cluster,
            key=lambda item: (item['position'][0][1], item['position'][0][0])
        )
    
        [texts.append(item['text']) for item in sorted_output]

    return texts
