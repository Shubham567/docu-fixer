import unittest
from unittest.mock import MagicMock, patch
from ai_engine.splitter import SplitterEngine

class TestSplitterEngine(unittest.TestCase):
    def setUp(self):
        # Mock SentenceTransformer to avoid loading heavy models during test
        with patch('ai_engine.splitter.SentenceTransformer') as MockModel:
            self.splitter = SplitterEngine()
            self.mock_model = MockModel.return_value
            # Setup mock embeddings
            # 3 pages. Page 1 & 2 similar, Page 3 different.
            # Embeddings: [ [1, 0], [0.9, 0.1], [0, 1] ]
            self.splitter.model.encode.return_value = [
                [1.0, 0.0],
                [0.9, 0.1],
                [0.0, 1.0]
            ]
            self.splitter.use_semantic = True

    def test_semantic_splitting(self):
        pages_data = [
            {"page": 1, "content": "Invoice 001"},
            {"page": 2, "content": "Invoice 001 Page 2"},
            {"page": 3, "content": "Contract Agreement"}
        ]

        # We expect similarity between 1 and 2 to be high (dot product ~0.9)
        # Similarity between 2 and 3 to be low (dot product ~0.1)
        # Threshold is 0.6 in code.

        groups = self.splitter.split_document(pages_data)

        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["pages"], [1, 2])
        self.assertEqual(groups[1]["pages"], [3])

    def test_fallback(self):
        self.splitter.use_semantic = False
        pages_data = [{"page": 1, "content": "A"}, {"page": 2, "content": "B"}]
        groups = self.splitter.split_document(pages_data)
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0]["group_id"], 1)

if __name__ == '__main__':
    unittest.main()
