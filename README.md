# Nipype, Arcana and Banana CVL Workshop - Melbourne 2019

[![GitHub issues](https://img.shields.io/github/issues/MonashBI/nipype_arcana_workshop.svg)](https://github.com/MonashBI/nipype_arcana_workshop/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/MonashBI/nipype_arcana_workshop.svg)](https://github.com/MonashBI/nipype_arcana_workshop/pulls/)
[![GitHub contributors](https://img.shields.io/github/contributors/MonashBI/nipype_arcana_workshop.svg)](https://GitHub.com/MonashBI/nipype_arcana_workshop/graphs/contributors/)
[![GitHub Commits](https://github-basic-badges.herokuapp.com/commits/MonashBI/nipype_arcana_workshop.svg)](https://github.com/MonashBI/nipype_arcana_workshop/commits/master)
[![GitHub size](https://github-size-badge.herokuapp.com/MonashBI/nipype_arcana_workshop.svg)](https://github.com/MonashBI/nipype_arcana_workshop/archive/master.zip)
[![GitHub HitCount](http://hits.dwyl.io/MonashBI/nipype_arcana_workshop.svg)](http://hits.dwyl.io/MonashBI/nipype_arcana_workshop)
[![Docker Hub](https://img.shields.io/docker/pulls/MonashBI/nipype_arcana_workshop.svg?maxAge=2592000)](https://hub.docker.com/r/MonashBI/nipype_arcana_workshop/)

This repository contains everything for the *Automating Neuroimaging Analysis Workflows with Nipype, Arcana and Banana* workshop to be held at Swinburne University on the 15 of November 2019 [(registration)](https://www.eventbrite.com.au/e/automating-neuroimaging-analysis-workflows-with-nipype-arcana-and-banana-registration-69832758661). Many of the materials for this course have been adpated from [Michael Notter's](https://github.com/miykael) excellent [Nipype tutorial](https://github.com/miykael/nipype_tutorial) and a series of workshops on "Python in neuroimaging" he and [Peer Herholz](https://github.com/PeerHerholz) have run ([Cambridge 2018](https://nbviewer.jupyter.org/github/miykael/workshop_cambridge/blob/master/program.ipynb) and [Marburg 2019](https://nbviewer.jupyter.org/github/PeerHerholz/workshop_marburg/blob/master/program.ipynb)).

If you have access to the [Characterisation Virtual Laboratory (CVL)](https://www.cvl.org.au) then all the requirements are already installed and ready for you to use. However, if you would like to run the materials from your own system there are (at least) three ways that you can configure it:

## 1. Docker

Probably the easiest way to go through the workshop material is to use the docker container `MonashBI/nipype_arcana_workshop`. It provides the computational environment to run the notebooks on any system with all necessary dependencies installed. To install [Docker](https://www.docker.com/) on your system, follow one of those links:

 - [Ubuntu](https://docs.docker.com/engine/installation/linux/ubuntu/) or [Debian](https://docs.docker.com/engine/installation/linux/docker-ce/debian/)
 - [Windows 7/8/9/10](https://docs.docker.com/toolbox/toolbox_install_windows/) or [Windows 10Pro](https://docs.docker.com/docker-for-windows/install/)
 - [macOS (from El Capitan 10.11 on)](https://docs.docker.com/docker-for-mac/install/) or [macOS (before El Capitan 10.11)](https://docs.docker.com/toolbox/toolbox_install_mac/).

Once Docker is installed, open up the docker terminal and test if it works with the command: `docker run hello-world`

**Note:** Linux users might need to use ``sudo`` to run ``docker`` commands or follow the [post-installation steps](https://docs.docker.com/engine/installation/linux/linux-postinstall/).

Once docker is running on your system you can continue with downloading the docker image for this workshop. For this use the command:

`docker pull MonashBI/nipype_arcana_workshop`

Once the download finished, proceed with the following steps:

1. Run the following command in a terminal: ```docker run -it --rm -p 8888:8888 MonashBI/nipype_arcana_workshop```
2. Copy paste the link that looks like ```http://20f109eba8e4:8888/?token=0312c1ef3b61d7a44ff5346d3d150c23249a548850e13868``` into your webbrowser.
3. Replace the hash number ```20f109eba8e4``` after `http://` with `localhost` or your local IP (probably `192.168.99.100`) if you're on windows.
4. Once Jupyter Notebook is open, click on the `program.ipynb` notebook, and you're good to go.

And if you want to have **access to the output data created within the docker container**, add the command  `-v /path/to/your/output_folder:/output` before `MonashBI/nipype_arcana_workshop`, where `/path/to/your/output_folder` should be a free folder on your system, such as `/User/your_account/Desktop/output`.

## Some useful Docker Commands

    Show running containers
    $ docker ps

    Show all installed Docker images
    $ docker images

    Show all (also stopped) containers
    $ docker ps -a

    Remove a container
    $ docker rm $CONTAINER_ID

    Remove a docker image
    $ docker rmi -f $IMAGE_ID

    Start a stopped container & attach to it
    $ docker start -ia $CONTAINER_ID

**Note**: when you stop a container (Ctrl-C), and then re-execute above "docker run" command, you will end up with a second container. If you want to access your previous container (e.g. with downloaded data), you must reconnect to it (see "docker start -ia" command below).



## 2. Native installation in virtual environment

If you don't care about some of the software dependencies, or have them already installed on your system, you can use pip or conda to create the necessary python environment to run the notebooks. While it is possible to install the dependencies globally on your system it is highly recommended to virtualize your installation so it doesn't mess up any other programs that you use.

### Option 1: Python 3 + Pip + Venv

`Pip` and `Venv` are built in to Python 3 and are pretty easy to use. However, sometimes a Python package might depend on a non-Python library that needs
to be installed separately. To install these non-Python dependencies it is strongly recommended to use a "package manager" such as [Homebrew](http://brew.sh) (macOS), [Chocolately](http://chocolatey.org) (Windows) or apt/yum (Linux).

1. Install Python 3 (NB: version 2 won't work) on your system using a package manager
2. Create a virtual environment somewhere on your system `python3 -m venv /path/to/your/venv` (replace '/' with '\' on Windows)
3. Activate the virtual environment `source /path/to/your/virtual-env/bin/activate` (`\path\to\virtual-env\Scripts\activate` on Windows)
4. Install the requirements in the virtualenv `pip3 install -r https://raw.githubusercontent.com/MonashBI/nipype_arcana_workshop/master/requirements.txt`.

NB: To deactivate the virtualenv afterwards run `deactivate`, and to reactivate it again just repeat Step 3.

### Option 2: Conda

Conda integrates package management for Python and non-Python dependencies into a single cross-platform system. It is therefore perhaps the simplest solution for native installation. However, if you install a lot of (obscure) packages you may find one that isn't supported by Conda and then it gets a bit tricky. This is why I personally prefer the Pip + Venv approach but for 99% of use cases they are interchangeable.

1. If you haven't yet, get conda on your system: https://conda.io/miniconda.html
2. Download the `environment.yml` file from [here].(https://github.com/MonashBI/nipype_arcana_workshop/blob/master/environment.yml)
3. Open up a conda terminal (or any other terminal), and create a new conda environment with the following command: `conda env create --name workshop --file /path/to/file/environment.yml`
4. Activate the conda environment with `source activate workshop` (for mac and linux) or with `activate workshop` (for windows)

### Opening up the notebook

Once you have your virtual environment installed (either by `venv` or `conda`) you should download this repository and start Jupyter notebook with the following commands:

1. Download the notebooks in this repository ([here](https://github.com/MonashBI/nipype_arcana_workshop/archive/master.zip)), save them in the desired location, i.e. (`Desktop/workshop`).
2. Download the three datasets [adhd](https://www.dropbox.com/sh/wl0auzjfnp2jia3/AAChCae4sCHzB8GJ02VHGOYQa?dl=1), [ds000114](https://www.dropbox.com/sh/s0m8iz8fer3j5el/AACMamy4DyTMHMBud1IVgEDka?dl=1) and [ds000228](https://drive.google.com/file/d/1TWMVjjsBzWJvOx_uq-YVbJU4Yw0Ob0Wh/view?usp=sharing) and put them into the workshop folder, i.e. (`Desktop/workshop`).
3. Go into the folder where you saved the just downloaded notebooks (i.e. `Desktop/workshop`) and run the following command from the folder that contains the `program.ipynb` notebook: `jupyter notebook program.ipynb`


## 3. Jupyter NBViewer

All the notebooks (but not the slides) can be looked at via [Jupyter nbviewer](https://nbviewer.jupyter.org/github/MonashBI/nipype_arcana_workshop/blob/master/program.ipynb). Like this you can see everything but cannot really interact with the scripts or run the code.
