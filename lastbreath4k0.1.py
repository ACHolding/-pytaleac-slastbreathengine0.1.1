#!/usr/bin/env python3
# last breath 4k 0.1 — files = off • Megalovania OST • python 3.14 • 60 fps

from __future__ import annotations

import array
import base64
import io
import math
import random
import struct
import sys
from typing import List

import pygame

FILES_OFF = True
MUTE = False
FPS = 60
WIDTH, HEIGHT = 640, 480

# Last Breath Phase 1 HUD layout — procedural, files = off
LB_BOX = pygame.Rect(170, 238, 300, 162)
DLG_BOX = pygame.Rect(32, 368, 576, 96)
STATS_Y = 432
SANS_X, SANS_Y = 320, 108
MENU_OPTS = ("FIGHT", "ACT", "ITEM", "MERCY")
PHASE1_TURNS_TO_CLEAR = 5

# base64 PNG — real Undertale wiki Sans sprites (files = off, RAM embed only)
SANS_ANIMS_B64 = {
    "idle_0": "iVBORw0KGgoAAAANSUhEUgAAAHYAAACXCAYAAADAv682AAAEP0lEQVR4nO2d7Y6cMBAEcbTv/8qOImWlEwoxxjN2u6n6eXcsHN6ixx9AOY6jHmDHr9UHADnQsKZ8jg2pNTc9SinH7mCsKUW5eMo209lkjDVFylg1Q3c2GGNNkTB2N1N3MBdjTVlq7O6mKpuLsaYsMdbNVEVzMdYUGtYUGtaUqRnrnq1KWYuxptCwptCwpnwcsmk0u8vk/c0AY035OFSP3+17TSoP93veTtFgjDXl8/Yx1QieXjEywVhTJDK2xdmEbNPr5P1lgLGm0LCm0LCmSKygGM2wq2q03OxvRu9fIZMx1hSJqljxG/8/lPqrV2CsKVuuK26N9JSG8a3tRo9LAYw1RSJjVWZT6t/P3WH2pgXGmiLRj52ddTUp2+/ufwYYa4p0xj41t056qoxy9mKsKRLGXmXS6iq1NLJS2VyMNWWrseIrg7OPq2zYr8VYU5YY28qmlplXht/9+d3tzuzQf/2CsaZIZOwVZ3NnV6FlcH9ZKzbugLGmpBh795t614hZKyzKw+q3d7sZ1T3GmhI6u/P0G967/d3P62X0bj2lqhljTVlibPa8aRZR/VsyFtYa2ztSNJpBam/xqIOrJTOyl4w1RXJdsdKYa+bxZ/bPMdYU6XcC9H7zs/4+u5+aYS7GmjJkbFZV12tw9ohVHTT17nmKPJ8Ya8ojY1UzLXusujw8/lnb/QRjTemaj529SrBl5ugKiyo0GxN9vjH2zcauMrXF1fGUm8d5NlxlZf/5OJ6cf4w1RXqVYi8qmVmDjB+5gmDsG41VydYoA2ojS0f3k53NPe2BsaZMzdin1eesu91KUD9YobrG2DcZq5QV//r7q/7nU8rgLE92DfLkCoCxpkzN2FUr9ltk32uzoneBsaakGhv9Tc0a0y1JVffK6hhj32RsxOxCBqv3vxMY+8aMVTU3uyouwf3kUZjdgb6qeLW52SsdisDYbvQdAmSsKV392Ctzz7/fnbo4WyPOK8aa8nHKpCjDyqIx7cgrIMaaMjRWvOrJauprlWrn+fjCHe2w5o726KfEqHxu1uwRT40BrWdQZM2bqlIF+vdUxaZIPDUG4sFYU6zutlPJyiowj4uxpiy9d+f8892qX2Uw1pQpxipkzkwU1kxhrClLq+LsbK0vu1L8BGNNsezH1ovVjG8yF2NNoWE7+GO+2jqvK2hYUywzVoWVGY+xpnzeMDZcXlgdY6wpVhm7S8U6A4w1xcrYrHt46oZXAow1hYY1hYY1hYY1hYY1ZeqaJxfqzRG1lWCsKRL37sy+G68mv1NAAYw1RcJYiAdjTaFhN1/bdAUNa0pKPzb63eoqzzSMfvd75v+FsaaEVsVPc6k176n+3tcSNALFk9lgTsZGPctwtxULJfh4I1dRkrGmSK55WlUFF7FnMI6AsaZIGdvK2iyTa1B/dRSqYmjC7I4pZKwpNKwpNKwpNKwpNKwpNKwpNOzhyW9reo9IcWVORgAAAABJRU5ErkJggg==",
    "idle_1": "iVBORw0KGgoAAAANSUhEUgAAAHYAAACXCAYAAADAv682AAAEWUlEQVR4nO2d227jMAxEzcL//8tcFNgAC7daWRYpDcdzHtumTkwfj66OHcfhh6Dja/cbEDmcR0Hcc28yZnZUR8aSYsgZm20ms8kylhQoY9EMrWywjCUFwthqplYwV8aSstXY6qYimytjSdliLJupiObKWFJUWFJUWFKWZix7tiJlrYwlRYUlRYUl5WTIptnstsXHW4GMJeVkaD1+Xj9qkj087vV1iAbLWFLOt4+pRvD0jpGJjCUFImN7XE3INt0XHy8DGUuKCkuKCksKxAqK2QxrtUbtZn8z+vgImSxjSYFoFSNe8f8Dqb/aQsaSUnJdcW+kxzrG9143+74QkLGkQGQsymyK//2/FWZveshYUiD6sauzzpOy/e7xVyBjSYHO2Kfm+qKnyiBnr4wlBcLYVibtbqVaJyuRzZWxpJQaK24ZnP2+rGC/VsaSssXYXjb1zGwZfvfnd193pUL/9YOMJQUiY1tczV3dCjXgVm/pwlbHk5bilNkJ0DNi1QoLe9j6RcrW1MLuvFIR8JsXaub5SJndiV7Z0CPqBHnQbj0E00+2K3UnDtQdgmo8Pc04lLFjJLYUls1cHzR1xeeHMjY6w57CcMGFFHZ0CLD1c4YTeufzXLt5GZ8b2tgWbBfAaxaMVymcT77/zDuWJgFIgf6yh9ErP+vvs/upGebKWFKmjM1q1Y0anD0U6ZOm3j1PkedTxpLyyFjUTJsdfPfgDJ393DPmylhSzgpjvC0zZ5fOONBsTPT5lrFvNhZ1NqY3FtujNWa7e/Ha9X08Of8ylpSSkwDomelBxs/cQWTsG41FydYoA7yTpbPHyc7mkXrIWFKWZuzT1ueqbYwW1A9GaF3L2DcZi5QVv/199Johm5zlyW6DPLkDyFhSlmbsrq0Yu3cw7OhdyFhSUo2NvlKzxnQtqdW9s3UsY99kbMTsQga7j18JGfvGjEU1N7tVbAv21oyg2R0x1irebW72SgcDGNuN3iGgjCVlqB/bMvf6++r45myNOK8ylpSTKZOiDLNNY9qRd0AZS8pZ8ZF56GuVfPB8fNCOdoH1yL0fBw/efZf9f7NmjzJa38pYUpY8gyJr3hQVB+jfy1hSIJ4aI+KRsaRQ7bZDyUoHmMeVsaRs3btz/Xm11i8yMpaUJcYiZM5KENZMyVhStraKs7PVX3an+BcZSwplP9YbqxnfZK6MJUWFHeDbfLR1Xi1UWFIoMxaFnRkvY0k53zA2bC9sHctYUqgytkqLdQUylhQqY7P28HjBO4GMJUWFJUWFJUWFJUWFJWXpmicW/OaI2k5kLCkQe3dW78bz5O8UQEDGkgJhrIhHxpKiwhZf29RChSUlpR8b/d3qKM80jP7u98zPJWNJCW0VP82l3rwn+ve+WtAIlJ7MJtZkbNSzDKutWLDg9xu5ilIZSwrkmqddrWADewbjDDKWFChje1mbZbIH9VdnUatYdNHsDinKWFJUWFJUWFJUWFJUWFJUWFJU2IOTP3GWmWJNXv0LAAAAAElFTkSuQmCC",
    "clenched": "iVBORw0KGgoAAAANSUhEUgAAAIAAAACMAQMAAACOMjPzAAAABlBMVEUAAAD///+l2Z/dAAABjElEQVRIx7XWsWolMQyF4R/UGvQqhm0H9OqCaQP3VQxuBWeLyWaTnRlPIOwpv8IuZIsDALg0+Jx/wSQpVxCSVCuQJGkBdkDegx8wfgJxQP0IBhK+AoiCBWwHbCsYUf4zcKiAsYBBBb4A0xz++jKXE/jwsQKfGq7XWMCQpH0F5lKxgtnBfAFWsdWMXIB8q6F9EOMMXnhqbLXLC9UZQsQIQVSkSWeQ0ur4QGpcA13p0qDM/ApGpg0AG7arzhDakyIbkYxrcPBUIXKjnaGzkVYxIo1+DY0091kYnX6GRiOtwRtGLiDyDQfyDAakVcwi7mGqxXyzCcYZSCj2mC0M2hV0SF4xKy3pV9AwmDFbUpZXYBmwx2zJq7gCYsIr5oT3V3cCDH7F/PUI2wNgHbuHQUgDv4c6Vpu4A973s9/DN2PZ7qGPJ8gD7B72xB6h5TdgPMPHGE5gDq0/wfYIvfO/QdA7FbcAUvqXJnCC76UtwIcAV9YdhAII+Z+LTyC9gKiPKnAB+V467mEmaOrvoZ/gN90MbCk6zT9iAAAAAElFTkSuQmCC",
    "fatal": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSAQMAAACaML3nAAAABlBMVEUAAAD///+l2Z/dAAABc0lEQVRIx+3UMYokMQyF4R+UGnQVH6BAV9ujCTotqKsIKjW8Cbp7mBnbE2y0wSr7AhsjSw/+179SIeWWLklbSpJqQ5MkjQ1d+nrXD8aT+Td86vMdP1mmwZagwjccoMI2LFDBlqnqe/529sBqYLlmpNUgNnRdGfGlz985IuOxY0gZ0pUrxqvtV62owyQNu1gyTsDi7AuaXTXu+1RvC4KP474fwpc05X37Z3u+sYEGqIwF+3u8G31mWj5Xo3FMtNcUdBq+ouOyzoFNbJgluoqB5YJXEVf3c8EDK8fOPhqsiEEUvmTDCjq2oNMwB1/SsmFHYmXYRKrBOeAwnInR4FRhD46Z3uCkgaiZ5omk7B7MJAqladhY0d75cizoz0128DEzBhzQPEMzMx7l0KLEn5l+D4MW91jRJItqoVoRybo3Vy4Zw7HLlcbETowG9yXWvAuwDZ+hZ6LNbO9I3DFf+dhn2q8k/Z2tuWA/Xj9mLPjOaR8r/lIfZF/vYj3YLbUAAAAASUVORK5CYII=",
    "glow_0": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAAEVklEQVR4nO2dSXLcMAxFxZTWOXGWPnEugFSq3AvLZnHC9NH/LdtWSy3yCSBESu26LrkIDL+iD4CscV8giNheCFprFwI0DIyWLYZZm4RuHg0DI9ywbEZlN46GgRFmGJpZWUyjYWC4G4ZuVrRpNAwMN8OqmRVlGg0Dgw0GBhsMDPMYVj12eccyGgYGGwwMNhgYN+q1Xw5jo/f+tKBhYNyo2VT73H615/f2+yF/f/z8T/v943ZRxtEwMNzHYdrjFDk0rGdWz7TR/jkOI194W8M+BjFr9Pfe/mkY+cLbGvaCMYzUvON8app0zJodL82aliU7fMFxGBhp5nRo1fbapmG7+9v9vl1oGBgw8xJHtcM26OGj7U6PywsaBkaa+2FPvKrj8vm9WarxI2gYGOmyRKtYIkaxc3b/WtAwMNLFsF3TxOkpA9GxjYaBkW5OR3TW1gaxKNo0GgZGmGGz1e6ecVZEGz6ChoHhZtjo2j8yqWekTH4+u91ov73v84KGgZFuHPY0zTsra0nGWzANho4o3TBN02CzPdhrzkTbzAajnoRzo/Ss7MhkBzxeBKJVrde+EzyiKXUErdUvXmbeKD0rK+Kc9ocnHbsxRJLUFr1xa7BqpsmiWVq/P9ww7RixC0pH2m6w1VJS73OUEzVL7/c8hzO7vzudYT2qNSz8RFKUBpHD4z+9wrD4C0a6hzSv9tRm9P/P7XrsXhl2TaNh1Q2zGk+tGifGJa1Ts2bP0+r5pGFVDcsaM+Sw6Gq10NBqOxoGxp21BtgzSQ6nEGSbVLN6vmlYFcOyVtfboFY3u/3z90VPunkeR+/80zAwYIq/2WOSKBk6Mp6GoRuWJXZp9VgZxKrT/VjHvufx0zAwzGPYbjbmtdynKY3jvLJNGoZqmPe1ePX/teZEaFXtrWN8z1gaBoZ5DIuaUh09Y9kq26Zh726Yds+yqvk1oyzUOlukYaiGzVaLvYnefzZoGHoMy2qadZbYlMd5p7BaXz1LjDbN+s5wS3KneXVGMGNYtXFYz7Tn39GR4Ng1e15pWNVKR9ZrflMyIqrmuXrFomHVa4lRjx7KPhdDFs/HC67ALI75o4u+7VB5NYv191rdDdi94jCGgWG2xtnqvlVWvManNAyMsKcIkD1oGBhsMDDglxtlSR68isc0DAz3xRDPz9HS92hoGBh31RuC3nhN4qFhYLhnidaxS4qbTcPAKDMOk850uGqm0TAw2GAD/puaaeIRGwyMMjEsC9YxlIaBcVetHbai2SINAwM+hkmiDM4DGgYGvGFWiyKymkvDwGCDgcEGA4MNBgYbDAzzOR1VkMkKjjU0DIx0r1SMeoHbLt41ShoGBpcbgUHDwGCDJZ270YMN9q7jMO2XjWZ5SJf2y1BPfxcNe7cs8fQF2FGvytB+gbf1i8Bf0LB3iWFaD+fKfof3ifbx8tX2xUkzpyMqK2zJHio2gjEMjHDDRrHMyjxRGm+dwiyxOKzWg8EYdmHxD+Ghx0ohgGOaAAAAAElFTkSuQmCC",
    "glow_1": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAAEUElEQVR4nO2dW5KcMAxFcYqFZenZmaZSNf0xJC6/9Lrins+ZpqGxD5KFDe26LrkIDL+iD4CscV8giNheCFprFwI0DIyWLYZZm4RuHg0DI9ywbEZlN46GgRFmGJpZWUyjYWC4G4ZuVrRpNAwMN8OqmRVlGg0Dgw0GBhsMDPMYVj12eccyGgYGGwwMNhgYN+q1Xw5jo/f+tKBhYNyo2VT73n615/f2K/K78/k//90uyjgaBob7OEx7nCKHhvXM6pk22j/HYeQHrzVMBjFr9P/e/mkY+cFrDfvAGEZq3nE+NU06Zs2Ol2ZNy5IdfuA4DIw0czq0antt07Dd/e1+3y40DAyYeYmj2mEb9PDRdqfH5QUNAyPN/bAnXtVx+f7eLNX4ETQMjHRZolUsEaPYObt/LWgYGOli2K5p4vSUgejYRsPASDenIzpra4NYFG0aDQMjzLDZanfPOCuiDR9Bw8BwM2x07R+Z1DNSJv8+u91ov73v84KGgZFuHPY0zTsra0nGWzANho4o3TBN02CzPdhrzkTbzAajnoRzo/Ss7MhkBzxeBKJVrde+EzyiKXUEvdUvPmbeKD0rK+Kc9ocnHbsxRJLUFr1xa7BqpsmiWVq/P9ww7RixC0pH2m6w1VJS7+8oJ2qW3u95Dmd2f3c6w3pUa1j4iaQoDSKHx396hWHxF4x0D2le7anN6PPP7XrsXhl2TaNh1Q2zGk+tGifGJa1Ts2bP0+r5pGFVDcsaM+Sw6Gq10NBqOxoGxp21BtgzSQ6nEGSbVLN6vmlYFcOyVtfboFY3u/3z90VPunkeR+/80zAwYIq/2WOSKBk6Mp6GoRuWJXZp9VgZxKrT/VjHvufx0zAwzGPYbjbmtdynKY3jvLJNGoZqmPe1ePXzWnMitKr21jG+ZywNA8M8hkVNqY6esWyVbdOwtxum3bOsan7NKAu1zhZpGKphs9Vib6L3nw0ahh7DsppmnSU25XHeKazWV88So02zvjPcktxpXp0RzBhWbRzWM+35f3QkOHbNnlcaVrXSkfWa35SMiKp5rl6xaFj1WmLUo4eyz8WQxfPxgSswi2P+6KJ/dqi8msX6e63uBuxecRjDwDBb42x13yorXuNTGgZG2FMEyB40DAw2GBjwy42yJA9exWMaBob7Yojn39HS92hoGBh31RuC3nhN4qFhYLhnidaxS4qbTcPAKDMOk850uGqm0TAw2GAD/pqaaeIRGwyMMjEsC9YxlIaBcVetHbai2SINAwM+hkmiDM4DGgYGvGFWiyKymkvDwGCDgcEGA4MNBgYbDAzzOR1VkMkKjjU0DIx0r1SMeoHbLt41ShoGBpcbgUHDwGCDJZ270YMN9tZxmPbLRrM8pEv7Zainv4uGvS1LPH0BdtSrMrRf4G39IvAPNOwtMUzr4VzZ7/A+0T5evtq+OGnmdERlhS3ZQ8VGMIaBEW7YKJZZmSdK461TmCUWh9V6MBjDLiy+ALvRx0qqO5OaAAAAAElFTkSuQmCC",
    "shrug": "iVBORw0KGgoAAAANSUhEUgAAAHgAAACmCAYAAAARUEuNAAAE0UlEQVR4nO2dwZLjIAwFw1b+/5fZ2oMP4xoWA5IQz93nseMMaUuAgPL5fOoHZPmz+wHAFxpYHBpYHBpYHBpYHBpYHBpYnO/uB6j1Zze8lLLtWRTBYHG+WY29/10LjP8/GCxO8R6Ltja2BSb/DgaL4xaDLyN7Zq2a+/Q53mo8BotjbrC3kS0TRz+3vqT/jcHiuMVgbyNG719ups+afxoYLM43Omu+89Sk+32f/n0VN7QHBouzbLCVIav9ZYz9HQwWZ/t88OpI1OgbpNzeFFb3yQoGi2NmsPUv2iu2V6P7njLGjcHipI3BsyNPXsaeOsaNweKkM3h0RGy3sV4jfFZgsDjpDD7d2GwmY7A40wZHmaM2xlyDTcZgcZZjsPcvUcXcXWCwOOmyaLWYuzsWY7A4NLA4NLA46WKw17rgGrx6MUsOgcHipDO4xWq2WYJrr7KMmWOwOOkN3l0RcXr/HoPFMVvZsNu06Fqomqz2qgUGi0MDi0MDi7O8T5ZVDO7VP1vdf7a/av35VHTAO/rBp2WtF4xFw1l7VUbF4qf0ri+TOwpYPVcUZNHiHBODs8ze1MabKkvMvYPB4pjvF20di1t4x8LqFPuffr4VGCzO8THYardZ1fpuDBbnG7W3htV9s2W1pfP9dpuMweIcE4NHT2+JylJr8n4xBosTdm7SrFFW+2KVzjzz6nXZ+r8XGCxOWAz2io33+0ZnrWXx87z3vMRgcb7ZR5qeXh9V8VEms+XR66zeeBgsjnsWvWqYdYXHKqurE6OzbAwWJ8zg2djSMz/LiNHq+cit70UMhrMNvl93sftc4mK0Z8fT7zFrMjFYnHCDvcaos650qIsjVavfE4PFOWY+ePWNUCezd+v9sVZPZx19LgwWZ1sM9p4vtuovl8lYOXqfp/8HDIacBl9kMbkYjUh5x/redcRgcbZn0VYVES1T62LFR7Yaq1GTMVic7QZ7Uxq/7NGzEa3mpa142j/GYHHkDc4aU63eAL03CgaLI2OwlRG1E2tXP8c7dt+fH4PFSWfwbLYaVatVjPrRUdk4BouTzmCr+VvrnQbK4qySd3beeiNgsDjpDN61AqGH91oir9WXGCzOdoOtf7leY8bFKUv3zqYxWJztBluze342GxgsjpzBUVl0cdrRbxZmk16KjMHelRclSSXHaFUqMVgcGYOjqZtj79N6cgwW53UGF+f9q0dZ3amelQ0vJ43B1iv2s9dS1cGd+y5Y4Q85DI7aq7HF6sp9a6Ofnv0wClm0ONvXB194zdtmJWqXIAwWJ43B4AMGi5OmH3wq1WgfbC8wWJx0Bj89SeyUbHk3GCxOGoN3z69GE1XThcHipDG4hXfsreJvDgwWJ73BXtRG9aWayRgsDg1szL83QabaaRpYnNfG4Cx45wAYLM52g7OMPRfRbBqDxdlucDQ1UYYbAQaL8zqDvdYoZX0zYLA4NLA4NLA4NLA4NLA4abLorFmo9widNxgszjFrk6JXH1bnMx+iwGBxjjEY5sBgcWhgkdqrFjSwOGl32RntP2bZM7JH6zm9zlvCYHHCs+jZuNWbd81+7m8xGtFipzvYE4Ot9orMXkFxx/p5R6s+icHipJlNGmVX1lwW97iMBoPFOc7gXiz2Mrsa9XdXIYuGHzCbJA4x+KPNX8mF9Yp/sfvcAAAAAElFTkSuQmCC",
    "point": "iVBORw0KGgoAAAANSUhEUgAAAHgAAACmCAYAAAARUEuNAAAE2klEQVR4nO2dzW7EIAwGl2rf/5WpesihkVD4sY35MnNr1U2yJRMbMKR8Pp/6AVl+dl8A+EIDi0MDi0MDi0MDi0MDi0MDi0MDi0MDi0MDi0MDi/ONPmGt/4e+SynRl/AqMFicbxZj73/XAuPHwGBxitd88GXkqrEtMLkPDBbHPAY/mblq7uz5y0uzdQwWxy2L9jLmOu7ok6C+tP+NweJ8o7LmVUaPeze9TJp/OhgsTvhYdK9Jd2N7/341NvdySgzHYHHCDe41wMvYt/W3MVicZYOtDXoyY/R85WZU62er75Gtv43B4pjF4NU71cqg0ezbG+/xgScwWJxtWbTVyNPubDq7yRgsThqDeznF2CwmY7A46Qx+6reeau4uMFicb7YRrLcYW4NiMQaLsxyDve5AVXOjwWBx0mXRXk+OGrySIssTCIPF+Z4yQrUa64vRfPLs53YZjcHipDG4xe6KiNPH0DFYnPQGZ62Fqslqr1pgsDg0sDg0sDjTe3R4xyDr49fO/rVXP3xXzMZgcaazaK8VAb278mTNWi8Yi4Yz9smyrkywWpG/OrZdjddI9Z7XGmKwOGYVHbvX4ETN3tTDascwWJx0Y9Gza5KiDaqTMZqVDZB7fXD0HRq9u85pa6iIweKki8Etnka4dmW15eFJtdtkDBbH3GCvWDz67oeoHKAm7xdjsDhpY/Bqf7JlfO38fe/nns7bOl4UGCyO+47v3jHxfvzorLUsns97z0sMFsc9Bs+aPDovHFXxUSaz5dHPWT35MFgctzefWd2R1hUeq6yuTozOsjFYnDCDL2Zj8UXWESPr/jExGDQMvn/O6p0Pq1jt2dH7PWZjMzFYnHCDre7MU1Y61MWRqtXvicHipJ1NGqV3dqlMjqSNXofXOxhHrwuDxdkWg71isXV/uUzGytHj9P4fMBhyGnyRxeQSVLFhNUbfghgszvYs2qoiomVqXaz4yFZjNWoyBouz3WBvSuPO7jVv9o1s3vT2jzFYHHmDs8ZU67etto6HweLIGOy1X1e9HXf1PN6x+379GCxOOoNns9WoWq1i1I+OysYxWJx0BlvN31qvjSqLs0re2XnriYDB4qQzeNcKhCe81xJ5rcLEYHG2G5x1t9qoLN07m8ZgcbYbbM3u+dlsYLA4cgZHZdElyT7ZF8wmvRQZg70rL0qSSo7RqlRisDgyBkdTN8fe3npyDBbndQYXI+N2jZmPrgTBYHHSGGy9Yj97LVUd3LnvghX+kMPgqL0aW6yu3Lc2uvfdD6MQg8XZvj74wmveNitRuwRhsDhpDAYfMFicNP3gU6mTsTRqLBuDxUlncO+bxE7JlneDweKkMXj3/Go0UTVdGCxOGoNbeMfeKv7kwGBx0hvsRW1UX6qZjMHi0MDG/D0JMtVO08DivDYGZ8E7B8BgcbYbnGXsuYhm0xgsznaDo6mJMtwIMFic1xnstUYp65MBg8WhgcWhgcWhgcWhgcVJk0VnzUK9R+i8wWBxjlmbFL36sDq/8yEKDBbnGINhDgwWhwYWqb1qQQOLk3aXndH+Y5Y9I59oXafX+5YwWJzwLHo2bj3Nu2Z/728xGtFipzvYE4Ot9orMXkFxx/p6R6s+icHipJlNGmVX1lwW97iMBoPFOc7gp1jsZXY16u+uQhYN/2A2SRxi8EebX1/o9pkjZfL4AAAAAElFTkSuQmCC",
    "dodge_l": "iVBORw0KGgoAAAANSUhEUgAAAHYAAACXCAYAAADAv682AAAEOklEQVR4nO2d246YMAxEccX//3KqSrtShRSFJL5MhjmP7bKwmIOdxIBd19UuQcef6gMQMSiwpNzXYbQWmznM7GJAxpJiqMVTtJnsJstYUmCMRTP0dINlLCnlxp5m6inmylhSyow93VR0c2UsKenGspmKaq6MJUWBJUWBJSUtx7LnVrRcK2NJUWBJUWBJuU/PTbu525L3l4WMJeU+vXr83X7WJFvc73M7VINlLCn3V8d5XqzeMaKRsaSU59gRTxOiTW/J+4tCxpKiwJKiwJJS3kGxm8N61ai9HG967x8lJ8tYUsqrYtQrvgfaeLWHjCXluL7i0UzPyPg22G73uFCQsaSU51iU1ZT283tPWb0ZIWNJKR/HZue6FpTb3+4/CxlLCmyOXTU3660yDTz3ylhSyo3t5aTqKtUGuRLdXBlLyjFzxT2Do4/LDh3XylhS0o0d5aaRmT3D3/772+2enDJ+/UXGklKeY3s8zc2uQm1zf1EdG2+RsaS4G/v2Sn1rRFaHhS1Wv7PbZVX3MpYUt9Wd1St8dvu3v2+W3af10KpmGUtKurHR66ZRmNP4VjlW1Bo7O1O0m4PQvuLRNrslo3KvciwpcH3FaHOuUccfPT6XsaTAfhNg9sqP+vnocWqUuTKWlGVjo6q6WYOjZ6zapqlvz5P3+ZSxpEwbi5rToueqbfH4s7Z7ImO/vh6b3SU4MnO3w6KBrcZ4n28Z+1Vjq0wd0Tuet8dpD8NROvufx7F6/mUsKbBdirOg5MzmZPzuHUTGfs1YlNzqZUAb5NLd/UTn5tl4yFhS0nLsavWZ9bSbOY2DUaprGfsVY9FyxWiGyesrIKgdH6t3ABlLSlqOrerYHxH9rE3V6ELGkhJmrPeVGjWna0FVd3V1LGO/YqzX6oI31fs/DRn7tRyLam50VWzO4+RdtLoj5qrianOjOx0MZG7X+wkB5divj2N75j7//3RacW71Oq8ylpSbJSd5GWZFc9red0AZS8ryXHHVm9XQe5Xa5Pn4RU+0i5on2r3fEoPye6NWj/TWGIH1DoqodVNUGsj4XlUxKeVvjRExyFhSaJ62Q8qXDWAtV8aSkmps70pGqSSZkLGkpBiLkHMyQeibkrGklFbF0bm1fexO8T8ylhTKcWzrdDR+yVwZS4oCO8E/89F6vXoosKRQ5lgUKnO8jCXl/sLcsH2wOpaxpFDl2FMq1gxkLClUxkY9x9MOvBPIWFIUWFIUWFIUWFIUWFJSe55YaC9n1CqRsaRAPLuT/UReC/6uAAIylhQIY4U/MpYUBfbw3qYeCiwpIeNY7++ro7zX0Pv775F/l4wlxbUqXs1Lo3VP9G+/mtMMlOffKWNJccmxXu8zPK1jwZyP17OLUsaSAtnzVFUFG9h7GHeQsaRAGTvKtVEmN6fx6i6qisUQre6QohxLigJLigJLigJLigJLigJLigJ7cfIXS3qPSONENscAAAAASUVORK5CYII=",
    "dodge_r": "iVBORw0KGgoAAAANSUhEUgAAAHYAAACXCAYAAADAv682AAAEO0lEQVR4nO2d246YMAxEccX//3KqSrtShRSFJL5MhjmP7bKwmIOdxIBd19UuQcef6gMQMSiwpCiwpNzXYbQWWxKY2cWAjCXFUKviaDPZTZaxpMAYi2bo6QbLWFLKjT3N1FPMlbGklBl7uqno5spYUtKNZTMV1VwZS4oCS4oCS0pajmXPrWi5VsaSosCSosCScp+em3ZztyXvLwsZS8p9evX4u/2sSba43+d2qAbLWFLur47zvFi9Y0QjY0kpz7EjniZEm96S9xeFjCVFgSVFgSWlvINiN4f1qlF7Od703j9KTpaxpJRXxahXfA+08WoPGUvKcX3Fo5mekfFtsN3ucaEgY0kpz7Eoqynt5/eesnozQsaSUj6Ozc51LSi3v91/FjKWFNgcu2pu1ltlGnjulbGklBvby0nVVaoNciW6uTKWlGPminsGRx+XHTqulbGkpBs7yk0jM3uGv/33t9s9OWX8+ouMJaU8x/Z4mptdhdrm/qI6Nt4iY0lxN/btlfrWiKwOC1usfme3y6ruZSwpbqs7q1f47PZvf98su0/roVXNMpaUdGOj102jMKfxrXKsqDV2dqZoNwehfcWjbXZLRuVe5VhS4PqK0eZco44/enwuY0mB/SbA7JUf9fPR49Qoc2UsKcvGRlV1swZHz1i1TVPfnifv8yljSZk2FjWnRc9V2+LxZ233RMZ+fT02u0twZOZuh0UDW43xPt8y9qvGVpk6onc8b4/THoajdPY/j2P1/MtYUmC7FGdByZnNyfjdO4iM/ZqxKLnVy4A2yKW7+4nOzbPxkLGkpOXY1eoz62k3cxoHo1TXMvYrxqLlitEMk9dXQFA7PlbvADKWlLQcW9WxPyL6WZuq0YWMJSXMWO8rNWpO14Kq7urqWMZ+xViv1QVvqvd/GjL2azkW1dzoqticx8m7aHVHzFXF1eZGdzoYyNyu9xMCyrFfH8f2zH3+/+m04tzqdV5lLCk3S07yMsyK5rS974AylpTlueKqN6uh9yq1yfPxi55oFzVPtHu/JQbl90atHumtMQLrHRRR66aoNJDxvapiUsrfGiNioHkoC+m22gCW/HQrJiXV2N6VjFJwMCFjSUkxFiHnZILQXiNjSSmtiqNza/vYneJ/ZCwplOPY1ml8+5K5MpYUBXaCf+ajtQT1UGBJocyxKFTmeBlLyv2FuWH7YHUsY0mhyrGnVKwZyFhSqIyNetyjHXgnkLGkKLCkKLCkKLCkKLCkpPY8sdBezqhVImNJgXjEI/vBrRb8+nkEZCwpEMYKf2QsKQrs4b1NPRRYUkLGsd6f4UZ5/Z33Z8Ij/y4ZS4prVbyal0brnuifCDWnGSjPv1PGkuKSY71ee3dax4I5H69nF6WMJQWy56mqCjaw1/XtIGNJgTJ2lGujTG5O49VdVBWLIVrdIUU5lhQFlhQFlhQFlhQFlhQFlhQF9uLkL9mvj0hMlQ6gAAAAAElFTkSuQmCC",
    "blaster": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAAEVklEQVR4nO2dSXLcMAxFxZTWOXGWPnEugFSq3AvLZnHC9NH/LdtWSy3yCSBESu26LrkIDL+iD4CscV8giNheCFprFwI0DIyWLYZZm4RuHg0DI9ywbEZlN46GgRFmGJpZWUyjYWC4G4ZuVrRpNAwMN8OqmRVlGg0Dgw0GBhsMDPMYVj12eccyGgYGGwwMNhgYN+q1Xw5jo/f+tKBhYNyo2VT73H615/f2+yF/f/z8T/v943ZRxtEwMNzHYdrjFDk0rGdWz7TR/jkOI194W8M+BjFr9Pfe/mkY+cLbGvaCMYzUvON8app0zJodL82aliU7fMFxGBhp5nRo1fbapmG7+9v9vl1oGBgw8xJHtcM26OGj7U6PywsaBkaa+2FPvKrj8vm9WarxI2gYGOmyRKtYIkaxc3b/WtAwMNLFsF3TxOkpA9GxjYaBkW5OR3TW1gaxKNo0GgZGmGGz1e6ecVZEGz6ChoHhZtjo2j8yqWekTH4+u91ov73v84KGgZFuHPY0zTsra0nGWzANho4o3TBN02CzPdhrzkTbzAajnoRzo/Ss7MhkBzxeBKJVrde+EzyiKXUErdUvXmbeKD0rK+Kc9ocnHbsxRJLUFr1xa7BqpsmiWVq/P9ww7RixC0pH2m6w1VJS73OUEzVL7/c8hzO7vzudYT2qNSz8RFKUBpHD4z+9wrD4C0a6hzSv9tRm9P/P7XrsXhl2TaNh1Q2zGk+tGifGJa1Ts2bP0+r5pGFVDcsaM+Sw6Gq10NBqOxoGxp21BtgzSQ6nEGSbVLN6vmlYFcOyVtfboFY3u/3z90VPunkeR+/80zAwYIq/2WOSKBk6Mp6GoRuWJXZp9VgZxKrT/VjHvufx0zAwzGPYbjbmtdynKY3jvLJNGoZqmPe1ePX/teZEaFXtrWN8z1gaBoZ5DIuaUh09Y9kq26Zh726Yds+yqvk1oyzUOlukYaiGzVaLvYnefzZoGHoMy2qadZbYlMd5p7BaXz1LjDbN+s5wS3KneXVGMGNYtXFYz7Tn39GR4Ng1e15pWNVKR9ZrflMyIqrmuXrFomHVa4lRjx7KPhdDFs/HC67ALI75o4u+7VB5NYv191rdDdi94jCGgWG2xtnqvlVWvManNAyMsKcIkD1oGBhsMDDglxtlSR68isc0DAz3xRDPz9HS92hoGBh31RuC3nhN4qFhYLhnidaxS4qbTcPAKDMOk850uGqm0TAw2GAD/puaaeIRGwyMMjEsC9YxlIaBcVetHbai2SINAwM+hkmiDM4DGgYGvGFWiyKymkvDwGCDgcEGA4MNBgYbDAzzOR1VkMkKjjU0DIx0r1SMeoHbLt41ShoGBpcbgUHDwGCDJZ270YMN9q7jMO2XjWZ5SJf2y1BPfxcNe7cs8fQF2FGvytB+gbf1i8Bf0LB3iWFaD+fKfof3ifbx8tX2xUkzpyMqK2zJHio2gjEMjHDDRrHMyjxRGm+dwiyxOKzWg8EYdmHxD+Ghx0ohgGOaAAAAAElFTkSuQmCC",
    "serious": "iVBORw0KGgoAAAANSUhEUgAAAIAAAACMAQMAAACOMjPzAAAABlBMVEUAAAD///+l2Z/dAAABjElEQVRIx7XWsWolMQyF4R/UGvQqhm0H9OqCaQP3VQxuBWeLyWaTnRlPIOwpv8IuZIsDALg0+Jx/wSQpVxCSVCuQJGkBdkDegx8wfgJxQP0IBhK+AoiCBWwHbCsYUf4zcKiAsYBBBb4A0xz++jKXE/jwsQKfGq7XWMCQpH0F5lKxgtnBfAFWsdWMXIB8q6F9EOMMXnhqbLXLC9UZQsQIQVSkSWeQ0ur4QGpcA13p0qDM/ApGpg0AG7arzhDakyIbkYxrcPBUIXKjnaGzkVYxIo1+DY0091kYnX6GRiOtwRtGLiDyDQfyDAakVcwi7mGqxXyzCcYZSCj2mC0M2hV0SF4xKy3pV9AwmDFbUpZXYBmwx2zJq7gCYsIr5oT3V3cCDH7F/PUI2wNgHbuHQUgDv4c6Vpu4A973s9/DN2PZ7qGPJ8gD7B72xB6h5TdgPMPHGE5gDq0/wfYIvfO/QdA7FbcAUvqXJnCC76UtwIcAV9YdhAII+Z+LTyC9gKiPKnAB+V467mEmaOrvoZ/gN90MbCk6zT9iAAAAAElFTkSuQmCC",
    "laugh": "iVBORw0KGgoAAAANSUhEUgAAAHAAAACeAQMAAADQYBz6AAAABlBMVEUAAAD///+l2Z/dAAABj0lEQVRIx6XVsYrrMBCF4QPTGvQqAbeBefUBt4G8yoBawX8LxcmNLYXdrLoPzGgkHcnSX4dDTFkApgQ5OeFKo9BizJDVlC5DmmS3lJYhpf6xxiRF6NnHkRDOlGE0+YRNImUTpkRKM1qQ1+94lWWTxZgelk0+YeEe7mjC5uHbjH4nnFflAzeAMuF1cUib0G8hLT5hyVbr7dXVge1a6zajEbWWNqHohzbhp7Rb61eDIZ3Sp8sRIQAKbUCDViC9z3VgYfGQrF08RpQDe0gPdOQJ0Nd4YlAvDkY7E5K6OtzhRAPIWukbNCJAc4gBt+4CeWSBWs3cVhvzXlf31bYhW1nX1dYaQ2YxMzNLJ440KL2N+ljC/xT4znZmeTHPtL1UEmfqSdeArs64jLhIRmh/Nw9UT9Azwidu+/KGLNB8xnRAbcx+cZrG3NPwJcM/Mae0H5Ev+NiA0ISp15GciaSSMzbp9Yf5JT9WtiKpLBPqvcd3+tbfi8dUB9KapGdW3mlwlUTlcReO3PMy5l2yx4N05PfjH8unUJ4YhdbBAAAAAElFTkSuQmCC",
    "hurt": "iVBORw0KGgoAAAANSUhEUgAAAGQAAAB2CAYAAAA+/DbEAAADq0lEQVR4nO2cQY4cIQxFy6PcYLZZ5v4nmmW2cwZmVZGChLCNgW/4f9tdFN3wsI0N8jxPeSgYfezuAPW/fj2gKmUuuCLyIIqEgEl225DZJGQjh4TcTggaEWjEkJBbCclGxi5SSMhthGQnYzUpJOQWQk4jYxUpJARMHBAwcUBOtyGn247ZtoSEgIkDAiYOCJg4IGDigICJAwImDgiYPjL5++Lw+b3P7VKaAblFHBAwcUBuq1x812/vHpcErf9R/Zi9V0dCbs0Yjs700piZdbva742+nxnDS7Ss+n3VDMue16ENARNsXZZ0vJoeYb3ndnt9LZEQMMGdoJLJ/v7b7qq4wioSAqZtlYuz1/IyOSIftXEtkZBTbEjUzPCSUhad0vW+p7ZVWpGQ7IREr/mtmVQWeT+9GWwlZTROISFggtvLKs61d7Rfo4Rqvb7e90hI1jikN8ItArT+fKudXnvaeKD3nDf+sJLce46EZLMh2pngXfPr9mXxHpP3fd7f2yOMhGQhJMrb0c7AVRlFcXpT0f1pkUJCsnhZs+KB3Zm6Mim+sD5XP09CshCyK1JGkRiJiCaXNuTUvSztzPn+/Uf1vQJyK+nqejIScqoNsXobNSmff7+eHbLutc3uBwk5nZBWJOwlpTjjhllV8LNEQm4lpP7834ur79WkWIlZvWsbLRJym5flzRhqiYmu0d1FCveyshAyuocVdY5Dgm2LVrv27pgxvI2Q2c9/N+IWNEK8KwYj9dMIicqfRGXerIq2maPtkhAwwZ4xtOYjRuOe1vu87XhFQsAER8grbS1uLXQvsScSAiYYQqzV6MWZ637jmDrSR9n1JSFggiFkVGUwp9/L7fO+rEslpRr6XZF6q70C4v3U7bVEL+tUQlbnQaztRSvq1Gy0baGXdfpdJ/Xnq05CWfurJVG7MxBFNgk5zYa8ipohAhIxj8q7a0xCstRloeSiZRIx1kpLbX9GM5ckJHtOPfruEu17ZBKJUefWozKVJCR7HKLNU4xGwrL4zhOUvS0Sckqkbs3oRUX0ZXNViLYfrMs6RMMZw11rvUzy0kZ/D3d7D1NYTj36jF8ZzLPU/fGeEp4tnqDKQkhUDjtaEnyjXStnP/q7o/4vxiFg2laXtfrGBTHWAu/yHknI6YRYZxaKrVot3tublRBUb2uXVtsS2pDbvazTiJPgWmgSkoUQ2pI9IiHZbEgUKafZDqu0/x8JQa9cnH23YnYV4++zriwkJDshaDdC79KsvToS8mDpB2vdhHICBJ/UAAAAAElFTkSuQmCC",
}
GASTER_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAFAAAAByAQMAAAD+u8TTAAAABlBMVEUAAAD///+l2Z/dAAAA/ElEQVQ4y6XUMarEMAwEUIFag65iSGvQ1QVuA76KwK1gtgiBlePPBv5Ur5hiqiH6M2z/pfiOGk86ASQL2RgwtkwhBYI8sxEAUMsMAQDXTFcACFkIhAKZjIuw35Sb/pt6MzIVoYiFcRU08x75gjJdQ0OGZ5qGBmfyNAl1HvZNcuuhnYUy+wwd/cEj9HxwHqHnWFinh8ooma16qJS2UCmUYqXABb6wXKyJrQiM4bV9k+WiW+IoMEadmThhjAMLXV1CMgkugAvoBdVLaJXIlKBaSD2TL1omgWoh0EKxWsVWkpcq9GAjahv2vmHpvW445oY8pm0IbEgAvebuSzb5AHEH2YB/GgUbAAAAAElFTkSuQmCC"
)

# Megalovania OST — SoundCloud timbre ref (Toby Fox); synth → base64 WAV (files = off)
SR = 22050
OST_BPM = 120.0

_NOTE = {
    "C": -9, "C#": -8, "Db": -8, "D": -7, "D#": -6, "Eb": -6, "E": -5, "F": -4,
    "F#": -3, "Gb": -3, "G": -2, "G#": -1, "Ab": -1, "A": 0, "A#": 1, "Bb": 1, "B": 2,
}


def _note_freq(name: str) -> float:
    octv = int(name[-1])
    key = name[:-1]
    return 440.0 * (2 ** ((_NOTE[key] + (octv - 4) * 12) / 12))


def _seq(text: str) -> list[tuple[str, float]]:
    out: list[tuple[str, float]] = []
    for tok in text.split():
        if tok == "R":
            out.append(("R", 1.0))
        elif ":" in tok:
            note, beats = tok.split(":")
            out.append((note, float(beats)))
    return out


def _osc(wave: str, freq: float, t: float, duty: float = 0.5) -> float:
    phase = (t * freq) % 1.0
    if wave in ("sq", "pulse"):
        return 1.0 if phase < duty else -1.0
    if wave == "thin":
        return 1.0 if phase < 0.125 else -1.0
    if wave == "tri":
        return 4.0 * abs(phase - 0.5) - 1.0
    return random.uniform(-1.0, 1.0)


def _vib(freq: float, t: float, depth: float = 0.015, rate: float = 5.5) -> float:
    return freq * (1.0 + depth * math.sin(t * rate * math.tau))


def _kick(buf: list[float], pos: int, vol: float = 0.30) -> None:
    length = min(380, len(buf) - pos)
    for j in range(length):
        t = j / SR
        freq = 195.0 * (0.992 ** j)
        env = (1.0 - j / length) ** 2.2
        buf[pos + j] += math.sin(t * freq * math.tau) * vol * env


def _snare(buf: list[float], pos: int, vol: float = 0.10) -> None:
    length = min(220, len(buf) - pos)
    for j in range(length):
        env = (1.0 - j / length) ** 1.6
        tone = math.sin(j / SR * 185 * math.tau) * 0.35
        noise = (random.random() * 2.0 - 1.0) * 0.65
        buf[pos + j] += (tone + noise) * vol * env


def _hat(buf: list[float], pos: int, vol: float = 0.022) -> None:
    length = min(90, len(buf) - pos)
    for j in range(length):
        buf[pos + j] += (random.random() * 2.0 - 1.0) * vol * (1.0 - j / length)


def _pcm_to_wav(buf: list[float]) -> bytes:
    peak = max(abs(s) for s in buf) or 1.0
    pcm = array.array("h", (int(max(-1.0, min(1.0, s * 0.85 / peak)) * 32767) for s in buf))
    raw = pcm.tobytes()
    out = io.BytesIO()
    out.write(b"RIFF")
    out.write(struct.pack("<I", 36 + len(raw)))
    out.write(b"WAVEfmt ")
    out.write(struct.pack("<IHHIIHH", 16, 1, 1, SR, SR * 2, 2, 16))
    out.write(b"data")
    out.write(struct.pack("<I", len(raw)))
    out.write(raw)
    return out.getvalue()


def _build_megalovania_wav() -> bytes:
    """D minor Megalovania loop — matches SoundCloud battle energy; no external files."""
    spb = 60.0 / OST_BPM
    melody = _seq(
        "D5:0.5 D5:0.5 D5:1 A4:0.5 Ab4:0.5 G4:1 "
        "D5:0.5 D5:0.5 D5:1 A4:0.5 Ab4:0.5 G4:1 "
        "D5:0.5 D5:0.5 D5:1 F4:0.5 G4:0.5 A4:1 "
        "A4:0.5 Ab4:0.5 G4:1 D5:0.5 D5:0.5 D5:1 "
        "F4:0.5 G4:0.5 A4:1 A4:0.5 Ab4:0.5 G4:1 "
        "D5:0.5 D5:0.5 D5:1 A4:0.5 Ab4:0.5 G4:1 "
        "D5:0.5 D5:0.5 D5:1 F4:0.5 G4:0.5 A4:1 "
        "A4:0.5 Ab4:0.5 G4:2"
    )
    bass = _seq("D3:1 D3:1 A2:1 A2:1 D3:1 D3:1 F3:1 G3:1 A3:1 A3:1 D3:1 D3:1 F3:1 G3:1 A3:2")
    arp = (
        ("D4", "F4", "A4", "D5"),
        ("A3", "C4", "E4", "A4"),
        ("Bb3", "D4", "F4", "Bb4"),
        ("G3", "Bb3", "D4", "G4"),
    )
    total_beats = sum(beats for _, beats in melody)
    samples = int(total_beats * spb * SR)
    buf = [0.0] * samples

    pos = 0
    for note, beats in melody:
        note_samples = int(beats * spb * SR)
        if note != "R":
            freq = _note_freq(note)
            for i in range(note_samples):
                t = (pos + i) / SR
                env = min(1.0, i / 80.0) * (1.0 if i < note_samples - 400 else (note_samples - i) / 400.0)
                buf[pos + i] += _osc("pulse", _vib(freq, t), t, 0.25) * 0.24 * env
        pos += note_samples

    pos = 0
    bass_i = 0
    while pos < samples:
        note, beats = bass[bass_i % len(bass)]
        bass_i += 1
        note_samples = min(int(beats * spb * SR), samples - pos)
        freq = _note_freq(note)
        for i in range(note_samples):
            env = 1.0 if i < note_samples - 300 else (note_samples - i) / 300.0
            buf[pos + i] += _osc("tri", freq, (pos + i) / SR) * 0.20 * env
        pos += note_samples

    sixteenth = max(1, int(spb * SR / 4))
    arp_i = arp_t = 0
    for i in range(0, samples, sixteenth):
        chord = arp[arp_i % len(arp)]
        note = chord[arp_t % len(chord)]
        freq = _note_freq(note)
        for j in range(min(sixteenth, samples - i)):
            env = 1.0 if j < sixteenth - 80 else (sixteenth - j) / 80.0
            buf[i + j] += _osc("thin", freq, (i + j) / SR) * 0.09 * env
        arp_t += 1
        if arp_t % len(chord) == 0:
            arp_i += 1

    beat = int(spb * SR)
    i = beat_n = 0
    while i < samples:
        if beat_n % 4 in (0, 2):
            _kick(buf, i, 0.32)
        if beat_n % 4 in (1, 3):
            _snare(buf, i, 0.11)
        for h in range(2):
            _hat(buf, i + h * beat // 2)
        i += beat
        beat_n += 1

    return _pcm_to_wav(buf)


_OST_WAV_CACHE: bytes | None = None
_OST_B64_CACHE: str | None = None


def _compose_ost_wav() -> bytes:
    global _OST_WAV_CACHE
    if _OST_WAV_CACHE is None:
        _OST_WAV_CACHE = _build_megalovania_wav()
    return _OST_WAV_CACHE


def _compose_ost_b64() -> str:
    global _OST_B64_CACHE
    if _OST_B64_CACHE is None:
        _OST_B64_CACHE = base64.b64encode(_compose_ost_wav()).decode("ascii")
    return _OST_B64_CACHE


class LBMusic:
    """Megalovania — synth-built base64 WAV in RAM; starts on first FIGHT (files = off)."""

    def __init__(self) -> None:
        self.ok = False
        self.mute = MUTE
        self.playing = False
        self.sound: pygame.mixer.Sound | None = None
        self._loaded = False

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return
        self._loaded = True
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(SR, -16, 1, 2048)
            wav = base64.b64decode(_compose_ost_b64())
            self.sound = pygame.mixer.Sound(io.BytesIO(wav))
            self.ok = True
        except (pygame.error, ValueError):
            self.sound = None

    def start_battle(self) -> None:
        """Begin looping battle OST — called when the player picks FIGHT the first time."""
        self._ensure_loaded()
        self.play_loop()

    def play_loop(self) -> None:
        if self.ok and self.sound and not self.mute and not self.playing:
            self.sound.play(-1)
            self.playing = True

    def stop(self) -> None:
        if self.sound:
            self.sound.stop()
            self.playing = False

    def toggle_mute(self) -> None:
        self.mute = not self.mute
        if not self.sound:
            return
        if self.mute:
            self.sound.stop()
            self.playing = False
        else:
            self.play_loop()


_LB_MUSIC: LBMusic | None = None


def get_music() -> LBMusic:
    global _LB_MUSIC
    if _LB_MUSIC is None:
        _LB_MUSIC = LBMusic()
    return _LB_MUSIC


class SansAnimator:
    """All Sans battle poses — real wiki sprites embedded as base64."""

    POSES = (
        "idle_0", "idle_1", "clenched", "fatal", "glow_0", "glow_1",
        "shrug", "point", "dodge_l", "dodge_r", "blaster", "serious", "laugh", "hurt",
    )

    def __init__(self) -> None:
        self.frames = {name: SpriteBank._from_b64(SANS_ANIMS_B64[name]) for name in self.POSES}
        self.pose = "shrug"
        self.tick = 0
        self.flash_pose: str | None = None
        self.flash_timer = 0

    def flash(self, pose: str, frames: int) -> None:
        self.flash_pose = pose
        self.flash_timer = frames

    def update(
        self,
        state: str,
        turn_timer: int,
        attack_pattern: int,
        blasters_firing: bool,
        player_hit: bool,
    ) -> None:
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer == 0:
                self.flash_pose = None
            return

        self.tick += 1
        if state == "INTRO":
            self.pose = "shrug"
        elif state in ("MENU", "SUBMENU"):
            self.pose = "idle_0" if (self.tick // 20) % 2 == 0 else "idle_1"
        elif state == "GAME_OVER":
            self.pose = "fatal"
        elif state == "PHASE_CLEAR":
            self.pose = "laugh"
        elif state == "SANS_TURN":
            if player_hit:
                self.pose = "hurt"
            elif turn_timer > 300:
                self.pose = "laugh"
            elif blasters_firing:
                self.pose = "glow_0" if (self.tick // 8) % 2 == 0 else "glow_1"
            elif attack_pattern == 0:
                self.pose = "point" if turn_timer > 60 else "clenched"
            elif attack_pattern == 1:
                self.pose = "blaster" if turn_timer > 30 else "serious"
            else:
                self.pose = "idle_0" if (self.tick // 20) % 2 == 0 else "idle_1"
        else:
            self.pose = "idle_0"

    def surface(self) -> pygame.Surface:
        key = self.flash_pose or self.pose
        return self.frames.get(key, self.frames["idle_0"])


class SpriteBank:
    """Undertale wiki sprites embedded as base64 — files = off."""

    def __init__(self) -> None:
        self.blaster = self._from_b64(GASTER_B64)
        self.sans_anim = SansAnimator()

    @staticmethod
    def _from_bytes(data: bytes) -> pygame.Surface:
        return pygame.image.load(io.BytesIO(data)).convert_alpha()

    @staticmethod
    def _from_b64(b64: str) -> pygame.Surface:
        return SpriteBank._from_bytes(base64.b64decode(b64))


_SPRITES: SpriteBank | None = None


def get_sprites() -> SpriteBank:
    global _SPRITES
    if _SPRITES is None:
        _SPRITES = SpriteBank()
    return _SPRITES


# --- INITIALIZATION ---
pygame.mixer.pre_init(SR, -16, 1, 2048)
pygame.init()
try:
    if not pygame.mixer.get_init():
        pygame.mixer.init(SR, -16, 1, 2048)
except pygame.error:
    pass
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("last breath 4k 0.1 — files = off")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)


def angle_diff_deg(a: float, b: float) -> float:
    d = math.degrees(a - b)
    return abs((d + 180) % 360 - 180)


def draw_text(surf, text, x, y, size, color, center=False):
    font = pygame.font.SysFont("impact", size)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surf.blit(rendered, rect)


def draw_heart(surface, x, y, size, color):
    pygame.draw.polygon(
        surface,
        color,
        [(x, y + size // 4), (x + size // 2, y - size // 4), (x + size, y + size // 4), (x + size // 2, y + size)],
    )


def draw_lb_box(surface: pygame.Surface, box: pygame.Rect) -> None:
    pygame.draw.rect(surface, BLACK, box)
    pygame.draw.rect(surface, WHITE, box, 4)


def draw_lb_player_stats(surface: pygame.Surface, hp: int, max_hp: int, name: str = "FRISK", lv: int = 19) -> None:
    draw_text(surface, name, 38, STATS_Y, 20, WHITE)
    draw_text(surface, f"LV {lv}", 140, STATS_Y, 20, WHITE)
    draw_text(surface, "HP", 220, STATS_Y, 20, WHITE)
    bar_x, bar_y, bar_w, bar_h = 250, STATS_Y + 2, 120, 20
    pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_w, bar_h))
    fill = max(0, int(bar_w * hp / max_hp))
    pygame.draw.rect(surface, YELLOW, (bar_x, bar_y, fill, bar_h))
    draw_text(surface, f"{hp} / {max_hp}", bar_x + bar_w + 8, STATS_Y + 2, 16, WHITE)


def draw_lb_sans_header(surface: pygame.Surface, sans_rect: pygame.Rect, hp: int, max_hp: int) -> None:
    draw_text(surface, "SANS", SANS_X, sans_rect.top - 30, 22, WHITE, center=True)
    bar = pygame.Rect(SANS_X - 60, sans_rect.bottom + 6, 120, 8)
    pygame.draw.rect(surface, (60, 0, 0), bar)
    pygame.draw.rect(surface, RED, (bar.x, bar.y, max(1, int(bar.w * hp / max_hp)), bar.h))
    draw_text(surface, "ATK 1  DEF 1", SANS_X, bar.bottom + 6, 14, GRAY, center=True)


def draw_lb_menu(surface: pygame.Surface, box: pygame.Rect, sel: int, quote: str = "") -> None:
    if quote:
        draw_text(surface, quote, box.x + 14, box.y + 12, 15, GRAY)
    draw_text(surface, "What will you do?", box.x + 14, box.y + 36, 17, WHITE)
    for i, opt in enumerate(MENU_OPTS):
        col = YELLOW if i == sel else WHITE
        if opt == "MERCY" and sel != i:
            col = GRAY
        draw_text(surface, opt, box.x + 20 + i * 68, box.bottom - 34, 16, col)


def draw_lb_dialogue(surface: pygame.Surface, box: pygame.Rect, text: str) -> None:
    pygame.draw.rect(surface, BLACK, box)
    pygame.draw.rect(surface, WHITE, box, 4)
    words = text.split()
    line, y = "", box.y + 16
    for word in words:
        trial = (line + " " + word).strip()
        if len(trial) > 52:
            draw_text(surface, line, box.x + 14, y, 18, WHITE)
            y += 24
            line = word
        else:
            line = trial
    if line:
        draw_text(surface, line, box.x + 14, y, 18, WHITE)


class Player:
    def __init__(self):
        self.x = LB_BOX.centerx
        self.y = LB_BOX.centery + 30
        self.size = 16
        self.speed = 4
        self.hp = 92
        self.max_hp = 92
        self.invuln_timer = 0

    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def move(self, keys, box):
        if self.invuln_timer > 0:
            self.invuln_timer -= 1
        dx = dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed
        self.x = max(box.left + self.size // 2, min(box.right - self.size // 2, self.x + dx))
        self.y = max(box.top + self.size // 2, min(box.bottom - self.size // 2, self.y + dy))

    def draw(self, surface):
        if self.invuln_timer == 0 or self.invuln_timer % 4 < 2:
            draw_heart(surface, self.x, self.y, self.size, RED)


class Bone:
    def __init__(self, x, y, w, h, speed, direction):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
        self.dir = direction

    def update(self):
        self.rect.x += self.speed * self.dir[0]
        self.rect.y += self.speed * self.dir[1]

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=3)


class GasterBlaster:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.angle = math.atan2(target_y - y, target_x - x)
        self.timer = 0
        self.firing = False
        self.beam_x = x
        self.beam_y = y

    def mouth_pos(self):
        dist = 40
        return (
            self.x + math.cos(self.angle) * dist,
            self.y + math.sin(self.angle) * dist,
        )

    def update(self):
        self.timer += 1
        if self.timer == 30:
            self.firing = True
        if self.firing:
            self.beam_x, self.beam_y = self.mouth_pos()
        if self.timer > 90:
            self.firing = False

    def draw(self, surface):
        bx, by = self.mouth_pos()
        blaster = get_sprites().blaster
        rotated = pygame.transform.rotate(blaster, -math.degrees(self.angle) - 90)
        rect = rotated.get_rect(center=(int(bx), int(by)))
        surface.blit(rotated, rect)
        if self.firing:
            beam_surf = pygame.Surface((800, 20), pygame.SRCALPHA)
            beam_surf.fill((255, 255, 255, 200))
            rotated_beam = pygame.transform.rotate(beam_surf, -math.degrees(self.angle))
            rect = rotated_beam.get_rect(center=(bx, by))
            surface.blit(rotated_beam, rect)


class Game:
    def __init__(self):
        self.state = "INTRO"
        self.dialogue = [
            "* LAST BREATH — PHASE 1",
            '* "you\'re not gonna give up, are you."',
            '* "on days like these, kids like you..."',
            '* "should be burning in hell."',
        ]
        self.dialogue_idx = 0
        self.battle_box = LB_BOX
        self.player = Player()
        self.bones: List[Bone] = []
        self.blasters: List[GasterBlaster] = []
        self.turn_timer = 0
        self.attack_pattern = 0
        self.sans_hp = 1
        self.sans_max_hp = 1
        self.shake = 0
        self.player_hit_flash = False
        self._menu_armed = False
        self.menu_sel = 0
        self.mercy = 0
        self.sans_turns = 0
        self.menu_quote = "* keeps staring."
        self.submenu_msg = ""
        self.submenu_timer = 0
        self.battle_music_started = False

    def reset_turn(self):
        self.bones.clear()
        self.blasters.clear()
        self.player.x = self.battle_box.centerx
        self.player.y = self.battle_box.centery + 30
        self.turn_timer = 0

    def handle_keydown(self, key: int) -> None:
        if self.submenu_timer > 0:
            self.submenu_timer = 0
            self.submenu_msg = ""
            if self.state == "SUBMENU":
                self.state = "MENU"
            return

        if self.state == "INTRO":
            if key in (pygame.K_z, pygame.K_RETURN):
                self.dialogue_idx += 1
                if self.dialogue_idx >= len(self.dialogue):
                    self.state = "MENU"
                    self._menu_armed = True
            return

        if self.state == "MENU":
            if key in (pygame.K_LEFT, pygame.K_a):
                self.menu_sel = (self.menu_sel - 1) % len(MENU_OPTS)
            elif key in (pygame.K_RIGHT, pygame.K_d):
                self.menu_sel = (self.menu_sel + 1) % len(MENU_OPTS)
            elif key not in (pygame.K_z, pygame.K_RETURN):
                return
            elif not self._menu_armed:
                return
            choice = MENU_OPTS[self.menu_sel]
            if choice == "FIGHT":
                if not self.battle_music_started:
                    self.battle_music_started = True
                    get_music().start_battle()
                self.state = "SANS_TURN"
                self.reset_turn()
                self.attack_pattern = random.randint(0, 1)
                self._menu_armed = False
            elif choice == "ACT":
                self.mercy = min(100, self.mercy + 15)
                self.submenu_msg = "* SANS — 1 ATK 1 DEF. The easiest enemy.\n* keeps dodging."
                self.state = "SUBMENU"
                self.submenu_timer = 90
            elif choice == "ITEM":
                self.submenu_msg = "* You have no items."
                self.state = "SUBMENU"
                self.submenu_timer = 60
            elif choice == "MERCY":
                if self.mercy >= 80:
                    self.state = "PHASE_CLEAR"
                else:
                    self.submenu_msg = "* SPARE was rejected."
                    self.state = "SUBMENU"
                    self.submenu_timer = 60
            return

        if self.state == "PHASE_CLEAR" and key in (pygame.K_z, pygame.K_RETURN, pygame.K_ESCAPE):
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self):
        keys = pygame.key.get_pressed()
        if self.shake > 0:
            self.shake -= 1

        if self.state == "MENU":
            self._menu_armed = True

        elif self.state == "SUBMENU":
            if self.submenu_timer > 0:
                self.submenu_timer -= 1
                if self.submenu_timer == 0:
                    self.submenu_msg = ""
                    self.state = "MENU"

        elif self.state == "SANS_TURN":
            self.player_hit_flash = False
            self.player.move(keys, self.battle_box)
            self.turn_timer += 1

            if self.attack_pattern == 0:
                if self.turn_timer % 20 == 0:
                    y_pos = random.randint(self.battle_box.y, self.battle_box.y + self.battle_box.h - 10)
                    self.bones.append(Bone(self.battle_box.right, y_pos, 20, 10, 4, (-1, 0)))
            elif self.attack_pattern == 1:
                if self.turn_timer % 60 == 0:
                    spawn_x = random.choice([self.battle_box.left, self.battle_box.right])
                    spawn_y = random.choice([self.battle_box.top, self.battle_box.bottom])
                    self.blasters.append(GasterBlaster(spawn_x, spawn_y, self.player.x, self.player.y))

            for b in self.bones[:]:
                b.update()
                if b.rect.x < self.battle_box.left - 50:
                    self.bones.remove(b)
                if b.rect.colliderect(self.player.get_rect()) and self.player.invuln_timer == 0:
                    self.player.hp -= 5
                    self.player.invuln_timer = 30
                    self.shake = 10
                    self.player_hit_flash = True
                    get_sprites().sans_anim.flash("hurt", 8)

            for gb in self.blasters[:]:
                gb.update()
                if gb.firing:
                    p_rect = self.player.get_rect()
                    angle_to_p = math.atan2(p_rect.centery - gb.beam_y, p_rect.centerx - gb.beam_x)
                    if angle_diff_deg(angle_to_p, gb.angle) < 5 and self.player.invuln_timer == 0:
                        self.player.hp -= 8
                        self.player.invuln_timer = 30
                        self.shake = 15
                        self.player_hit_flash = True
                        get_sprites().sans_anim.flash("dodge_l", 10)
                if gb.timer > 90:
                    self.blasters.remove(gb)

            if self.turn_timer > 360:
                self.state = "MENU"
                self.bones.clear()
                self.blasters.clear()
                self.player.x = self.battle_box.centerx
                self.player.y = self.battle_box.centery + 30
                self.sans_turns += 1
                self.menu_quote = random.choice([
                    "* you're going to have a bad time.",
                    "* keeps dodging.",
                    "* guess you really hate bad puns.",
                ])
                if self.sans_turns >= PHASE1_TURNS_TO_CLEAR:
                    self.state = "PHASE_CLEAR"

            if self.player.hp <= 0:
                self.state = "GAME_OVER"
                self.player.hp = 0

        blasters_on = any(gb.firing for gb in self.blasters) if self.state == "SANS_TURN" else False
        get_sprites().sans_anim.update(
            self.state,
            self.turn_timer,
            self.attack_pattern,
            blasters_on,
            self.player_hit_flash,
        )

    def _draw_sans(self, temp_surf: pygame.Surface) -> pygame.Rect:
        sans_img = get_sprites().sans_anim.surface()
        sans_rect = sans_img.get_rect(center=(SANS_X, SANS_Y))
        temp_surf.blit(sans_img, sans_rect)
        draw_lb_sans_header(temp_surf, sans_rect, self.sans_hp, self.sans_max_hp)
        return sans_rect

    def draw(self, surface):
        shake_x = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        shake_y = random.randint(-self.shake, self.shake) if self.shake > 0 else 0
        temp_surf = pygame.Surface((WIDTH, HEIGHT))
        temp_surf.fill(BLACK)

        if self.state == "INTRO":
            self._draw_sans(temp_surf)
            if self.dialogue_idx < len(self.dialogue):
                draw_lb_dialogue(temp_surf, DLG_BOX, self.dialogue[self.dialogue_idx])
            draw_text(temp_surf, "[ Z ]", DLG_BOX.right - 36, DLG_BOX.bottom - 24, 14, GRAY)
            draw_lb_player_stats(temp_surf, self.player.hp, self.player.max_hp)

        elif self.state in ("MENU", "SUBMENU"):
            self._draw_sans(temp_surf)
            draw_lb_box(temp_surf, self.battle_box)
            if self.state == "SUBMENU" and self.submenu_msg:
                for i, line in enumerate(self.submenu_msg.split("\n")):
                    draw_text(temp_surf, line, self.battle_box.x + 14, self.battle_box.y + 16 + i * 22, 16, WHITE)
                draw_text(temp_surf, "[ Z ]", self.battle_box.right - 36, self.battle_box.bottom - 24, 14, GRAY)
            else:
                draw_lb_menu(temp_surf, self.battle_box, self.menu_sel, self.menu_quote)
            draw_lb_player_stats(temp_surf, self.player.hp, self.player.max_hp)
            if self.mercy > 0:
                draw_text(temp_surf, f"mercy {self.mercy}%", SANS_X, 188, 14, YELLOW, center=True)

        elif self.state == "SANS_TURN":
            self._draw_sans(temp_surf)
            draw_lb_box(temp_surf, self.battle_box)
            for b in self.bones:
                b.draw(temp_surf)
            for gb in self.blasters:
                gb.draw(temp_surf)
            self.player.draw(temp_surf)
            draw_lb_player_stats(temp_surf, self.player.hp, self.player.max_hp)

        elif self.state == "GAME_OVER":
            self._draw_sans(temp_surf)
            draw_text(temp_surf, "GAME OVER", WIDTH // 2, HEIGHT // 2, 40, RED, center=True)
            draw_text(temp_surf, "Stay determined...", WIDTH // 2, HEIGHT // 2 + 50, 20, WHITE, center=True)
            draw_text(temp_surf, "[ ESC to quit ]", WIDTH // 2, HEIGHT // 2 + 90, 16, GRAY, center=True)

        elif self.state == "PHASE_CLEAR":
            self._draw_sans(temp_surf)
            draw_text(temp_surf, "PHASE 1 CLEAR", WIDTH // 2, HEIGHT // 2 - 20, 36, YELLOW, center=True)
            draw_text(temp_surf, "* Sans vanishes into a pun.", WIDTH // 2, HEIGHT // 2 + 24, 18, WHITE, center=True)
            draw_text(temp_surf, "[ ESC or Z to quit ]", WIDTH // 2, HEIGHT // 2 + 64, 16, GRAY, center=True)
            draw_lb_player_stats(temp_surf, self.player.hp, self.player.max_hp)

        surface.blit(temp_surf, (shake_x, shake_y))


def main():
    get_sprites()
    music = get_music()
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_m:
                    music.toggle_mute()
                elif event.key == pygame.K_F4:
                    pygame.display.toggle_fullscreen()
                else:
                    game.handle_keydown(event.key)
        game.update()
        game.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    music.stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
