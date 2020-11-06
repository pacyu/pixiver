pixiver
=======

[![logo2](https://img.shields.io/badge/pypi-0.0.8.8161-blue.svg)](https://pypi.org/project/pixiver/)
[![build](https://travis-ci.org/yomikochan/pixiver.svg?branch=master)](https://travis-ci.org/yomikochan/pixiver)

This is a python package for getting illustration works with pixiv ajax interfaces.

Move to [Chinese Version](README-cn.md).

Install
-------

`$ pip install -U pixiver`

Quick Start
-----------

```python
from pixiver.pixiv import Pixiv

p = Pixiv(username='user', password='pw')
pw = p.works(73225282)
pw.mark()
pw.like()
pw.bookmark()
pw.save_original()
```