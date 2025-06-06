#!/bin/python

import m3u8
import socket
import random
import json

import sys

from urllib.parse import urlsplit, urlunsplit

def main():
    yt_dlp_json = json.load(sys.stdin)
    m3u_manifest = yt_dlp_json['url']  # Assuming it's a M3U manifest.

    playlist = m3u8.load(m3u_manifest)
    domains = frozenset(urlsplit(seg.uri).netloc for seg in playlist.segments)
    offending_domains = set()

    for domain in domains:
        try:
            # Select the first address; although, not a good practice to do so.
            socket.getaddrinfo(domain, 'https', proto=socket.IPPROTO_TCP)[0]
        except socket.gaierror as err:
            error, _ = err.args
            if error == socket.EAI_NONAME:
                offending_domains.add(domain)

                print('DNS resolution failed for', domain, file=sys.stderr)
            else:
                raise

    # Domains that were qualified as good.
    domains = list(domains - offending_domains)

    for seg in playlist.segments:
        _, netloc, path, _, _ = urlsplit(seg.uri)
        if netloc not in domains:
            netloc = random.choice(domains)

            # Update the URL only if it's offending.
            seg.uri = urlunsplit(('https', netloc, path, '', ''))

    sys.stdout.write(playlist.dumps())

if __name__ == '__main__':
    main()
