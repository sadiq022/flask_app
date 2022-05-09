FROM python:3.8-alpine
COPY ./requirement.txt /app/requirement.txt
WORKDIR /app
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install -r requirement.txt
COPY . /app
ENTRYPOINT [ "python" ]
EXPOSE 4001
CMD ["main.py" ]