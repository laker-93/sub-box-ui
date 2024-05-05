FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV PORT 8888

RUN pip install --upgrade pip
COPY ./ToredoCore /app/toredocore
RUN pip install -e /app/toredocore
COPY ./sub-box-ui/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Setup App Files
COPY ./sub-box-ui/subbox_landing /app

CMD python /app/runner.py -e $APP_ENVIRONMENT
