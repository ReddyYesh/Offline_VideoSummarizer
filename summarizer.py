import re
from collections import Counter
from typing import List


def split_into_sentences(text: str, max_words_per_chunk: int = 40) -> List[str]:
    """
    Tries to split text into sentences using punctuation.
    If that fails (e.g., Vosk transcript without .?!), falls back to
    splitting into fixed-size word chunks.
    """
    text = text.strip()
    if not text:
        return []

    # First try normal sentence splitting using punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    # If we got multiple sentences, just use them
    if len(sentences) > 1:
        return sentences

    # Otherwise, fallback: chunk by words (for punctuation-less transcripts)
    words = text.split()
    if len(words) <= max_words_per_chunk:
        # Very short text, return as one chunk
        return [" ".join(words)]

    chunks = []
    for i in range(0, len(words), max_words_per_chunk):
        chunk = " ".join(words[i : i + max_words_per_chunk])
        chunks.append(chunk)

    return chunks


def tokenize(text: str) -> List[str]:
    # Lowercase and keep only alphabetic tokens
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return words


class OfflineSummarizer:
    def __init__(self, max_sentences: int = 5):
        self.max_sentences = max_sentences

        # Very small stopword list (can be extended)
        self.stopwords = set(
            [
                "the", "is", "am", "are", "a", "an", "and", "or", "of", "to",
                "in", "it", "that", "this", "for", "on", "with", "as", "at",
                "by", "from", "be", "was", "were", "will", "would", "can",
                "could", "should", "have", "has", "had", "do", "does", "did",
                "you", "i", "we", "they", "he", "she", "them", "him", "her",
                "my", "your", "our", "their"
            ]
        )

    def summarize(self, text: str) -> str:
        text = text.strip()
        if not text:
            return ""

        # Now this will either be real sentences or word chunks
        sentences = split_into_sentences(text)

        if not sentences:
            return ""

        # Build word frequency
        words = tokenize(text)
        words = [w for w in words if w not in self.stopwords and len(w) > 2]
        freq = Counter(words)

        # Score sentences
        sentence_scores = []
        for sent in sentences:
            sent_words = tokenize(sent)
            score = sum(freq.get(w, 0) for w in sent_words)
            sentence_scores.append((score, sent))

        # Pick top N sentences (never more than we actually have)
        sentence_scores.sort(reverse=True, key=lambda x: x[0])
        top_n = min(self.max_sentences, len(sentence_scores))
        top_sentences = [s for _, s in sentence_scores[:top_n]]

        # Preserve original order in summary
        sentence_order = {s: i for i, s in enumerate(sentences)}
        top_sentences.sort(key=lambda s: sentence_order.get(s, 0))

        summary = " ".join(top_sentences)
        return summary.strip()
