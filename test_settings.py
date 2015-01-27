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
    # Use of this custom URLs provides a shortcut when testing apphooks
    'ROOT_URLCONF': 'aldryn_people.tests.urls',
    'TIME_ZONE': 'Europe/Zurich',
    'HAYSTACK_CONNECTIONS': HAYSTACK_CONNECTIONS,
    'INSTALLED_APPS': [
        'aldryn_people',
        'easy_thumbnails',
        'filer',
        'parler',
        'sortedm2m',
    ],
    'MIGRATION_MODULES': {
        'filer': 'filer.migrations_django',
    },
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
