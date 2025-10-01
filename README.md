# hanime-plugin

This yt-dlp plugin adds support for numerous hentai websites, including but not limited to **hanime.tv**, **hstream.moe** and **HentaiHaven**.

[![Python package](https://github.com/cynthia2006/hanime-tv-plugin/actions/workflows/python-package.yml/badge.svg)](https://github.com/cynthia2006/hanime-tv-plugin/actions/workflows/python-package.yml)
[![PyPI version](https://badge.fury.io/py/hanime-tv-plugin.svg)](https://badge.fury.io/py/hanime-tv-plugin)

## Installation

You can install this package with pip:
```
pip install --user hanime-plugin
```

See [installing yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#installing-plugins) for the other methods this plugin package can be installed.

## Support

Most of the websites support only downloading singular videos, not playlists; only, **hanime.tv** has playlist support as of this date.

|                                                          | 720p               | 1080p                | 4K                   |
| -------------------------------------------------------- | ------------------ | -------------------- | -------------------- |
| hanime.tv                                                | :white_check_mark: | :x:*                 | :x:                  |
| hstream.moe                                              | :white_check_mark: | :white_check_mark: † | :white_check_mark: † |
| hentaihaven.co,<br/>hentaihaven.com,<br/>hentaihaven.xxx | :white_check_mark: | :white_check_mark:   | :x:                  |

\* Requires paid membership, something which is beyond the scope of this plugin.

† [AV1](https://en.wikipedia.org/wiki/AV1) encodes; so expect superior quality. 

Addtionally, **hstream.moe** suports direct 10-bit 1080p HEVC encodes from its website, but downloading files directly may be unreliable at times. 

Though it should especially be notable to videophiles, that although AV1 is superior to HEVC, the AV1 encodes provided by the website are idosyncratically encoded with 8-bit instead of 10-bit. The quality difference between the two isn't noticeable to the layperson, but those who seek perfection beaware.

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

```
$ yt-dlp https://hanime.tv/playlists/bjjsczgesrlcylidtrjr
```
or
```
$ yt-dlp https://hanime.tv/videos/hentai/fuzzy-lips-2?playlist_id=bjjsczgesrlcylidtrjr
```

## FAQ

1. **Why these extractors are not already included in yt-dlp?**

   The foundations for the oldest extactor in this package — for hanime.tv — were first laid out by [rxqv](https://github.com/rxqv/htv) in a separate tool, whose development ceased in 2021.

   xsbee's [proposal](https://github.com/yt-dlp/yt-dlp/issues/4007) for a hanime.tv extractor was turned down, and the reasons for turning it down were quite ironic — in that these hentai websites "promote piracy" — as if the whole point of yt-dlp wasn't that to begin with. This might be due to the fact that YouTubeDL (yt-dlp's predecessor) has had quite a controversial past regarding its legality, so far as to be removed from Github in 2020.

   Either way, xsbee mantained a fork of yt-dlp with a hanime.tv extractor for a while, beforing ceasing development in 2023. This plugin was originally based off of that extractor code, plus some additional features were added in 2024.

   As of 2025, this plugin not only includes an extractor for **hanime.tv** but other major hentai websites. 

2. **Why ~~are~~ were some fragments skipped when downloading from hanime.tv, resulting in a shorter video?**

   From a speculation (in June 2025), it ~~seems~~ seemed that several of hanime.tv's CDNs ~~are~~ were dead; as a result of which, fragments URLs enlisted in the [M3U8 manifest](https://en.wikipedia.org/wiki/HTTP_Live_Streaming) ~~are~~ were broken (DNS resolution fails), and thus after several retries yt-dlp gives up, and skips the fragments as its default action. This ~~is~~ was even worse on the website itself, where the video ~~goes~~ went into endless buffering. 

   The workaround ~~is~~ was to simply gather all domain names within the M3U8 manifest that function, and replace those which malfunction with any one from the list that function (chosen randomly).
   
   
