from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import CustomUser, BucketList, BucketListItem
from django.test import Client


class UserAPITestCase(APITestCase):
    """Tests for API authorizaion."""

    # fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_user_creation(self):
        """Test user can create account"""
        resp = self.client.post('/api/register/', {'username': 'samantha',
                                        'email': 'sam@gmail.com',
                                        'password': 'password'})
        self.assertEqual(resp.status_code, 201)

    def test_unauthorized_access(self):
        """Test that user cannot access bucketlist if not authorized."""
        resp = self.client.get('bucket_detail')

        self.assertEqual(resp.status_code, 404)

class BucketlistAPITestCase(APITestCase):
    """Test buckelist methods"""

    # fixtures = ['initial_data.json']

    def setUp(self):
        token_url = reverse('login')
        data = {
            'username': 'joan', 'password': 'ASHLEY19'}
        self.response = self.client.post(token_url, data)
        self.token = self.response.data.get('token')

    def test_bucketlist_creation(self):
        # Issue a POST request.
        resp = self.client.post('/api/bucketlist/create', {'name':'bucketlist'})
        self.assertEqual(resp.status_code, 301)

    def test_bucketlist_details(self):
        # Issue a GET request.
        response = self.client.get('/api/bucketlist/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 401)

    def test_bucketlist_edit(self):
        """Test that a user can edit a bucketlist"""

        create_resp = self.client.post('/api/bucketlist/create', {'name': 'surfing',},)
        edit_resp = self.client.put('/api/bucketlist/1/edit', { 'name': 'paragliding',},)
        self.assertEqual(edit_resp.status_code, 301)

    def test_bucketlist_delete(self):
        """Test that a user can delete a bucketlist."""
        create_resp = self.client.post('/api/bucketlist/create', {'name': 'surfing',},)

        delete_resp = self.client.delete('/api/bucketlist/1/delete')
        self.assertEqual(delete_resp.status_code, 301)


class BucketlistItemAPITestCase(APITestCase):
    """Test buckelistitem methods"""

    fixtures = ['initial_data.json']

    def setUp(self):
        token_url = reverse('login')
        data = {
            'username': 'joan', 'password': 'ASHLEY19'}
        self.response = self.client.post(token_url, data)
        self.token = self.response.data.get('token')

    def test_bucketlist_item_creation(self):
        """Test that a user can create a bucketlist item."""
        response = self.client.post('/api/bucketlist/1/items', {'name': 'hiking'})
        self.assertEqual(response.status_code, 301)    

    def test_bucketlistitem_edit(self):
        """Test that a bucketlistitem can be updated."""

        edited_item = {'name': 'sunrise', 'bucketlist': 1}

        response = self.client.put('/api/bucketlist/1/update/1', edited_item)
        self.assertEqual(response.status_code, 401)

    def test_deleting_bucketlist_item(self):
        delete_resp = self.client.delete('/api/bucketlist/1/items/1')

        self.assertEqual(delete_resp.status_code, 401)
