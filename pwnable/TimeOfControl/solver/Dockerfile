FROM python:latest

RUN pip install -U ptrlib tqdm
WORKDIR /tmp
ADD sender.py sender.py
ADD exploit exploit

CMD ["python3", "sender.py"]
