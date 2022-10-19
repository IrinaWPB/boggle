
from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle



class FlaskTests(TestCase):
    
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Tests rendered homepage"""
        
        with self.client as client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            self.assertIn('board', session)

            self.assertIn('Times played:', html)

            self.assertIn('Score:', html)

            self.assertIn('Time left:', html)

    def test_check_word(self):
        """Tests invalid words"""

        with self.client as client:
            self.client.get('/')

            response = self.client.get('/check-word?word=beautiful')
            self.assertEqual(response.json['result'], 'not-on-board')

            response = self.client.get('/check-word?word=vnjfansvl')
            self.assertEqual(response.json['result'], 'not-word')

    def test_word(self):
        """Tests a valid word"""

        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["A", "B", "C", "D", "E"], 
                                    ["F", "G", "H", "I", "J"], 
                                    ["K", "L", "M", "N", "O"], 
                                    ["P", "Q", "R", "S", "T"], 
                                    ["U", "V", "W", "X", "Y"]]
            res = client.get('/check-word?word=bag')
            self.assertEqual(res.json['result'], 'ok')

  
    def test_post_view(self):
        """Tests updated info in session"""

        with self.client as client:
            with client.session_transaction() as session:
                session['highest_score'] = 10
                session['times_played'] = 3
            res = client.post('/score', json={"score":"12"})

            with client.session_transaction() as changed_session:
                self.assertEqual(res.status_code, 200)

                #Updates higest score if score is higher than current record                
                self.assertEqual(changed_session["highest_score"], 12)

                #Updates times_played when game is finished
                self.assertEqual(changed_session["times_played"], 4)





            


