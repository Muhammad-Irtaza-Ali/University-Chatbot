"""Small, local BM25 passage retriever. No model or external API required."""
from collections import Counter
from dataclasses import dataclass
import math
import re

STOPWORDS = set('a an the is are was were be to of in on for and or with from what which how can do does i my me please about'.split())

@dataclass(frozen=True)
class Passage:
    source: str
    page: int
    number: int
    text: str

@dataclass(frozen=True)
class Match:
    passage: Passage
    score: float
    coverage: float


def tokenize(text):
    return [word for word in re.findall(r'[^\W_]+', text.casefold(), flags=re.UNICODE)
            if word not in STOPWORDS and len(word) > 1]


def chunk_text(text, source, page=1, words=100, overlap=20):
    if words < 1 or not 0 <= overlap < words:
        raise ValueError('Choose a positive chunk length and a smaller overlap.')
    tokens = text.split()
    passages = []
    for start in range(0, len(tokens), words - overlap):
        piece = tokens[start:start + words]
        if not piece:
            break
        passages.append(Passage(source, page, len(passages) + 1, ' '.join(piece)))
        if start + words >= len(tokens):
            break
    return passages


def search(query, passages, limit=3, min_coverage=0.34):
    """Return cited text matches. Scores are ranking signals, not confidence."""
    terms = set(tokenize(query))
    if not terms or not passages or limit <= 0:
        return []
    counts = [Counter(tokenize(p.text)) for p in passages]
    lengths = [sum(c.values()) for c in counts]
    average = sum(lengths) / len(lengths) or 1
    document_frequency = Counter(term for c in counts for term in c)
    matches = []
    for passage, count, length in zip(passages, counts, lengths):
        coverage = len(terms.intersection(count)) / len(terms)
        if coverage < min_coverage:
            continue
        score = 0.0
        for term in terms:
            frequency = count[term]
            if not frequency:
                continue
            df = document_frequency[term]
            idf = math.log(1 + (len(passages) - df + 0.5) / (df + 0.5))
            score += idf * frequency * 2.5 / (frequency + 1.5 * (0.25 + 0.75 * length / average))
        if score > 0:
            matches.append(Match(passage, score, coverage))
    return sorted(matches, key=lambda match: (-match.score, match.passage.source,
                                             match.passage.page, match.passage.number))[:limit]
