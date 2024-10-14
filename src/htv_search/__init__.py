import argparse
import requests
import json

from datetime import datetime

def htv_search():
    parser = argparse.ArgumentParser(
        epilog="Total pages and result count will be displayed"
    )

    real_order = {
        'title': 'title_sortable',
        'views': 'views',
        'likes': 'likes',
        'upload_date': 'created_at_unix',
        'release_date': 'released_at_unix'
    }

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

    args = parser.parse_args()

    req = {
        'blacklist': args.no_tag,
        'brands': args.brand,
        'tags': args.tag,
        'order_by': real_order.get(args.order),
        'ordering': 'asc' if args.ascending else 'desc',
        'tags_mode': 'OR' if args.broad_search else 'AND',
        'page': args.page - 1,
        'search_text': args.QUERY
    }

    r = requests.post('https://search.htv-services.com/', json=req)
    r = r.json()

    hits = json.loads(r['hits'])

    if args.verbose:
        res_fmt = """---
    {name} ({id:d})

    {description}

        aka
            {titles}
        by {brand} ({brand_id:d})
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
    else:
        res_fmt = "{name}: https://hanime.tv/hentai/video/{slug}"

    for hit in hits:
        minutes, seconds = divmod(hit['duration_in_ms'], 60000)
        hours, minutes = divmod(minutes, 60)

        if args.verbose:
            hit.update({
                'duration': '{0}:{1}:{2}'.format(hours, minutes, seconds),
                'release_date': datetime.utcfromtimestamp(hit['released_at']),
                'upload_date': datetime.utcfromtimestamp(hit['created_at']),
                'titles': '\n        '.join(hit['titles']),
                'tags': ', '.join(hit['tags']),
            })

        print(res_fmt.format(**hit))

    if not args.verbose:
        print('---')

    print(f"Page {r['page'] + 1} of {r['nbPages']}, Results {r['nbHits']}")
