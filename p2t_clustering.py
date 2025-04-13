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
    
        texts.append([item['text'] for item in sorted_output])

    return texts
