from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from ..models import Diplomat

DIPLOMAT_LIST_URL = reverse('diplomat-list')
DIPLOMAT_NEW_URL = reverse('diplomat-new')


def get_url_by_action_and_id(action='detail', id='1'):
    return reverse(f'diplomat-{action}', args=[id])


def get_diplomat_url_with_filters(filters: dict):
    tokens = [DIPLOMAT_LIST_URL, '?']
    filters_paired_tokens = list(map(lambda kv: '='.join(kv), filters.items()))
    joined_filters = '&'.join(filters_paired_tokens)
    tokens.append(joined_filters)

    return ''.join(tokens)


def create_sample_diplomat(first_name='John', last_name='Doe',
                           country_iso='BG', path='CO'):
    payload = {'first_name': first_name,
               'last_name': last_name,
               'email': f'{first_name}.{last_name}@mail.com',
               'age': 23,
               'phone': '+9934002314',
               'country_iso': country_iso,
               'path': path}
    new = Diplomat.objects.create(**payload)
    return new


class PublicDiplomatViewsTests(TestCase):
    """Tests for publicly accessed Diplomat's Views."""
    def setUp(self):
        self.client = Client()
        newly_created = create_sample_diplomat()
        self.new_id = newly_created.id

    def test_diplomat_list_redirects_unauthenticated(self):
        """Test that diplomat list view redirects unauthenticated users."""
        response = self.client.get(DIPLOMAT_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('accounts/login', response.url)

    def test_diplomat_detail_redirects_unauthenticated(self):
        """Test that diplomat detail view redirects unauthenticated users."""
        response = self.client.get(get_url_by_action_and_id('detail',
                                                            self.new_id))

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('accounts/login', response.url)

    def test_diplomat_edit_redirects_unauthenticated(self):
        """Test that diplomat edit view redirects unauthenticated users."""
        response = self.client.get(get_url_by_action_and_id('edit',
                                                            self.new_id))

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('accounts/login', response.url)

    def test_diplomat_delete_redirects_unauthenticated(self):
        """Test that diplomat edit view redirects unauthenticated users."""
        response = self.client.get(get_url_by_action_and_id('delete',
                                                            self.new_id))

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn('accounts/login', response.url)


class PrivateDiplomatViewsTests(TestCase):
    """Tests for Diplomat views which are retrieved by authenticated user."""
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            'test@somedomain.com',
            'testpass1'
        )
        self.client.force_login(self.user)
        newly_created = create_sample_diplomat()
        self.new_id = newly_created.id

    def test_diplomat_list_GET(self):
        """Test retrieving list of Diplomats."""
        response = self.client.get(DIPLOMAT_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'diplomat_list.html')

    def test_diplomat_detail_GET(self):
        """Test retrieving Detail View of Diplomat."""
        response = self.client.get(get_url_by_action_and_id('detail',
                                                            self.new_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'diplomat_detail.html')

    def test_diplomat_delete_GET(self):
        """Test retrieving Delete View of Diplomat."""
        response = self.client.get(get_url_by_action_and_id('delete',
                                                            self.new_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'diplomat_delete.html')

    def test_diplomat_edit_GET(self):
        """Test retrieving Edit View of Diplomat."""
        response = self.client.get(get_url_by_action_and_id('edit',
                                                            self.new_id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'diplomat_form.html')

    def test_diplomat_new_GET(self):
        """Test retrieving New View of Diplomat."""
        response = self.client.get(DIPLOMAT_NEW_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'diplomat_form.html')

    def test_diplomat_query_filter_by_name(self):
        """Test the filtering by name."""
        url = get_diplomat_url_with_filters({'name': 'John'})

        response = self.client.get(url)

        object_list = response.context.get('object_list', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'diplomat_list.html')
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].first_name, 'John')
        self.assertEqual(object_list[0].last_name, 'Doe')

    def test_diplomat_query_filter_by_iso(self):
        """Test the filtering by iso."""
        create_sample_diplomat(first_name='George', country_iso='NL')
        url = get_diplomat_url_with_filters({'iso': 'NL'})

        response = self.client.get(url)

        object_list = response.context.get('object_list', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'diplomat_list.html')
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].country_iso, 'NL')
        self.assertEqual(object_list[0].first_name, 'George')

    def test_diplomat_query_filter_by_path(self):
        """Test the filtering by path."""
        create_sample_diplomat(first_name='George', path='PO',
                               country_iso='NL')
        url = get_diplomat_url_with_filters({'path': 'PO'})

        response = self.client.get(url)

        object_list = response.context.get('object_list', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'diplomat_list.html')
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].country_iso, 'NL')
        self.assertEqual(object_list[0].path, 'PO')
        self.assertEqual(object_list[0].first_name, 'George')

    def test_diplomat_query_filter_by_all_filters(self):
        """Test the filtering by all three filters: 'name', 'iso', 'region'."""
        create_sample_diplomat(first_name='George', path='PO',
                               country_iso='NL')
        create_sample_diplomat(first_name='George', path='PO',
                               country_iso='BG')
        url = get_diplomat_url_with_filters({'name': 'George',
                                             'path': 'PO',
                                             'iso': 'NL'})

        response = self.client.get(url)
        object_list = response.context.get('object_list', None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'diplomat_list.html')
        self.assertEqual(len(object_list), 1)
        self.assertEqual(object_list[0].country_iso, 'NL')
        self.assertEqual(object_list[0].path, 'PO')
        self.assertEqual(object_list[0].first_name, 'George')
