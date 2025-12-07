#!/usr/bin/env python3
"""
Unit tests for the TPM chunking implementation.
================================================

Tests:
- TokenLimitExceeded exception
- parse_tpm_error() function
- Chunking logic
- Error handling flow

Run with: python -m pytest test_chunking.py -v
Or simply: python test_chunking.py
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import (
    TokenLimitExceeded,
    parse_tpm_error,
    estimate_tokens,
)


class TestTokenLimitExceededException(unittest.TestCase):
    """Tests for the TokenLimitExceeded exception class."""

    def test_exception_stores_values(self):
        """Exception should store limit and requested token counts."""
        exc = TokenLimitExceeded(limit=12000, requested=20322, message="Test error")
        
        self.assertEqual(exc.limit, 12000)
        self.assertEqual(exc.requested, 20322)
        self.assertEqual(str(exc), "Test error")

    def test_exception_can_be_raised_and_caught(self):
        """Exception should be raisable and catchable."""
        with self.assertRaises(TokenLimitExceeded) as context:
            raise TokenLimitExceeded(limit=12000, requested=25000, message="TPM exceeded")
        
        self.assertEqual(context.exception.limit, 12000)
        self.assertEqual(context.exception.requested, 25000)


class TestParseTpmError(unittest.TestCase):
    """Tests for the parse_tpm_error() function."""

    def test_parse_standard_groq_error(self):
        """Should parse standard Groq TPM error message."""
        error_msg = (
            "Request too large for model `llama-3.3-70b-versatile` in organization "
            "`org_01kbrx41wtesrrvwj0z361z1xk` service tier `on_demand` on tokens per "
            "minute (TPM): Limit 12000, Requested 20322, please reduce your message "
            "size and try again."
        )
        
        result = parse_tpm_error(error_msg)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["limit"], 12000)
        self.assertEqual(result["requested"], 20322)

    def test_parse_different_numbers(self):
        """Should parse various token counts correctly."""
        error_msg = "Limit 6000, Requested 15000"
        
        result = parse_tpm_error(error_msg)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["limit"], 6000)
        self.assertEqual(result["requested"], 15000)

    def test_parse_large_numbers(self):
        """Should handle large token counts."""
        error_msg = "Limit 128000, Requested 250000"
        
        result = parse_tpm_error(error_msg)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["limit"], 128000)
        self.assertEqual(result["requested"], 250000)

    def test_returns_none_for_non_tpm_error(self):
        """Should return None for non-TPM errors."""
        error_msg = "Invalid API key"
        
        result = parse_tpm_error(error_msg)
        
        self.assertIsNone(result)

    def test_returns_none_for_empty_string(self):
        """Should return None for empty string."""
        result = parse_tpm_error("")
        
        self.assertIsNone(result)

    def test_case_insensitive(self):
        """Should handle case variations."""
        error_msg = "limit 12000, requested 20000"
        
        result = parse_tpm_error(error_msg)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["limit"], 12000)
        self.assertEqual(result["requested"], 20000)


class TestEstimateTokens(unittest.TestCase):
    """Tests for the estimate_tokens() function."""

    def test_estimate_basic(self):
        """Should estimate tokens from word count."""
        # 100 words * 1.3 = 130 tokens
        result = estimate_tokens(100)
        self.assertEqual(result, 130)

    def test_estimate_zero(self):
        """Should handle zero words."""
        result = estimate_tokens(0)
        self.assertEqual(result, 0)

    def test_estimate_large(self):
        """Should handle large word counts."""
        # 10000 words * 1.3 = 13000 tokens
        result = estimate_tokens(10000)
        self.assertEqual(result, 13000)


class TestChunkingLogic(unittest.TestCase):
    """Tests for the chunking behavior."""

    def test_chunk_calculation(self):
        """Verify chunk size calculation based on TPM limit."""
        tpm_limit = 12000
        safe_input_tokens = int(tpm_limit * 0.7)  # 8400
        chunk_char_size = safe_input_tokens * 4   # 33600 chars
        
        self.assertEqual(safe_input_tokens, 8400)
        self.assertEqual(chunk_char_size, 33600)

    def test_text_splitting_simulation(self):
        """Simulate how text would be split into chunks."""
        # Create a mock transcript
        words = ["word"] * 10000  # 10000 words, ~50000 chars
        transcript = " ".join(words)
        
        tpm_limit = 12000
        safe_input_tokens = int(tpm_limit * 0.7)
        chunk_char_size = safe_input_tokens * 4
        
        # Simulate chunking
        chunks = []
        current_chunk = []
        current_size = 0
        overlap_words = 50
        
        for word in words:
            word_size = len(word) + 1
            if current_size + word_size > chunk_char_size and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = current_chunk[-overlap_words:] if len(current_chunk) > overlap_words else []
                current_size = sum(len(w) + 1 for w in current_chunk)
            current_chunk.append(word)
            current_size += word_size
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        # Should create multiple chunks
        self.assertGreater(len(chunks), 1)
        print(f"\n  Simulated chunking: {len(words)} words → {len(chunks)} chunks")
        
        # Each chunk should be under the size limit (except possibly last)
        for i, chunk in enumerate(chunks[:-1]):
            self.assertLessEqual(len(chunk), chunk_char_size + 1000)  # Allow some tolerance


class TestIntegrationMocked(unittest.TestCase):
    """Integration tests with mocked API calls."""

    @patch('app.requests.post')
    def test_413_error_triggers_token_limit_exceeded(self, mock_post):
        """A 413 response should raise TokenLimitExceeded."""
        from app import call_openai_compatible
        
        # Mock a 413 response
        mock_response = MagicMock()
        mock_response.status_code = 413
        mock_response.json.return_value = {
            "error": {
                "message": "Limit 12000, Requested 20322"
            }
        }
        mock_post.return_value = mock_response
        
        config = {
            "name": "Test Provider",
            "env_key": "TEST_API_KEY",
            "api_url": "https://api.test.com/v1/chat/completions",
            "model": "test-model"
        }
        
        with patch.dict(os.environ, {"TEST_API_KEY": "fake-key"}):
            with self.assertRaises(TokenLimitExceeded) as context:
                call_openai_compatible("system", "user message", config)
            
            self.assertEqual(context.exception.limit, 12000)
            self.assertEqual(context.exception.requested, 20322)

    @patch('app.requests.post')
    def test_successful_response_returns_content(self, mock_post):
        """A successful response should return the content."""
        from app import call_openai_compatible
        
        # Mock a successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {"content": "Generated notes here"},
                "finish_reason": "stop"
            }]
        }
        mock_post.return_value = mock_response
        
        config = {
            "name": "Test Provider",
            "env_key": "TEST_API_KEY",
            "api_url": "https://api.test.com/v1/chat/completions",
            "model": "test-model"
        }
        
        with patch.dict(os.environ, {"TEST_API_KEY": "fake-key"}):
            result = call_openai_compatible("system", "user message", config)
            
            self.assertEqual(result, "Generated notes here")


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""

    def test_parse_tpm_error_with_extra_whitespace(self):
        """Should handle extra whitespace in error message."""
        error_msg = "Limit  12000,   Requested  20322"
        
        result = parse_tpm_error(error_msg)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["limit"], 12000)
        self.assertEqual(result["requested"], 20322)

    def test_parse_tpm_error_partial_match(self):
        """Should return None if only partial match."""
        error_msg = "Limit 12000"  # Missing Requested
        
        result = parse_tpm_error(error_msg)
        
        self.assertIsNone(result)

    def test_token_limit_exceeded_inheritance(self):
        """TokenLimitExceeded should be an Exception."""
        exc = TokenLimitExceeded(1000, 2000, "test")
        
        self.assertIsInstance(exc, Exception)


def run_tests():
    """Run all tests with verbose output."""
    print("\n" + "=" * 60)
    print("  🧪 Running TPM Chunking Unit Tests")
    print("=" * 60 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTokenLimitExceededException))
    suite.addTests(loader.loadTestsFromTestCase(TestParseTpmError))
    suite.addTests(loader.loadTestsFromTestCase(TestEstimateTokens))
    suite.addTests(loader.loadTestsFromTestCase(TestChunkingLogic))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationMocked))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("  ✅ All tests passed!")
    else:
        print(f"  ❌ {len(result.failures)} failures, {len(result.errors)} errors")
    print("=" * 60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

