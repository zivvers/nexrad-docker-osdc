# DOCKERIZED JUPYTER NOTEBOOK TO RUN *"DE-BUGGING" NEXRAD LEVEL 2 PLOTTING - DOCKERIZED* tutorial

*"DE-BUGGING" NEXRAD LEVEL 2 PLOTTING - DOCKERIZED* is meant to be a more advanced tutorial for Griffin users who are already experienced at plotting and animation production in Python. It leaves most of the Python code "under the hood" in favor of using Docker containers to execute Python scripts. While Docker might seem like overkill for a simple plotting application, using this tutorial to learn Docker will enable a Griffin user to develop more sophisticated Docker implementations with all the benefits that Docker offers. 

### SECTION I: Deploying Jupyter Docker container

1. Build `jupyter_dood` Docker image

    ```
	cd /home/ubuntu/docker_images/jupyter_dood
	docker build -t 'jupyter_dood' .
    ```

2. *From your Local Machine (e.g. your laptop)*:add following lines to ~/.ssh (replacing \<OSDC username\> with your OSDC username)

    ```
        Host 172.17.*
        User ubuntu
        ProxyCommand ssh <OSDC username>@griffin.opensciencedatacloud.org nc %h %p 2> /dev/null
    ```

3. *From Griffin VM* run Docker container with jupyter_dood Docker image

    ```
	docker run -it -v /var/run/docker.sock:/var/run/docker.sock -v /home/ubuntu/docker_images:/home/jovyan/work/docker_images \
		-v /home/ubuntu/nexrad:/home/jovyan/work/nexrad -p 8888:8888 jupyter_dood
    ```

4. *From your Local Machine*

    ```
        ssh -L <local port>:localhost:<griffin port> -N <Griffin VM IP Address>
    ```
        replacing \<griffin port\> with \<port\> given in `jupyter notebook --no-browser` output as

        > The Jupyter Notebook is running at: http://[all ip addresses on your system]:\<port\>/ 

4. *From your Local Machine*

    open browser, enter `http://localhost:<local port>`	


### SECTION II: What are these directories and files?

- `docker_images`: directory with sub-directories for Docker images
    - `animation_maker`: directory to make animation making Docker image
	- `Dockerfile`: file to build this environment
    - `jupyter_dood`: directory to make Jupyter Notebook Docker image
	- `Dockerfile`: file to build this environment
    - `plot_maker`: directory to make plotting Docker image
	- `Dockerfile`: file to build this environment
- `nexrad`: directory shared among Docker containers to NEXRAD L2 manipulation
   - `animation_html`: directory into which we will save animation HTML files
   - `animation_maker.py`: Python file to produce animation from static NEXRAD plots
   - `filtered_nexrad_plotter.py`: Python file to produce filtered plots of NEXRAD L2 data
   - `input_files`: directory into which we will download NEXRAD L2 files
   - `mayfly_arks.txt`: file containing ark IDs for relevant NEXRAD L2 data
   - `NEXRAD_Docker_Notebook.ipynb`: Jupter Notebook for tutorial
   - `output_plots` directory into which we will save weather radar plots
   - `unfiltered_nexrad_plotter.py`: Python file to produce raw plots of NEXRAD L2 data
