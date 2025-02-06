import unittest
import requests

class TestPsychometricsAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5001/api/psychometrics"

    def test_model_method(self):
        """
        Test the extraction endpoint using the 'model' method.
        """
        payload = {
            "text": "I always verify the sender's email and update my systems regularly. I follow all security protocols meticulously.",
            "method": "model"
        }
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200, "Expected status code 200")
        data = response.json()
        # Check that all expected keys are in the response
        self.assertIn("awareness", data)
        self.assertIn("conscientiousness", data)
        self.assertIn("stress", data)
        self.assertIn("neuroticism", data)
        self.assertIn("risk_tolerance", data)
        print("Model extraction response:", data)

    def test_prompt_method(self):
        """
        Test the extraction endpoint using the 'prompt' method.
        """
        payload = {
            "text": "I sometimes overlook security protocols when I'm in a hurry.",
            "method": "prompt"
        }
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200, "Expected status code 200")
        data = response.json()
        # Check that all expected keys are present
        self.assertIn("awareness", data)
        self.assertIn("conscientiousness", data)
        self.assertIn("stress", data)
        self.assertIn("neuroticism", data)
        self.assertIn("risk_tolerance", data)
        print("Prompt extraction response:", data)

    def test_invalid_method(self):
        """
        Test the endpoint with an invalid extraction method.
        """
        payload = {
            "text": "Test text for invalid method.",
            "method": "invalid_method"
        }
        response = requests.post(self.BASE_URL, json=payload)
        # Expect a 400 Bad Request response
        self.assertEqual(response.status_code, 400, "Expected status code 400 for invalid method")
        data = response.json()
        self.assertIn("error", data)
        print("Invalid method response:", data)

    def test_no_text(self):
        """
        Test the endpoint when no text is provided.
        """
        payload = {
            "text": "",
            "method": "model"
        }
        response = requests.post(self.BASE_URL, json=payload)
        # Expect a 400 Bad Request because text is required.
        self.assertEqual(response.status_code, 400, "Expected status code 400 when no text is provided")
        data = response.json()
        self.assertIn("error", data)
        print("No text provided response:", data)
    def test_azure_method(self):
        """
        Test the extraction endpoint using the 'azure' method.
        """
        payload = {
            "text": "I am concerned about the reliability of our outdated servers.",
            "method": "azure"
        }
        response = requests.post(self.BASE_URL, json=payload)
        self.assertEqual(response.status_code, 200, "Expected status code 200")
        data = response.json()
        # Depending on your Azure mapping logic, you might check for specific keys.
        self.assertIn("stress", data)  # example: check if stress was extracted/mapped
        print("Azure extraction response:", data)

if __name__ == '__main__':
    unittest.main()
