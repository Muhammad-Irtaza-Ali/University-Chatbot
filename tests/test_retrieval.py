import unittest
from retrieval import chunk_text, search, tokenize

class RetrievalTests(unittest.TestCase):
    def test_retrieves_relevant_source_and_page(self):
        docs = chunk_text('Computer vision uses images for recognition.', 'vision.pdf', page=7)
        docs += chunk_text('Database transactions preserve consistency.', 'database.pdf', page=2)
        result = search('computer vision', docs)
        self.assertEqual(len(result), 1)
        self.assertEqual((result[0].passage.source, result[0].passage.page), ('vision.pdf', 7))

    def test_unmatched_and_stopword_queries_abstain(self):
        docs = chunk_text('Computer vision studies images.', 'notes.txt')
        self.assertEqual(search('scholarship deadline', docs), [])
        self.assertEqual(search('what is the', docs), [])
        self.assertEqual(search('', docs), [])

    def test_chunks_preserve_tail_and_citation(self):
        text = ' '.join(f'word{i}' for i in range(205))
        docs = chunk_text(text, 'long.txt', page=3)
        self.assertEqual(len(docs), 3)
        self.assertTrue(docs[-1].text.endswith('word204'))
        self.assertTrue(all(p.source == 'long.txt' and p.page == 3 for p in docs))

    def test_unicode_terms_work_without_translation(self):
        docs = chunk_text('جامعہ میں تعلیم اور تحقیق', 'urdu.txt')
        self.assertTrue(search('تحقیق', docs))
        self.assertIn('تحقیق', tokenize('تحقیق'))

    def test_invalid_chunk_settings(self):
        with self.assertRaises(ValueError):
            chunk_text('sample', 'file', words=20, overlap=20)

    def test_empty_documents_and_deterministic_ties(self):
        self.assertEqual(search('vision', []), [])
        docs = chunk_text('vision project', 'b.txt') + chunk_text('vision project', 'a.txt')
        self.assertEqual(search('vision', docs)[0].passage.source, 'a.txt')

if __name__ == '__main__':
    unittest.main()
