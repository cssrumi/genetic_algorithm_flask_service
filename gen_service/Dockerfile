FROM pypy:3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# FIX for : Issue with fetching http://deb.debian.org/debian/dists/jessie-updates/InRelease with docker
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list

# Run python's package manager and install packages
#RUN apt-get update
#RUN apt-get install -y freetds-dev
RUN pip install --upgrade pip
#RUN pypy3 -m pip install cython
RUN pip install -r requirements.txt

# Run apt-get, to install the SSH server, and supervisor
#RUN apt-get update \
#    && apt-get install -y supervisor \
#    && rm -rf /var/lib/apt/lists/* \
#    && apt-get clean

# start scripts
#COPY scripts/runapp.sh /usr/bin/

# supervisor config
#ADD supervisor/app.conf /etc/supervisor/conf.d/

# Run the chmod command to change permissions on above file in the /bin directory
#RUN chmod 755 /usr/bin/runapp.sh
RUN chmod 755 /app/src/app.py

# Default environmental variables

# run commands in supervisor
#CMD ["supervisord", "-n"]
CMD ["pypy3", "src/app.py"]
