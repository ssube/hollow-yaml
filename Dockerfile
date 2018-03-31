FROM python:3.6

COPY . /app

RUN pip3 install -r requirements.txt \
 && python -OO -m py_compile hollow.py

CMD [ "/app/hollow.py" ]