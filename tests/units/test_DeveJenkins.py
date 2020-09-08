from pathlib import Path

from DirectoryManager import DirectoryManager
from File import File


def test_download_all_files():
    DirectoryManager.createDirectory('./Temp')
    assert Path('./Temp').is_dir() == True

def test_file():
    f = File(name="sql.sql", path=Path("./Temp/sql.sql"))
    assert f.spoolPath == Path("./Temp/sql.log")