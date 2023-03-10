"""
This is a simple script to pull your record collection
from Discogs and output it in a table.
"""

from collections import OrderedDict
from rich.console import Console
from rich.table import Table
import creds
import discogs_client

CONSOLE = Console()
USER_TOKEN = creds.user_token


def get_user_auth():
    user_client = discogs_client.Client('collection/0.1',
                                        user_token=USER_TOKEN)

    return user_client.identity()


def get_record_collection(user):

    #
    # Created a dict to allow more data control as the
    # discogs and rich Classes can be restrictive
    #
    record_collection = {}
    table = Table(title="Album Collection")
    table.add_column("Artist", justify="left", style="cyan")
    table.add_column("Album", justify="left", style="green")
    table.add_column("Year", justify="left", style="yellow")
    table.add_column("Format", justify="left", style="red")
    with CONSOLE.status('Gathering your collection...', spinner='bouncingBall'):
        for item in user.collection_folders[0].releases:
            if item.release.artists[0].name in record_collection:
                record_collection[item.release.artists[0].name].update({
                    item.release.title: ({
                        'year': item.release.year,
                        'format': item.release.formats[0]['name'],
                    })
                })
            else:
                record_collection.update({
                    item.release.artists[0].name: ({
                        item.release.title: ({
                            'year': item.release.year,
                            'format': item.release.formats[0]['name'],
                        })
                    })
                })

        #
        # Alphabetize Artists as keys
        #
        record_collection = OrderedDict(sorted(record_collection.items()))

        #
        # Format data and add to table
        #
        for artist_name, album_values in record_collection.items():
            for album_name, rformat in album_values.items():
                table.add_row(artist_name,
                              album_name,
                              str(rformat['year']),
                              rformat['format'],
                              )
    CONSOLE.print(table)
    CONSOLE.print(user.collection_folders[0].count)


def main():
    user = get_user_auth()
    get_record_collection(user)


if __name__ == '__main__':
    main()
