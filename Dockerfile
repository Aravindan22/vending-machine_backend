FROM python:3.9
WORKDIR /
ARG PORT
COPY ./requirements.txt /requirements.txt 
RUN pip install --no-cache-dir --upgrade -r //requirements.txt
COPY ./ /
EXPOSE 80
ENTRYPOINT ["uvicorn", "backend.main:app","--proxy-headers", "--host", "0.0.0.0", "--port", $PORT]