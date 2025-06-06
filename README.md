# hanime-tv-plugin

This yt-dlp plugin adds support for the hanime.tv extractor.

[![Python package](https://github.com/cynthia2006/hanime-tv-plugin/actions/workflows/python-package.yml/badge.svg)](https://github.com/cynthia2006/hanime-tv-plugin/actions/workflows/python-package.yml)
[![PyPI version](https://badge.fury.io/py/hanime-tv-plugin.svg)](https://badge.fury.io/py/hanime-tv-plugin)


## History

This extractor was first founded by [rxqv](https://github.com/rxqv/htv), as a separate tool.

xsbee's, [proposal](https://github.com/yt-dlp/yt-dlp/issues/4007) for a hanime.tv extractor was turned down. They apparently, maintained a fork of yt-dlp with a hanime.tv extractor for a while. This plugin is based on that extractor code, plus some additional features.

## Installation

Requires yt-dlp `2023.07.06` or above.

You can install this package with pip:
```
pip install --user hanime-tv-plugin
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the other methods this plugin package can be installed.

## Features

- Downloads upto **720p**; **1080p** requires premium membership, which is outside the scope of this plugin.
- Downloads of entire playlists—public or unlisted.

## Examples

- To download a single video:
  ```
  yt-dlp https://hanime.tv/hentai/video/green-eyes-ane-kyun-yori-1
  ```

- To download an entire playlist:
  ```
  yt-dlp https://hanime.tv/playlists/bjjsczgesrlcylidtrjr
  ```
  Alternatively,
  ```
  yt-dlp https://hanime.tv/videos/hentai/fuzzy-lips-2?playlist_id=bjjsczgesrlcylidtrjr
  ```

## Search

A [search script](https://github.com/xsbee/yt-dlp/releases/download/htv/htv-search.py) is included as well for convenience, and can be invoked through `htv-search` if it's in the PATH.

```
usage: htv-search [-h] [-q QUERY] [-b BRAND] [-t TAG] [-T TAG] [-o {title,views,likes,upload_date,release_date}] [-p PAGE]
                  [--ascending] [--broad-search] [--verbose]

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        text to search with
  -b BRAND, --brand BRAND
                        search for videos produced by a company/brand
  -t TAG, --tag TAG     search for videos having a tag
  -T TAG, --no-tag TAG  search for videos not having a tag
  -o {title,views,likes,upload_date,release_date}, --order {title,views,likes,upload_date,release_date}
                        property to sort results by
  -p PAGE, --page PAGE  page number to show
  --ascending           show results in ascending order
  --broad-search        use broad search for whitelist of tags
  --verbose             show details about a result

Total pages and result count will be displayed
```

A few usecases include the following are shown below. Note that, a search query is not always needed.

- Simple search query (`kanojo x kanojo x kanojo`). Although case-insensitive, this however, is not a fuzzy search.

    ```
    $ htv-search "kanojo x kanojo x kanojo"
    ---
    Kanojo x Kanojo x Kanojo 3 (00:27:23) | by MS Pictures
    released on 2011-05-20 | 3579342 views, 12726 likes
    https://hanime.tv/hentai/video/kanojo-x-kanojo-x-kanojo-3
    ---
    Kanojo x Kanojo x Kanojo 2 (00:29:38) | by MS Pictures
    released on 2010-06-18 | 6015325 views, 16392 likes
    https://hanime.tv/hentai/video/kanojo-x-kanojo-x-kanojo-2
    ---
    Kanojo x Kanojo x Kanojo 1 (00:29:40) | by MS Pictures
    released on 2009-12-25 | 6757651 views, 24783 likes
    https://hanime.tv/hentai/video/kanojo-x-kanojo-x-kanojo-1
    ---
    Page 1 of 1, Results 3
    ```

- With multiple tags (including `creampie` and `loli`, but excluding `ugly bastard` and `rape`).

    ```
    $ htv-search -t loli -t creampie -T 'ugly bastard' -T 'rape'
    ---
    Shoujo Kyouiku RE 1 (00:00:00) | by Mary Jane
    released on 2019-07-04 | 5440718 views, 13031 likes
    https://hanime.tv/hentai/video/shoujo-kyouiku-re-1
    ---
    Oyasumi Sex 1 (00:16:18) | by Mary Jane
    released on 2018-10-26 | 5433932 views, 16120 likes
    https://hanime.tv/hentai/video/oyasumi-sex-1
    ---
    Shoujo Ramune 4 (00:20:14) | by Mary Jane
    released on 2018-03-01 | 7041368 views, 12562 likes
    https://hanime.tv/hentai/video/shoujo-ramune-4
    ---
    Shoujo Ramune 3 (00:16:35) | by Mary Jane
    released on 2017-11-23 | 5715137 views, 10983 likes
    https://hanime.tv/hentai/video/shoujo-ramune-3
    ---
    Shoujo Ramune 1 (00:19:04) | by Mary Jane
    released on 2016-10-06 | 10503540 views, 21120 likes
    https://hanime.tv/hentai/video/shoujo-ramune-1
    ---
    Page 1 of 1, Results 5
    ```

- Verbose information, showing all information that could be retrieved.

    ```
    $ htv-search --verbose 'kowaremono the animation'
    ---
    [ Kowaremono The Animation ]
    
    ""Based on the erotic manga by Yoshiron.
    
    A man’s wife walks out on him. He feels like shit and ends up getting drunk. Good thing he has custody of their teenage daughter. Time to Merry Christmas that bitch instead!
    
    Source: HH.org""
    
        aka
            Kowaremono The Animation
            娘ワレモノ THE ANIMATION
            Broken Things Kasumi: The Animation
        by Bootleg
        duration 00:17:50
        views 3319313
        likes 10734
        censored? False
        has
            big boobs, blow job, bondage, incest, school girl, creampie, facial, mind break, public sex, virgin, boob job, uncensored, hd
    
        cover https://git-covers.pages.dev/images/kowaremono-the-animation.jpg
        poster https://git-posters.pages.dev/images/kowaremono-the-animation-pv1.jpg
        monthly rank 470
        released_at 2015-12-04
        uploaded_at 2015-12-29
        downloads 179208
        url https://hanime.tv/hentai/video/kowaremono-the-animation
    ---
    Page 1 of 1, Results 1
    ```

## FAQ

1. Why are some fragments are skipped during download, resulting in a shorter video?

   From speculation, it seems several of hanime.tv's CDNs are dead; as a result of which, fragments URLs enlisted in the M3U manifest are broken (DNS resolution fails), and thus after several retries yt-dlp gives up, and skips the fragments as the default action. This is even worse on the website itself, as the video goes into endless buffering. The workaround is to simply gather all domain names within the M3U manifest that function, and replace those which malfunction with any one from the list that function (chosen randomly).

   A script `htv-patch-m3u8` included in this package, which accepts the JSON produced by `yt-dlp`, retrieves the malfunctioning M3U manifest, patches it, and produces a function M3U manifest. The M3U manifest can be fed to FFmpeg (incidentally, an external downloader for `yt-dlp` as well).
   
   **Note:** This script handles only single videos, playlists aren't supported as of now.

   ```
   $ yt-dlp -j "https://hanime.tv/hentai/video/ikenai-koto-the-animation-1" | htv-patch-m3u8 | ffmpeg -protocol_whitelist fd,tcp,tls,https,crypto -f hls -extension_picky 0 -i - -c copy "Ikenai Koto - The Animation.mp4"
   ```
   
   
