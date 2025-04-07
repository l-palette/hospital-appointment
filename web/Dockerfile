FROM alpine

RUN apk add python3
RUN apk add curl
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python3.12 get-pip.py --break-system-packages
RUN rm get-pip.py

COPY . /web/
WORKDIR /web/

RUN pip install -r requirements.txt --break-system-packages

CMD ["python3", "app.py"]