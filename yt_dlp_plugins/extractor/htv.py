import urllib.parse

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.networking import Request
from yt_dlp.utils import (
    traverse_obj,
    str_or_none,
    int_or_none,
    url_or_none,
    urljoin,
    base_url,
    OnDemandPagedList
)

class HanimeTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?hanime\.tv/(videos/hentai|hentai/video)/(?P<id>[a-z0-9\-]+)(?:\?playlist_id=(?P<lid>[a-z]+))?'
    # TODO add _TESTS

    def _real_extract(self, url):
        video_id, playlist_id = self._match_valid_url(url).group('id', 'lid')

        # Delegate to playlist extractor if the user requested to download the entire playlist.
        if self._yes_playlist(playlist_id, video_id):
            return self.url_result(urljoin('https://hanime.tv/playlists/', playlist_id),
                                   ie=HanimeTVPlaylistIE.ie_key())

        page = self._download_json('https://h.freeanimehentai.net/api/v8/video', video_id, query={'id': video_id})
        formats = []

        video = page['hentai_video']
        servers = page['videos_manifest']['servers']

        for server in servers:
            for stream in server['streams']:
                # For now, premium streams can not be downloaded; neither is practical.
                if not stream.get('is_guest_allowed'):
                    continue

                formats.append({
                    'url': stream['url'],
                    'ext': 'mp4',
                    'format_id': str_or_none(stream['id']),
                    'width': int_or_none(stream.get('width')),
                    'height': int_or_none(stream.get('height')),
                    'filesize_approx': int_or_none(stream.get('filesize_mbs'), invscale=1000000),
                })

        return {
            'id': video.get('slug'),
            'title': video.get('name'),
            'creator': video.get('brand'),
            'duration': int_or_none(video.get('duration_in_ms'), scale=1000),
            'timestamp': int_or_none(video.get('released_at_unix')),
            'thumbnail': url_or_none(video.get('poster_url')),
            'formats': formats,
            'ext': 'mp4',
        }


class HanimeTVPlaylistIE(InfoExtractor):
    _VALID_URL = r"https?://(?:www\.)?hanime\.tv/playlists/(?P<id>[a-z0-9\-]+)"
    # TODO add _TESTS

    def _real_extract(self, url):
        playlist_id = self._match_id(url)

        # Official website does 24 hits/request; we do the same.
        init_page = self._download_json('https://h.freeanimehentai.net/api/v8/playlist_hentai_videos', None, headers={
                'X-Signature-Version': 'web2'
            }, query={
                'playlist_id': playlist_id,
                '__order': 'sequence,DESC',
                '__offset': 0,
                '__count': 24,
                # The additional information (including playlist title) is fetched only once.
                'personalized': 1
            })
        playlist_name = traverse_obj(init_page, ('playlist', 'title'), expected_type=str)

        def fetch_page(pagenum):
            # Re-use the cached page.
            page = init_page if pagenum == 0 else self._download_json(
                'https://h.freeanimehentai.net/api/v8/playlist_hentai_videos', None,
                headers={
                    'X-Signature-Version': 'web2'
                }, query={
                    'playlist_id': playlist_id,
                    '__order': 'sequence,DESC',
                    '__offset': pagenum*24,
                    '__count': 24
                })

            data = page['fapi']['data']

            return [self.url_result(
                        urljoin('https://hanime.tv/videos/hentai/', entry['slug']),
                        video_id=entry['id'],
                        video_title=entry['title'],
                        ie_key=HanimeTVIE.ie_key())
                    for entry in data]

        return self.playlist_result(OnDemandPagedList(fetch_page, 24), playlist_name)
