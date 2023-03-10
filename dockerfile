FROM python:3.11.1
COPY . .
RUN pip3 install -r requirements.txt
CMD [ "python3" , "bot.py" ]