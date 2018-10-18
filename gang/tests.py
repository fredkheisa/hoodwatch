from django.test import TestCase
from .models import Neighbour
from django.contrib.auth.models import User


class HoodTestClass(TestCase):
    """
    Test neighbour class and its functions
    """
    def setUp(self):
        self.user = User.objects.create(id =1, username='a')
        self.hood = Neighbour(name='mtaani', location='huko tu', user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.hood, Neighbour))

    
    def test_save_method(self):
        """
        Function to test that neighbourhood is being saved
        """
        self.hood.create_neigborhood()
        hoods = Neighbour.objects.all()
        self.assertTrue(len(hoods) > 0)

    def test_delete_method(self):
        """
        Function to test that a neighbourhood can be deleted
        """
        self.hood.create_neigborhood()
        self.hood.delete_neigborhood

    def test_update_method(self):
        """
        Function to test that a neighbourhood's details can be updated
        """
        self.hood.create_neigborhood()
        new_hood = Neighbour.objects.filter(name='mtaani').update(name='Bias')
        hoods = Neighbour.objects.get(name='Bias')
        self.assertTrue(hoods.name, 'Bias')

    
    def test_get_hood_by_id(self):
        """
        Function to test if you can get a hood by its id
        """
        self.hood.create_neigborhood()
        this_hood= self.hood.get_by_id(self.hood.id)
        hood = Neighbour.objects.get(id=self.hood.id)
        self.assertTrue(this_hood, hood)

  