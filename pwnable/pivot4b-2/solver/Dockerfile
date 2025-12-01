FROM python:latest

RUN pip install -U ptrlib

WORKDIR /tmp
ADD solve.py solve.py
ADD chall chall
ADD libc.so.6 libc.so.6

CMD ["python3", "solve.py"]
