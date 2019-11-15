FROM kbase/sdkbase2:python
MAINTAINER KBase Developer
# -----------------------------------------
# In this section, you can install any system dependencies required
# to run your App.  For instance, you could place an apt-get update or
# install line here, a git checkout to download code, or run any other
# installation scripts.

# RUN apt-get update
RUN apt-get update
RUN apt-get install -y tzdata
RUN apt-get install -y git gcc-multilib  openjdk-8-jdk openjdk-8-jre-headless maven \
gnuplot ghostscript graphviz imagemagick python-matplotlib

RUN apt-get install wget

RUN wget https://github.com/CIDARLAB/cello/archive/develop.zip

RUN unzip develop.zip

RUN mv cello-develop cello

RUN cd ./cello/resources/library && bash install_local_jars.sh

RUN cd ./cello && mvn -e clean compile

# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
