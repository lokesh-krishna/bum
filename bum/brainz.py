"""
Musicbrainz related functions.
"""
import time
import musicbrainzngs as mus

from .__init__ import __version__


def init():
    """Initialize musicbrainz."""
    mus.set_useragent("python-bum: A cover art daemon.",
                      __version__,
                      "https://github.com/dylanaraps/bum")


def get_cover(song, size=250, retry_delay=5, retries=1):
    """Download the cover art."""
    try:
        data = mus.search_releases(artist=song["artist"],
                                   release=song["album"],
                                   limit=1)
        release_id = data["release-list"][0]["release-group"]["id"]

        return mus.get_release_group_image_front(release_id, size=size)

    except mus.NetworkError:
        if retries == 0:
            raise mus.NetworkError("Failure connecting to MusicBrainz.org")
        time.sleep(retry_delay)
        get_cover(song, size, retries=retries - 1)

    except mus.ResponseError:
        return False
