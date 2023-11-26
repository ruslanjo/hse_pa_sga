import json
from collections import defaultdict
import logging

from utils.text_preprocessor import TextPreprocessor

logger = logging.getLogger(__name__)


class InvertedIndex:
    def __init__(
            self,
            word_to_docs: defaultdict[str, set[int]],
    ):
        self._word_to_docs = word_to_docs

    def query(
            self,
            text: str,
            tp: TextPreprocessor,):
        """Returns set of common article_id for all words"""
        intersect_mode = False
        common = set()
        words = tp.prepare_input_text(text)

        for w in words:
            art_ids = self._word_to_docs.get(w)
            if art_ids is None:
                logger.warning(f'No article ids in index found for word {w}')
            elif not intersect_mode:
                common = art_ids
                intersect_mode = True
            else:
                common = common.intersection(art_ids)
        return ','.join(str(x) for x in sorted(common))

    def dump(self, filepath) -> None:
        w_d_map = self._word_to_docs.copy()
        for k, v in w_d_map.items():
            w_d_map[k] = list(v)  # noqa
            
        data = json.dumps(w_d_map, indent=4)
        with open(filepath, 'w') as f:
            f.write(data)

    @classmethod
    def load(cls, filepath):
        with open(filepath, 'r') as f:
            data = f.read()
        
        w_d_map = json.loads(data)
        for k, v in w_d_map.items():
            w_d_map[k] = set(v)
        return InvertedIndex(word_to_docs=w_d_map)
