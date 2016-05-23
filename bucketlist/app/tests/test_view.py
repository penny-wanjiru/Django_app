from django.core.urlresolvers import reverse
from django.test import TestCase
from app.models import CustomUser, BucketList, BucketListItem


class BucketlistViewTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='anotheruser',
            password='anotherpassword')
        self.bucketlist = BucketList.objects.create(
            name='bucketlist_two', user=self.user)
        self.bucketlistitem = BucketListItem.objects.create(
            name='bucketlistitem_two', bucketlist=self.bucketlist)

    def tearDown(self):
        BucketList.objects.all().delete()
        BucketListItem.objects.all().delete()

    def test_index_view(self):
        resp = self.client.post(reverse('index'), { 'username' :'anotheruser1',
            'email':'another1@gmail.com',
            'password':'anotherpassword1',
            'password_two':'anotherpassword1'})
        self.assertEqual(resp.status_code, 302)


    def test_bucketlist_view(self):
        resp = self.client.get(reverse('bucket_add'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.bucketlist, resp.context['bucketlist'])

    def test_bucketlist_delete(self):
        pass
    #   resp = self.client.post(reverse('bucketlist_delete'))   
