FROM python:3.9
WORKDIR /
ARG PORT
COPY ./requirements.txt /requirements.txt 
RUN pip install -r /requirements.txt
COPY ./ /
EXPOSE 80
ENTRYPOINT ["uvicorn", "backend.main:app","--proxy-headers", "--host", "0.0.0.0", "--port", "80"]