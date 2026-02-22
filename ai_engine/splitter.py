import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from ai_engine.utils import logger

class SplitterEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        try:
            self.model = SentenceTransformer(model_name)
            self.use_semantic = True
        except Exception as e:
            logger.warning(f"Failed to load SentenceTransformer: {e}. Falling back to basic splitting.")
            self.use_semantic = False

    def split_document(self, pages_data):
        """
        Splits the document into logical groups based on semantic coherence (FR-2.2).
        """
        if not pages_data:
            return []

        # Default strategy: 1 page = 1 group if semantic fails
        if not self.use_semantic:
            return [{"group_id": i+1, "pages": [p["page"]], "classification": "Unknown"} for i, p in enumerate(pages_data)]

        # 1. Embeddings
        texts = [p["content"] for p in pages_data]
        embeddings = self.model.encode(texts)

        # 2. Calculate Similarity between consecutive pages
        groups = []
        current_group = [pages_data[0]["page"]]

        threshold = 0.6  # Tunable parameter (lower = more splitting)

        for i in range(len(embeddings) - 1):
            sim = cosine_similarity([embeddings[i]], [embeddings[i+1]])[0][0]
            logger.info(f"Similarity between Page {i+1} and {i+2}: {sim:.4f}")

            if sim < threshold:
                # Semantic Break -> New Group
                groups.append({
                    "group_id": len(groups) + 1,
                    "pages": current_group,
                    "classification": self.classify_group(texts[i]) # Simple classification based on content
                })
                current_group = [pages_data[i+1]["page"]]
            else:
                # Semantic Continuity -> Same Group
                current_group.append(pages_data[i+1]["page"])

        # Add the last group
        groups.append({
            "group_id": len(groups) + 1,
            "pages": current_group,
            "classification": self.classify_group(texts[-1])
        })

        return groups

    def classify_group(self, text):
        """
        Simple heuristic classification based on keywords in the text.
        In a real system, this would be a trained classifier model.
        """
        text_lower = text.lower()
        if "invoice" in text_lower:
            return "Invoice"
        elif "contract" in text_lower or "agreement" in text_lower:
            return "Contract"
        elif "receipt" in text_lower:
            return "Receipt"
        elif "statement" in text_lower:
            return "Bank Statement"
        else:
            return "General Document"
