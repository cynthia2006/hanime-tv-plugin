# hanime-plugin

This yt-dlp plugin adds support for numerous hentai websites, including but not limited to **hanime.tv**, **hstream.moe** and **HentaiHaven**.

[![Python package](https://github.com/cynthia2006/hanime-plugin/actions/workflows/python-package.yml/badge.svg)](https://github.com/cynthia2006/hanime-plugin/actions/workflows/python-package.yml)
[![PyPI version](https://badge.fury.io/py/hanime-plugin.svg)](https://pypi.org/project/hanime-plugin/)

## Installation

You can install this package with pip:
```
pip install --user hanime-plugin
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the other methods this plugin package can be installed.

## Support

The following is table of sites — ordered by overall subjective UX of site — and video resolutions each site offer. **To request support for a site, please open a Github issue.**

|                                                        | 720p               | 1080p                | 4K                   |
| ------------------------------------------------------ | ------------------ | -------------------- | -------------------- |
| hstream.moe                                            | :white_check_mark: | :white_check_mark: † | :white_check_mark: † |
| oppai.stream                                           | :white_check_mark: | :white_check_mark: ‡ | :white_check_mark: ‡ |
| hentaihaven.co<br/>hentaihaven.com<br/>hentaihaven.xxx | :white_check_mark: | :white_check_mark:   | :x:                  |
| hanime.tv                                              | :white_check_mark: | :x:*                 | :x:                  |
| ohentai.org                                            | :white_check_mark: | :x:                  | :x:                  |
| hentaimama.io                                          | :white_check_mark: | :x:                  | :x:                  |


\* Requires paid membership; beyond the scope of this plugin.

† [AV1](https://en.wikipedia.org/wiki/AV1) encodes. ‡ VP9 encodes.

> **hstream.moe**'s AV1 encodes are 8-bit, whereas direct HEVC downloads are 10-bit. This information is useful to videophiles; normal users can ignore.

## Examples

### Downloading a single video

```
$ yt-dlp https://hanime.tv/videos/hentai/fuzzy-lips-1
```

or 

```
$ yt-dlp -f - https://hentaihaven.com/video/soshite-watashi-wa-sensei-ni/episode-1
```

### Downloading a whole playlist

Only **hanime.tv** has playlists; others don't, and videos must be downloaded separately as of now.

```
$ yt-dlp https://hanime.tv/playlists/bjjsczgesrlcylidtrjr
```
or
```
$ yt-dlp https://hanime.tv/videos/hentai/fuzzy-lips-2?playlist_id=bjjsczgesrlcylidtrjr
```

## FAQ

### Why these extractors are not already included in yt-dlp?

The foundations for the oldest extactor in this package — for hanime.tv — were first laid out by [rxqv](https://github.com/rxqv/htv) in a separate tool, whose development ceased in 2021.

xsbee's [proposal](https://github.com/yt-dlp/yt-dlp/issues/4007) for a hanime.tv extractor was turned down, and the reasons for turning it down were quite ironic — in that these hentai websites "promote piracy" — as if the whole point of yt-dlp wasn't that to begin with. This might be due to the fact that YouTubeDL (yt-dlp's predecessor) has had quite a controversial past regarding its legality, so far as to be removed from Github in 2020.

Either way, xsbee mantained a fork of yt-dlp with a hanime.tv extractor for a while, beforing ceasing development in 2023. This plugin was originally based off of that extractor code, plus some additional features were added in 2024.

As of 2025, this plugin not only includes an extractor for **hanime.tv** but other major hentai websites. 

