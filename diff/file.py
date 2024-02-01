from pathlib import Path
from typing import Tuple, List, Dict
from multiprocessing import Pool
import re


def collect_files(
    base_path: Path,
    secondary_path: Path,
    regex: str = ''
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    base_files = _collect_files_from_path(base_path, regex=regex)
    secondary_files = _collect_files_from_path(secondary_path, regex=regex)
    keys = set(base_files.keys()).union(set(secondary_files.keys()))
    for key in keys:
        if key not in base_files:
            base_files[key] = []
        if key not in secondary_files:
            secondary_files[key] = []
    return base_files, secondary_files


def _collect_files_from_path(
    path: Path,
    regex: str
):
    file_paths = _get_files_in_path(path=path)
    file_paths = _filter_file_path_by_regex(
        file_paths=file_paths,
        regex=regex
    )
    files = _read_files(file_paths=file_paths)
    return files


def _get_files_in_path(
    path: Path
):
    return [
        file_path for file_path in path.iterdir() if file_path.is_file()
    ]


def _filter_file_path_by_regex(
    file_paths: List[Path],
    regex: str = ""
):
    if regex != "":
        pattern = re.compile(regex)
        file_paths = [
            file_path for file_path in file_paths if pattern.search(file_path.name)
        ]
    return file_paths


def _read_file(
    file_path: Path
) -> Tuple[Path, List[str]]:
    lines = []
    with open(file_path, 'r', errors='ignore') as f:
        lines = f.readlines()
    return (file_path, lines)


def _read_files(
    file_paths: List[Path]
) -> Dict[str, List[str]]:
    files = {}
    with Pool() as pool:
        map_result = pool.map_async(_read_file, file_paths)
        for result in map_result.get():
            files[result[0].name] = result[1]
    return files
