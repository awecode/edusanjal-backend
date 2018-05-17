from django.conf import settings

from versatileimagefield.utils import build_versatileimagefield_url_set


def create_set(img, sizes):
    files = build_versatileimagefield_url_set(img, sizes)
    dct = {}
    # TODO Handle Amazon S3
    prefix = settings.BASE_URL
    for key, val in files.items():
        dct[key] = prefix + val
    return dct
