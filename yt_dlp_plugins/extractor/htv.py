import re

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import traverse_obj, str_or_none, bool_or_none, int_or_none, url_or_none, urljoin, clean_html, OnDemandPagedList

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

        video = traverse_obj(page, ('hentai_video'), default={}, expected_type=dict)
        description = clean_html(video.get('description'))
        servers = traverse_obj(page, ('videos_manifest', 'servers'), default=[], expected_type=list)

        for server in servers:
            for streams in server.get('streams', []):
                # For now, premium streams can not be downloaded; neither is practical.
                if not streams.get('is_guest_allowed'):
                    continue

                # FIXME The M3U manifest may contain broken links to segments. Interestingly though,
                # the domain names, appearing in the URLs of media segments, seem to be alternate
                # domains to access the same resource. For example, say 'leviathan-25x-05.top' can't
                # be accessed for some reason, and an alternate domain 'leviathan-25x-06.top' exists,
                # the same resource can be accessed from there as well. This is an issue with that
                # website, not with our extractor.
                #
                # NOTE: We assume that stream kind is always 'hls', but it might change as well.
                formats.append({
                    'url': url_or_none(streams.get('url')),
                    'ext': 'mp4',
                    'vcodec': 'h264',
                    'acodec': 'aac',
                    'format_id': str_or_none(streams.get('id')),
                    'width': int_or_none(streams.get('width')),
                    'height': int_or_none(streams.get('height')),
                    'filesize_approx': int_or_none(streams.get('filesize_mbs'), invscale=1000000)
                })

        return {
            'id': video.get('slug'),
            'title': video.get('name'),
            'creator': video.get('brand'),
            'duration': int_or_none(video.get('duration_in_ms'), scale=1000),
            'timestamp': int_or_none(video.get('created_at_unix')),
            'release_timestamp': int_or_none(video.get('released_at_unix')),
            'description': description,
            'view_count': int_or_none(video.get('views')),
            'like_count': int_or_none(video.get('likes')),
            'tags': [tag.get('text') for tag in video.get('hentai_tags', [])],
            'dislike_count': int_or_none(video.get('dislikes')),
            'thumbnail': url_or_none(video.get('poster_url')),
            'series': traverse_obj(page, ('hentai_franchise', 'title'), expected_type=str),
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

            data = traverse_obj(page, ('fapi', 'data'), default=[], expected_type=list)

            return [self.url_result(
                        urljoin('https://hanime.tv/videos/hentai/', entry.get('slug')),
                        video_id=entry.get('id'),
                        video_title=entry.get('name'),
                        ie_key=HanimeTVIE.ie_key())
                    for entry in data]

        return self.playlist_result(OnDemandPagedList(fetch_page, 24), playlist_name)
