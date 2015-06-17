# -*- coding: utf-8 -*-
"""
Sublime Text Color Scheme Editor.

Licensed under MIT
Copyright (c) 2013 Isaac Muse <isaacmuse@gmail.com>
"""
import sys
import argparse
import codecs
import json
import os
import plistlib
import sys
import threading
import time
import uuid
import wx
from wx.lib.embeddedimage import PyEmbeddedImage

from . import editor
from .lib import messages
from .lib.custom_app import CustomApp, DebugFrameExtender, init_app_log
from .lib.custom_app import set_debug_mode
from .lib.custom_app import debug, debug_struct, error
from .lib.default_new_theme import theme as default_new_theme
from .lib.file_strip.json import sanitize_json
from .lib.rgba import RGBA

__version__ = "1.0.0"

BG_COLOR = None
FG_COLOR = None
DEBUG_CONSOLE = False

SHORTCUTS = {
    "osx": u'''
===Applicatioon Shortcuts===
Find Next: ⌘ + F
Find Next: ⌘ + G
Find Prev: ⌘ + ⇧ + G
Save: ⌘ + S
Save As: ⌘ + ⇧ + S

===Table Shortcuts===
Edit Row: Enter
Move Row Up (Style Settings): ⌥ + ↑
Move Row Down (Style Settings): ⌥ + ↓
Switch to Global Settings: ⌥ + ←
Switch to Style Settings: ⌥ + →
Delete Row: ⌫
Insert Row: ⌘ + I
Toggle 'bold' font: B
Toggle 'italic' font: I
Toggle 'underlined' font: U
''',

    "windows": u'''
===Applicatioon Shortcuts===
Find Next: Control + F
Find Next: Control + G
Find Prev: Control + Shift + G
Save: Control + S
Save As: Control + Shift + S

===Table Shortcuts===
Edit Row: Enter
Move Row Up (Style Settings): Alt + ↑
Move Row Down (Style Settings): Alt + ↓
Switch to Global Settings: Alt + ←
Switch to Style Settings: Alt + →
Delete Row: Delete
Insert Row: Control + I
Toggle 'bold' font: B
Toggle 'italic' font: I
Toggle 'underlined' font: U
''',

    "linux": u'''
===Applicatioon Shortcuts===
Find Next: Control + F
Find Next: Control + G
Find Prev: Control + Shift + G
Save: Control + S
Save As: Control + Shift + S

===Table Shortcuts===
Edit Row: Enter
Move Row Up (Style Settings): Alt + ↑
Move Row Down (Style Settings): Alt + ↓
Switch to Global Settings: Alt + ←
Switch to Style Settings: Alt + →
Delete Row: Delete
Insert Row: Control + I
Toggle 'bold' font: B
Toggle 'italic' font: I
Toggle 'underlined' font: U
'''
}


# Icon by Isaac Muse
AppIcon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABmJLR0QA/wD/AP+gvaeTAAAA"
    "CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3QYJBiAcFTQbJAAAAB1pVFh0Q29tbWVudAAA"
    "AAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAZiElEQVR42u2bebBlV3Xef2vtvc+59w09qdXq"
    "bqk1gVpqSUhqNGAmi9mmJBw7YYYYiAOUUzFU2XEqTiVVTC5PkGDHmAq4bIzJABgXk8AISzKT"
    "mIRASLSEsKaW1OpB6um9e+8Z9t4rf+zznmQQQkYIcMW3a9c59/a795z1rbW+Nex14J9f//z6"
    "//olP46L1L+WNO+/ZiTVnGvfe/ZkuO7Ksgeu8WuuG8U9e9UO7mvTF18RH+1784/WD4cXfzXo"
    "4nrXvOsxPZD9pem/Mtv/jBOe+8nTTjpGFo5bVF95o2mj3HdwYnfe16Td9/YTmRvdLePR1ZsX"
    "qrfdDTetfU+W6Qc+Xfef+Lnmn4QFhJddv9C97+zJ+BeuPSdOjr7nnA3tOZc+ab0++6kn8jPn"
    "bUIERMplY8y0XaKPmZyLEdx860E+84VbufyqG/nsF25Hth6/22845vfbv3vpO6rnfWy++9jz"
    "Jj+VAPgXfn0+fmDnxF365bfLnt3/7rXP2xL+9S+dzrh2pJyZG3nGI0ddOaqgOCfkbPQx03eJ"
    "po00XWQ67ZjOelJKBK9cdvku/vL/fol79kxwp+742/7aVz+7fubHFtornrf8o7hvfaQ/4H7+"
    "Sg8QLP5H3fG+/JoL7PWX/8lTwiVPP5mmTTRdQkXIZsSY6WOi7RJNE+m6RN8nupiIOZNiLjel"
    "BZwjRxt2Pm4rf/S7L+C3fv2ZLOy97Vmu+jXLd9/zEYDFJ/3v+Z+oBVS/smux+8oNrZtzR847"
    "vhr9xqvOIiVYmA+MakddKaNKqYMSglIFJQTBOynsZ5ByLsD0ibaLdH2iayN9LNYwm/W0TWQy"
    "aQnq+OhHbuBTn9iFpo7Ruec9P73uVX995JVqP7QCHxF6217ye+7QPZe98tLH+F94+jayCSE4"
    "VAXnQEVQlcHvC80D5AwxZVIqLhDjinVkYkw4FUJQgnd4p1iGnGBpqeW4Y9fw+PO28s1rbifs"
    "v+2F4dobXrR8+Mp3HHfhW9xkz5X2Y7OA6pmful0O7D3pdS8/m2PWjliYD9SVY1QrdVW0Xweh"
    "qpTKK94LwWvRvq74npGzkXKxgBgzKSVGtaNpI10XaZtEO+uZNT3tLLLvniW6aYPFyF/8yRXQ"
    "zjDv0m1L7/SnXvCH41uvef3sUeMAeaYJQPWkD8/coYMn/eqLz2I8CqhzpGxkM1KGlIyUjJiM"
    "Phpdn4nJ6PpE2ye6LtP2hR/aLtH1iT5l+pQYjwMxZXKGnAsXZMAyzCYRsWJZISgv/zdPZlR7"
    "5nLvzq5eZpuu+YrseNI75x81AOwKsfqJH2pd24ye/6wTCc4VgstGNhluGlI2YipCp5SJOdN1"
    "uYDR5QJEl+n7YvZdX86dKjFlzCi/mTPZht+MxnSWwMA5R1BlPPL8y5c+gUphHAK57ibrrv6c"
    "nXvBH4wfFQDqp3xk2XV9tfO09axdHCFOySak4YZjKoKnlfNchI7R6FMRvFsROBYraPuSB/Qx"
    "sTTtuPfgjL0HJhxdamm7DBnEhMOHOywVMEahAK8o4yrwrEvOo3bC2FeMR+3kumt+c3bxL17+"
    "sGR72Jlg9XNX3OAO7J+frz3nnLEBhFWN52QDCKwKrw5iFATDMLwJ5gTJueTAUjjAzEgpDcdM"
    "7DMpQdNH+i7TNRHLRkpgZlgywtjRRcWLgCrr1i9w5rkncec3b8VJ4NJ1L4kf//Bz/I/EAsLL"
    "di1Wv/TFX68O3HWWV+WJ522i7TMpDgIDGUi9EbORBlKLMRNTpk95leG7Pg3aL+zfxUSf0sAV"
    "w+epWExKRoqQMjSzRI6GZahrh+QSvhTBi6NS4TFnbOX44zew4JW5OHWXPPZXb1r7niyPOAzm"
    "69/RjeeeerXqiA1r53jMyYs4dTinwxJUFfWgUghKBERL3BMMG25jpeJJOZFycZWUjGRF6zFl"
    "8uBGfV9S5dhnYg99l7EYISZGlUCOaI7laAmJHY7IdO9+vDVUy3dv3HzLjTecfMqz77jlzs/0"
    "P7QLjJ9x2X5dXiY4x8nb5ukjOAd5SGJSliJQdGQVYjbUQJMhGJLBopAVnAoihgq07YzRqCab"
    "wcAhKRY3SJHh3EhRyAnUEskSKfUcOtCxMCd4l1FvWMpYZaxZWxGqhEqGDua+/dkP/unyl+WH"
    "4oDwgm9W0iz9bHXPd45VP4/zjnWLNWZaWHrFf7MRIzhnRMuoKTGBSAYRLAmQaZoZi24/c2HG"
    "4uIiOlZijDRtZJoWaNN6LIN0dzNfCZO4QBNHpGyYRZCESAKLIJHpkYa5WhgFsJQwg262xMI6"
    "T384IZbI9Lz07JdftfeEMy698m/+y+QfnQjNP/VDs6qPI+8dG9aOOXXbGka1Mqocde0YjZTK"
    "O+paqEJJeKrq/oTHO3BOkPZOtm8Vth5/AhuP2cDCwgIiQs6ZI0eOsHfffg4dvI+b71ngoh2e"
    "hYVFbrh5xu67IrHtsdhC7MldD32DdR10DXQN4wrmx0qaTdn/7VtoDtzLZO8epJ9CO6GLE/74"
    "yK3yj7KA8IJvVr4//JR6zy0jcfN451mYD6SUVsNeskzOSsbuZ3/LaBJUS8krIrj2dp60cwvb"
    "t28nhIq2j3z6q3dz76EWBU7cssDF55/N4SNHGY9v4uyzd+Kcctvdt2N2GJEIljFLOCmWYBKB"
    "hGmknTT4JFg7Q+iox0JXA1qswEnmV8655Mo9x5/zvE9+8ncmD9sCFp5z2b56+egm5yqCd2zb"
    "PM/CYlWKm9oxrh3VSrpbO+qh2PFBCE7wztB0lOdetIYzzzwTM0NE+NOPfBvVkuWJgCDklHnJ"
    "z5/KqCrkCnD5393GTd++D0sduW+h75HYIl2H9Q30xQJopqR2Ce06uqP3QTNlec9upJtBP8Ga"
    "CTnN+J0D98nDC4NPjwJQH7xrk4riVArTeyUP7J0tE62Eu4SRUyaZEa3k8zFnksHpm1t27Diz"
    "RACDPfdOiRh9LiQaE3QxEzO89+O3oCqYDfWMZEQjEFGK9pWIaI9qwmmPSA/SoNaT0zIiHdmm"
    "+MoIdU8VIvUoE8bCv33yJa97zXN+efQDAdj82F3zc//iqndqmMM5wVcODZAtka0kNQkr78lk"
    "jCQl60vJyvsBoPPP3c5qDSiAxSFqQLSVvy3uk4FPfP5OVMstiWSMhFhEJaIaES1HlQ6VHpUG"
    "kQ6RFpUWYYbThjDqqWqjGsNobIQ5ZS7u+833v/Q97Q8EYO+7z1kO06PPF+/RIKhmVCCtCJZz"
    "sQQrWl+N4xhpBRAyuT/Cli1bVttfAizUEGM7CA0xQ0ZIKDEL37lzSt/3A/NnVBLqEqqpCC8R"
    "pz2qPWiHSI9QhIcW73vUdYxHRj3K1KOMn3e4OWXt5LYTHqxv8KCZoF/au1GHuK3OcAFiSiQy"
    "UQYhrQiayIUQrXweB2Cc01Xhi0aFxcVFLjphiqWGTHGDjJRCCkM08sXr9nDbnYeYTBtUe5xE"
    "RPqicdejGnGuxVE0rtoi2uB9i/MNleuo6kwYGX5OkLHixoqMK17/jPNOf+1zLvbfNwq4S67w"
    "afeda4Ob4pyhzlBXOKAICmZCTIJfjQYyJEUQTUu5ajBN38s5IsI55zwOkeu559BRbltaD64G"
    "STgSKpHrbt7H9TfdBamYOYPZW444F7HUIfREWpzrMOkw30PfIa5HxxmJGQ3QR4fmjOuV4DKz"
    "tVv+c1pz3L+Hzyw9qAVse+zJYXH7ttehrpi/K50dcSXjTzkP5p6J3E+IvQ1uYPf/f3aBtm3v"
    "J7WV3GJ+nosuuoidO07kiduWOHXuHjzLiKZi8poH/46IpOLz2hN8WvV1aAmux2mPDz3edYS6"
    "aL4aJeraVjWv9cpyjGzpZ5qTn5C+by3gz3rRfG6WfqPuZqc673DB4X0BwfmhveUNN1iFyuAi"
    "XhBXzlVLx8d5ARNO2bIGFfkeS1i3bh1bt25lfuRY75eo8yGW21RyCOvwElF61DqUHrEGzS1C"
    "g6NDbYZYi+Ypnoag5TtOelQNnGGukLZ4iGq0mfp/vvvP3vR9XWDhhC394f33bMOVclbVEJ9x"
    "Xkuh4w2BkpNnSALFeDNqRkJQAxElmXLVrgM89XGbS0vMfS/dOOc46cQTOenEE9mzZw/H3nUX"
    "+w4e5cBS4QMkgsXiChRAzCKWWwgRyQ3OesRlpAfnEhaV2AuSBE2KIuTkUMv4OHvoMHjo1JNn"
    "2GytqqEulyWGqKE+o2ql6nNGFiMTiVZWHsgwiRVOGCz/zR+6cSiRH7pfuXXrVi688ELOPv2x"
    "nLZ5hNOIcz3OF1/3rkNdh/oO73oq31FXmTDOVKNi+mEEOhLcSNGR4mpBR4rUDgmCyxP3kAAc"
    "eaWakj0SETHEGeJWBC/vdbAO0QxqRfDVf6U3kJVSGToBgTd/+Cauue0wwEMCISKceuopnH/+"
    "+Ww/YTNKR/BxEL6EP+86QuipqkSoI1VlhDpTjQypFK0UVo5ei+CjgFaCOJHvzn6/1y6lG4RL"
    "CBl1hvj7gRAdzgdAnDdkyBOylCQpiZEkY2JkB9nBJ27cz+9+6jvsPjgZWuMPDoSZMR6P2bnz"
    "PDZv3Iy6Hhd6vGsJVaSuM/W4aLwaGVWdCFVCKsVVCl7QUDjJVYIGRYIDheTUHhKAte/JSu57"
    "kYS4hIaMDNqWgQ/U58EKBnCcIQ40CKhgfojtClEhimEOTBKZlg9941b+/Opd7F8agDB7UEuo"
    "6xFn7XhcYXqfSmJTJaoqUYVIqPKwEq5SnBesEqQqWteqtOBcHRCXya68f8hqcO7Ga+cbz1GL"
    "3RaRuhi0REQ9ohl1MoABEnRwCVBfQqaGUjOoGpUt86z1PZoTn81bcZJRBe8ys77l49d9i/Xj"
    "wNN3nMaGhcUHtYYtW7awft0mmuluNGVEE84SEg3JCXUZc4pJiTiqUkhPShKmCBAgzTDNJFfn"
    "+3PzBwEgLd0nKXe7VdLpEBEXS1nrMuK0uIVqsQoBdYp4RZwgXhCVQpJeqZzjiReeQ0qJW667"
    "nYkotTMqNWqf8JLpYsvl13+FbevW8+Qdj38Qd8gce+xm9t1zG5ITLpW2sLqIxlSIeOgOZyvu"
    "LbnoTbOUo3qyFltvqrnJdwPwD1xgrrI+tYc+T5oCpfbGZSAVzfu8avLiAFesQHwBQGtKPlCB"
    "qxzHHHMMx2w8lrM21ASfCD5Sh0hwkcpFvEtULnPv0j18+cYv/oPUeTVxmqsIIRFCwteZykdC"
    "KJmeOgEHpsCgBLyUvCQIWo1IOSJaiq1G5u5+1Rv/w9rvC8A96x7fTj79xg9KnmHWFo27CD6B"
    "pvsBURu0bgWEUJINHFCBBMNrGe5QgR1bN1HRUmmPdz3eRbxGvB+Wixyc7KHrun+QOYoofTpY"
    "fH34W1flQrw6CKxagPBS3NFJUY6CH9WIg0TCgCOtfbWKk/R9AWjfsMmAWevUjA6sW7UE0Yw4"
    "Kd8YtI+jCO4F8SBBkGBULhH8/dc5bvNmzvBS4rp2eC0gVBqpXCZ4w4fMbDb7ntT58NEbcL4n"
    "1IkQMt7lVW2bgCiYK7djbuXeivaRhLlEyolZhA++/8t/uOW0TdOHDIMbLnju4VbcvpQ7jBZj"
    "pQ1lRZ1OEK+l4nFAWDmChEzlS9hyDwAAM87dfjobZ6WWFzqcdjiXqHxGJTI9eoS5ubnVfkDO"
    "kSNLt6PaEHzE+VInsKKEQRHiQIf3ouV9Yf8ak0xOiWSGec3A9A2//Mb8UADYmqe9tp0dvvOj"
    "mqbk1BUAVpAdhDZnEKRQqAdqw4VMCCVL8xpx9KtxPVlm06ZN7Dj+FDYuBayZDTl7BG1pmwnr"
    "7TS896vkp+r5zh1/gfel4FGXCveUzYbiIlqi+v2aBxOoRotAxKynT5HOMnvSujtOf8LOQz8w"
    "Ebr9rb84m1393r9K1pJTQ0o9JhlTI+uwJeOBkKECanA+4VxbTFsjXlpE29WY/n++fjk377+d"
    "7du3c9b2MznJbcPvnSPucczuqFkfT2Pnzsevah6Er9/8e7iBOEXyKpgmBjIcAVvpcQxg+NFc"
    "aZgSSTnRx8ikFb70lTv/+7lPfcyhhwyDq/uAW0/bs+RGd7jcnxSsI6UO7zxUrpi8FywAdcZp"
    "R1BKC5zSvRl2NLnryH6COib9IT536+f4+wPf4uLHXszWLVs5ePA+Zs0M5xwbN24k+AqAg8s3"
    "snv/x1bdhKHNZqv7SsMek1gRXoplmhguBLCAaUfKkabrmeVM513adcOB63fd8Ffdw9kak3zM"
    "yUuzr3z4jg3bz3mB1AEXPK6ucLUvKeecwwcjuEzlC+EF6QjaU0micj3iO27c//fcuP8mPIX0"
    "YlrmtoPXc+fhm3BVZjTncFVkudnD3iNf49b9H2ZpuguVUtpaTmU0ZGjDWc7YcJ5zxiyDZbKl"
    "obqcJ6eWvmuZNTOW25ZJE7nuwJpPJDf31wf3Hjr4cPYFzG6/doa6e4/6+fvWpu4YT0OSmqwe"
    "gsekxXslOMNLxpnhLKFkRBJmuXSGKJ+ps9X2GprpcsvdR77BvqW+fF8TQTKqLUoPORXhB81b"
    "zqWtTC7uOFSolowsGUGoRuvomykpRZrYMuk7Zn2iSdk+8r5r/xz4zneb/0PtDgtza7594P2/"
    "/xr6CSm3pDwjDZ3XSlvIU5QGtQaYgM5Qm4HNUBpEpiAzRJrC/Nog2uKkw0uDyATVrnymDaJT"
    "nHSQI1hpsVqORdukoSs9aH3oR0NGxOHr9aTUka2nSy1N1zHrItMu8/V96z6w6YQNe4dC9WHv"
    "DRrLh/bo2mPtoIx3bczdmTFOqaJgeQTZ4YeNT1WK9q3EXBUQMmIZhbJBooaK4MRKi01zqTjF"
    "ho5vAisTIWKZMgyQB0taab6XlQdGwDLiaoKrSP2MbC1talnuGpbbjkmXWLaqu+x/ff0DwNcf"
    "MJb78LfHrZ0uz7559c1rLrjwhQshiyMSXE/wkaCJyrWo6wiuJDdBE14agksl0fGR4DLeJWqX"
    "8T7hXU/Q0t4OrnR91TJiCbVctD/4OzmVVDYnclr5vCyVNcOuUkvMHbN+xqSZsbQ8Y9L0LE8S"
    "b/tvN71Y1O22bHf8sAMSd7n5xemdH//oq7vJIXxcxrdHyZPD5O4IFqeQJ4hNEaaoTVA6vDZ4"
    "1+KkxekM7xrEzVApS9wMcS1Gh+WenHssR9KwCvn1ZIuYpUKAVpqyZh71G0BTifO5pekbJrOG"
    "o8tTJk1kMsvsOrTmsmphMaSYvvFIBiTE+m6fiD4mbT2xW6yas70m5oMMft0StFiD1w4fIrWP"
    "xUJcJPhUKj+NBJcILpZESRLOMvqAtTJvI7lsalq+3xVSSgMxLSLisdySUkfbN0zbGZPJjKPL"
    "MyaTnmnTsS8u3PeXb7/2TX3TXQPc90gHJTtrZ3G668YD1c5zzxjL8nFCS62JOQdeI6KzIf+P"
    "VCHhfU/lE5VGnEZC6PHS4zXjMLwZkNCcEbMS6igAlL3+IdxZwpJDdQGsxnKP5Y6YWtq+YdY0"
    "LE1mHF2asjzpmMwiR/vQ/9FbrnvFIPg3flSToveCbTp8zXVfWXj8454wtuV1klsckUozC5Vn"
    "5KFyCacdtYtULg09+4gXww+dY58TYoZmK6HNSuuNnMCKxsmCsxGii2AeSz1935BTR7ci+PK0"
    "CL40Y3naMZn2TJNLb33zDS8CeuCqByO9RzIqexdw8r1f/daVc+edvmNep8cZMzw9Yh1OImMP"
    "C2FE7ZTKG8EMh6GWcEbp4hgoJYEppAeaHUIFqUaZRwhYNnLsybEhxo6+b5gN5r60PGVpacby"
    "csN0mCJdSlX71jdd/2LnwIyrgOZHDQDAbuCUe792y+f11JPs2Pnu7Cwdmlu8RcRKBak54bMS"
    "LBCsppY5fB5TMY+zMY55nM2hNodYjZlDshSiix059vR9Rx9b2qalaRqm0xnLS1OOLpXjZNLS"
    "NJHJNLO3Xbjrj3/72lcPhecXgIOP1qywlPKHZ1Xr166ZO0bnnv6yM941V2cZVcK4CizUI+bG"
    "FaPKMzcKjKpAHTx1cHh1OBW8Cl7KDKEIJWewXLSeE7GPWJ+IfUfb9XRdTzPraJqGrot0baTp"
    "ErFPfPXW8Gd/877rLhvu7wvAvkd7WFqGBOppflytj7MuPuO3nvbbJ42mZ4RKGAVl5JVRXTOq"
    "AtUgfF15gleCK0MXfmh/6VDmiCUkJVKKpK6A0PeJrutou47UlznD2Ee6Tjhi/ujb3/S1Vy0e"
    "Mz9aum8yAT4LHPpxTYuvfO8CYFu1dqHqjix3L3zDz757o7QbfDDqULbDKq8E5wneD+PvUqZO"
    "5P6JcaVMQ1uKpJjJMZJTeZgipUxKmT5G+l5psf6qzx99y5f/9rYbhns4CnwOaH9Sj8xsBS4Q"
    "FW+m4n2Sf/Wfnva2LfXSiYojeEEFKq/lOQKG9FnKQxPKMDprNlR7K+OzRswJMvQ9HLb66Bc+"
    "v++t11xx+7fqcXDtrE/AjcOSh0N4j+YzQw44BzhFVAjz46pbmnZPe8WFl5566uIlG6vlY6V3"
    "4n3GB0GGCVJHqfAUGz4rk2d9BKc9h/N4afd+ufoD/+NL7wJ4gOAHgGtLFfbT9dTYGDgTOBGQ"
    "0ZpR6BvLqWsTwMUvPf+Zx29b3Lkwx9Y5z6JzODFDcpeb5CfTxu49eG974xc/es0n9u61KcDC"
    "unE9XZp1uTR2DwDfGlj+h9b6ownAyk35AYRTgLWlfydU49r72vtsarPDkw4b9pDFyWhxXAVv"
    "kvqY+jamvksr5etsCL+3Duc/EsEftecGH6zDBhwLbALWA/Olh/ygrzgIeQTYP6zpd4H70/3g"
    "5A+wjAdyhn/A9UtxUAB4qO/xTxWAh3Nt+0ncxP8DB2tSbeIgNgsAAAAASUVORK5CYII=")

JSON_ADD = 1
JSON_DELETE = 2
JSON_MODIFY = 3
JSON_MOVE = 4
JSON_UUID = 5
JSON_NAME = 6


#################################################
# Live Update Manager
#################################################
class LiveUpdate(threading.Thread):

    """
    Live update of the file.

    This is mainly so Sublime can refersh the theme as you edit.
    """

    def __init__(self, func, queue):
        """Initialize."""

        self.func = func
        self.queue = queue
        self.last_queue_len = len(queue)
        self.abort = False
        self.last_update = 0.0
        self.done = False
        self.locked = False
        threading.Thread.__init__(self)

    def kill_thread(self):
        """Kill thread."""

        self.abort = True

    def lock_queue(self):
        """Lock the queue."""

        if not self.is_queue_locked():
            self.locked = True
            return True
        return False

    def release_queue(self):
        """Release the queue."""

        if self.is_queue_locked():
            self.locked = False
            return True
        return False

    def is_queue_locked(self):
        """Check if queue is locked."""

        return self.locked

    def is_done(self):
        """Check if done."""

        return self.done

    def update(self, queue):
        """Update the theme."""

        request = None
        for x in queue:
            if x == "all":
                request = x
                break
            elif x == "json":
                if request == "tmtheme":
                    request = "all"
                else:
                    request = x
            elif x == "tmtheme":
                if request == "json":
                    request = "all"
                    break
                else:
                    request = x

        wx.CallAfter(self.func, request, "Live Thread")

    def _process_queue(self):
        """Process the queue."""

        while not self.lock_queue():
            time.sleep(.2)
        current_queue = self.queue[0:self.last_queue_len]
        del self.queue[0:self.last_queue_len]
        self.last_queue_len = len(self.queue)
        self.release_queue()
        return current_queue

    def run(self):
        """Run the thread."""

        while not self.abort:
            now = time.time()
            if len(self.queue) and (now - .5) > self.last_update:
                if len(self.queue) != self.last_queue_len:
                    self.last_queue_len = len(self.queue)
                else:
                    self.update(self._process_queue())
                    self.last_update = time.time()
            if self.abort:
                break
            time.sleep(.5)
        if len(self.queue):
            self.update(self._process_queue())
        self.done = True


#################################################
# Grid Helper Class
#################################################
class GridHelper(object):

    """Grid helper."""

    cell_select_semaphore = False
    range_semaphore = False
    current_row = None
    current_col = None

    def setup_keybindings(self):
        """Setup grid keybindings."""

        deleteid = wx.NewId()
        insertid = wx.NewId()

        self.Bind(wx.EVT_MENU, self.on_delete_row, id=deleteid)
        self.Bind(wx.EVT_MENU, self.on_insert_row, id=insertid)

        accel_tbl = wx.AcceleratorTable(
            [
                (wx.ACCEL_NORMAL, wx.WXK_DELETE, deleteid),
                (wx.ACCEL_CMD, ord('I'), insertid) if sys.platform == "darwin" else (wx.ACCEL_CTRL, ord('I'), insertid)
            ]
        )
        self.SetAcceleratorTable(accel_tbl)

    def go_cell(self, grid, row, col, focus=False):
        """Go to cell."""

        if focus:
            grid.GoToCell(row, col)
        else:
            grid.SetGridCursor(row, col)
        bg = grid.GetCellBackgroundColour(row, 0)
        lum = RGBA(bg.GetAsString(wx.C2S_HTML_SYNTAX)).luminance()
        if lum > 128:
            bg.Set(0, 0, 0)
        else:
            bg.Set(255, 255, 255)
        grid.SetCellHighlightColour(bg)

    def mouse_motion(self, event):
        """Capture if mouse is dragging."""

        if event.Dragging():       # mouse being dragged?
            pass                   # eat the event
        else:
            event.Skip()           # no dragging, pass on to the window

    def grid_key_down(self, event):
        """Check for certain key down events in the grid."""

        no_modifiers = event.GetModifiers() == 0
        alt_mod = event.GetModifiers() == wx.MOD_ALT
        if no_modifiers and event.GetKeyCode() == ord('B'):
            self.toggle_bold()
            return
        elif no_modifiers and event.GetKeyCode() == ord('I'):
            self.toggle_italic()
            return
        elif no_modifiers and event.GetKeyCode() == ord('U'):
            self.toggle_underline()
            return
        elif no_modifiers and event.GetKeyCode() == wx.WXK_RETURN:
            self.edit_cell()
            return
        elif alt_mod and event.GetKeyCode() == wx.WXK_UP:
            self.row_up()
            return
        elif alt_mod and event.GetKeyCode() == wx.WXK_DOWN:
            self.row_down()
            return
        elif alt_mod and event.GetKeyCode() == wx.WXK_LEFT:
            self.on_panel_left(event)
            return
        elif alt_mod and event.GetKeyCode() == wx.WXK_RIGHT:
            self.on_panel_right(event)
            return
        elif event.AltDown():
            # Eat...NOM NOM
            if event.GetKeyCode() == wx.WXK_UP:
                return
            elif event.GetKeyCode() == wx.WXK_DOWN:
                return
            elif event.GetKeyCode() == wx.WXK_LEFT:
                return
            elif event.GetKeyCode() == wx.WXK_RIGHT:
                return
        elif event.ShiftDown():
            # Eat...NOM NOM
            if event.GetKeyCode() == wx.WXK_UP:
                return
            elif event.GetKeyCode() == wx.WXK_DOWN:
                return
            elif event.GetKeyCode() == wx.WXK_LEFT:
                return
            elif event.GetKeyCode() == wx.WXK_RIGHT:
                return
        event.Skip()

    def grid_select_cell(self, event):
        """Grid cell selected."""

        grid = self.m_plist_grid
        if not self.cell_select_semaphore and event.Selecting():
            self.cell_select_semaphore = True
            self.current_row = event.GetRow()
            self.current_col = event.GetCol()
            self.go_cell(grid, self.current_row, self.current_col)
            self.cell_select_semaphore = False
        event.Skip()

    def on_panel_left(self, event):
        """Handle left key press."""

        grid = self.m_plist_grid
        grid.GetParent().GetParent().ChangeSelection(0)
        grid.GetParent().GetParent().GetPage(0).m_plist_grid.SetFocus()

    def on_panel_right(self, event):
        """Handle right key press."""

        grid = self.m_plist_grid
        grid.GetParent().GetParent().ChangeSelection(1)
        grid.GetParent().GetParent().GetPage(1).m_plist_grid.SetFocus()

    def on_row_up(self, event):
        """Handle row up."""

        self.row_up()

    def on_row_down(self, event):
        """Handle row down."""

        self.row_down()

    def on_insert_row(self, event):
        """Handle insert row."""

        self.insert_row()

    def on_delete_row(self, event):
        """Handle delete row."""

        self.delete_row()

    def on_edit_cell_key(self, event):
        """Handle edit cell key."""

        self.edit_cell()

    def on_toggle_bold(self, event):
        """Handle bold event."""

        self.toggle_bold()

    def on_toggle_italic(self, event):
        """Handle italic event."""

        self.toggle_italic()

    def on_toggle_underline(self, event):
        """Handle underline event."""

        self.toggle_underline()

    def toggle_bold(self):
        """Override for toggle bold."""

        pass

    def toggle_italic(self):
        """Override for toggle italic."""

        pass

    def toggle_underline(self):
        """Override for toggle underline."""

        pass

    def row_up(self):
        """Override row up."""

        pass

    def row_down(self):
        """Override for row down."""
        pass

    def edit_cell(self):
        """Override for edit cell."""
        pass

    def delete_row(self):
        """Override for delete row."""

        pass

    def insert_row(self):
        """Override for insert tow."""

        pass


#################################################
# Grid Display Panels
#################################################
class StyleSettings(editor.StyleSettingsPanel, GridHelper):

    """Style settings handler."""

    def __init__(self, parent, scheme, update):
        """Initialize."""

        super(StyleSettings, self).__init__(parent)
        self.setup_keybindings()
        self.parent = parent
        wx.EVT_MOTION(self.m_plist_grid.GetGridWindow(), self.on_mouse_motion)
        self.m_plist_grid.SetDefaultCellBackgroundColour(self.GetBackgroundColour())
        self.read_plist(scheme)
        self.update_plist = update

    def read_plist(self, scheme):
        """Read the plist."""

        foreground = RGBA(scheme["settings"][0]["settings"].get("foreground", "#000000"))
        background = RGBA(scheme["settings"][0]["settings"].get("background", "#FFFFFF"))
        global BG_COLOR
        BG_COLOR = background
        global FG_COLOR
        FG_COLOR = foreground
        count = 0

        for s in scheme["settings"]:
            if "name" in s:
                self.m_plist_grid.AppendRows(1)
                self.update_row(count, s)
                count += 1
        self.resize_table()
        self.go_cell(self.m_plist_grid, 0, 0)

    def update_row(self, count, s):
        """Update stye row."""

        self.m_plist_grid.SetCellValue(count, 0, s["name"])
        self.m_plist_grid.SetCellValue(count, 4, s.get("scope", ""))
        settings = s["settings"]
        b = self.m_plist_grid.GetCellBackgroundColour(count, 0)
        if "background" in settings:
            try:
                bg = RGBA(settings["background"].strip())
                bg.apply_alpha(BG_COLOR.get_rgb())
                self.m_plist_grid.SetCellValue(count, 2, settings["background"])
            except:
                bg = BG_COLOR
                self.m_plist_grid.SetCellValue(count, 2, "")
        else:
            bg = BG_COLOR
        b = self.m_plist_grid.GetCellBackgroundColour(count, 0)
        b.Set(bg.r, bg.g, bg.b)
        self.m_plist_grid.SetCellBackgroundColour(count, 0, b)
        self.m_plist_grid.SetCellBackgroundColour(count, 1, b)
        self.m_plist_grid.SetCellBackgroundColour(count, 2, b)
        self.m_plist_grid.SetCellBackgroundColour(count, 3, b)
        self.m_plist_grid.SetCellBackgroundColour(count, 4, b)
        if "foreground" in settings:
            try:
                fg = RGBA(settings["foreground"].strip())
                fg.apply_alpha(BG_COLOR.get_rgb())
                self.m_plist_grid.SetCellValue(count, 1, settings["foreground"])
            except:
                fg = FG_COLOR
                self.m_plist_grid.SetCellValue(count, 1, "")
        else:
            fg = FG_COLOR
        f = self.m_plist_grid.GetCellTextColour(count, 0)
        f.Set(fg.r, fg.g, fg.b)
        self.m_plist_grid.SetCellTextColour(count, 0, f)
        self.m_plist_grid.SetCellTextColour(count, 1, f)
        self.m_plist_grid.SetCellTextColour(count, 2, f)
        self.m_plist_grid.SetCellTextColour(count, 3, f)
        self.m_plist_grid.SetCellTextColour(count, 4, f)

        fs_setting = settings.get("fontStyle", "")
        font_style = []
        for x in fs_setting.split(" "):
            if x in ["bold", "italic", "underline"]:
                font_style.append(x)

        self.m_plist_grid.SetCellValue(count, 3, " ".join(font_style))
        fs = self.m_plist_grid.GetCellFont(count, 0)
        fs.SetWeight(wx.FONTWEIGHT_NORMAL)
        fs.SetStyle(wx.FONTSTYLE_NORMAL)
        fs.SetUnderlined(False)

        if "bold" in font_style:
            fs.SetWeight(wx.FONTWEIGHT_BOLD)

        if "italic" in font_style:
            fs.SetStyle(wx.FONTSTYLE_ITALIC)

        if "underline" in font_style:
            fs.SetUnderlined(True)

        self.m_plist_grid.SetCellFont(count, 0, fs)
        self.m_plist_grid.SetCellFont(count, 1, fs)
        self.m_plist_grid.SetCellFont(count, 2, fs)
        self.m_plist_grid.SetCellFont(count, 3, fs)
        self.m_plist_grid.SetCellFont(count, 4, fs)

    def resize_table(self):
        """Resize the table."""

        self.m_plist_grid.BeginBatch()
        nb_size = self.parent.GetSize()
        total_size = 0
        for x in range(0, 5):
            self.m_plist_grid.AutoSizeColumn(x)
            total_size += self.m_plist_grid.GetColSize(x)
        delta = nb_size[0] - 20 - total_size
        if delta > 0:
            self.m_plist_grid.SetColSize(4, self.m_plist_grid.GetColSize(4) + delta)
        self.m_plist_grid.EndBatch()

    def set_object(self, obj):
        """Set the object."""

        row = self.m_plist_grid.GetGridCursorRow()
        self.update_row(row, obj)
        self.update_plist(JSON_MODIFY, {"table": "style", "index": row, "data": obj})
        self.resize_table()

    def edit_cell(self):
        """Handle editting the cell."""

        grid = self.m_plist_grid
        row = grid.GetGridCursorRow()
        editor = self.GetParent().GetParent().GetParent()
        ColorEditor(
            editor,
            {
                "name": grid.GetCellValue(row, 0),
                "scope": grid.GetCellValue(row, 4),
                "settings": {
                    "foreground": grid.GetCellValue(row, 1),
                    "background": grid.GetCellValue(row, 2),
                    "fontStyle": grid.GetCellValue(row, 3)
                }
            }
        ).ShowModal()

    def delete_row(self):
        """Handle row delete."""

        row = self.m_plist_grid.GetGridCursorRow()
        self.m_plist_grid.DeleteRows(row, 1)
        self.m_plist_grid.GetParent().update_plist(JSON_DELETE, {"table": "style", "index": row})

    def insert_row(self):
        """Handle inserting into row."""

        obj = {
            "name": "New Item",
            "scope": "comment",
            "settings": {
                "foreground": "#FFFFFF",
                "background": "#000000",
                "fontStyle": ""
            }
        }
        editor = self.GetParent().GetParent().GetParent()
        ColorEditor(
            editor,
            obj,
            insert=True
        ).ShowModal()

    def row_up(self):
        """Handle row up."""

        grid = self.m_plist_grid
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        if row > 0:
            text = [grid.GetCellValue(row, x) for x in range(0, 5)]
            bg = [grid.GetCellBackgroundColour(row, x) for x in range(0, 5)]
            fg = [grid.GetCellTextColour(row, x) for x in range(0, 5)]
            font = [grid.GetCellFont(row, x) for x in range(0, 5)]
            grid.DeleteRows(row, 1, False)
            grid.InsertRows(row - 1, 1, True)
            [grid.SetCellValue(row - 1, x, text[x]) for x in range(0, 5)]
            [grid.SetCellBackgroundColour(row - 1, x, bg[x]) for x in range(0, 5)]
            [grid.SetCellTextColour(row - 1, x, fg[x]) for x in range(0, 5)]
            [grid.SetCellFont(row - 1, x, font[x]) for x in range(0, 5)]
            self.go_cell(grid, row - 1, col, True)
            grid.GetParent().update_plist(JSON_MOVE, {"from": row, "to": row - 1})
            grid.SetFocus()

    def row_down(self):
        """Handle row down."""

        grid = self.m_plist_grid
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        if row < grid.GetNumberRows() - 1:
            text = [grid.GetCellValue(row, x) for x in range(0, 5)]
            bg = [grid.GetCellBackgroundColour(row, x) for x in range(0, 5)]
            fg = [grid.GetCellTextColour(row, x) for x in range(0, 5)]
            font = [grid.GetCellFont(row, x) for x in range(0, 5)]
            grid.DeleteRows(row, 1, False)
            grid.InsertRows(row + 1, 1, True)
            [grid.SetCellValue(row + 1, x, text[x]) for x in range(0, 5)]
            [grid.SetCellBackgroundColour(row + 1, x, bg[x]) for x in range(0, 5)]
            [grid.SetCellTextColour(row + 1, x, fg[x]) for x in range(0, 5)]
            [grid.SetCellFont(row + 1, x, font[x]) for x in range(0, 5)]
            self.go_cell(grid, row + 1, col, True)
            grid.GetParent().update_plist(JSON_MOVE, {"from": row, "to": row + 1})
            grid.SetFocus()

    def is_fontstyle_cell(self):
        """Check if fontstyle cell."""

        return self.m_plist_grid.GetGridCursorCol() == 3

    def toggle_font_style(self, row, attr):
        """Toggle the font style."""

        # if not self.is_fontstyle_cell():
        #     return
        grid = self.m_plist_grid
        text = [grid.GetCellValue(row, x) for x in range(0, 5)]
        style = text[3].split(" ")
        try:
            idx = style.index(attr)
            del style[idx]
        except:
            style.append(attr)
        text[3] = " ".join(style)

        obj = {
            "name": text[0],
            "scope": text[4],
            "settings": {
                "foreground": text[1],
                "background": text[2],
                "fontStyle": text[3]
            }
        }
        grid.GetParent().update_row(row, obj)
        self.update_plist(JSON_MODIFY, {"table": "style", "index": row, "data": obj})
        self.resize_table()

    def toggle_bold(self):
        """Toggle bold."""

        self.toggle_font_style(self.m_plist_grid.GetGridCursorRow(), "bold")

    def toggle_italic(self):
        """Toggle italic."""

        self.toggle_font_style(self.m_plist_grid.GetGridCursorRow(), "italic")

    def toggle_underline(self):
        """Toggle underline."""

        self.toggle_font_style(self.m_plist_grid.GetGridCursorRow(), "underline")

    def on_mouse_motion(self, event):
        """Handle mouse motion event."""

        self.mouse_motion(event)

    def on_edit_cell(self, event):
        """Handle editing cell event."""

        self.edit_cell()

    def on_grid_key_down(self, event):
        """Handle key down event on grid."""

        self.grid_key_down(event)

    def on_grid_select_cell(self, event):
        """Handle grid select event."""

        self.grid_select_cell(event)

    def on_row_up_click(self, event):
        """Handle row up click."""

        self.row_up()

    def on_row_down_click(self, event):
        """Handle row down click."""

        self.row_down()

    def on_row_add_click(self, event):
        """Handle row add click."""

        self.insert_row()

    def on_row_delete_click(self, event):
        """Handle row delete click."""

        self.delete_row()

    def on_grid_label_left_click(self, event):
        """Handle grid label left click."""

        return


class GlobalSettings(editor.GlobalSettingsPanel, GridHelper):

    """GlobalSettings."""

    def __init__(self, parent, scheme, update, reshow):
        """Initialize."""

        super(GlobalSettings, self).__init__(parent)
        self.setup_keybindings()
        self.parent = parent
        wx.EVT_MOTION(self.m_plist_grid.GetGridWindow(), self.on_mouse_motion)
        self.m_plist_grid.SetDefaultCellBackgroundColour(self.GetBackgroundColour())
        self.read_plist(scheme)
        self.reshow = reshow
        self.update_plist = update

    def read_plist(self, scheme):
        """Read plist to get global settings."""

        foreground = RGBA(scheme["settings"][0]["settings"].get("foreground", "#000000"))
        background = RGBA(scheme["settings"][0]["settings"].get("background", "#FFFFFF"))
        global BG_COLOR
        BG_COLOR = background
        global FG_COLOR
        FG_COLOR = foreground
        count = 0

        for k in sorted(scheme["settings"][0]["settings"].iterkeys()):
            v = scheme["settings"][0]["settings"][k]
            self.m_plist_grid.AppendRows(1)
            self.update_row(count, k, v)
            count += 1
        self.resize_table()

        self.go_cell(self.m_plist_grid, 0, 0)

    def resize_table(self):
        """Resize teh table."""

        self.m_plist_grid.BeginBatch()
        nb_size = self.parent.GetSize()
        total_size = 0
        for x in range(0, 2):
            self.m_plist_grid.AutoSizeColumn(x)
            total_size += self.m_plist_grid.GetColSize(x)
        delta = nb_size[0] - 20 - total_size
        if delta > 0:
            self.m_plist_grid.SetColSize(1, self.m_plist_grid.GetColSize(1) + delta)
        self.m_plist_grid.EndBatch()

    def update_row(self, count, k, v):
        """Update row."""

        try:
            bg = RGBA(v.strip())
            if k != "background":
                bg.apply_alpha(BG_COLOR.get_rgb())
            fg = RGBA("#000000") if bg.luminance() > 128 else RGBA("#FFFFFF")
        except:
            bg = RGBA("#FFFFFF")
            fg = RGBA("#000000")

        self.m_plist_grid.SetCellValue(count, 0, k)
        self.m_plist_grid.SetCellValue(count, 1, v)

        b = self.m_plist_grid.GetCellBackgroundColour(count, 0)
        f = self.m_plist_grid.GetCellTextColour(count, 0)

        b.Set(bg.r, bg.g, bg.b)
        f.Set(fg.r, fg.g, fg.b)

        self.m_plist_grid.SetCellBackgroundColour(count, 0, b)
        self.m_plist_grid.SetCellBackgroundColour(count, 1, b)

        self.m_plist_grid.SetCellTextColour(count, 0, f)
        self.m_plist_grid.SetCellTextColour(count, 1, f)

    def set_object(self, key, value):
        """Set the object."""

        row = self.m_plist_grid.GetGridCursorRow()
        col = self.m_plist_grid.GetGridCursorCol()
        self.update_row(row, key, value)
        self.update_plist(JSON_MODIFY, {"table": "global", "index": key, "data": value})
        if key == "background" or key == "foreground":
            self.reshow(row, col)
        self.resize_table()

    def delete_row(self):
        """Delete the row."""

        row = self.m_plist_grid.GetGridCursorRow()
        col = self.m_plist_grid.GetGridCursorCol()
        name = self.m_plist_grid.GetCellValue(row, 0)
        self.m_plist_grid.DeleteRows(row, 1)
        self.m_plist_grid.GetParent().update_plist(JSON_DELETE, {"table": "global", "index": name})
        if name == "foreground" or name == "background":
            self.m_plist_grid.GetParent().reshow(row, col)

    def validate_name(self, name):
        """Validate the name."""

        valid = True
        editor = self.GetParent().GetParent().GetParent()
        for k in editor.scheme["settings"][0]["settings"]:
            if name == k:
                valid = False
                break
        return valid

    def insert_row(self):
        """Insert a new row."""

        new_name = "new_item"
        count = 0
        while not self.validate_name(new_name):
            new_name = "new_item_%d" % count
            count += 1

        editor = self.GetParent().GetParent().GetParent()
        GlobalEditor(
            editor,
            editor.scheme["settings"][0]["settings"],
            new_name,
            "nothing",
            insert=True
        ).ShowModal()

    def edit_cell(self):
        """Edit the cell."""
        grid = self.m_plist_grid
        row = grid.GetGridCursorRow()
        editor = self.GetParent().GetParent().GetParent()
        GlobalEditor(
            editor,
            editor.scheme["settings"][0]["settings"],
            grid.GetCellValue(row, 0),
            grid.GetCellValue(row, 1)
        ).ShowModal()

    def on_grid_label_left_click(self, event):
        """Handle grid label left click."""

        return

    def on_mouse_motion(self, event):
        """Handle mouse motion event."""

        self.mouse_motion(event)

    def on_edit_cell(self, event):
        """Handle edit cell event."""

        self.edit_cell()

    def on_grid_key_down(self, event):
        """Handle grid key down event."""

        self.grid_key_down(event)

    def on_grid_select_cell(self, event):
        """Handle grid select cell event."""

        self.grid_select_cell(event)

    def on_row_add_click(self, event):
        """Handle add row click event."""

        self.insert_row()

    def on_row_delete_click(self, event):
        """Handle delete row event."""

        self.delete_row()


#################################################
# Settings Dialogs
#################################################
class SettingsKeyBindings(object):

    """Key binding for settings."""

    def setup_keybindings(self):
        """Setup the key bindings."""
        self.Bind(wx.EVT_CHAR_HOOK, self.on_char_hook)

    def on_char_hook(self, event):
        """Evaluate keycode on char hook."""

        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()
        event.Skip()


class GlobalEditor(editor.GlobalSetting, SettingsKeyBindings):

    """GlobalEditor."""

    def __init__(self, parent, current_entries, name, value, insert=False):
        """Initialize."""

        super(GlobalEditor, self).__init__(parent)
        self.setup_keybindings()
        self.Fit()
        size = self.GetSize()
        self.SetMinSize(size)
        size.Set(-1, size[1])
        self.SetMaxSize(size)
        self.obj_key = name
        self.obj_val = value
        self.color_save = ""
        self.apply_settings = False
        self.color_setting = False
        self.m_color_picker.Disable()
        self.entries = current_entries
        self.current_name = name
        self.valid = True
        self.insert = bool(insert)

        self.m_name_textbox.SetValue(self.obj_key)
        try:
            RGBA(self.obj_val)
            self.color_setting = True
            self.color_save = self.obj_val
            self.m_color_picker.Enable()
            self.m_color_checkbox.SetValue(True)
        except:
            pass
        self.m_value_textbox.SetValue(self.obj_val)

    def on_color_button_click(self, event):
        """Handle color button click event."""

        if not self.color_setting:
            event.Skip()
            return
        color = None
        data = wx.ColourData()
        data.SetChooseFull(True)

        alpha = None

        text = self.m_value_textbox.GetValue()
        rgb = RGBA(text)
        if len(text) == 9:
            alpha == text[7:9]

        # set the default color in the chooser
        data.SetColour(wx.Colour(rgb.r, rgb.g, rgb.b))

        # construct the chooser
        dlg = wx.ColourDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            # set the panel background color
            color = dlg.GetColourData().GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
            self.m_value_textbox.SetValue(color if alpha is None else color + alpha)
        dlg.Destroy()
        event.Skip()

    def on_global_checkbox(self, event):
        """Handle global checkbox event."""

        if event.IsChecked():
            self.m_color_picker.Enable()
            self.color_setting = True
            try:
                RGBA(self.m_value_textbox.GetValue())
                self.on_color_change(event)
            except:
                self.m_value_textbox.SetValue("#000000")
            return
        else:
            self.color_setting = False
            self.m_color_picker.Disable()
            self.m_color_picker.SetBackgroundColour(wx.Colour(255, 255, 255))
            self.m_color_picker.Refresh()
        event.Skip()

    def is_name_valid(self):
        """Check if name is valid."""

        valid = True
        name = self.m_name_textbox.GetValue()
        if name != self.current_name:
            for k in self.entries:
                if name == k:
                    valid = False
                    break
        return valid

    def on_global_name_blur(self, event):
        """Handle global name blur event."""

        if not self.is_name_valid():
            errormsg(
                "Key name \"%s\" already exists in global settings. "
                "Please use a different name." % self.m_name_textbox.GetValue()
            )
            self.m_name_textbox.SetValue(self.current_name)
        else:
            self.current_name = self.m_name_textbox.GetValue()

    def on_color_change(self, event):
        """Handle color change event."""

        if not self.color_setting:
            event.Skip()
            return
        text = self.m_value_textbox.GetValue()
        try:
            cl = RGBA(text)
        except:
            event.Skip()
            return

        cl.apply_alpha(BG_COLOR.get_rgb())
        bg = wx.Colour(cl.r, cl.g, cl.b)
        self.m_color_picker.SetBackgroundColour(bg)
        self.m_color_picker.Refresh()

    def on_color_focus(self, event):
        """Handle color focus event."""

        if not self.color_setting:
            event.Skip()
            return
        if self.color_setting:
            self.color_save = self.m_value_textbox.GetValue()
        event.Skip()

    def on_color_blur(self, event):
        """Handle color blur event."""

        if not self.color_setting:
            event.Skip()
            return
        if self.color_setting:
            text = self.m_value_textbox.GetValue()
            try:
                RGBA(text)
            except:
                self.m_value_textbox.SetValue(self.color_save)
        event.Skip()

    def on_apply_button_click(self, event):
        """Handle apply button click event."""

        self.m_apply_button.SetFocus()
        if self.is_name_valid():
            self.apply_settings = True
            self.Close()
        else:
            errormsg(
                "Key name \"%s\" already exists in global settings. "
                "Please use a different name." % self.m_name_textbox.GetValue()
            )
            self.m_name_textbox.SetValue(self.current_name)

    def on_set_color_close(self, event):
        """Handle set color close event."""

        self.obj_key = self.m_name_textbox.GetValue()
        self.current_name = self.obj_key

        if self.apply_settings:
            self.obj_val = self.m_value_textbox.GetValue()

            if self.insert:
                grid = self.Parent.m_global_settings.m_plist_grid
                num = grid.GetNumberRows()
                row = grid.GetGridCursorRow()
                if num > 0:
                    grid.InsertRows(row, 1, True)
                else:
                    grid.AppendRows(1)
                    row = 0
                grid.GetParent().update_row(row, self.obj_key, self.obj_val)
                grid.GetParent().go_cell(grid, row, 0)
                self.Parent.update_plist(JSON_ADD, {"table": "global", "index": self.obj_key, "data": self.obj_val})
            else:
                self.Parent.set_global_object(self.obj_key, self.obj_val)

        event.Skip()


class ColorEditor(editor.ColorSetting, SettingsKeyBindings):

    """Color editor."""

    def __init__(self, parent, obj, insert=False):
        """Initialize."""

        super(ColorEditor, self).__init__(parent)
        self.setup_keybindings()
        self.Fit()
        size = self.GetSize()
        self.SetMinSize(size)
        size.Set(-1, size[1])
        self.SetMaxSize(size)
        self.foreground_save = ""
        self.background_save = ""
        self.apply_settings = False
        self.color_obj = obj
        self.insert = bool(insert)

        self.m_bold_checkbox.SetValue(False)
        self.m_italic_checkbox.SetValue(False)
        self.m_underline_checkbox.SetValue(False)

        for x in self.color_obj["settings"]["fontStyle"].split(" "):
            if x == "bold":
                self.m_bold_checkbox.SetValue(True)
            elif x == "italic":
                self.m_italic_checkbox.SetValue(True)
            elif x == "underline":
                self.m_underline_checkbox.SetValue(True)

        self.m_name_textbox.SetValue(self.color_obj["name"])
        self.m_scope_textbox.SetValue(self.color_obj["scope"])

        self.m_foreground_textbox.SetValue(self.color_obj["settings"]["foreground"])
        if self.color_obj["settings"]["foreground"] == "":
            cl = RGBA("#FFFFFF")
            bg = wx.Colour(cl.r, cl.g, cl.b)
            self.m_foreground_picker.SetBackgroundColour(bg)
            if cl.luminance() > 128:
                fg = wx.Colour(0, 0, 0)
            else:
                fg = wx.Colour(255, 255, 255)
            self.m_foreground_button_label.SetForegroundColour(fg)

        self.m_background_textbox.SetValue(self.color_obj["settings"]["background"])
        if self.color_obj["settings"]["background"] == "":
            cl = RGBA("#FFFFFF")
            bg = wx.Colour(cl.r, cl.g, cl.b)
            self.m_background_picker.SetBackgroundColour(bg)
            if cl.luminance() > 128:
                fg = wx.Colour(0, 0, 0)
            else:
                fg = wx.Colour(255, 255, 255)
            self.m_background_button_label.SetForegroundColour(fg)

    def on_foreground_button_click(self, event):
        """Handle foreground button click event."""

        color = None
        data = wx.ColourData()
        data.SetChooseFull(True)

        alpha = None

        text = self.m_foreground_textbox.GetValue()
        if text == "":
            rgb = RGBA("#FFFFFF")
        else:
            rgb = RGBA(text)
            if len(text) == 9:
                alpha == text[7:9]

        # set the default color in the chooser
        data.SetColour(wx.Colour(rgb.r, rgb.g, rgb.b))

        # construct the chooser
        dlg = wx.ColourDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            # set the panel background color
            color = dlg.GetColourData().GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
            self.m_foreground_textbox.SetValue(color if alpha is None else color + alpha)
        dlg.Destroy()
        event.Skip()

    def on_background_button_click(self, event):
        """Handle background button click event."""

        color = None
        data = wx.ColourData()
        data.SetChooseFull(True)

        alpha = None

        text = self.m_background_textbox.GetValue()
        if text == "":
            rgb = RGBA("#FFFFFF")
        else:
            rgb = RGBA(text)
            if len(text) == 9:
                alpha == text[7:9]

        # set the default color in the chooser
        data.SetColour(wx.Colour(rgb.r, rgb.g, rgb.b))

        # construct the chooser
        dlg = wx.ColourDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            # set the panel background color
            color = dlg.GetColourData().GetColour().GetAsString(wx.C2S_HTML_SYNTAX)
            self.m_background_textbox.SetValue(color if alpha is None else color + alpha)
        dlg.Destroy()
        event.Skip()

    def on_background_change(self, event):
        """On background change event."""

        text = self.m_background_textbox.GetValue()
        try:
            if text == "":
                cl = RGBA("#FFFFFF")
            else:
                cl = RGBA(text)
        except:
            event.Skip()
            return

        cl.apply_alpha(BG_COLOR.get_rgb())
        bg = wx.Colour(cl.r, cl.g, cl.b)
        self.m_background_picker.SetBackgroundColour(bg)
        if cl.luminance() > 128:
            fg = wx.Colour(0, 0, 0)
        else:
            fg = wx.Colour(255, 255, 255)
        self.m_background_button_label.SetForegroundColour(fg)
        self.m_background_picker.Refresh()

    def on_foreground_change(self, event):
        """Handle foreground change event."""

        text = self.m_foreground_textbox.GetValue()
        try:
            if text == "":
                cl = RGBA("#FFFFFF")
            else:
                cl = RGBA(text)
        except:
            event.Skip()
            return

        cl.apply_alpha(BG_COLOR.get_rgb())
        bg = wx.Colour(cl.r, cl.g, cl.b)
        self.m_foreground_picker.SetBackgroundColour(bg)
        if cl.luminance() > 128:
            fg = wx.Colour(0, 0, 0)
        else:
            fg = wx.Colour(255, 255, 255)
        self.m_foreground_button_label.SetForegroundColour(fg)
        self.m_foreground_picker.Refresh()

    def on_foreground_focus(self, event):
        """Handle foreground focus event."""
        self.foreground_save = self.m_foreground_textbox.GetValue()
        event.Skip()

    def on_background_focus(self, event):
        """Handle background focus event."""
        self.background_save = self.m_background_textbox.GetValue()
        event.Skip()

    def on_foreground_blur(self, event):
        """Handle foreground blur event."""
        text = self.m_foreground_textbox.GetValue()
        if text != "":
            try:
                RGBA(text)
            except:
                self.m_foreground_textbox.SetValue(self.foreground_save)
        event.Skip()

    def on_background_blur(self, event):
        """Handle background blur event."""
        text = self.m_background_textbox.GetValue()
        if text != "":
            try:
                RGBA(text)
            except:
                self.m_background_textbox.SetValue(self.background_save)
        event.Skip()

    def on_apply_button_click(self, event):
        """Handle appply button click event."""

        self.apply_settings = True
        self.Close()

    def on_set_color_close(self, event):
        """Handle set color close event."""

        fontstyle = []
        if self.m_bold_checkbox.GetValue():
            fontstyle.append("bold")
        if self.m_italic_checkbox.GetValue():
            fontstyle.append("italic")
        if self.m_underline_checkbox.GetValue():
            fontstyle.append("underline")

        if self.apply_settings:
            self.color_obj = {
                "name": self.m_name_textbox.GetValue(),
                "scope": self.m_scope_textbox.GetValue(),
                "settings": {
                    "foreground": self.m_foreground_textbox.GetValue(),
                    "background": self.m_background_textbox.GetValue(),
                    "fontStyle": " ".join(fontstyle)
                }
            }

            if self.insert:
                grid = self.Parent.m_style_settings.m_plist_grid
                num = grid.GetNumberRows()
                row = grid.GetGridCursorRow()
                if num > 0:
                    grid.InsertRows(row, 1, True)
                else:
                    grid.AppendRows(1)
                    row = 0
                grid.GetParent().update_row(row, self.color_obj)
                grid.GetParent().go_cell(grid, row, 0)
                self.Parent.update_plist(JSON_ADD, {"table": "style", "index": row, "data": self.color_obj})
            else:
                self.Parent.set_style_object(self.color_obj)
        event.Skip()


#################################################
# Editor Dialog
#################################################
class Editor(editor.EditorFrame, DebugFrameExtender):

    """Main editor."""

    def __init__(self, parent, scheme, j_file, t_file, live_save, debugging=False):
        """Initialize."""

        super(Editor, self).__init__(parent)
        self.live_save = bool(live_save)
        self.updates_made = False
        mod = wx.ACCEL_CMD if sys.platform == "darwin" else wx.ACCEL_CTRL
        self.set_keybindings(
            [
                (mod, ord('B'), self.on_shortcuts),
                (mod | wx.ACCEL_SHIFT, ord('S'), self.on_save_as),
                (mod, ord('S'), self.on_save),
                (mod, ord('F'), self.focus_find),
                (mod, ord('G'), self.on_next_find),
                (mod | wx.ACCEL_SHIFT, ord('G'), self.on_prev_find)
            ],
            self.on_debug_console if debugging else None
        )
        if debugging:
            self.open_debug_console()
        self.SetTitle("Color Scheme Editor - %s" % os.path.basename(t_file))
        self.search_results = []
        self.cur_search = None
        self.last_UUID = None
        self.last_plist_name = None
        self.scheme = scheme
        self.json = j_file
        self.tmtheme = t_file
        debug_struct(scheme, "Color Scheme")

        try:
            self.m_global_settings = GlobalSettings(
                self.m_plist_notebook, scheme,
                self.update_plist, self.rebuild_tables
            )
            self.m_style_settings = StyleSettings(
                self.m_plist_notebook, scheme,
                self.update_plist
            )
        except Exception as e:
            debug("Failed to load scheme settings!")
            debug(e)
            raise

        self.m_plist_name_textbox.SetValue(scheme["name"])
        self.m_plist_uuid_textbox.SetValue(scheme["uuid"])
        self.last_UUID = scheme["uuid"]
        self.last_plist_name = scheme["name"]

        self.m_menuitem_save.Enable(False)

        self.m_plist_notebook.InsertPage(0, self.m_global_settings, "Global Settings", True)
        self.m_plist_notebook.InsertPage(1, self.m_style_settings, "Scope Settings", False)
        self.queue = []
        if self.live_save:
            self.update_thread = LiveUpdate(self.save, self.queue)
            self.update_thread.start()

    def update_plist(self, code, args={}):
        """Update plist."""

        if code == JSON_UUID:
            self.scheme["uuid"] = self.m_plist_uuid_textbox.GetValue()
            self.updates_made = True
        elif code == JSON_NAME:
            self.scheme["name"] = self.m_plist_name_textbox.GetValue()
            self.updates_made = True
        elif code == JSON_ADD and args is not None:
            debug("JSON add")
            if args["table"] == "style":
                self.scheme["settings"].insert(args["index"] + 1, args["data"])
            else:
                self.scheme["settings"][0]["settings"][args["index"]] = args["data"]
            self.updates_made = True
        elif code == JSON_DELETE and args is not None:
            debug("JSON delete")
            if args["table"] == "style":
                del self.scheme["settings"][args["index"] + 1]
            else:
                del self.scheme["settings"][0]["settings"][args["index"]]
            self.updates_made = True
        elif code == JSON_MOVE and args is not None:
            debug("JSON move")
            from_row = args["from"] + 1
            to_row = args["to"] + 1
            item = self.scheme["settings"][from_row]
            del self.scheme["settings"][from_row]
            self.scheme["settings"].insert(to_row, item)
            self.updates_made = True
        elif code == JSON_MODIFY and args is not None:
            debug("JSON modify")
            if args["table"] == "style":
                obj = {
                    "name": args["data"]["name"],
                    "scope": args["data"]["scope"],
                    "settings": {
                    }
                }

                settings = args["data"]["settings"]

                if settings["foreground"] != "":
                    obj["settings"]["foreground"] = settings["foreground"]

                if settings["background"] != "":
                    obj["settings"]["background"] = settings["background"]

                if settings["fontStyle"] != "":
                    obj["settings"]["fontStyle"] = settings["fontStyle"]

                self.scheme["settings"][args["index"] + 1] = obj
            else:
                self.scheme["settings"][0]["settings"][args["index"]] = args["data"]
            self.updates_made = True
        else:
            debug("No valid edit actions!")

        if self.live_save:
            while not self.update_thread.lock_queue():
                time.sleep(.2)
            self.queue.append("tmtheme")
            self.update_thread.release_queue()
        elif self.updates_made:
            self.m_menuitem_save.Enable(True)

    def rebuild_plist(self):
        """Rebuild plist."""

        self.scheme["name"] = self.m_plist_name_textbox.GetValue()
        self.scheme["uuid"] = self.m_plist_uuid_textbox.GetValue()
        self.scheme["settings"] = [{"settings": {}}]
        for r in range(0, self.m_global_settings.m_plist_grid.GetNumberRows()):
            key = self.m_global_settings.m_plist_grid.GetCellValue(r, 0)
            val = self.m_global_settings.m_plist_grid.GetCellValue(r, 1)
            self.scheme["settings"][0]["settings"][key] = val

        for r in range(0, self.m_style_settings.m_plist_grid.GetNumberRows()):
            name = self.m_style_settings.m_plist_grid.GetCellValue(r, 0)
            foreground = self.m_style_settings.m_plist_grid.GetCellValue(r, 1)
            background = self.m_style_settings.m_plist_grid.GetCellValue(r, 2)
            fontstyle = self.m_style_settings.m_plist_grid.GetCellValue(r, 3)
            scope = self.m_style_settings.m_plist_grid.GetCellValue(r, 4)

            obj = {
                "name": name,
                "scope": scope,
                "settings": {
                }
            }

            if foreground != "":
                obj["settings"]["foreground"] = foreground

            if background != "":
                obj["settings"]["background"] = background

            if fontstyle != "":
                obj["settings"]["fontStyle"] = fontstyle

            self.scheme["settings"].append(obj)

        if self.live_save:
            while not self.update_thread.lock_queue():
                time.sleep(.2)
            self.queue.append("tmtheme")
            self.update_thread.release_queue()

    def save(self, request, requester="Main Thread"):
        """Save."""

        debug("%s requested save - %s" % (requester, request))
        if request == "tmtheme" or request == "all":
            try:
                with codecs.open(self.tmtheme, "w", "utf-8") as f:
                    f.write((plistlib.writePlistToString(self.scheme) + '\n').decode('utf8'))
            except:
                errormsg('Unexpected problem trying to write .tmTheme file!')

        if request == "json" or request == "all":
            try:
                with codecs.open(self.json, "w", "utf-8") as f:
                    f.write(
                        (
                            json.dumps(
                                self.scheme,
                                sort_keys=True, indent=4, separators=(',', ': ')
                            ) + '\n'
                        ).decode('raw_unicode_escape')
                    )
                self.updates_made = False
                if not self.live_save:
                    self.m_menuitem_save.Enable(False)
            except:
                errormsg('Unexpected problem trying to write .tmTheme.JSON file!')

    def rebuild_tables(self, cur_row, cur_col):
        """Rebuild the tables."""

        cur_page = self.m_plist_notebook.GetSelection()

        self.m_global_settings.m_plist_grid.DeleteRows(0, self.m_global_settings.m_plist_grid.GetNumberRows())
        self.m_global_settings.read_plist(self.scheme)
        self.m_global_settings.go_cell(self.m_global_settings.m_plist_grid, 0, 0)

        self.m_style_settings.m_plist_grid.DeleteRows(0, self.m_style_settings.m_plist_grid.GetNumberRows())
        self.m_style_settings.read_plist(self.scheme)
        self.m_style_settings.go_cell(self.m_style_settings.m_plist_grid, 0, 0)

        if cur_page == 0:
            self.m_plist_notebook.ChangeSelection(cur_page)
            if cur_row is not None and cur_col is not None:
                self.m_global_settings.go_cell(self.m_global_settings.m_plist_grid, cur_row, cur_col, True)
        elif cur_page == 1:
            self.m_plist_notebook.ChangeSelection(cur_page)
            if cur_row is not None and cur_col is not None:
                self.m_style_settings.go_cell(self.m_style_settings.m_plist_grid, cur_row, cur_col, True)

    def set_style_object(self, obj):
        """Set style object."""

        self.m_style_settings.set_object(obj)

    def set_global_object(self, key, value):
        """Set global object."""

        self.m_global_settings.set_object(key, value)

    def focus_find(self, event):
        """Set focus on search panel."""

        self.m_search_panel.SetFocus()
        event.Skip()

    def find(self):
        """Find."""

        self.search_results = []
        pattern = self.m_search_panel.GetValue().lower()
        panel = self.m_style_settings if self.m_plist_notebook.GetSelection() else self.m_global_settings
        self.cur_search = panel
        grid = panel.m_plist_grid
        for r in range(0, grid.GetNumberRows()):
            for c in range(0, grid.GetNumberCols()):
                if pattern in grid.GetCellValue(r, c).lower():
                    self.search_results.append((r, c))

    def find_next(self, current=False):
        """Find next."""

        panel = self.m_style_settings if self.m_plist_notebook.GetSelection() else self.m_global_settings
        if self.cur_search is not panel:
            debug("Find: Panel switched.  Upate results.")
            self.find()
        grid = panel.m_plist_grid
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        next = None
        for i in self.search_results:
            if current and row == i[0] and col == i[1]:
                next = i
                break
            elif row == i[0] and col < i[1]:
                next = i
                break
            elif row < i[0]:
                next = i
                break
        if next is None and len(self.search_results):
            next = self.search_results[0]
        if next is not None:
            grid.SetFocus()
            panel.go_cell(grid, next[0], next[1], True)

    def find_prev(self, current=False):
        """Find previous."""

        panel = self.m_style_settings if self.m_plist_notebook.GetSelection() else self.m_global_settings
        if self.cur_search is not panel:
            debug("Find: Panel switched.  Upate results.")
            self.find()
        grid = panel.m_plist_grid
        row = grid.GetGridCursorRow()
        col = grid.GetGridCursorCol()
        prev = None
        for i in reversed(self.search_results):
            if current and row == i[0] and col == i[1]:
                prev = i
                break
            elif row == i[0] and col > i[1]:
                prev = i
                break
            elif row > i[0]:
                prev = i
                break
        if prev is None and len(self.search_results):
            prev = self.search_results[-1]
        if prev is not None:
            grid.SetFocus()
            panel.go_cell(grid, prev[0], prev[1], True)

    def file_close_cleanup(self):
        """File close cleanup."""

        if self.live_save:
            self.update_thread.kill_thread()
            if self.live_save:
                while not self.update_thread.is_done():
                    time.sleep(0.5)
        if self.live_save and self.updates_made:
            self.save("json")
        elif not self.live_save and self.updates_made:
            if yesno("You have unsaved changes.  Save?", "Color Scheme Editor"):
                self.save("all")

    def on_plist_name_blur(self, event):
        """Handle plist name blur event."""

        set_name = self.m_plist_name_textbox.GetValue()
        if set_name != self.last_plist_name:
            self.last_plist_name = set_name
            self.update_plist(JSON_NAME)
        event.Skip()

    def on_uuid_button_click(self, event):
        """Handle UUID button event."""

        self.last_UUID = str(uuid.uuid4()).upper()
        self.m_plist_uuid_textbox.SetValue(self.last_UUID)
        self.update_plist(JSON_UUID)
        event.Skip()

    def on_uuid_blur(self, event):
        """Handle UUID blur event."""

        try:
            set_uuid = self.m_plist_uuid_textbox.GetValue()
            uuid.UUID(set_uuid)
            if set_uuid != self.last_UUID:
                self.last_UUID = set_uuid
                self.update_plist(JSON_UUID)
        except:
            self.on_uuid_button_click(event)
            errormsg('UUID is invalid! A new UUID has been generated.')
            debug("Bad UUID: %s!" % self.m_plist_uuid_textbox.GetValue())
        event.Skip()

    def on_plist_notebook_size(self, event):
        """Handle plist notebook size event."""

        self.m_global_settings.resize_table()
        self.m_style_settings.resize_table()
        event.Skip()

    def on_open_new(self, event):
        """Handle open new event."""

        self.file_close_cleanup()
        save_file = query_user_for_file(self, action="select")
        if save_file is not None:
            j_file, t_file, color_scheme = parse_file(save_file)
            if j_file is not None and t_file is not None:
                self.json = j_file
                self.tmtheme = t_file
                self.SetTitle("Color Scheme Editor - %s" % os.path.basename(t_file))
                self.scheme = color_scheme
                self.m_plist_name_textbox.SetValue(self.scheme["name"])
                self.m_plist_uuid_textbox.SetValue(self.scheme["uuid"])
                self.last_UUID = self.scheme["uuid"]
                self.last_plist_name = self.scheme["name"]
                self.rebuild_tables(None, None)

    def on_save(self, event):
        """Handle save event."""

        if not self.live_save:
            self.save("all")

    def on_save_as(self, event):
        """Handle save as event."""

        save_file = query_user_for_file(self, action="new")
        if save_file is not None:
            j_file = None
            t_file = None
            is_json = save_file.lower().endswith("tmtheme.json")
            if is_json:
                j_file = save_file
                t_file = save_file[:-5]
            else:
                j_file = save_file + ".JSON"
                t_file = save_file
            self.json = j_file
            self.tmtheme = t_file
            self.SetTitle("Color Scheme Editor - %s" % os.path.basename(t_file))
            if self.live_save:
                while not self.update_thread.lock_queue():
                    time.sleep(.2)
                del self.queue[0:len(self.queue)]
                self.update_thread.release_queue()
            self.save("all")

    def on_about(self, event):
        """Handle about event."""

        infomsg(
            "Color Scheme Editor: version %s" % __version__,
            bitmap=messages.MessageIcon(AppIcon.GetBitmap(), 64, 64)
        )
        event.Skip()

    def on_find(self, event):
        """Handle find event."""

        self.find()
        event.Skip()

    def on_find_finish(self, event):
        """Handle find finish event."""

        self.find_next(current=True)

    def on_next_find(self, event):
        """Handle next find event."""

        self.find_next()

    def on_prev_find(self, event):
        """Handle previous find event."""

        self.find_prev()

    def on_shortcuts(self, event):
        """Handle shortcuts event."""

        if sys.platform == "darwin":
            msg = SHORTCUTS["osx"]
        elif sys.platform == "linux2":
            msg = SHORTCUTS["linux"]
        else:
            msg = SHORTCUTS["windows"]
        infomsg(msg, "Shortcuts")

    def on_debug_console(self, event):
        """Handle debug console event."""

        self.open_debug_console()

    def on_close(self, event):
        """Handle close event."""

        self.close_debug_console()
        self.file_close_cleanup()
        event.Skip()


#################################################
# Basic Dialogs
#################################################
def filepicker(msg, wildcard, save=False):
    """Call file picker."""

    return messages.filepickermsg(msg, wildcard, save)


def yesno(question, title='Yes or no?', bitmap=None, yes="Okay", no="Cancel"):
    """Prompt for yes/no."""

    return messages.promptmsg(question, title, bitmap, yes, no)


def infomsg(msg, title="INFO", bitmap=None):
    """Info message."""

    messages.infomsg(msg, title, bitmap)


def errormsg(msg, title="ERROR", bitmap=None):
    """Error message."""

    error(msg)
    messages.errormsg(msg, title, bitmap)


def warnmsg(msg, title="WARNING", bitmap=None):
    """Warning message."""

    messages.warnmsg(msg, title, bitmap)


#################################################
# Helper Functions
#################################################
def query_user_for_file(parent, action):
    """Query the user for file to use."""

    file_path = None
    select_file = action == "select"
    new_file = action == "new"
    select = False
    done = False
    if sys.platform == "darwin":
        wildcard = "(*.tmTheme;*.tmTheme.JSON)|*.tmTheme;*.JSON"
    else:
        wildcard = "(*.tmTheme;*.tmTheme.JSON)|*.tmTheme;*.tmTheme.JSON"
    if not select_file and not new_file:
        select = yesno("Create a new theme or select an existing one?", "Color Scheme Editor", yes="Select", no="New")
    elif select_file:
        select = True
    while not done:
        if select:
            result = filepicker("Choose a theme file:", wildcard)
            if result is not None:
                debug(result)
                if not result.lower().endswith(".tmtheme.json") and not result.lower().endswith(".tmtheme"):
                    errormsg("File must be of type '.tmtheme' or '.tmtheme.json'")
                    debug("Select: Bad extension: %s" % result)
                    continue
                file_path = result
                debug("Select: File selected: %s" % file_path)
            done = True
        else:
            result = filepicker("Theme file to save:", wildcard, True)
            if result is not None:
                if not result.lower().endswith(".tmtheme.json") and not result.lower().endswith(".tmtheme"):
                    errormsg("File must be of type '.tmtheme' or '.tmtheme.json'")
                    debug("New: Bad extension: %s" % result)
                    continue
                if result.lower().endswith("tmtheme.json"):
                    with codecs.open(result, "w", "utf-8") as f:
                        f.write(
                            (
                                json.dumps(
                                    default_new_theme,
                                    sort_keys=True, indent=4, separators=(',', ': ')
                                ) + '\n'
                            ).decode('raw_unicode_escape')
                        )
                else:
                    with codecs.open(result, "w", "utf-8") as f:
                        f.write((plistlib.writePlistToString(default_new_theme) + '\n').decode('utf8'))
                file_path = result
                debug("New: File selected: %s" % file_path)
            done = True
    return file_path


def parse_file(file_path):
    """Parse the scheme file."""

    j_file = None
    t_file = None
    color_scheme = None
    is_json = file_path.lower().endswith("tmtheme.json")

    try:
        with open(file_path, "r") as f:
            color_scheme = json.loads(sanitize_json(f.read(), True)) if is_json else plistlib.readPlist(f)
    except:
        errormsg('Unexpected problem trying to parse file!')

    if color_scheme is not None:
        if is_json:
            j_file = file_path
            t_file = file_path[:-5]

            if not os.path.exists(t_file):
                try:
                    with codecs.open(t_file, "w", "utf-8") as f:
                        f.write((plistlib.writePlistToString(color_scheme) + '\n').decode('utf8'))
                except:
                    debug("tmTheme file write error!")
        else:
            j_file = file_path + ".JSON"
            t_file = file_path

            if not os.path.exists(j_file):
                try:
                    with codecs.open(j_file, "w", "utf-8") as f:
                        f.write(
                            (
                                json.dumps(
                                    color_scheme,
                                    sort_keys=True, indent=4, separators=(',', ': ')
                                ) + '\n'
                            ).decode('raw_unicode_escape')
                        )
                except:
                    debug("JSON file write error!")

    return j_file, t_file, color_scheme


def parse_arguments(script):
    """Parse the command arguments."""

    parser = argparse.ArgumentParser(
        prog='subclrschm',
        description='Sublime Color Scheme Editor - Edit Sublime Color Scheme'
    )
    # Flag arguments
    parser.add_argument('--version', action='version', version=('%(prog)s ' + __version__))
    parser.add_argument('--debug', '-d', action='store_true', default=False, help=argparse.SUPPRESS)
    parser.add_argument('--log', '-l', nargs='?', default=script, help="Absolute path to directory to store log file")
    parser.add_argument('--live_save', '-L', action='store_true', default=False, help="Enable live save.")
    # Mutually exclusinve flags
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--select', '-s', action='store_true', default=False, help="Prompt for theme selection")
    group.add_argument('--new', '-n', action='store_true', default=False, help="Open prompting for new theme to create")
    # Positional
    parser.add_argument('file', nargs='?', default=None, help='Theme file')
    return parser.parse_args()


#################################################
# Main
#################################################
def main(script):
    """Main."""

    cs = None
    j_file = None
    t_file = None
    args = parse_arguments(script)

    if os.path.exists(args.log):
        args.log = os.path.join(os.path.normpath(args.log), 'subclrschm.log')

    init_app_log(args.log)
    if args.debug:
        set_debug_mode(True)
    debug('Starting ColorSchemeEditor')
    debug('Arguments = %s' % str(args))

    app = CustomApp(redirect=args.debug)  # , single_instance_name="subclrschm")
    if args.file is None:
        action = ""
        if args.select:
            action = "select"
        elif args.new:
            action = "new"
        args.file = query_user_for_file(None, action)

    if args.file is not None:
        j_file, t_file, cs = parse_file(args.file)

    if j_file is not None and t_file is not None:
        main_win = Editor(
            None, cs, j_file, t_file,
            live_save=args.live_save, debugging=args.debug
        )
        main_win.Show()
        app.MainLoop()
    return 0


def cli():
    """Handle command line interface."""

    if sys.platform == "darwin" and len(sys.argv) > 1 and sys.argv[1].startswith("-psn"):
        script_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "..", "..", "..")
        del sys.argv[1]
    else:
        script_path = os.path.dirname(os.path.abspath(sys.argv[0]))

    sys.exit(main(script_path))
