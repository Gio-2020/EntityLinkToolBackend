FROM python:3.8.13

ADD . /TestServer

WORKDIR /TestServer

# RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# CMD python manage.py runserver 0.0.0.0:8282
