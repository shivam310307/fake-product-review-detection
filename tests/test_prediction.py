"""
Automated Unit Tests for ML Model Prediction Engine
===================================================
"""

import unittest
from src.prediction import predict_single_review, get_model_status

class TestPrediction(unittest.TestCase):
    
    def test_model_status(self):
        status = get_model_status()
        self.assertIn('decision_tree', status)
        self.assertIn('adaboost', status)
        self.assertTrue(status['decision_tree'], "Decision Tree model should be present")
        self.assertTrue(status['adaboost'], "AdaBoost model should be present")

    def test_adaboost_prediction(self):
        sample = "I tested this product for two weeks. It works reasonably well, battery lasts 14 hours."
        res = predict_single_review(sample, model_name='adaboost')
        self.assertIn(res['prediction_label'], ['Genuine', 'Fake'])
        self.assertIn(res['prediction_binary'], [0, 1])
        self.assertGreaterEqual(res['confidence_score'], 0.5)
        self.assertAlmostEqual(res['genuine_probability'] + res['fake_probability'], 1.0, places=3)
        self.assertIsInstance(res['top_keywords'], list)
        self.assertIn('disclaimer', res)

    def test_decision_tree_prediction(self):
        sample = "BEST PRODUCT IN THE ENTIRE WORLD AMAZING INCREDIBLE BUY NOW WOW WOW WOW!!!"
        res = predict_single_review(sample, model_name='decision_tree')
        self.assertIn(res['prediction_label'], ['Genuine', 'Fake'])
        self.assertIn(res['prediction_binary'], [0, 1])
        self.assertGreaterEqual(res['confidence_score'], 0.5)
        self.assertAlmostEqual(res['genuine_probability'] + res['fake_probability'], 1.0, places=3)

    def test_empty_review_handling(self):
        res = predict_single_review("", model_name='adaboost')
        self.assertIn(res['prediction_label'], ['Genuine', 'Fake'])

    def test_unknown_model_fallback(self):
        # Should fallback gracefully to adaboost or decision_tree
        res = predict_single_review("Great battery life", model_name='non_existent_model')
        self.assertIn(res['prediction_label'], ['Genuine', 'Fake'])

if __name__ == '__main__':
    unittest.main()
