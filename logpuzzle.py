#!/usr/bin/env python
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:

10.254.254.28 - - [06/Aug/2007:00:13:48 -0700]
"GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U;
Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

__author__ = "Shaquon Kelley"

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    url_list = []
    with open(filename) as file:
        for line in file:
            match = re.search('puzzle', line)
            if match:
                url = re.search(r'\S+puzzle+\S+.jpg', line)
                if url:
                    url_list.append(url.group())
    sorted_url_list = sorted(list(set(url_list)), key=lambda url: url[-8:-4])
    print("list sorted")
    return sorted_url_list


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    if not os.path.exists(dest_dir):
        path = 'mkdir -p {0}'.format(dest_dir)
        os.system(path)
        print("Path created.")
    else:
        print("Path already exists.")

    print("Image download in progress...")
    image_tags = ""

    for i, image_url in enumerate(img_urls):
        print("Image", i, "downloaded!")

        urllib.urlretrieve(
            "http://code.google.com"
            + image_url, dest_dir
            + "/img"
            + str(i)
            + ".jpeg"
            )
        image_tags += """
        <img src='./{0}/img{1}{2}' />
        """.format(
                    dest_dir,
                    str(i),
                    ".jpeg"
                    )
    print("Download Complete.")

    html = """
            <html>
            <head>
            </head>
                <body>
                <div style="display:flex">
                    {0}
                </div>
                </body>
            </html>
            """.format(image_tags)

    f = open('index.html', 'w')
    f.write(html)
    print("HTML created")


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--todir',
        help='destination directory for downloaded images'
        )
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
