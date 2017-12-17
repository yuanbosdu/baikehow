# -*- coding: iso-8859-1 -*-

#apt-get install qrencode
import os
from subprocess import Popen, PIPE
from hashlib import sha1
from MoinMoin.Page import Page

qr_options = ["-s", "4"]


def png_path(request, pagename, text):
        return "/home/baikehow/moin/wiki/data/qr", png_filename(text)


def png_url(request, pagename, text):
        return "/data/qr/" + png_filename(text)


def png_filename(text):
        return sha1(text).hexdigest()[:16] + ".png"


def macro_QR(macro, text=None):
        if text is None:
                text = macro.request.getQualifiedURL(macro.request.page.url(macro.request))

        prefix, suffix = png_path(macro.request, macro.request.page.page_name, text)
        if not os.path.exists(prefix):
                os.mkdir(prefix)

        filename = os.path.join(prefix, suffix)
        if not os.path.exists(filename):
                p = Popen(["qrencode", "-o", filename] + qr_options, stdin=PIPE)
                p.stdin.write(text)
                p.stdin.close()
                p.wait()

        img_url = png_url(macro.request, macro.request.page.page_name, text)
        return macro.formatter.image(img_url, alt=text, title=text)