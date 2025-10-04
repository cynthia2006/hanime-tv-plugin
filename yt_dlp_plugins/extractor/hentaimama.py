from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import urlencode_postdata, js_to_json

class HentaimamaIE(InfoExtractor):
    _VALID_URL = r'https://hentaimama.io/episodes/(?P<id>[\w-]+)'
    _TITLE_RE = r'<input .*name="title" .*value="([^"]+)">'
    _POSTER_RE = r'<div class="imagen">.*<img src="([^"]+")>'

    def _real_extract(self, url):
        video_id = self._match_id(url)
        page = self._download_webpage(url, video_id)
        
        video_title = self._search_regex(self._TITLE_RE, page, 'video_title')
        poster_url = self._search_regex(self._POSTER_RE, page, 'poster url', default=None)

        ajax_data = self._search_json(r'var data\s*=\s*', page, 'ajax data',
                                      contains_pattern=r'{(?s:.*?)}',
                                      transform_source=js_to_json,
                                      video_id=video_id)
        
        hm_json = self._download_json('https://hentaimama.io/wp-admin/admin-ajax.php', video_id,
                                      data=urlencode_postdata(ajax_data),
                                      headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        jwp_page_url = self._search_regex(r'src="([^"]+)"', hm_json[0], 'JWPlayer page')
        jwp_page = self._download_webpage(jwp_page_url, video_id)

        # NOTE As of now, the websites serves identical files for both download and JWPlayer.
        # JWPlayer is the more feasible choice, because in future if the websites switches to
        # using HLS or DASH, this code won't be required to change.
        results = self._extract_jwplayer_data(jwp_page, video_id, require_title=False)
        results['title'] = video_title

        if poster_url:
            results['thumbnail'] = poster_url
        
        return results
