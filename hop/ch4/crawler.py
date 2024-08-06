from hop.ch4.iterator import Iterator, igrep, imap

from collections import deque

from lxml import html
import requests

def traverse(starting_url: str) -> Iterator[str]:
    queue = deque([starting_url])
    seen = set()

    def doit():
        while len(queue) > 0:
            url = queue.popleft()
            if url in seen:
                continue

            r = requests.get(url)
            if r.status_code != 200:
                continue

            dom = html.fromstring(r.text)
            dom.make_links_absolute(url)
            for href in dom.xpath("//a/@href"):
                queue.append(href)
            return url
    return doit
