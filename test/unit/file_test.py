from diff.file import (
    collect_files,
    _read_file,
    _read_files,
    _collect_files_from_path,
    _get_files_in_path,
    _filter_file_path_by_regex
)
from unittest.mock import mock_open, patch
from pathlib import Path

def test_wildcard_filter_by_regex():
    paths = [
        Path("test.ls"),
        Path("test.py")
    ]
    new_paths = _filter_file_path_by_regex(
        file_paths=paths
    )
    assert paths == new_paths

def test_file_filter_by_regex():
    paths = [
        Path("test.ls"),
        Path("test.py")
    ]
    regex = ".*\\.py$"
    new_paths = _filter_file_path_by_regex(
        file_paths=paths,
        regex=regex
    )
    assert len(new_paths) == 1
    assert new_paths[0] == paths[1]

def test_read_file():
    with patch('builtins.open', mock_open()) as mocked_file:
        _read_file('test.txt')
    mocked_file.assert_called_with('test.txt', 'r')

def test_read_files():
    path = Path(__file__)
    files = _read_files(
        file_paths=[path]
    )
    assert path.name in files

def test_get_files_in_path():
    file_path = Path(__file__)
    dir_path = file_path.parent
    paths = _get_files_in_path(
        path=dir_path
    )
    assert len(paths) != 0
    assert file_path in paths

def test_collect_files_from_path():
    file_path = Path(__file__)
    dir_path = file_path.parent
    regex = ''
    files = _collect_files_from_path(
        path=dir_path,
        regex=regex
    )
    assert len(files) != 0
    assert file_path.name in files
    assert len(files[file_path.name]) > 0

def test_collect_files():
    file_path = Path(__file__)
    dir_path = file_path.parent
    regex = ''
    base_files, secondary_files = collect_files(
        base_path=dir_path,
        secondary_path=dir_path,
        regex=regex
    )
    assert file_path.name in base_files
    assert file_path.name in secondary_files
