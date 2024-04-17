FROM python:3.12.3
WORKDIR /app
COPY ./ /app
ENV ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
EXPOSE 8000
CMD ["python3", "bot.py"]
