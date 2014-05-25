# encoding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from manozodynas.testutils import StatefulTesting
from lxml.cssselect import CSSSelector
from manozodynas.models import *
from django.test import Client

class WordAddTest(StatefulTesting):
    def test_word_add(self):
        self.open(reverse('word'))
        self.assertStatusCode(200)
        qs = Word.objects.all()
	# checking that testing_word doesn't exist
        self.assertFalse(qs.filter(word='testing_word', type='n').exists())
        self.selectForm('#word_form')
        self.submitForm({
             'word': 'test',
             'type': 'n',
        })
        self.assertStatusCode(302)
	# checking that testing_word exists
        self.assertTrue(qs.filter(word='testing_word', type='n').exists())

class WordDeleteTest(StatefulTesting):
    def test_word_delete(self):
	# adding testing word via post
        c = Client()
        response = c.post('/word', {
             'word': 'testing_word',
             'type': 'a',
        })
        self.assertEqual(response.status_code, 302)
        qs = Word.objects.all()
	# checking if that testing_word exists
        self.assertTrue(qs.filter(word='testing_word').exists())
        word = qs.get(word='testing_word')
        id = str(word.id)
	# trying to delete testing_word
        response = c.post('/word/'+id+'/delete/')
        self.assertEqual(response.status_code, 302)
	# checking if testing_word doesn't exist anymore
        self.assertFalse(qs.filter(word='testing_word').exists())

class IndexTestCase(StatefulTesting):
    def test_index_page(self):
        self.open(reverse('index'))
        self.assertStatusCode(200)


class LoginTestCase(StatefulTesting):

    fixtures = ['test_fixture.json']

    def test_login_page(self):
        self.open(reverse('login'))
        self.assertStatusCode(200)

    def test_good_login(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'test',
            'password': 'test',
        })
        self.assertStatusCode(302)

    def test_bad_login(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'bad',
            'password': 'bad',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')

    def test_no_input(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': '',
            'password': '',
        })
        self.assertStatusCode(200)
        self.selectMany('.errorlist')

    def test_no_username(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': '',
            'password': 'test',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')

    def test_no_password(self):
        self.open(reverse('login'))
        self.selectForm('#login')
        self.submitForm({
            'username': 'test',
            'password': '',
        })
        self.assertStatusCode(200)
        self.selectOne('.errorlist')
