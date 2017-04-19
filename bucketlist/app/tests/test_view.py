from django.core.urlresolvers import reverse
from django.test import TestCase
from app.models import User, BucketList, BucketListItem


class BucketlistViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='anotheruser',
            password='anotherpassword')
        self.login = self.client.login(
            username='anotheruser', password='anotherpassword')
        self.bucketlist = BucketList.objects.create(
            name='bucketlist_two', user=self.user)
        self.bucketlistitem = BucketListItem.objects.create(
            name='bucketlistitem_two', bucketlist=self.bucketlist)

    def tearDown(self):
        BucketList.objects.all().delete()
        BucketListItem.objects.all().delete()

    def test_index_view(self):
        """Tests that user can register"""
        resp = self.client.post(reverse('index'), {'username': 'anotheruser1',
            'email': 'another1@gmail.com',
            'password': 'anotherpassword1',
            'password_two':'anotherpassword1'})
        self.assertEqual(resp.status_code, 302)

    def test_index_validation(self):
        """Tests that a user has to fill in correct confirm password"""
        resp = self.client.post(reverse('index'), {'username': 'anotheruser1',
            'email': 'another1@gmail.com',
            'password': 'anotherpassword1',
            'password_two':'anotherpassword2'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Passwords do not match", status_code=200)

    def test_login_view(self):
        """Tests that a user can login"""
        resp = self.client.post(reverse('login'),
                                {'username': 'anotheruser',
                                 'password': 'anotherpassword'})
        self.assertEqual(resp.status_code, 302)

    def test_auth_login_view(self):
        """Tests that a user cannot submit empty fields"""
        resp = self.client.post(reverse('login'), {
            'username': '',
            'password': ''})
        self.assertEqual(resp.status_code, 200)
        # self.assertContains(resp, "All fields are required!", status_code=400)

    def test_user_logout(self):
        """Tests that a user can logout"""
        resp = self.client.post(reverse('logout'))
        self.assertEqual(resp.status_code, 405)

    def test_bucketlist_view(self):
        """Tests creation of a bucketlist"""
        resp = self.client.get(reverse('bucket_add'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(BucketList.objects.count(), 1)


    def test_bucketlist_delete(self):
        """Tests deletion of a bucketlist"""
        resp = self.client.get(reverse('bucketlist_delete',
                                       kwargs={'pk': self.bucketlist.id}))
        self.assertEqual(resp.status_code, 302)

    def test_bucketlist_update(self):
        """Tests updating of a bucketlist"""
        resp = self.client.post(
            reverse('bucketlist_edit',
                    kwargs={'pk': self.bucketlist.id}),
            {'name': 'Skydiving'})
        self.assertEqual(resp.status_code, 302)


    def test_item_update(self):
        """Test updating of a bucketlist item."""
        resp = self.client.post(
            reverse('items_edit', kwargs={'pk': self.bucketlistitem.id,
                                          'bucketlist': self.bucketlist.id}),
            {'name': 'gliding'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(BucketListItem.objects.get(id=self.bucketlistitem.id).name,
            'gliding')

    def test_item_delete(self):
        """Test deletion of a bucketlist item."""
        resp = self.client.get(
            reverse('bucketlistitems_delete',
                    kwargs={'pk': self.bucketlistitem.id,
                            'bucketlist': self.bucketlist.id}))
        self.assertEqual(resp.status_code, 302)
