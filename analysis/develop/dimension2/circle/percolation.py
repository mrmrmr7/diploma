from scipy.spatial.distance import euclidean as dist
from operator import itemgetter

def is_intersect(c1, c2, d):
    return dist(itemgetter('x', 'y')(c1), 
                itemgetter('x', 'y')(c2)) <= d
    
def split_on_clusters(circles, radius, verbose=False):
    markers = { i['index']: i['index'] for i in circles }
    for i in range(len(circles)):
        for j in [*range(0, i), *range(i + 1, len(circles))]:
            if is_intersect(circles[i], circles[j], 3 * radius):
                i_marker = markers[circles[i]['index']]
                j_marker = markers[circles[j]['index']]
                circles_with_marker_i = [ k for k, v in markers.items() if v == i_marker ]
                for c in circles_with_marker_i:
                    markers[c] = j_marker
    clusters = { i: [] for i in set(markers.values()) }
    for k, v in markers.items():
        clusters[v] = clusters[v] + [k]
    return clusters


def get_clusters_ranges(circles, clusters, radius):
    clusters_ranges = { }
    
    for k, v in clusters.items():
        cluster_circles = [ i for i in circles if i['index'] in v ]
        min_x = min([ c['x'] - radius for c in cluster_circles ])
        max_x = max([ c['x'] + radius for c in cluster_circles ])
        min_y = min([ c['y'] - radius for c in cluster_circles ])
        max_y = max([ c['y'] + radius for c in cluster_circles ])
        
        clusters_ranges[k] = {  'min_x': min_x, 'max_x': max_x,
                                'min_y': min_y, 'max_y': max_y, }
        
    return clusters_ranges
    
def get_biggest_cluster(clusters_ranges): 
    sizes = [(k, v['max_x'] - v['min_x']) for k, v in clusters_ranges.items()]
    return max(sizes, key=lambda x: x[1])