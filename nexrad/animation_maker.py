#!/usr/bin/env python 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# this function must be fed: 
#	
#  	- file containing names of absolute file paths of .png after -f flag 
# 	- absolute path name of animation after -n flag
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib.image as mpimg
from tempfile import NamedTemporaryFile
from functools import partial
import argparse

    # initialize plot
fig = plt.figure(figsize=(9, 12))
    # 'get current axes' to make for easy plotting
ax = plt.gca()

#imobj = ax.imshow(np.zeros((100, 100)), origin='lower', alpha=1.0, zorder=1, aspect=1)
imobj = ax.imshow(np.zeros((100, 100)),origin='lower',aspect='auto')


# initialize image for animation
def init():
    imobj.set_data(np.zeros((100, 100)))
    return imobj,


# function to read single plot, display image
def animate(i, plot_files):
    #file_name = file_prefix + str(i) + '.png'
    file_name = plot_files[i]
    img = mpimg.imread(file_name)[-1::-1]
    imobj.set_data(img)
    plt.axis('off')
    return imobj,


def anim_to_html(anim):
    if not hasattr(anim, '_encoded_video'):
        with NamedTemporaryFile(suffix='.mp4') as f:
	    
	    file_name = f.name.encode('utf-8')
	    anim.save(file_name, fps=20, extra_args=['-vcodec', 'libx264'])
            video = open(file_name, "rb").read()
        anim._encoded_video = video.encode("base64")
    return VIDEO_TAG.format(anim._encoded_video)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='make animation of plots in .txt files')

    parser.add_argument('-f','--plots_file',type=argparse.FileType('r'), required=True)
    parser.add_argument('-n','--animation_name', type=str, required=True)
    args = parser.parse_args()
    
    # let's make this into a list!
    plot_files = [file_name.strip() for file_name in args.plots_file.readlines()]
    plot_files.sort()


    imobj = ax.imshow(np.zeros((100, 100)), origin='lower', alpha=1.0, zorder=1, aspect=1 )

    anim = animation.FuncAnimation(fig, partial(animate, plot_files=plot_files), init_func=init, 
				repeat = True, frames=range(0,len(plot_files)), 
                               	interval=10000, blit=True, repeat_delay=1000)

    # now let's embed the animation into some HTML
    VIDEO_TAG = """<video controls>
 	<source src="data:video/x-m4v;base64,{0}" type="video/mp4">
 	Your browser does not support the video tag.
	</video>"""

    html = anim_to_html(anim)
    anim_html_f = args.animation_name

    
    f = open(anim_html_f, 'w')
    f.write(html)
    f.close() 
