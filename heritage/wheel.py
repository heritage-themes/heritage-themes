"""Python wheels written by hand, so that the same sources give the same bytes."""
import base64, hashlib, io, zipfile

DATE = (2020, 1, 1, 0, 0, 0)  # the date of every entry, as the other zips date theirs


def pack(distribution, version, entries, metadata, licence, extra=None):
    """The wheel as bytes. entries maps a path in the wheel to its bytes; extra maps a file name in the .dist-info
    folder, such as entry_points.txt, to its bytes. The wheel is pure Python, for any interpreter and platform, and its
    entries are sorted."""
    stem = f"{distribution.replace('-', '_')}-{version}"
    dist_info = f"{stem}.dist-info"
    entries = dict(entries)
    entries[f"{dist_info}/METADATA"] = metadata.encode("utf-8")
    entries[f"{dist_info}/WHEEL"] = ("Wheel-Version: 1.0\nGenerator: heritage-themes build.py\n"
                                     "Root-Is-Purelib: true\nTag: py3-none-any\n").encode("utf-8")
    entries[f"{dist_info}/LICENSE"] = licence
    for name, content in (extra or {}).items():
        entries[f"{dist_info}/{name}"] = content
    entries[f"{dist_info}/RECORD"] = record(entries, f"{dist_info}/RECORD").encode("utf-8")
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(entries):
            info = zipfile.ZipInfo(path, DATE)
            info.compress_type, info.external_attr, info.create_system = zipfile.ZIP_DEFLATED, 0o644 << 16, 3
            z.writestr(info, entries[path])
    return out.getvalue()


def record(entries, own_path):
    """The wheel's RECORD: each entry's path, SHA-256 and size, and its own path without them."""
    lines = []
    for path in sorted(entries):
        digest = base64.urlsafe_b64encode(hashlib.sha256(entries[path]).digest()).rstrip(b"=").decode()
        lines.append(f"{path},sha256={digest},{len(entries[path])}")
    lines.append(f"{own_path},,")
    return "\n".join(lines) + "\n"
