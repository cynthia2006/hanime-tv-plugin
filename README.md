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

### pipx

Had you installed yt-dlp using **pipx**, you should inject this plugin.

```
pipx inject yt-dlp hanime-plugin
```

## Support

The following is table of sites — ordered by overall subjective UX of site — and video resolutions each site offer. **To request support for a site, or complain about a broken site, please open a Github issue.**

|                  | 720p               | 1080p                | 4K                   |
| ---------------- | ------------------ | -------------------- | -------------------- |
| hstream.moe      | :white_check_mark: | :white_check_mark: † | :white_check_mark: † |
| oppai.stream     | :white_check_mark: | :white_check_mark: ‡ | :white_check_mark: ‡ |
| hentaihaven.com  | :white_check_mark: | :white_check_mark:   | :x:                  |
| hanime.tv        | :white_check_mark: | :x:*                 | :x:                  |
| ohentai.org      | :white_check_mark: | :x:                  | :x:                  |
| hentaimama.io    | :white_check_mark: | :x:                  | :x:                  |

>[!IMPORTANT]
> **hanime.tv** requires a JS runtime; currently only [Deno](https://deno.land) is supported, so install that, ensuring it's in PATH, otherwise this plugin won't work for that site.

\* Requires paid membership; beyond the scope of this plugin.

† [AV1](https://en.wikipedia.org/wiki/AV1) encodes. ‡ VP9 encodes.

## Examples

### Downloading a single video

```
$ yt-dlp https://hanime.tv/videos/hentai/fuzzy-lips-1
```

or 

```
$ yt-dlp -f - https://hentaihaven.com/video/soshite-watashi-wa-sensei-ni/episode-1
```

## FAQ

### Why supports for these sites are not already included in yt-dlp?

The foundations for **hanime.tv** downloads were first laid out by [rxqv](https://github.com/rxqv/htv) as a separate tool, but the development ceased in 2021. Had it become dysfunctional eventually, [an issue](https://github.com/yt-dlp/yt-dlp/issues/4007) was raised for adding support for **hanime.tv** in upstream yt-dlp; was turned down, citing the website allows piracy. This may have to do with the fact that **YouTubeDL** — yt-dlp's predecessor — had quite a controversial past; so far as to be wiped out from Github in 2020 as the result of DMCA complaint by Google.

Meanwhile, xsbee maintained a fork of yt-dlp with a hanime.tv extractor they made, before ceasing development in 2023. This plugin was originally based off of that extractor code. Support for other sites have been added in late 2025.

### Earlier version had support for hanime.tv playlists, what happened?

These additional features were added in 2024 on top of xsbee's original code. However, franchise and playlist downloads have since been removed because of [code rot](https://en.wikipedia.org/wiki/Software_rot).
