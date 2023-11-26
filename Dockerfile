FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
ENV PORT 8888

# Setup App Environment
ARG ENVIRONMENT
ENV APP_ENVIRONMENT ${ENVIRONMENT}

RUN pip install --upgrade pip
COPY ./ToredoCore /app/toredocore
RUN pip install -e /app/toredocore
COPY ./subbox-landing/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Setup App Files
COPY ./subbox-landing/subbox_landing /app/subbox_landing

CMD python /app/subbox_landing/runner.py -e $APP_ENVIRONMENT
