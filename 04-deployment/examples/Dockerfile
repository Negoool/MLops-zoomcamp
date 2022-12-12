FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt


COPY ["./model.bin", "hm.py", "./"]

ENTRYPOINT [ "python", "hm.py" ]
