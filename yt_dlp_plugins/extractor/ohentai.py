import re

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import js_to_json

class OhentaiIE(InfoExtractor):
    _VALID_URL = r'https://ohentai\.org/detail\.php\?vid=(?P<id>[\w\-=]+)'
    _TITLE_RE = r"<h1 class='title'>([^<]+)</h1>"

    def _real_extract(self, url):
        video_id = self._match_id(url)

        page = self._download_webpage(url, video_id)        
        title = self._html_search_regex(self._TITLE_RE, page, 'title', flags=re.DOTALL)

        jwp_data = self._search_json(r'SendPlay\s*.\s*setup\s*\(', page, 'JWPlayer data', video_id,
                                     end_pattern=r'\);', transform_source=js_to_json)
        
        result = self._parse_jwplayer_data(jwp_data, video_id=video_id, require_title=False)
        result['title'] = title

        for fmt in result['formats']:
            fmt['http_headers'] = {'Referer': 'https://ohentai.org/'}

        return result
