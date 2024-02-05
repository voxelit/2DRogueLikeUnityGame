"""
Test Cases TestAccountModel
"""
import json
from random import randrange
from unittest import TestCase
from models import db, app
from models.account import Account, DataValidationError

ACCOUNT_DATA = {}

class TestAccountModel(TestCase):
    """Test Account Model"""

    @classmethod
    def setUpClass(cls):
        """ Load data needed by tests """
        db.create_all()  # make our sqlalchemy tables
        global ACCOUNT_DATA
        with open('tests/fixtures/account_data.json') as json_data:
            ACCOUNT_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnext from database"""
        db.session.close()

    def setUp(self):
        """Truncate the tables"""
        self.rand = randrange(0, len(ACCOUNT_DATA))
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_accounts(self):
        """ Test creating multiple Accounts """
        for data in ACCOUNT_DATA:
            account = Account(**data)
            account.create()
        self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))

    def test_create_an_account(self):
        """ Test Account creation using known data """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        self.assertEqual(len(Account.all()), 1)

    def test_repr(self):
        """Test the representation of an account"""
        account = Account()
        account.name = "Foo"
        self.assertEqual(str(account), "<Account 'Foo'>")

    def test_to_dict(self):
        """ Test account to dict """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        result = account.to_dict()
        self.assertEqual(account.name, result["name"])
        self.assertEqual(account.email, result["email"])
        self.assertEqual(account.phone_number, result["phone_number"])
        self.assertEqual(account.disabled, result["disabled"])
        self.assertEqual(account.date_joined, result["date_joined"])

    def test_from_dict(self):
        """ Test account from dict """
        testDict = ACCOUNT_DATA[self.rand]
        account = Account()
        account.from_dict(testDict)
        self.assertEqual(account.name, testDict["name"])
        self.assertEqual(account.email, testDict["email"])
        self.assertEqual(account.phone_number, testDict["phone_number"])
        self.assertEqual(account.disabled, testDict["disabled"])

    def test_update(self):
        """ Test account update """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        newData = ACCOUNT_DATA[self.rand] # get a new set of data to replace old data
        account.from_dict(newData)
        account.update()
        self.assertEqual(len(Account.all()), 1) # make sure that same account was updated
        self.assertEqual(account.name, newData["name"]) # make sure account matches new data
        self.assertEqual(account.email, newData["email"])
        self.assertEqual(account.phone_number, newData["phone_number"])
        self.assertEqual(account.disabled, newData["disabled"])

    def test_updateFail(self):
        """ Test invalid account update """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        newData = ACCOUNT_DATA[self.rand] # get a new set of data to replace old data
        account.from_dict(newData)
        account.id = False  # turn account into invalid account
        try:
            account.update()
        except:
            print("Invalid account")

    def test_delete_an_account(self):
        """ Test Account Deletion """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        account.delete()
        self.assertEqual(len(Account.all()), 0)

    def test_find_account(self):
        """ Test Account Search """
        data = ACCOUNT_DATA[self.rand] # get a random account
        account = Account(**data)
        account.create()
        searchID = account.id
        result = Account.find(searchID)
        self.assertEqual(result, account)