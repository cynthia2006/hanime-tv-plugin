import re

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import traverse_obj, str_or_none, bool_or_none, int_or_none, url_or_none, urljoin, clean_html, OnDemandPagedList

class HanimeTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?hanime\.tv/(videos/hentai|hentai/video)/(?P<id>[a-z0-9\-]+)'
    _TESTS = [{
        'url': 'https://hanime.tv/videos/hentai/itadaki-seieki',
        'md5': '68a3fbb672229cecd12b52528168e6ff',
        'info_dict': {
            'id': 'itadaki-seieki',
            'title': 'Itadaki! Seieki',
            'creator': 'Pashmina',
            'description': str,
            'duration': 1378,
            'upload_date': '20160607',
            'release_date': '20140327',
            'timestamp': 1465257759,
            'release_timestamp': 1395932400,
            'thumbnail': r're:^https?://.*\.jpg$',
            'series': 'Itadaki! Seieki',
            'view_count': int,
            'like_count': int,
            'tags': list,
            'dislike_count': int,
            'ext': 'mp4',
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        entries = []
        
        def video_result(page):
            formats = []

            video = traverse_obj(page, ('hentai_video'), default={}, expected_type=dict)
            description = clean_html(video.get('description'))
            servers = traverse_obj(page, ('videos_manifest', 'servers'), default=[], expected_type=list)
            
            for server in servers:
                for streams in server.get('streams', []):
                    # TODO notify yt-dlp of premium streams
                    if streams.get('kind') == 'premium_alert':
                        continue

                    formats.append({
                        'url': url_or_none(streams.get('url')),
                        'ext': 'mp4',
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
        
        page = self._download_json('https://hanime.tv/api/v8/video', None, query={'id': video_id})
        franchise = traverse_obj(page, ('hentai_franchise'), default={}, expected_type=dict)
        franchise_videos = traverse_obj(page, ('hentai_franchise_hentai_videos'), default=[], expected_type=list)
        
        entries.append(video_result(page))

        is_franchise = self._configuration_arg('franchise', [False], ie_key=HanimeTVIE.ie_key())[0]
        if is_franchise:
            for entry in franchise_videos[1:]:
                page = self._download_json('https://hanime.tv/api/v8/video', None, query={'id': str_or_none(entry.get('slug'))})

                entries.append(video_result(page))

        return self.playlist_result(entries, playlist_title=str_or_none(franchise.get('title')))


class HanimeTVPlaylistIE(InfoExtractor):
    _VALID_URL = r"https?://(?:www\.)?hanime\.tv/playlists/(?P<id>[a-z0-9\-]+)"
    # TODO add _TESTS

    def _real_extract(self, url):
        playlist_id = self._match_id(url)

        num_page_ents = int_or_none(self._configuration_arg('num_page_ents', ie_key=HanimeTVIE.ie_key()), default=24)

        def fetch_page(pagenum):
            page = self._download_json('https://hanime.tv/api/v8/playlist_hentai_videos', None, headers={
                'X-Signature-Version': 'web2'
            }, query={
                'playlist_id': playlist_id,
                # TODO possible extractor arg
                '__order': 'sequence,DESC',
                '__offset': pagenum*num_page_ents,
                '__count': num_page_ents
            })

            data = traverse_obj(page, ('fapi', 'data'), default=[], expected_type=list)

            return [self.url_result(
                        urljoin('https://hanime.tv/videos/hentai/', entry.get('slug')),
                        video_id=entry.get('id'),
                        video_title=entry.get('name'),
                        ie_key=HanimeTVIE.ie_key())
                    for entry in data]

        # TODO where is the playlist title?
        return self.playlist_result(OnDemandPagedList(fetch_page, num_page_ents), playlist_id)
