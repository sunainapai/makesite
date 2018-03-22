import requests
from pyquery import PyQuery
from urllib.parse import urlparse
from dateutil.parser import parse
import time
import argparse


def main():
    """
        Loads initial URLs then all URLs from the same website recursively.
    """

    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str,
                        help="Website URL", required=True)
    parser.add_argument("-o", "--out", type=str,
                        help="Sitemap destination file", required=True)
    args = parser.parse_args()

    global baseUrl, l, validHeaders, smHeader, smFooter, smItem

    baseUrl = args.url
    validHeaders = ['text/html']
    smHeader = """<?xml version="1.0" encoding="UTF-8"?>
                  <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
    smFooter = '</urlset>'
    smItem = """<url>
        <loc>{{link}}</loc>
        <lastmod>{{date}}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>"""

    # List of all URLs
    l = {}

    # Initiate scanning
    scanUrl(baseUrl)

    # Create sitemap
    sitemap = createSitemap()

    # write sitemap to file
    writeToFile(sitemap, args.out)


def scanUrl(url):

    global baseUrl, l

    print(" * Scanning %s" % url)

    # Load URL with requests
    r = requests.get(url)

    # Return `None` if the page noes not have a valid header
    if not hasValidHeader(r):
        return None

    # Skip pages with invalid statuses
    if r.status_code < 200 or r.status_code >= 300:
        return None

    pq = PyQuery(getPageContent(r))
    for link in pq('a'):
        # Get link found
        try:
            url = link.attrib['href']
        except KeyError as e:
            continue

        # Skip URL if it's just a local anchor
        if url[:1] == '#':
            continue

        # If a URL is a relative URL, make it a full URL
        if getScheme(url) is None:
            url = getFullUrl(url)

        # Remove anchor from URL
        url = removeAnchor(url)

        # Skip any URL that's not part of the original website
        if not isSameWebsite(url):
            continue

        if url and url.strip('./') not in l.keys():
            # print(url)
            l[url.strip('./')] = getDateLastModified(r)

            scanUrl(url)


def getPageContent(r):
    """
        Returns the source code of a web page
    """

    return r.text


def getDateLastModified(r):
    """
        Returns the page modification date (can default to the current date
        if not available) at the format YYYY-MM-DD
    """

    lastModified = r.headers.get('Last-Modified')

    if lastModified:
        dt = parse(lastModified)
        return dt.strftime('%Y-%m-%d')

    # Returns current date as a default
    return time.strftime('%Y-%m-%d')


def hasValidHeader(r):
    """
        Check if the page has an accepted header
    """

    global validHeaders

    for validHeader in validHeaders:
        if validHeader in r.headers.get('content-type'):
            return True

    return False


def getScheme(url):
    """
        Returns URL scheme ("http", "https" or `None`)
    """

    scheme = urlparse(url).scheme

    if scheme:
        return scheme

    return None


def removeAnchor(url):
    """
        "http://www.website.com#my-anchor" -> "http://www.website.com"
    """

    if url.find('#') > 0:
        return url[:url.find('#')]

    return url


def isSameWebsite(url):
    """
        Verified if the discovered URL is part of the original website
    """

    global baseUrl

    if urlparse(url).netloc == urlparse(baseUrl).netloc:
        return True

    return False


def getFullUrl(url):
    """
        Returns a full URL with schema and domain for relative URLs
    """

    global baseUrl

    if url[:1] == '/':
        return baseUrl.strip('/') + url

    print(' * Unknown format: %s' % url)
    return None


def createSitemap():
    """
        Returns the sitemap
    """

    global l, smHeader, smFooter, smItem

    print(' * Creating sitemap with %d URLs' % (len(l)))

    # Set header
    sitemap = smHeader + '\n'

    # Loop thru URLs and populate sitemap
    for url in l:
        # Get date
        date = l[url]

        # Create sitemap section
        item = smItem
        item = item.replace('{{link}}', url)
        item = item.replace('{{date}}', date)

        # Add to sitemap
        sitemap = sitemap + item + '\n'

    # Set footer
    sitemap = sitemap + smFooter

    return sitemap


def writeToFile(content, filename):
    """
        Write the sitemap to the destination file
    """

    print(' * Writting sitemap to `%s`' % (filename))

    with open(filename, 'a') as out:
        out.write(content)


if __name__ == '__main__':
    main()
