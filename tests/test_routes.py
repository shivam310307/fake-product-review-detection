"""
Automated Integration Tests for Flask Routes and Security Guardrails
=====================================================================
"""

import unittest
from app import create_app, db, User, PredictionHistory

class TestFlaskRoutes(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Provision test admin user
        test_user = User(username='testadmin', role='admin')
        test_user.set_password('TestPass@123')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ReviewGuard AI', response.data)
        self.assertIn(b'Decision Tree', response.data)
        self.assertIn(b'AdaBoost', response.data)

    def test_unauthenticated_dashboard_open_access(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Operational Intelligence Dashboard', response.data)

    def test_login_success(self):
        response = self.client.post('/login', data={
            'username': 'testadmin',
            'password': 'TestPass@123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Operational Intelligence Dashboard', response.data)

    def test_login_failure(self):
        response = self.client.post('/login', data={
            'username': 'testadmin',
            'password': 'WrongPassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_authenticated_predict_route(self):
        # Log in first
        self.client.post('/login', data={
            'username': 'testadmin',
            'password': 'TestPass@123'
        })

        # Submit prediction
        response = self.client.post('/predict', data={
            'review_text': 'I bought this mouse 3 days ago. The scroll wheel is very smooth.',
            'model_choice': 'adaboost',
            'rating': '5',
            'category': 'Electronics'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prediction Verdict', response.data)

        # Verify recorded in DB
        pred = PredictionHistory.query.first()
        self.assertIsNotNone(pred)
        self.assertEqual(pred.category, 'Electronics')

    def test_ssrf_protection_blocked(self):
        """Verify that private IP ranges are rejected before network requests."""
        # Log in first
        self.client.post('/login', data={
            'username': 'testadmin',
            'password': 'TestPass@123'
        })

        # Test local loopback attack
        response = self.client.post('/live_prediction', data={
            'product_url': 'http://127.0.0.1:8080/admin',
            'model_choice': 'adaboost'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Live URL Analysis Error', response.data)

    def test_api_predict_endpoint(self):
        response = self.client.post('/api/predict', json={
            'text': 'The packaging arrived damaged and the keyboard was missing the USB dongle.',
            'model': 'adaboost',
            'rating': 1,
            'category': 'Electronics'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('prediction_label', data)
        self.assertIn('confidence_score', data)

if __name__ == '__main__':
    unittest.main()
