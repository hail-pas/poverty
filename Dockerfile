FROM python:3.8
RUN mkdir -p /usr/share/nginx/poverty
RUN mkdir ~/.pip
RUN echo "[global]\nindex-url = https://mirrors.aliyun.com/pypi/simple/\nformat = columns" > ~/.pip/pip.conf
WORKDIR /usr/share/nginx/poverty
ENV PYTHONPATH=/usr/share/nginx/poverty
COPY requirements.txt /usr/share/nginx/poverty/
RUN pip install -r requirements.txt
COPY . /usr/share/nginx/poverty