import unittest
import os
from unittest.mock import MagicMock, patch
import src.response as rp

class TestChatVLM(unittest.TestCase):
    
    @patch("src.response.HF_TOKEN", "fake-token")
    @patch("src.response.pipeline")
    @patch("src.response.AutoConfig")
    @patch("src.response.Image.open")
    def test_chat_vlm_response_local(self, mock_open, mock_autoconfig, mock_pipeline):
        mock_img = MagicMock()
        mock_img.save = MagicMock()
        mock_open.return_value = mock_img
        
        mock_pipeline_instance = MagicMock()
        mock_pipeline_instance.return_value = [{"generated_text": [{"content": "This is a test response"}]}]
        mock_pipeline.return_value = mock_pipeline_instance
        
        image = "./test_img.jpg"
        query = "What is there in the image?"
        response = rp.generate_response(image, query, True, "")
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertEqual(response, "This is a test response")
        mock_open.assert_called_once_with(image)
        
        mock_autoconfig.from_pretrained.assert_called_once_with(
            "google/gemma-3-4b-it",
            token=rp.HF_TOKEN
        )
        mock_pipeline.assert_called_once_with(
            "image-text-to-text",
            model="google/gemma-3-4b-it"
        )
        mock_pipeline_instance.assert_called_once()
    
    @patch("src.response.HF_TOKEN", "fake-token")
    @patch("src.response.InferenceClient")
    @patch("src.response.Image.open")
    def test_chat_vlm_response_api(self, mock_open, mock_inference):
        # test if a response is generated for a given query and image
        mock_img = MagicMock()
        mock_img.save = MagicMock()
        mock_open.return_value = mock_img
        
        mock_chat_completion = MagicMock()
        mock_chat_completion.choices = [MagicMock()]
        mock_chat_completion.choices[0].message.content = "This is a test response"
        
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.return_value = mock_chat_completion
        mock_inference.return_value = mock_client_instance
        
        image = "./test_img.jpg"
        query = "What is there in the image?"
        response = rp.generate_response(image, query, False, "")
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertEqual(response, "This is a test response")
        mock_open.assert_called_once_with(image)
        mock_inference.assert_called_once()
        mock_client_instance.chat.completions.create.assert_called_once()

    @unittest.skipUnless(
        os.getenv("RUN_REAL_API_TESTS") == "1",
        "Real HF API test"
    )
    def test_chat_vlm_response_real_api(self):
        # test if a response is generated for a given query and image on api
        image = "./test_img.jpg"
        query = "What is there in the image?"
        response = rp.generate_response(image, query, False, "")
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
    
    # def test_chat_vlm_response_real_local(self):
    #     # test if a response is generated for a given query and image on local model
    #     image = "./test_img.jpg"
    #     query = "What is there in the image?"
    #     response = rp.generate_response(image, query, True, "")
        
    #     self.assertIsNotNone(response)
    #     self.assertIsInstance(response, str)
        
