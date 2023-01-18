FROM python

WORKDIR /src

COPY . .

RUN pip install -U pip && \
    pip3 install -r ./3.2-crud/requirements.txt && \
    python ./3.2-crud/manage.py migrate

CMD ["python", "./3.2-crud/manage.py", "runserver", "0.0.0.0:8001"]
