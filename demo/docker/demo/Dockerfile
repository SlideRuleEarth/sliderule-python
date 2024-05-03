FROM continuumio/miniconda3
MAINTAINER JP Swinski (jp.swinski@nasa.gov)

# Environment
ENV PYTHONPATH=/usr/local/lib

# Install SlideRule client
COPY environment.yml /environment.yml
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "sliderule_env", "/bin/bash", "-c"]
RUN conda install -c conda-forge voila

# Install Voila Demo
COPY voila_demo.ipynb /voila_demo.ipynb

# Local install of client (only if necessary)
COPY sliderule /sliderule
RUN cd /sliderule/clients/python && pip install .

# Entry point
COPY docker-entrypoint.sh /usr/local/etc/
ENTRYPOINT ["/bin/bash"]