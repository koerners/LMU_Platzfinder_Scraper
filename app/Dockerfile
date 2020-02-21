FROM ubuntu

RUN apt-get update -y && \
apt-get install python3-pip -y \
&& apt-get install git -y


ENV APP_PATH /usr/src/app
RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

EXPOSE 5000

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN sh letsencrypt_install.sh

CMD sh startserver.sh