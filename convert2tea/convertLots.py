#!/usr/bin/env python

"""
Simple script to loop through a list of projects and convert them to tea.
"""

__author__ = "James Reynolds"
___email__ = "magnusviri@me.edu"
__copyright__ = ""
__license__ = "MIT"
__version__ = "0.0.1"

import argparse
import sys

import convert2tea

def parse(args):
    parser = argparse.ArgumentParser(
        "convertLots", description="Convert lots of formula to tea using AI"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="print version and exit"
    )
    parser.add_argument(
        "-n", "--dry-run", action="store_true", help="print prompt and exit"
    )
    options = parser.parse_args(args)
    return options


def main():
    options = parse(sys.argv[1:])
    dry_run = options.dry_run
    version = options.version

    if version:
        print(__version__)
        sys.exit(0)

    projects = {
        "c": [
            # "abseil",
            # "apr-util",
            # "argocd",
            # "argon2",
            # "aspell",
            # "augeas",
            # "aws-sdk-cpp",
            # "bash-completion",
            # "bdw-gc",
            # "berkeley-db",
            # "capstone",
            # "carthage",
            # "ceres-solver",
            # "cfitsio",
            # "cgal",
            # "chruby",
            # "cppunit",
            # "cscope",
            # "dbus",
            # "dialog",
            # "dnsmasq",
            # "docker-machine",
            # "eigen",
            # "eksctl",
            # "elixir",
            # "emacs",
            # "epsilon",
            # "exiftool",
            # "fftw",
            # "findutils",
            # "freetds",
            # "frei0r",
            # "gdal",
            # "ghostscript",
            # "git-gui",
            # "git-lfs",
            # "gl2ps",
            # "glew",
            # "gnuplot",
            # "googletest",
            # "gpp",
            # "graphicsmagick",
            # "graphviz",
            # "groff",
            # "groonga",
            # "grpc",
            # "gts",
            # "guile",
            # "hdf5",
            # "hicolor-icon-theme",
            # "hiredis",
            # "httpd",
            # "hunspell",
            # "hwloc",
            # "isl",
            # "itstool",
            # "jbig2dec",
            # "jemalloc",
            # "json-c",
            # "krb5",
            # "ldns",
            # "libaec",
            # "libass",
            # "libatomic_ops",
            # "libb2",
            # "libbluray",
            # "libcbor",
            # "libcerf",
            # "libdap",
            # "libde265",
            # "libfido2",
            # "libgeotiff",
            # "libgsf",
            # "libheif",
            # "libidn",
            # "liblinear",
            # "liblqr",
            # "libmatio",
            # "libmaxminddb",
            # "libmng",
            # "libpq",
            # "libraw",
            # "librdkafka",
            # "librttopo",
            # "libsamplerate",
            # "libsmi",
            # "libsndfile",
            # "libsodium",
            # "libspatialite",
            # "libssh2",
            # "libtermkey",
            # "libunibreak",
            # "libusb",
            # "libvidstab",
            # "libvorbis",
            # "libvpx",
            # "libvterm",
            # "libyaml",
            # "lima",
            # "luajit",
            # "luarocks",
            # "lzip",
            # "lzlib",
            # "macvim",
            # "mandoc",
            # "mariadb",
            # "mecab-ipadic",
            # "mercurial",
            # "metis",
            # "minizip",
            # "molten-vk",
            # "mozjpeg",
            # "msgpack",
            # "mysql-client",
            # "neofetch",
            # "netpbm",
            # "nghttp2",
            # "nspr",
            # "nss",
            # "open-mpi",
            # "openblas",
            # "opencore-amr",
            # "openjdk",
            # "openldap",
            # "openslide",
            # "openssh",
            # "openvpn",
            # "p7zip",
            #"php", <- TOO MANY TOKENS
            # "pinentry",
            # "pkcs11-helper",
            # "podman",
            # "poppler",
            # "poppler-qt5",
            # "postgis",
            # "pstree",
            # "psutils",
            # "pulumi",
            # "qhull",
            # "rapidjson",
            # "rbenv",
            # "re2",
            # "rtmpdump",
            # "ruby-install",
            # "s-lang",
            # "screenresolution",
            # "sdl2",
            # "smartmontools",
            # "source-highlight",
            # "speex",
            # "srt",
            # "subversion",
            # "suite-sparse",
            # "tcl-tk",
            # "telnet",
            # "theora",
            # "thrift",
            # "tidy-html5",
            # "tldr",
            # "tree-sitter",
            # "uchardet",
            # "unibilium",
            # "unixodbc",
            # "utf8cpp",
            # "utf8proc",
            # "vault",
            # "vde",
            # "vtk",
            # "wangle",
            # "wimlib",
            # "wireshark",
            # "wxwidgets",
            # "x264",
            # "x265",
            # "xerces-c",
            # "xmlto",
            # "xvid",
            # "xxhash",
            # "zimg",
            # "zsh-syntax-highlighting",
        ],
        # "go": [
        #     "aws-iam-authenticator",
        #     "colima",
        #     "counterfeiter",
        #     "docker-compose",
        #     "flyctl",
        #     "gitlab-runner",
        #     "gox",
        #     "jfrog-cli",
        #     "kind",
        #     "mkcert",
        #     "mockery",
        #     "rclone",
        #     "tflint",
        # ],
        # "meson": [
        #     "atk",
        #     "cgif",
        #     "dav1d",
        #     "gsettings-desktop-schemas",
        #     "jsoncpp",
        #     "libepoxy",
        #     "librist",
        #     "libspng",
        #     "orc",
        #     "pygobject3",
        #     "qemu",
        #     "rubberband",
        #     "scrcpy",
        #     "vips",
        # ],
        "python": [
            #"asciidoc.rb",
            "certbot.rb",
            "cfn-lint.rb",
            "flit.rb",
            "hatch.rb",
            "httpie.rb",
            "ipython.rb",
            "jupyterlab.rb",
            "mitmproxy.rb",
            "mypy.rb",
            "pyenv-virtualenv.rb",
            "python-build.rb",
            "scons.rb",
            "sip.rb",
            "yamllint.rb",
        ],
        "ruby": [
            "cocoapods",
            "edencommon",
            "git-lfs",
            "ronn",
        ],
        "rust": [
            "libimagequant",
            "rav1e",
            "rustup-init",
        ],
    }


    # Loop through projects
    for lang, project_list in projects.items():
        for project in project_list:
            url = f"https://raw.githubusercontent.com/Homebrew/homebrew-core/master/Formula/{project}.rb"
            convert2tea.convertFiles(lang, project, url, dry_run)


if __name__ == "__main__":
    main()
