import abc
import logging


logger = logging.getLogger(__name__)

Articles = dict[int, str]


class AbstractDocReader(abc.ABC):
    @abc.abstractmethod
    def read(self) -> Articles:
        pass


class LocalFileSystemDocReader(AbstractDocReader):
    """
    Reader uses assumption that documents divided between each other by
    blank line and also store their IDs as first word separated from other text by \t
    """
    __break_point = 1_000
    __sep_sym = '\t'

    def __init__(self, path: str):
        self.path = path

    def read(self) -> Articles:
        res = {}
        with open(self.path, encoding='utf-8') as docs:
            data = docs.read()

        documents = data.strip().split('\n')

        for doc in documents:
            _id = ''
            it_num = 0

            for sym in doc:
                if sym == self.__sep_sym or it_num > self.__break_point:
                    break
                _id += sym
                it_num += 1
            try:
                _id = int(_id)
                res[_id] = doc
            except ValueError:
                logger.warning(f'No id found for document {doc}')
        return res
