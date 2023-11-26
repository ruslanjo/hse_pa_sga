import argparse
from enum import Enum


class AvailableMode(Enum):
    BUILD: str = 'build'
    QUERY: str = 'query'


REQUIRED_CLI_PARAMS = {
    AvailableMode.BUILD.value: ('dataset', 'index'),
    AvailableMode.QUERY.value: ('index', 'query_file')
}


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='InvertedIndex',
        description='Builds and executes query on inverted index',
        epilog='by Tarutin.R'
    )
    parser.add_argument('mode', choices=[AvailableMode.QUERY.value, AvailableMode.BUILD.value])
    parser.add_argument('--dataset', help='path to dataset to build Inverted Index')
    parser.add_argument('--index', help='path for Inverted Index dump/load')
    parser.add_argument('--query_file', help='query_file with collection of queries to run against Inverted Index')
    args = parser.parse_args()
    _check_all_params_provided(REQUIRED_CLI_PARAMS, args)
    return args


def _check_all_params_provided(
        required_p: dict[str, tuple[str]],
        args: argparse.Namespace,
) -> None:
    mode_params = required_p[args.mode]
    status = all(
        getattr(args, p) is not None for p in mode_params
    )
    if not status:
        raise ValueError(
            f'Please provide all required params {mode_params}'
        )
