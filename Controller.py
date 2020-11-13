#!/usr/bin/env python3

from Model import Obj
from View import View

class Controller:
    ''' A class to interface a View GUI with an Obj object. '''
    def __init__(self, filename='', move_amount=20, *args, **kwargs):
        self._obj = None # start with no object
        self._move_amount = move_amount
        self._initialise_display(*args, **kwargs)

        self._update_display()
        self._view.mainloop()

    def _initialise_display(self, *args, **kwargs):
        ''' Create the display and add relevant bindings. '''
        self._view = View(*args, **kwargs)
        self._add_bindings()

    def _add_bindings(self):
        self._bindings = {
            '<Up>'      : lambda e=None: self._move('<Up>'),
            '<Down>'    : lambda e=None: self._move('<Down>'),
            '<Left>'    : lambda e=None: self._move('<Left>'),
            '<Right>'   : lambda e=None: self._move('<Right>'),
            'load_file' : self._load_file,
        }

        self._view.update_bindings(self._bindings)

    def _set_obj(self, filename=''):
        self._obj = Obj.from_file(self._view.get_canvas(), filename)

    def _move(self, direction):
        try:
            self._obj.move(direction, self._move_amount)
        except AttributeError:
            pass # no object yet

    def _load_file(self, event=None):
        self._set_obj()
        return self._obj.filename

    def _update_display(self):
        zoom, rotation, spin = self._view.get_latest()
        try:
            self._obj.draw(zoom, rotation, spin)
        except AttributeError:
            pass # no object yet
        self._view.after(1, self._update_display) # continue looping

if __name__ == '__main__':
    Controller()
    
