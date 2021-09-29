from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from progame.views import PublicIndexTemplateView


class TestUrls(TestCase):

    def test_public_index_resolves(self):
        url = reverse('progame:public_index')
        self.assertEquals(resolve(url).func.view_class, PublicIndexTemplateView)

    # repetir método acima para todas as urls
    # ...
