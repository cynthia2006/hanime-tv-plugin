import re
import json
import argparse

from datetime import date
from urllib.request import urlopen, Request

real_order = {
    'title': 'title_sortable',
    'views': 'views',
    'likes': 'likes',
    'upload_date': 'created_at_unix',
    'release_date': 'released_at_unix'
}

parser = argparse.ArgumentParser(
    epilog="Total pages and result count will be displayed"
)

parser.add_argument('QUERY',
                    nargs='?',
                    default='',
                    help='text to search with')

parser.add_argument('-b', '--brand',
                    action='append',
                    default=[],
                    help="search for videos produced by a company/brand")

parser.add_argument('-t', '--tag',
                    action='append',
                    default=[],
                    help="search for videos having a tag")

parser.add_argument('-T', '--no-tag',
                    action='append',
                    metavar='TAG',
                    default=[],
                    help="search for videos not having a tag")

parser.add_argument('-o', '--order',
                    choices=['title', 'views', 'likes', 'upload_date', 'release_date'],
                    help="property to sort results by")

parser.add_argument('-p', '--page',
                    type=int,
                    default=1,
                    help="page number to show")

parser.add_argument('--ascending',
                    action='store_true',
                    help="show results in ascending order")

parser.add_argument('--broad-search',
                    action='store_true',
                    help="use broad search for whitelist of tags")

parser.add_argument('--verbose',
                    action='store_true',
                    help='show details about a result')

res_fmt_verbose = """---
[ {name} ]

""{description}""

    aka
        {titles}
    by {brand}
    duration {duration}
    views {views:d}
    likes {likes:d}
    censored? {is_censored}
    has
        {tags}

    cover {cover_url}
    poster {poster_url}
    monthly rank {monthly_rank:d}
    released_at {release_date}
    uploaded_at {upload_date}
    downloads {downloads}
    url https://hanime.tv/hentai/video/{slug}
---"""

res_fmt = """---
{name} ({duration}) | by {brand}
released on {release_date} | {views:d} views, {likes:d} likes
https://hanime.tv/hentai/video/{slug}"""

def main():
    args = parser.parse_args()
    req = Request('https://search.htv-services.com/',
        data=json.dumps({
                'blacklist': args.no_tag,
                'brands': args.brand,
                'tags': args.tag,
                'order_by': real_order.get(args.order),
                'ordering': 'asc' if args.ascending else 'desc',
                'tags_mode': 'OR' if args.broad_search else 'AND',
                'page': args.page - 1,
                'search_text': args.QUERY
            }).encode('ascii'),
        headers={
            'Content-Type': 'application/json'
        })

    res = json.load(urlopen(req))
    hits = json.loads(res['hits'])

    for hit in hits:
        minutes, seconds = divmod(hit['duration_in_ms'], 60000)
        seconds //= 1000
        hours, minutes = divmod(minutes, 60)

        hit |= {
            'duration': '{0:02}:{1:02}:{2:02}'.format(hours, minutes, seconds),
            'release_date': date.fromtimestamp(hit['released_at']),
            'description': re.sub(r'<[^>]*>', '', hit['description'])
        }

        if args.verbose:
            hit |= {
                'upload_date': date.fromtimestamp(hit['created_at']),
                'titles': '\n        '.join(hit['titles']),
                'tags': ', '.join(hit['tags']),
            }
            print(res_fmt_verbose.format(**hit))
        else:
            print(res_fmt.format(**hit))


    if not args.verbose:
        print('---')

    print(f"Page {res['page'] + 1} of {res['nbPages']}, Results {res['nbHits']}")

if __name__ == '__main__':
    main()
