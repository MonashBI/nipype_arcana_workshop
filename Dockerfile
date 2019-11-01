# Creates the docker container for the workshop in Cambridge
# Run the container with the following command:
#   docker run -it --rm -p 8888:8888 peerherholz/workshop_marburg

FROM miykael/nipype_tutorial:latest

ARG DEBIAN_FRONTEND=noninteractive

USER root

#------------------------------------
# Install HarvardOxford atlas via FSL
#------------------------------------

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
           fsl-harvard-oxford-atlases \
           fsl-harvard-oxford-cortical-lateralized-atlas \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#---------------------------------
# Update conda environment 'neuro'
#---------------------------------

USER neuro

COPY ["requirements.txt", "/requirements.txt"]

RUN conda install -y -q --name neuro bokeh \
                                     holoviews \
                                     plotly \
                                     dipy \
                                     vtk \
    && sync && conda clean -tipsy && sync \
    && bash -c "source activate neuro \
                && pip install  --no-cache-dir -r /requirements.txt" \
    && rm -rf ~/.cache/pip/* \
    && sync

#-----------------------------------------------
# Download workshop required part of the dataset
#-----------------------------------------------

RUN rm -rf /opt/conda/pkgs/*

USER neuro

RUN bash -c 'source activate neuro && datalad get -J 4 -r \
    /data/ds000114/dataset_description.json \
    /data/ds000114/dwi* \
    /data/ds000114/sub* \
    /data/ds000114/task-* \
    /data/ds000114/derivatives/freesurfer/sub-01 \
    /data/ds000114/derivatives/fmriprep/sub-01/ses-test/func/*fingerfootlips*'

#------------------------------------------------
# Copy workshop notebooks into image and clean up
#------------------------------------------------

USER root

COPY ["test_notebooks.py", "/home/neuro/workshop/test_notebooks.py"]

COPY ["program.ipynb", "/home/neuro/workshop/program.ipynb"]

COPY ["notebooks", "/home/neuro/workshop/notebooks"]

COPY ["slides", "/home/neuro/workshop/slides"]

RUN chown -R neuro /home/neuro/workshop

USER neuro

WORKDIR /home/neuro/workshop

RUN ln -s /data/ds000114 /usr/share/fsl/data/atlases notebooks/data/

RUN ln -s /output notebooks/

RUN mkdir -p ~/.jupyter && echo 'c.NotebookApp.ip = "0.0.0.0"' > ~/.jupyter/jupyter_notebook_config.py

RUN mkdir -p ~/.ipython/profile_default/startup/

RUN printf "import warnings\nwarnings.filterwarnings('ignore')" > ~/.ipython/profile_default/startup/disable-warnings.py

CMD ["jupyter-notebook", "program.ipynb"]
