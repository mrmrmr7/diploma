
import numpy as np

class Statistic:
    def __init__(self, figures=None, ranges=None):
        self.figures = figures
        self.axis_points = None
        self.axis_distributions = None
        self.axis_ranges = ranges

    def get_axis_points(self, figures=None):
        print("\nRetrieving axis points start.")
        figures = figures if figures else self.figures

        axis_points = {}
        axis_arr = figures[0].keys()
        for axis in axis_arr:
            axis_points[axis] = [] 

        for figure in figures:
            for axis in axis_arr:
                arr = axis_points[axis]
                arr.append(figure[axis])
                axis_points[axis] = arr

        self.axis_points = axis_points
        print("Retrieving axis points done\n")
        return axis_points

    
    def get_single_axis_distribution(self, data=None, axis_range=None, pocket_count=10):
        axis_range = next(iter(self.axis_ranges.values())) if not axis_range else axis_range
        h = axis_range / pocket_count
        distribution = np.zeros(pocket_count + 1)

        for v in data:
            distribution[int(v/h)] += 1

        return distribution[:-1]


    def get_axis_distributions(self, figures=None, pocket_count=10):
        print(f"\nFinding axis distributions start.")
        axis_points = self.axis_points if self.axis_points else self.get_axis_points(figures)
        axis_distributions = {}

        for axis, arr in axis_points.items():
            axis_distributions[axis] = self.get_single_axis_distribution(arr, pocket_count=pocket_count) 
        
        self.axis_distributions = axis_distributions
        print(f"Finding axis distributions done\n")
        return axis_distributions


    def get_uniform_fit(self, arr_to_fit=None, pocket_count=10):
        data = arr_to_fit if any(arr_to_fit) else self.axis_distributions
        xfit = np.arange(pocket_count) 
        np_fit = np.polyfit(xfit, data, 1) 
        fit_points = np_fit[0]*xfit + np_fit[1]
        return fit_points, np_fit[0]


    def get_all_statistic(self, figures=None, pocket_count=10):
        print("\nGetting all statistic start.")

        axis_points = self.get_axis_points(figures)
        axis_distributions = self.get_axis_distributions(figures, pocket_count=pocket_count)

        fits = {}
        is_uniform = {}
        a_val = {}
        for axis in axis_points.keys():
            fits[axis], a_fit_param = self.get_uniform_fit(axis_distributions[axis], pocket_count=pocket_count)
            a_val[axis] = a_fit_param
            is_uniform[axis] = abs(a_fit_param) < 0.2

        print("Getting all statistic done\n")
        return {
            'axis_points': axis_points,
            'axis_distributions': axis_distributions, 
            'axis_fits': fits, 
            'is_axis_uniform': is_uniform, 
            'fit_a_coef': a_val
            }

