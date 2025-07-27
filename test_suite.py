import unittest
import json
import os
import sys
import tempfile
from unittest.mock import patch, MagicMock

# Add the project directory to the path
sys.path.append('/home/ubuntu/mental_health_ai')

# Import modules to test
from data_exporter import export_logs_to_csv, get_all_logs
from notification_system import set_reminder, display_reminder
from wellness_coach import breathing_exercise, sleep_tracker_manual_entry
from api_server import app as api_app
from auth_system import generate_token, verify_token

class TestDataExporter(unittest.TestCase):
    """Test data export functionality."""
    
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        self.test_file.close()
    
    def tearDown(self):
        if os.path.exists(self.test_file.name):
            os.unlink(self.test_file.name)
    
    def test_export_logs_to_csv(self):
        """Test CSV export functionality."""
        import pandas as pd
        
        # Create test data
        test_data = pd.DataFrame({
            'timestamp': ['2025-07-26T10:00:00'],
            'message': ['Test message']
        })
        
        # Test export
        result = export_logs_to_csv('test', test_data, self.test_file.name)
        self.assertIn('Successfully exported', result)
        
        # Verify file exists and has content
        self.assertTrue(os.path.exists(self.test_file.name))
        
        # Test reading back the data
        read_data = get_all_logs(self.test_file.name)
        self.assertEqual(len(read_data), 1)
        self.assertEqual(read_data.iloc[0]['message'], 'Test message')

class TestNotificationSystem(unittest.TestCase):
    """Test notification and reminder functionality."""
    
    @patch('builtins.print')
    def test_display_reminder(self, mock_print):
        """Test reminder display function."""
        test_message = "Test reminder message"
        display_reminder(test_message)
        
        # Check that print was called with the reminder message
        mock_print.assert_called_with(f"\n!!! REMINDER: {test_message} !!!\n")

class TestWellnessCoach(unittest.TestCase):
    """Test wellness coach functionality."""
    
    @patch('time.sleep')
    @patch('builtins.print')
    def test_breathing_exercise(self, mock_print, mock_sleep):
        """Test breathing exercise function."""
        # Run a very short breathing exercise
        breathing_exercise(duration_seconds=1)
        
        # Verify that print was called (exercise started)
        self.assertTrue(mock_print.called)
        
        # Verify that sleep was called (timing functionality)
        self.assertTrue(mock_sleep.called)

class TestAPIServer(unittest.TestCase):
    """Test API server endpoints."""
    
    def setUp(self):
        self.app = api_app.test_client()
        self.app.testing = True
    
    def test_home_endpoint(self):
        """Test the home endpoint."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('AI Mental Health Companion API', data['message'])
    
    def test_chat_endpoint(self):
        """Test the chat endpoint."""
        test_message = {"message": "Hello, how are you?"}
        
        response = self.app.post('/api/chat',
                               data=json.dumps(test_message),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('response', data)
        self.assertIn('timestamp', data)
    
    def test_mood_logging(self):
        """Test mood logging endpoint."""
        test_mood = {
            "mood": "happy",
            "intensity": 8,
            "notes": "Feeling great today!"
        }
        
        response = self.app.post('/api/mood',
                               data=json.dumps(test_mood),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('mood_entry', data)
    
    def test_journal_creation(self):
        """Test journal entry creation."""
        test_journal = {
            "title": "Test Entry",
            "content": "This is a test journal entry."
        }
        
        response = self.app.post('/api/journal',
                               data=json.dumps(test_journal),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('journal_entry', data)
    
    def test_analytics_endpoint(self):
        """Test analytics endpoint."""
        response = self.app.get('/api/analytics')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('overview', data)
        self.assertIn('mood_analytics', data)

class TestAuthSystem(unittest.TestCase):
    """Test authentication system."""
    
    def test_token_generation_and_verification(self):
        """Test JWT token generation and verification."""
        user_id = 123
        
        # Generate token
        token = generate_token(user_id)
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)
        
        # Verify token
        verified_user_id = verify_token(token)
        self.assertEqual(verified_user_id, user_id)
    
    def test_invalid_token_verification(self):
        """Test verification of invalid token."""
        invalid_token = "invalid.token.here"
        result = verify_token(invalid_token)
        self.assertIsNone(result)

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_complete_workflow(self):
        """Test a complete user workflow."""
        # This would test the integration of multiple components
        # For now, we'll just verify that all modules can be imported
        try:
            import data_exporter
            import notification_system
            import wellness_coach
            import api_server
            import auth_system
            self.assertTrue(True)  # All imports successful
        except ImportError as e:
            self.fail(f"Failed to import module: {e}")

def run_tests():
    """Run all tests and return results."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestDataExporter,
        TestNotificationSystem,
        TestWellnessCoach,
        TestAPIServer,
        TestAuthSystem,
        TestIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result

if __name__ == '__main__':
    print("Running Mental Health AI Companion Test Suite...")
    print("=" * 50)
    
    result = run_tests()
    
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed. Please review the output above.")

