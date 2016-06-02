#!/usr/bin/env python 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# this function must be fed: 
#
#	- nexrad file names (absolute path ONLY) after -f flag
# 	- output directory (absolute path) after -d flag
#	- name of file to put plot names into after -p flag 
#	- (optional) -b flag if want bioscatter, not weather
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import pyart
import argparse
import os.path
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.animation as animation
import matplotlib.image as mpimg
import matplotlib as mpl
from functools import partial

# takes 3 numpy arrays, returns array 
# where 2 of 3 arrays must have True for
# returned array to have True
def two_true(a,b,c):
    return np.logical_or(
            np.logical_and(a, np.logical_or(b,c)),
            np.logical_and(c, np.logical_or(a,b)),
            np.logical_and(b, np.logical_or(c,a))
            )

def plot_filtered_nexrad(nexrad_file, bioscatter):
 
    fig = plt.figure(figsize=(9, 12))
    ax = fig.add_subplot(111)
    
    radar = pyart.io.read_nexrad_archive(nexrad_file)
    refl_grid = radar.get_field(0, 'reflectivity')
    rhohv_grid = radar.get_field(0, 'cross_correlation_ratio')
    zdr_grid = radar.get_field(0, 'differential_reflectivity')

    # filter the data by making numpy arrays of boolean variables
    refl_high = np.greater_equal(refl_grid, 12)
    rhohv_high = np.greater_equal(rhohv_grid, .99)
    zdr_low = np.less(np.abs(zdr_grid), 2.3)
    

    this_is_weather = two_true(refl_high, rhohv_high,zdr_low)
    
    if bioscatter:
        
        mask = this_is_weather
    
    else:
        
        mask = np.logical_not(this_is_weather)
    
    # mask the data
    QC_refl_grid = np.ma.masked_where(mask,refl_grid)
    
    # extract weather sweeps from original radar data
    qc = radar.extract_sweeps([0])
    # replace reflectivity in original weather sweep with QC reflectivity
    qc.add_field_like('reflectivity', 'reflectivityqc', QC_refl_grid)
    
    # set up pyart display of data
    display = pyart.graph.RadarMapDisplay(qc)
    # plot data over map of area
    display.plot_ppi_map('reflectivityqc',0, 
        min_lat=radar.latitude['data'][0]-2.5, max_lat=radar.latitude['data'][0]+2.5, 
        min_lon=radar.longitude['data'][0]-2.5, max_lon=radar.longitude['data'][0]+2.5,
        lat_0=radar.latitude['data'][0], lon_0=radar.longitude['data'][0],
        ax=ax #attach to fig
    )

    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
    plt.show()
    return fig



def save_figures(plot_function, radar_files, output_dir, file_prefix=''):
    plot_file_names = []
    for nexrad_file in radar_files:
        plot_fig = plot_function(nexrad_file)

        # make plot file name out of radar file name
	relative_plot_name = file_prefix + nexrad_file.split('/')[-1].split('.gz')[0]

	plot_file_name = os.path.join(output_dir, relative_plot_name) + '.png' 
	plot_file_names.append(plot_file_name)
        plot_fig.savefig(plot_file_name, format='png') #save plot as png
        
    return plot_file_names



if __name__ == "__main__":
	# set up command line argument parsing
	parser = argparse.ArgumentParser(description='Make unfiltered plot(s) of NEXRAD L2 Data')

	parser.add_argument('-f', '--files', type=str, nargs='+',required=True)
	parser.add_argument('-d', '--output-dir', type=str, required=True)
	parser.add_argument('-p', '--plot-file-file', type=str, required=True)
	parser.add_argument('-b', '--bioscatter', action='store_true') 
	parser.add_argument('-n', '--file-name-prefix', type=str)

	args = parser.parse_args()

	# get arguments supplied on command line
	output_dir = args.output_dir
	input_files = args.files
	plot_file_f = args.plot_file_file
	bioscatter = args.bioscatter
	plot_file_prefix = args.file_name_prefix

	# concatenate for full input file path
	input_nexrad_abs_files = args.files


	# check that those files exist before plotting
	assert(all(os.path.isfile(f) for f in input_nexrad_abs_files))

	
	# make and save plots!
	
	if plot_file_prefix is not None:
	    plot_file_names = save_figures(partial(plot_filtered_nexrad, bioscatter=bioscatter), input_nexrad_abs_files, output_dir, plot_file_prefix)
	
	else:
	    plot_file_names = save_figures(partial(plot_filtered_nexrad, bioscatter=bioscatter), input_nexrad_abs_files, output_dir)

	# write plot file names to file
	plot_file_names_f = [os.path.join(output_dir,file_name) for file_name in plot_file_names]
	
	f = open(os.path.join(output_dir, plot_file_f), 'w')
	f.write('\n'.join(plot_file_names_f))
