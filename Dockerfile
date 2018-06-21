FROM python:3.6-alpine
WORKDIR /srv
COPY . .
RUN apk add --update build-base python3-dev libffi-dev py3-pip && \
	pip3 install -r requirements.txt
EXPOSE 80
CMD ["python3", "api.py"]