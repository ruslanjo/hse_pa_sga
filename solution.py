import sys

from cli import get_cli_args, AvailableMode
from utils.document_reader import LocalFileSystemDocReader
from utils.funcs import create_index
from utils.text_preprocessor import TextPreprocessor
from inverted_index import InvertedIndex


def query(
        idx_path: str,
        query_file_path: str,
        tp: TextPreprocessor,
) -> None:
    idx = InvertedIndex.load(idx_path)
    with open(query_file_path, 'r') as q_f:
        for line in q_f.readlines():
            res = idx.query(line, tp=tp)
            sys.stdout.write(res + '\n')


def build(
        path_to_text: str,
        idx_path: str,
        tp: TextPreprocessor
) -> InvertedIndex:
    doc_reader = LocalFileSystemDocReader(path=path_to_text)
    articles = doc_reader.read()
    idx = create_index(articles=articles, tp=tp)
    idx.dump(idx_path)
    return idx


if __name__ == '__main__':
    cli_args = get_cli_args()
    mode = cli_args.mode

    text_preproc = TextPreprocessor()

    if mode == AvailableMode.QUERY.value:
        query(idx_path=cli_args.index, query_file_path=cli_args.query_file, tp=text_preproc)

    if mode == AvailableMode.BUILD.value:
        build(idx_path=cli_args.index, path_to_text=cli_args.dataset, tp=text_preproc)

    #path = '/home/ruslant/dev/data_science/hse/SGA-2/tests/wikipedia_sample.txt'
    #doc_reader = LocalFileSystemDocReader(path=path)
    #articles = doc_reader.read()

    # tp = TextPreprocessor(articles=articles, lmtzr=wnl)
    # #idx = create_index(articles=articles, tp=tp)
    # #res = idx.query('Anarchism', tp=tp)
    # #idx.dump('./idx.json')
    # idx = InvertedIndex.load('./idx.json')
    # res = idx.query('Anarchism', tp=tp)
    # a = 3

