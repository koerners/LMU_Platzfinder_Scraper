FROM python

ENV APP_PATH /usr/src/app
RUN mkdir -p $APP_PATH
WORKDIR $APP_PATH

EXPOSE 8080

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD sh startserver.sh