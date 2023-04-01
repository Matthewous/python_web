FROM python:3.11

COPY ./stocks_products/requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt
COPY . /src
EXPOSE 6060
ENV MY_ENV=netology
WORKDIR src
RUN python /src/stocks_products/manage.py

CMD [ "python3", "-u", "manage.py", "--host", "0.0.0.0", "--port", "6060" ]