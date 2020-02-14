# Nipype, Arcana and Banana CVL Workshop - Melbourne, Nov 2019/Sydney, Feb 2020

[![GitHub issues](https://img.shields.io/github/issues/MonashBI/nipype_arcana_workshop.svg)](https://github.com/MonashBI/nipype_arcana_workshop/issues/)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/MonashBI/nipype_arcana_workshop.svg)](https://github.com/MonashBI/nipype_arcana_workshop/pulls/)
[![GitHub contributors](https://img.shields.io/github/contributors/MonashBI/nipype_arcana_workshop.svg)](https://GitHub.com/MonashBI/nipype_arcana_workshop/graphs/contributors/)
[![GitHub Commits](https://github-basic-badges.herokuapp.com/commits/MonashBI/nipype_arcana_workshop.svg)](https://github.com/MonashBI/nipype_arcana_workshop/commits/master)
[![GitHub size](https://github-size-badge.herokuapp.com/MonashBI/nipype_arcana_workshop.svg)](https://github.com/MonashBI/nipype_arcana_workshop/archive/master.zip)
[![GitHub HitCount](http://hits.dwyl.io/MonashBI/nipype_arcana_workshop.svg)](http://hits.dwyl.io/MonashBI/nipype_arcana_workshop)
[![Docker Hub](https://img.shields.io/docker/pulls/monashbi/nipype_arcana_workshop.svg?maxAge=2592000)](https://hub.docker.com/r/monashbi/nipype_arcana_workshop/)

This repository contains everything for the *Automating Neuroimaging Analysis Workflows with Nipype, Arcana and Banana* workshop, which was held at Swinburne University on the 15 of November 2019 and Sydney University on the 10th of February 2020. Many of the materials for this course have been adapted from [Michael Notter's](https://github.com/miykael) excellent [Nipype tutorial](https://github.com/miykael/nipype_tutorial) and a series of workshops he and [Peer Herholz](https://github.com/PeerHerholz) have run on "Python in neuroimaging" ([Cambridge 2018](https://nbviewer.jupyter.org/github/miykael/workshop_cambridge/blob/master/program.ipynb) and [Marburg 2019](https://nbviewer.jupyter.org/github/PeerHerholz/workshop_marburg/blob/master/program.ipynb)).

If you get access to the Characterisation Virtual Laboratory (CVL) before the workshop (recommended option) then all the software tools requirements are already installed and ready for you to use. To create an account on CVL@ MASSIVE you need your institutional email. Follow the instructions here: https://www.cvl.org.au/cvl-desktop/cvl-accounts and join project `fs97`. The CVL aims at giving you (and researchers in Australia) resources such as compute nodes, RAM and GPU to do computational analysis through a virtual desktop. It has all the software required installed and runs using the high performance compute power of MASSIVE. If you have specific questions or issues with the creation of your account, feel free to email help@massive.org.au or check the useful documentation https://docs.massive.org.au/.

Once you have an account please follow the instructions under "Configuring your CVL Account" on the [program](https://nbviewer.jupyter.org/github/MonashBI/nipype_arcana_workshop/blob/master/program.ipynb) to get up and running.

If you would like to run the materials from your own system there are (at least) three ways that you can configure it, make sure you do this before the day of the workshop:

## 1. Docker

Probably the easiest way to go through the workshop material is to use the docker image `monashbi/nipype_arcana_workshop`. It provides the computational environment to run the notebooks on any system with all necessary dependencies installed. To install [Docker](https://www.docker.com/) on your system, follow one of those links:

 - [Ubuntu](https://docs.docker.com/engine/installation/linux/ubuntu/) or [Debian](https://docs.docker.com/engine/installation/linux/docker-ce/debian/)
 - [Windows 7/8/9/10](https://docs.docker.com/toolbox/toolbox_install_windows/) or [Windows 10Pro](https://docs.docker.com/docker-for-windows/install/)
 - [macOS (from El Capitan 10.11 on)](https://docs.docker.com/docker-for-mac/install/) or [macOS (before El Capitan 10.11)](https://docs.docker.com/toolbox/toolbox_install_mac/).

Once Docker is installed, open up the docker terminal and test if it works with the command: `docker run hello-world`

**Note:** Linux users might need to use ``sudo`` to run ``docker`` commands or follow the [post-installation steps](https://docs.docker.com/engine/installation/linux/linux-postinstall/).

Once docker is running on your system you can continue with downloading the docker image for this workshop. For this use the command:

`docker pull monashbi/nipype_arcana_workshop`

Once the download finished, proceed with the following steps:

1. Run the following command in a terminal: ```docker run -it -p 8888:8888 monashbi/nipype_arcana_workshop```
2. Copy paste the link that looks like ```http://20f109eba8e4:8888/?token=0312c1ef3b61d7a44ff5346d3d150c23249a548850e13868``` into your webbrowser.
3. Replace the hash number ```20f109eba8e4``` after `http://` with `localhost` or your local IP (probably `192.168.99.100`) if you're on windows.
4. Once Jupyter Notebook is open, click on the `program.ipynb` notebook, and you're good to go.

And if you want to have **access to the output data created within the docker container**, add the command  `-v /path/to/your/output_folder:/output` before `monashbi/nipype_arcana_workshop`, where `/path/to/your/output_folder` should be a folder on your system, such as `/User/your_account/Documents/projectBanana/output`.

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

If you already have the following software dependencies installed on your workstation (or are only doing the non-neuroimaging notebooks):

* convert3d >=1.0
* ants >=2.3
* fsl >=6.0
* graphviz >=2.30
* matlab >=r2018a

you can use pip or conda to create the necessary python environment to run the notebooks. While it is possible to install the dependencies globally on your system it is highly recommended to virtualise your installation so it doesn't mess up any other programs that you use.

### Option 1: Python 3 + Pip + Venv

`Pip` and `Venv` are built in to Python 3 and are pretty easy to use. However, sometimes a Python package might depend on a non-Python library that needs
to be installed separately. To install these non-Python dependencies it is strongly recommended to use a "package manager" such as [Homebrew](http://brew.sh) (macOS), [Chocolately](http://chocolatey.org) (Windows) or apt/yum (Linux).

1. Install Python 3 (NB: version 2 won't work) on your system using a package manager
2. Create a virtual environment somewhere on your system `python3 -m venv /path/to/your/venv` (replace '/' with '\\' on Windows)
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

Once you have your virtual environment installed (either by `venv` or `conda`) you should clone this repository, download the test data and start Jupyter notebook with the following commands:

1. Using [Git](https://git-scm.com), clone [this repository](https://github.com/MonashBI/nipype_arcana_workshop/archive/master.zip) somewhere sensible on your workstation i.e. (`~/git/arcana-workshop`).
2. Download the ["A test-retest fMRI dataset for motor, language and spatial attention functions" dataset by Gorgolewski et al.](https://openneuro.org/datasets/ds000114/versions/00003) + derivatives using [Datalad](https://www.datalad.org) in the 'notebooks/data' sub-directory of the cloned repository.
   ```bash
   cd notebooks/data
   datalad install -r ///workshops/nih-2017/ds000114
   cd ds000114
   datalad update -r
   datalad get -r .
   ```
3. Symlink the `$FSLDIR/data/atlases` directory into the `notebooks/data` sub-directory
4. Create the `notebooks/data/output` directory
5. Go to the root of the cloned repo and run the following command: `jupyter notebook program.ipynb`. This should open a new window in your browser with the address 'http://localhost:8888'.


## 3. Jupyter NBViewer

All the notebooks can be looked at via [Jupyter nbviewer](https://nbviewer.jupyter.org/github/MonashBI/nipype_arcana_workshop/blob/master/program.ipynb). Like this you can see everything but cannot really interact with the scripts or run the code.
