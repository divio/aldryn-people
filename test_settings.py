HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
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


# def run():
#     from djangocms_helper import runner
#     runner.cms('aldryn_people')

def run():
    import sys
    from djangocms_helper import runner
    if len(sys.argv) == 1:
        sys.argv.append('test')
    sys.argv.append('--extra-settings=test_settings.py')
    runner.cms('aldryn_people')

if __name__ == "__main__":
    run()
