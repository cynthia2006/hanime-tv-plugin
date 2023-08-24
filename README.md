This yt-dlp plugin adds support for the hanime.tv extractor. 

## History

This extractor was first founded by [rxqv](https://github.com/rxqv/htv), as a separate tool. A prime feature of that tool was the ability to search and download all videos in a hentai series.

xsbee, who also made an [issue](https://github.com/yt-dlp/yt-dlp/issues/4007) on yt-dlp repo, took on the apparently stale rxqv repo, converting it into a yt-dlp extractor.

This repository takes the extractor code and makes it a plugin, which makes maintainence rather easier.

## Installation

Requires yt-dlp `2023.07.06` or above.

You can install this package with pip:
```
python3 -m pip install -U https://github.com/lroy1998/hanime-tv-plugin/archive/master.zip
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the other methods this plugin package can be installed.

## Search

This plugin does not have the searching functionality as was in the original rxqv repository. However, xsbee had also made a [search script](https://github.com/xsbee/yt-dlp/releases/download/htv/htv-search.py), which can be used separately from this plugin to search without the web interface.


```
usage: htv-search.py [-h] [-q QUERY] [-b BRAND] [-t TAG] [-T TAG] [-o {title,views,likes,upload_date,release_date}] [-p PAGE] [--ascending] [--broad-search] [--verbose]

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
---
```
$ chmod +x htv-search.py
```

command should be run to make the script executable.

### Examples

- Simple text query

    ```
    $ ./htv-search.py -q "kanojo x kanojo x kanojo"
    Kanojo x Kanojo x Kanojo 3: https://hanime.tv/hentai/video/kanojo-x-kanojo-x-kanojo-3
    Kanojo x Kanojo x Kanojo 2: https://hanime.tv/hentai/video/kanojo-x-kanojo-x-kanojo-2
    Kanojo x Kanojo x Kanojo 1: https://hanime.tv/hentai/video/kanojo-x-kanojo-x-kanojo-1
    ---
    Page 1 of 1, Results 3
    ```

- With multiple tags

    ```
    $ ./htv-search.py -t harem -t 'big boobs' -t x-ray -t uncensored
    Shoujo-tachi no Sadism 2: https://hanime.tv/hentai/video/shoujo-tachi-no-sadism-2
    Shoujo-tachi no Sadism 1: https://hanime.tv/hentai/video/shoujo-tachi-no-sadism
    Ikenai Koto The Animation 1: https://hanime.tv/hentai/video/ikenai-koto-the-animation-1
    Yubisaki Annainin 2: https://hanime.tv/hentai/video/yubisaki-annainin-2
    Yubisaki Annainin 1: https://hanime.tv/hentai/video/yubisaki-annainin-1
    ---
    Page 1 of 1, Results 5
    ```
