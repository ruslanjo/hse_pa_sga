import logging
from collections import defaultdict

from inverted_index import InvertedIndex
from utils.document_reader import Articles
from utils.text_preprocessor import TextPreprocessor


logger = logging.getLogger(__name__)


def create_index(
        articles: Articles,
        tp: TextPreprocessor,
) -> InvertedIndex:
    word_to_docs = defaultdict(set)
    for art_id, text in articles.items():
        logger.warning(f'processing {art_id}')
        unique_w = tp.prepare_input_text(text)
        for w in unique_w:
            word_to_docs[w].update([art_id])

    return InvertedIndex(
        word_to_docs=word_to_docs
        )
