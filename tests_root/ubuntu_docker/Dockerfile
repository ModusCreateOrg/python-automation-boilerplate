FROM ubuntu:xenial
MAINTAINER Sergiu Popescu <sergiu@moduscreate.com>

# Setting for packages installation
ENV DEBIAN_FRONTEND noninteractive

# Install openssh and lsb-release
RUN apt-get update && \
    apt-get install -y  openssh-server=1:7.2* lsb-release=9.20160110 \
                        net-tools=1.60*

# Setting the loginuid process attribute become optional
RUN sed -i 's/^(session\s+)required(\s+pam_loginuid.so)$/$1optional$2/g' \
    /etc/pam.d/sshd

# Ensure directory to store sshd pid exists
RUN mkdir -p /var/run/sshd

# Standard SSH port
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]


# Setting for packages installation
ENV DEBIAN_FRONTEND noninteractive

# Remove timesync systemd service
RUN rm /etc/systemd/system/sysinit.target.wants/systemd-timesyncd.service

# Usefull to have systemd functionnal
CMD ["/sbin/init"]


# Install apt-utils
RUN apt-get update && \
    apt-get install -y --no-install-recommends --assume-yes apt-utils

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl git-core build-essential git libreadline-dev \
                       zlib1g-dev libssl-dev libbz2-dev libsqlite3-dev \
                       zip unzip


# Install pyenv
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN echo $PATH
RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | sh

#Install Python v2.7.6 and pip v1.5.4
RUN pyenv install 2.7.6
RUN pyenv global 2.7.6
RUN pip install -U pip==1.5.4


# Install nvm v0.33.11, node v8.11.2 and set it as default
ENV NVM_ROOT /root/.nvm
ENV NODE_VERSION 8.11.2
RUN echo $PATH
RUN curl https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash && \
    . $NVM_ROOT/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default && \
    npm config set user 0 && \
    npm config set unsafe-perm true
#    npm config set cache $NVM_ROOT
ENV NODE_PATH $NVM_ROOT/v$NODE_VERSION/lib/node_modules
ENV PATH      $NVM_ROOT/versions/node/v$NODE_VERSION/bin:$PATH


#RUN mkdir -p /var/www/app

# Install tests dependencies
RUN pip install Appium-Python-Client Faker future gherkin-official py pylint pytest pytest-bdd \
    python-dateutil pyyaml requests retry selenium
RUN npm install -g appium@1.7.2

# Usefull to have systemd functionnal
CMD ["/sbin/init"]
