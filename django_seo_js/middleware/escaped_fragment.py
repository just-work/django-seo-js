from django_seo_js import settings
from django_seo_js.backends import SelectedBackend
from django_seo_js.helpers import request_should_be_ignored

import logging
logger = logging.getLogger(__name__)


class EscapedFragmentMiddleware(SelectedBackend):
    def process_request(self, request):
        logger.error('Processing request...')
        logger.error(request)
        if not settings.ENABLED:
            logger.error('SEO JS is not enabled')
            return

        if request_should_be_ignored(request):
            logger.error('Request was ignored!')
            return

        if "_escaped_fragment_" not in request.GET:
            logger.error('Escaped fragment not in GET-params')
            return

        url = self.backend.build_absolute_uri(request)
        try:
            logger.error('Processing url {}'.format(url))
            return self.backend.get_response_for_url(url)
        except Exception as e:
            logger.exception(e)


class HashBangMiddleware(EscapedFragmentMiddleware):

    def __init__(self, *args, **kwargs):
        logging.info(
            "Deprecation note: HashBangMiddleware has been renamed EscapedFragmentMiddleware,"
            " for more clarity. Upgrade your MIDDLEWARE_CLASSES to \n"
            "   'django_seo_js.middleware.EscapedFragmentMiddleware'"
            " when you get a chance. HashBangMiddleware will be removed in v0.5"
        )
        super(HashBangMiddleware, self).__init__(*args, **kwargs)
