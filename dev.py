# coding: utf-8
import twitter
import os

from cocos.director import *
from cocos.menu import *
from cocos.scene import *
from cocos.layer import *
from cocos.actions import *
from pyglet import font
from cocos.text import *

import random

api = twitter.Api()
twitties = api.GetSearch('#devincachu', per_page=30)

def wrap(text, width):
    def _generator():
        it = iter(text.split(' '))
        word = it.next()
        yield word
        pos = len(word) - word.rfind('\n') - 1
        for word in it:
            if "\n" in word:
                lines = word.split('\n')
            else:
                lines = (word,)
            pos += len(lines[0]) + 1
            if pos > width:
                yield '\n'
                pos = len(lines[-1])
            else:
                yield ' '
                if len(lines) > 1:
                    pos = len(lines[-1])
            yield word
    return u''.join(_generator())


class Background(Layer):

    is_event_handler = True

    def __init__(self):
        super(Background, self).__init__()
        twittie = random.choice(twitties)
        text = twittie.text

        texts = wrap(text, 28).split('\n')

        self.labels = []

        for text in texts:
            label = Label(text,
                font_name="Operating instructions",
                font_size=40,
                anchor_x='center', anchor_y='center',
                color=(255, 255, 255, 200)
            )
            self.add(label)
            self.labels.append(label)

        for indice, label in enumerate(self.labels):
            label.position = -100, 500 - (100 * indice)
            label.do(MoveTo((400, 500 - (100 * indice)), duration=2))

        self.name_label = Label('by @' +twittie.user.screen_name,
            font_name="Operating instructions",
            font_size=20,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 200)
        )
        self.name_label.position = 150, 50
        self.add(self.name_label)


    def on_key_press (self, key, modifiers):
        twittie = random.choice(twitties)
        text = twittie.text

        texts = wrap(text, 28).split('\n')

        self.remove(self.name_label)

        for label in self.labels:
            self.remove(label)

        self.labels = []

        for text in texts:
            label = Label(text,
                font_name="Operating instructions",
                font_size=40,
                anchor_x='center', anchor_y='center',
                color=(255, 255, 255, 200)
            )
            self.add(label)
            self.labels.append(label)

        for indice, label in enumerate(self.labels):
            label.position = -100, 500 - (100 * indice)
            label.do(MoveTo((400, 500 - (100 * indice)), duration=2))

        self.name_label = Label('by @' +twittie.user.screen_name,
            font_name="Operating instructions",
            font_size=20,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 200)
        )
        self.name_label.position = 150, 50
        self.add(self.name_label)


if __name__ == "__main__":
    font_path = os.path.join(os.path.dirname(__file__), 'media/font')
    font.add_directory(font_path)

    director.init(resizable=False, width=800, height=600)
    background = Background()

    scene = Scene(background)
    director.run(scene)
