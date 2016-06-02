#!/usr/bin/env python 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# this function must be fed: 
#
#	- nexrad file names (absolute path ONLY) after -f flag
# 	- output directory (absolute path) after -d flag
#	- name of file to put plot names into after -p flag 
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



def plot_unfiltered_nexrad(nexrad_file):
    # initialize figure 
    fig = plt.figure(figsize=(7, 10))
    ax = fig.add_subplot(111)
    
    radar = pyart.io.read_nexrad_archive(nexrad_file)
    # set up pyart display of data
    display = pyart.graph.RadarMapDisplay(radar)
    
    # plot data over map of area
    display.plot_ppi_map('reflectivity',0, 
        min_lat=radar.latitude['data'][0]-2, max_lat=radar.latitude['data'][0]+2, 
        min_lon=radar.longitude['data'][0]-2, max_lon=radar.longitude['data'][0]+2,
        ax=ax #attach to fig
    )
   
     
    # let's check it out!
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
	parser.add_argument('-n', '--file-name-prefix', type=str)
	parser.add_argument('-p', '--plot-file-file', type=str, required=True)
	args = parser.parse_args()

	# get arguments supplied on command line
	output_dir = args.output_dir
	input_files = args.files
	plot_file_f = args.plot_file_file
 	plot_file_prefix = args.file_name_prefix	

	# concatenate for full input file path
	input_nexrad_abs_files = args.files

	# check that those files exist before plotting
	assert(all(os.path.isfile(f) for f in input_nexrad_abs_files))

	
	# make and save plots!
	if plot_file_prefix is None:

	    plot_file_names = save_figures(plot_unfiltered_nexrad, input_nexrad_abs_files, output_dir)

	else:
	    plot_file_names = save_figures(plot_unfiltered_nexrad, input_nexrad_abs_files, output_dir, plot_file_prefix)
	
	# write plot file names to file
	plot_file_names_f = [os.path.join(output_dir,file_name) for file_name in plot_file_names]
	
	f = open(os.path.join(output_dir, plot_file_f), 'w')
	f.write('\n'.join(plot_file_names_f))
