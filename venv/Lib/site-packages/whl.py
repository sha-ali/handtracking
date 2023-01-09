#!/usr/bin/env python
"""Minimalist wheel building"""
import argparse
import ast
import base64
import hashlib
import logging
import os
import re
import zipfile


__version__ = "0.0.3"


log = logging.getLogger(__name__)


# https://packaging.python.org/specifications/core-metadata/
METADATA_TEMPLATE = """\
Metadata-Version: 2.1
Name: {name}
Version: {version}
"""


# https://www.python.org/dev/peps/pep-0427/
WHEEL_TEMPLATE = """\
Wheel-Version: 1.0
Generator: whl {__version__}
Root-Is-Purelib: true
"""


class WhlError(Exception):
    pass


def get_version(fname):
    with open(fname) as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=", 1)[-1].strip().strip("'").strip('"')
    raise WhlError("Failed to autodetect __version__")


def get_module_docstring(path):
    """get a .py file docstring, without actually executing the file"""
    with open(path) as f:
        return ast.get_docstring(ast.parse(f.read()))


def get_record(path, data=None, arcname=None):
    if data is None:
        with open(path, "rb") as f:
            data = f.read()
    checksum = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=")
    if path.startswith("./"):
        path = path[2:]
    if arcname is None:
        arcname = path
    line = "{},sha256={},{}".format(arcname, checksum.decode(), len(data))
    return line


def _str2list(arg):
    if isinstance(arg, str):
        return [arg]
    return arg


def get_dist_files(src):
    if src is None:
        return []
    if src.endswith(".py"):
        return [src]
    blacklist = {"README.rst", "setup.py", "setup.cfg", ".coverage"}
    dist_files = []
    for root, dirs, fnames in os.walk(src):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fname in fnames:
            if fname not in blacklist and not fname.endswith((".whl", ".pyc")):
                relpath = os.path.join(root, fname)
                dist_files.append(relpath)
    return dist_files


def make_wheel(
    src=None,

    # core metadata fields
    name=None,
    version=None,
    # dynamic  # new in version 2.2 but I can't find the spec for 2.2
    platform=None,
    supported_platform=None,
    summary=None,
    description=None,
    description_content_type=None,
    keywords=None,
    home_page=None,
    download_url=None,
    author=None,
    author_email=None,
    maintainer=None,
    maintainer_email=None,
    license=None,
    classifier=None,
    requires_dist=None,
    requires_python=None,
    requires_external=None,
    project_url=None,
    # provides_extra  # changed in version 2.3 but I can't find the spec for 2.3
    provides_dist=None,
    obsoletes_dist=None,

    py2=True,
    py3=True,
    output_dir=".",
):
    if name is None:
        raise WhlError("name is required")
    if version is None:
        raise WhlError("version is required")
    METADATA = METADATA_TEMPLATE.format(name=name, version=version)
    metadata_lines = []
    if platform is not None:
        metadata_lines.extend("Platform: {}".format(x) for x in _str2list(platform))
    if supported_platform is not None:
        metadata_lines.extend("Supported-Platform: {}".format(x) for x in _str2list(supported_platform))
    if summary is not None:
        metadata_lines.append("Summary: {}".format(summary))
    if description_content_type is not None:
        metadata_lines.append("Description-Content-Type: {}".format(description_content_type))
    if keywords is not None:
        metadata_lines.append("Keywords: {}".format(keywords))
    if home_page is not None:
        metadata_lines.append("Home-page: {}".format(home_page))
    if download_url is not None:
        metadata_lines.append("Download-URL: {}".format(download_url))
    if author is not None:
        metadata_lines.append("Author: {}".format(author))
    if author_email is not None:
        metadata_lines.append("Author-email: {}".format(author_email))
    if maintainer != author and maintainer is not None:
        metadata_lines.append("Maintainer: {}".format(maintainer))
    if maintainer_email != author_email and maintainer_email is not None:
        metadata_lines.append("Maintainer-email: {}".format(maintainer_email))
    if license is not None:
        metadata_lines.append("License: {}".format(license))
    if classifier is not None:
        metadata_lines.extend("Classifier: {}".format(x) for x in _str2list(classifier))
    if requires_dist is not None:
        metadata_lines.extend("Requires-Dist: {}".format(x) for x in _str2list(requires_dist))
    if requires_python is not None:
        metadata_lines.append("Requires-Python: {}".format(requires_python))
    if requires_external is not None:
        metadata_lines.extend("Requires-External: {}".format(x) for x in _str2list(requires_external))
    if project_url is not None:
        metadata_lines.extend("Project-URL: {}".format(x) for x in _str2list(project_url))
    _provides_extra = []
    # auto-generate Provides-Extra from Requires-Dist entries
    for req in _str2list(requires_dist or []):
        if ";" in req:
            suffix = req.split(";")[-1]
            if "extra" in suffix:
                val = suffix.split("==")[-1].strip()
                val = val.strip("'")
                val = val.strip('"')
                if re.match(r"^([a-z0-9]|[a-z0-9]([a-z0-9-](?!-))*[a-z0-9])$", val):
                    _provides_extra.append(val)
                # see https://packaging.python.org/en/latest/specifications/core-metadata/#provides-extra-multiple-use
    for extra in {}.fromkeys(_provides_extra):
        metadata_lines.append("Provides-Extra: {}".format(extra))
    if provides_dist is not None:
        metadata_lines.extend("Provides-Dist: {}".format(x) for x in _str2list(provides_dist))
    if obsoletes_dist is not None:
        metadata_lines.extend("Obsoletes-Dist: {}".format(x) for x in _str2list(obsoletes_dist))
    if metadata_lines:
        METADATA += "\n".join(metadata_lines) + "\n"
    if description is not None:
        METADATA += "\n" + description

    WHEEL = WHEEL_TEMPLATE.format(__version__=__version__)
    if py2:
        WHEEL += "Tag: py2-none-any\n"
    if py3:
        WHEEL += "Tag: py3-none-any\n"

    tags = "py2.py3"
    if py2 and not py3:
        tags = "py2"
    elif py3 and not py2:
        tags = "py3"

    whl_name = "{}-{}-{}-none-any.whl".format(name.replace("-", "_"), version, tags)
    dist_info_name = "{}-{}.dist-info".format(name.replace("-", "_"), version)
    whl_path = os.path.join(output_dir, whl_name)

    RECORD = []
    zf = zipfile.ZipFile(whl_path, "w")
    if src:
        if isinstance(src, (list, tuple)):
            dist_files = src
            parent = os.path.dirname(os.path.abspath(src[0]))
        else:
            dist_files = get_dist_files(src)
            parent = os.path.dirname(os.path.abspath(src))
        for path in dist_files:
            arcname = os.path.relpath(path, parent)
            zf.write(path, arcname)
            record = get_record(path, arcname=arcname)
            RECORD.append(record)
            log.info(record)

    METADATA = METADATA.encode("utf-8")
    WHEEL = WHEEL.encode("utf-8")

    info_metadata = os.path.join(dist_info_name, "METADATA")
    RECORD.append(get_record(info_metadata, data=METADATA))
    zf.writestr(info_metadata, METADATA)

    info_wheel = os.path.join(dist_info_name, "WHEEL")
    RECORD.append(get_record(info_wheel, data=WHEEL))
    zf.writestr(info_wheel, WHEEL)

    RECORD.append("{},,".format(os.path.join(dist_info_name, "RECORD")))
    RECORD_BYTES = "\n".join(RECORD).encode("utf-8")
    zf.writestr(os.path.join(dist_info_name, "RECORD"), RECORD_BYTES)

    zf.close()
    return whl_path


def main():
    parser = argparse.ArgumentParser(
        prog="whl.py", description="Minimalist wheel building"
    )
    parser.add_argument("-2", dest="py2", action="store_true")
    parser.add_argument("-3", dest="py3", action="store_true")
    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Where to put the generated .whl file (default: %(default)s)",
    )
    parser.add_argument(
        "src",
        default=".",
        nargs="?",
        help=(
            "Directory of files to pack into wheel (default: %(default)s), "
            "the dirname will be used as the distribution name. "
            "This can also be a single .py file"
        ),
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    parser.add_argument("-v", "--verbose", action="count", default=0)
    args = parser.parse_args()
    if args.verbose >= 2:
        level = logging.DEBUG
    elif args.verbose == 1:
        level = logging.INFO
    else:
        level = logging.WARNING
    logging.basicConfig(level=level)
    py2 = args.py2
    py3 = args.py3
    if not (py2 or py3):
        # universal by default
        py2 = py3 = True
    assert py2 or py3

    src = os.path.abspath(args.src)
    name = os.path.basename(src)
    if os.path.isdir(args.src):
        init = os.path.join(src, "__init__.py")
        if not os.path.isfile(init):
            raise WhlError("{} must contain an __init__.py".format(src))
        version = get_version(init)
        docstring = get_module_docstring(init)
        readme = os.path.join(src, "..", "README.rst")
    elif os.path.isfile(src):
        version = get_version(src)
        if name.endswith(".py"):
            name = name[:-3]
        docstring = get_module_docstring(src)
        readme = os.path.join(os.path.dirname(src), "README.rst")
    else:
        raise WhlError("Unknown source: {}".format(src))

    description = None
    if os.path.isfile(readme):
        with open(readme) as f:
            description = f.read()

    summary = None
    if docstring:
        summary = docstring.splitlines()[0]

    whl_path = make_wheel(
        src=src,
        name=name,
        version=version,
        summary=summary,
        description=description,
        py2=py2,
        py3=py3,
        output_dir=args.output_dir,
    )
    print(whl_path)


if __name__ == "__main__":
    main()
