from django.test import TestCase
from app.models import User, BucketList, BucketListItem


class BucketlistModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='pennyuser',
            password='password')
        self.bucketlist = BucketList.objects.create(
            name='bucketlist_one', user=self.user)
        self.bucketlistitem = BucketListItem.objects.create(
            name='bucketlstitem_one', bucketlist=self.bucketlist)

    def tearDown(self):
        User.objects.all().delete()
        BucketList.objects.all().delete()
        BucketListItem.objects.all().delete()

    def test_user_registration(self):
        """Tests that a user can create an account"""
        self.assertEqual(self.user.get_username(), 'pennyuser')
        self.assertIsInstance(self.user, User)

    def test_bucketlist_creation(self):
        """Tests that a user can create a bucketlist"""
        self.assertTrue(BucketList.objects.all())
        self.assertIn('bucketlist_one',
                      BucketList.objects.get(name='bucketlist_one').name)
        self.assertIsInstance(self.bucketlist, BucketList)

    def test_bucketlistitem_creation(self):
        """Tests that a user can create an item"""
        self.assertTrue(BucketListItem.objects.all())
        self.assertIn('bucketlstitem_one',
                      BucketListItem.objects.get(name='bucketlstitem_one').name)
        self.assertIsInstance(self.bucketlistitem, BucketListItem)
