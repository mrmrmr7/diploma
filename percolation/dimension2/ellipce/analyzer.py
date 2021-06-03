from scipy.spatial.distance import euclidean as dist
from scipy.spatial.distance import euclidean as distance
import math as m
import random
from operator import itemgetter as get


class Analyzer:
    def split_on_clusters(self, ellipces, coef):
        markers = {i.index: i.index for i in ellipces}
        for i in range(len(ellipces)):
            for j in [*range(0, i), *range(i + 1, len(ellipces))]:
                if ellipces[i].is_intersect(ellipces[j], coef):
                    i_marker = markers[ellipces[i].index]
                    j_marker = markers[ellipces[j].index]
                    circles_with_marker_i = [
                        k for k, v in markers.items() if v == i_marker]
                    for c in circles_with_marker_i:
                        markers[c] = j_marker
        clusters = {i: [] for i in set(markers.values())}
        for k, v in markers.items():
            clusters[v] = clusters[v] + [k]
        return clusters

    def get_clusters_ranges(self, circles, clusters):
        clusters_ranges = {}

        for k, v in clusters.items():
            cluster_circles = [i for i in circles if i.index in v]
            min_x = min([c.x for c in cluster_circles])
            max_x = max([c.x for c in cluster_circles])
            min_y = min([c.y for c in cluster_circles])
            max_y = max([c.y for c in cluster_circles])

            clusters_ranges[k] = {'min_x': min_x, 'max_x': max_x,
                                  'min_y': min_y, 'max_y': max_y, }

        return clusters_ranges

    def _get_biggest_cluster(self, clusters_ranges):
        sizes = [(k, v['max_x'] - v['min_x'])
                 for k, v in clusters_ranges.items()]
        return max(sizes, key=lambda x: x[1])

    def get_biggest_cluster(self, ellipces, coef):
        clusters = self.split_on_clusters(ellipces, coef)
        clusters_ranges = self.get_clusters_ranges(ellipces, clusters)
        biggest_cluster_number = self._get_biggest_cluster(clusters_ranges)

        cluster_max = [biggest_cluster_number[0],
                       *(clusters[biggest_cluster_number[0]])]
        biggest_cluster = [c for c in ellipces if c.index in cluster_max]

        return biggest_cluster, {'size': biggest_cluster_number[1] + 2 * ellipces[0].a}
