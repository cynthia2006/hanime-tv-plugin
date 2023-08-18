import re

from yt_dlp.extractor.common import InfoExtractor

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
        page = self._download_json('https://hanime.tv/api/v8/video', video_id, query={'id': video_id})

        video = page['hentai_video']
        description = re.sub(r'<\/?\w+[^>]*>', r'', video['description'])
        franchise = page['hentai_franchise']

        formats = []

        for server in page['videos_manifest']['servers']:
            for streams in server['streams']:
                # Premium streams are to be ignored
                if streams['kind'] != "hls":
                    continue

                formats.append({
                    'url': streams['url'],
                    'ext': 'mp4',
                    'format_id': f'mp4-{streams["height"]}',
                    'width': streams['width'],
                    'height': int(streams['height']),
                    # 'filesize_approx': streams['filesize_mbs'] * 1048576,
                })

        return {
            'id': video['slug'],
            'title': video['name'],
            'creator': video['brand'],
            'duration': video['duration_in_ms'] / 1000,
            'timestamp': video['created_at_unix'],
            'release_timestamp': video['released_at_unix'],
            'description': description,
            'view_count': video['views'],
            'like_count': video['likes'],
            'tags': [tag['text'] for tag in video['hentai_tags']],
            'dislike_count': video['dislikes'],
            'thumbnail': video['poster_url'],
            'series': franchise['title'],
            'formats': formats,
            'ext': 'mp4',
        }
