from io import BytesIO
from unittest.mock import Mock

from dissect.extfs.c_ext import c_ext
from dissect.extfs.extfs import INode

from dissect.target.filesystems.extfs import ExtFilesystemEntry


def test_stat_information() -> None:
    extfs = Mock(block_size=0x1000)
    extfs.sb.s_inode_size = 129

    entry = INode(extfs, 42)

    inode_bytes = (
        b"\xa4\x81\xe8\x03\xbb\x0e\x00\x00\x9f!\tf\xb8\x17\xe8f\x9f!\tf\x00\x00\x00\x00\xe8\x03\x01\x00\x08\x00"
        b"\x00\x00\x00\x00\x08\x00\x04\x00\x00\x00\n\xf3\x01\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x01\x00\x00\x00\xa1\x8b\xa8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00t\xab\x19\x19\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x90p\x00\x00 \x00\xe44\xe0\xe8Ho\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\xb8\x17\xe8f\xe0\xe8Ho\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    )

    inode = c_ext.ext4_inode(BytesIO(inode_bytes))

    entry._inode = inode

    fs_entry = ExtFilesystemEntry(Mock(), "some/path", entry)

    stat_info = fs_entry.lstat()

    assert stat_info.st_ino == 42
    assert stat_info.st_nlink == 1
    assert stat_info.st_uid == 1000
    assert stat_info.st_gid == 1000
    assert stat_info.st_size == 3771

    assert stat_info.st_atime == 1711874463.0
    assert stat_info.st_atime_ns == 1711874463000000000
    assert stat_info.st_mtime == 1711874463.0
    assert stat_info.st_mtime_ns == 1711874463000000000
    assert stat_info.st_ctime == 1726486456.466762
    assert stat_info.st_ctime_ns == 1726486456466762296
    assert stat_info.st_birthtime == 1726486456.466762
    assert stat_info.st_birthtime_ns == 1726486456466762296

    assert stat_info.st_blksize == 0x1000
    assert stat_info.st_blocks == 8