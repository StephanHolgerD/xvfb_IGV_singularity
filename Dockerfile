FROM continuumio/miniconda3

RUN conda install -c bioconda igv
RUN conda install -c conda-forge xvfbwrapper
RUN conda install -c conda-forge jupyterlab
RUN apt-get update
RUN apt-get install -y xvfb
RUN apt-get install -y libxtst6
ADD IGV-snapshot-automator /opt/IGV-snapshot-automator
ADD entry.sh /opt
RUN useradd -ms /bin/bash newuser
COPY IGV-snapshot-automator/igv /home/newuser/igv
RUN mkdir -p /home/newuser/output
RUN chmod 777 -R /home/newuser
RUN chmod 777 -R /opt
USER newuser
