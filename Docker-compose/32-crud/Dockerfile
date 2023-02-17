FROM python

WORKDIR /src/32-crud

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
#    sed -i 's/\r$//g' /src/32-crud/entrypoint.sh && \
#    chmod +x /src/32-crud/entrypoint.sh

#ENTRYPOINT ["/src/32-crud/entrypoint.sh"]
ENTRYPOINT python manage.py migrate && \
           python manage.py collectstatic

CMD ["gunicorn", "stocks_products.wsgi:application", "--bind", "0.0.0.0:8001"]