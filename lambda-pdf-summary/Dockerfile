# lambda base image (python)
FROM amazon/aws-lambda-python:3.8

RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

WORKDIR /var/task/lambda-pdf-summary

COPY lambda_function.py /var/task/
COPY . .

RUN pip install -r requirements.txt

CMD ["lambda_function.lambda_handler"]