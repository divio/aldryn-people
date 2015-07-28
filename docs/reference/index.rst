#########
Reference
#########

*****
Email
*****

ALDRYN_JOBS_DEFAULT_SEND_TO
===========================

Optional, the email address to which job applications will be sent by default. Your Django project
will need to be configured for email transfer.


******************
Attachment storage
******************

Job applicants can attach files in support of their applications for vacancies. These files are
saved and stored using Django's file storage API. You need to ensure that the storage options you
choose are appropriately secured against unauthorised access:

ALDRYN_JOBS_ATTACHMENT_STORAGE
==============================

The storage object that is going to be passed directly to ``FileField`` constructor.

Refer to Django's file storage API documentation for more info.

Default: ``None`` (which means ``django.core.files.storage.default_storage`` is going to be used).

ALDRYN_JOBS_ATTACHMENT_UPLOAD_DIR
=================================

The directory atachments will be uploaded to.

Default: ``attachments/%Y/%m/``.


File Count & Size
=================

* ``ALDRYN_JOBS_ATTACHMENTS_MAX_COUNT``: Max amount of files to be uploadable (default: 5)
* ``ALDRYN_JOBS_ATTACHMENTS_MIN_COUNT``: Min amount of files to be uploadable (default: 0)
* ``ALDRYN_JOBS_ATTACHMENTS_MAX_FILE_SIZE``: Max file size (each) (default: 5MB)
