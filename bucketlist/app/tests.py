from django.test import TestCase

from .models import CustomUser, BucketList, BucketListItem


class BucketlistModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(
            username='testuser',
            password='testpassword')
        self.bucketlist = BucketList.objects.create(
            name='testbucketlist', user=self.user)
        self.bucketlistitem = BucketListItem.objects.create(
            name='testbucketlstitem', bucketlist=self.bucketlist)

    def tearDown(self):
        CustomUser.objects.all().delete()
        BucketList.objects.all().delete()
        BucketListItem.objects.all().delete()

    def test_bucketlist_creation(self):
        self.assertTrue(BucketList.objects.all())
        self.assertIn('testbucketlist',
                      BucketList.objects.get(name='testbucketlist').name)
        self.assertIsInstance(self.bucketlist, BucketList)
