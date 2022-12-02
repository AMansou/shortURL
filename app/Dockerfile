FROM python:3.6 as builder
COPY . /src
RUN pip install --user  boto3 flask flask_restful

FROM python:3.6 as app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /src .

ENV PATH=/root/.local:$PATH
EXPOSE 5000

CMD ["python3", "app.py"]
