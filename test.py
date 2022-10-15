
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle



class FlaskTests(TestCase):
    
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        with self.client as client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            self.assertIn('board', session)

            self.assertIn('Times played:', html)

            self.assertIn('Score:', html)

            self.assertIn('Time left:', html)

    def test_check_word(self):
        with self.client as client:
            self.client.get('/')

            response = self.client.get('/check-word?word=beautiful')
            self.assertEqual(response.json['result'], 'not-on-board')

            response = self.client.get('/check-word?word=vnjfansvl')
            self.assertEqual(response.json['result'], 'not-word')

    def test_word(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["A", "B", "C", "D", "E"], 
                                    ["F", "G", "H", "I", "J"], 
                                    ["K", "L", "M", "N", "O"], 
                                    ["P", "Q", "R", "S", "T"], 
                                    ["U", "V", "W", "X", "Y"]]
            res = client.get('/check-word?word=bag')
            self.assertEqual(res.json['result'], 'ok')

##############################################################
# My post tests are not working. Can not find a bug       
    def test_post_record(self):
        with self.client as client:
            with self.client.session_transaction() as session:
                session['highest_score'] = 10
            res = client.post('/score', data={"score":"12"})

            self.assertEqual(res.status.code, 200)
            self.assertEqual(session["highest_score"], 12)
    
    def test_times_played(self):
        with self.client as client:
            with self.client.session_transaction() as session:
                session['times_played'] = 3
            res = client.post('/score', data={"score" : 10})
            self.assertEqual(session["times_played"])

      



            


