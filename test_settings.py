HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://localhost:9001/solr/default',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
        'EXCLUDED_INDEXES': ['thirdpartyapp.search_indexes.BarIndex'],
    },
    'en': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://my-solr-server/solr/my-site-en/',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
    'de': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://my-solr-server/solr/my-site-de/',
        'TIMEOUT': 60 * 5,
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    },
}

HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'HAYSTACK_CONNECTIONS': HAYSTACK_CONNECTIONS,
    'INSTALLED_APPS': [
        'filer',
        'easy_thumbnails',
        'aldryn_people',
    ],
    'THUMBNAIL_PROCESSORS': (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    ),
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_people')

if __name__ == "__main__":
    run()
