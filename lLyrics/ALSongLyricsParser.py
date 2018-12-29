# Parser for lyrics.alsong.co.kr
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import requests
import re
import string

import Util
import jamotools

TEMPLATE = """\
<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:ns2="ALSongWebServer/Service1Soap"
xmlns:ns1="ALSongWebServer"
xmlns:ns3="ALSongWebServer/Service1Soap12">
<SOAP-ENV:Body><ns1:GetResembleLyric2>
<ns1:stQuery>
<ns1:strTitle>{title}</ns1:strTitle>
<ns1:strArtistName>{artist}</ns1:strArtistName>
<ns1:nCurPage>{page}</ns1:nCurPage>
</ns1:stQuery>
</ns1:GetResembleLyric2>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

class Parser(object):
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.lyrics = ""

    def parse(self):

        data=TEMPLATE.format(
            title=self.title,
            artist=self.artist,
            page=0,
            ).encode()

        # create lyrics Url
        resp = requests.post(
            'http://lyrics.alsong.co.kr/alsongwebservice/service1.asmx',
            data=TEMPLATE.format(
                title=jamotools.join_jamos(self.title),
                artist=jamotools.join_jamos(self.artist),
                page=0,
            ).encode(),
            headers={'Content-Type': 'application/soap+xml'},
        )

        self.lyrics = self.get_lyrics(resp.text)

        return self.lyrics

    def get_lyrics(self, resp):
        # cut HTML source to relevant part
        start = resp.find("<strLyric>")
        if start == -1:
            print("lyrics start not found")
            return ""
        resp = resp[(start + 10):]
        end = resp.find("</strLyric>")
        if end == -1:
            print("lyrics end not found ")
            return ""
        resp = resp[:end]

        # replace unwanted parts
        resp = resp.replace("&lt;br&gt;", "\n")
        resp = resp.strip()

        return resp
