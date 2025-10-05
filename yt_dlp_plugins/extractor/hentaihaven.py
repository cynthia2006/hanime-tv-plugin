import re
import base64

from yt_dlp.extractor.common import InfoExtractor, ExtractorError
from yt_dlp.utils import multipart_encode

class HentaiHavenIE(InfoExtractor):
    _VALID_URL = r'https?://hentaihaven\.(co|com|xxx)/video/(?P<id>[\w\-_]+).*'
    _VIDEO_TITLE_RE = r'chapter-heading" class="h3">([^<]+)'
    _HH_EMBED_RE = r'[^"]+/wp-content/plugins/player-logic/player\.php[^"]+'
    _CIPHER_MAP = dict(zip(b'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm',
                           b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'))

    def _decipher_sec_token(self, s):
        b = s.encode('ascii')

        for _ in range(3):
            # Map the characters which are part of the cipher, leave the rest.
            b = bytes(map(lambda c: self._CIPHER_MAP.get(c) or c, b))
            b = base64.b64decode(b)

        return b.decode('ascii')

    def _real_extract(self, url):
        video_id = self._match_id(url)

        hh_page = self._download_webpage(url, video_id)

        video_title = self._html_search_regex(self._VIDEO_TITLE_RE, hh_page, 'title')
        embed_url = self._search_regex(self._HH_EMBED_RE, hh_page, 'embed', group=0)
        
        hh_page = self._download_webpage(embed_url, video_id)
        
        cipher_text = self._html_search_meta('x-secure-token', hh_page).lstrip('sha512-')       
        interim = self._parse_json(self._decipher_sec_token(cipher_text), video_id)
        api_url = '{}/api.php'.format(interim['uri'])
        payload = {
            'action': 'zarat_get_data_player_ajax',
            'a': interim['en'],
            'b': interim['iv']
        }
        raw_payload, mime = multipart_encode(payload)
        
        hh_res = self._download_json(api_url, video_id, headers={'Content-Type': mime},
                                     data=raw_payload)

        if hh_res['status'] is False:
            raise ExtractorError('Unable to extract JWPlayer data',
                                 video_id=video_id, ie=HentaiHavenIE.ie_key())

        for src in hh_res['data']['sources']:
            src['file'] = src.pop('src')

        result = self._parse_jwplayer_data(hh_res['data'], video_id, require_title=False)
        result['title'] = video_title

        return result

