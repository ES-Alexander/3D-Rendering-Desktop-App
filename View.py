#!/usr/bin/env python3

import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog

from sys import platform
if platform.startswith('linux'):
    from PIL import Image
    import pyscreenshot as ImageGrab
else:
    from PIL import Image, ImageGrab

SCREEN_SCALE = 2 if platform.startswith('darwin') else 1

from collections import defaultdict

class View(tk.Tk):
    ''' A GUI class for displaying a movable object on a canvas. '''
    def __init__(self, title='3D-Viz', min_size=(1165,630), bg='#131113',
                 fg='white', canvas_dims=(840,560), canvas_colour='white',
                 padding=(20,20), default_zoom=20):
        super().__init__()
        self._padding  = padding
        self._initialise_window(title, min_size, bg, fg)
        # initialise a dictionary of bindings that do nothing
        self._bindings = defaultdict(lambda:lambda event=None:None)

        self._create_canvas(canvas_dims, canvas_colour)
        self._create_controls(default_zoom)

    def _initialise_window(self, title, min_size, bg, fg):
        self.title(title)
        self.minsize(*min_size)
        self['bg'] = bg

    def _create_canvas(self, canvas_dims, canvas_colour):
        self._canvas = tk.Canvas(self, width=canvas_dims[0],
                                 height=canvas_dims[1], bg=canvas_colour)
        self._canvas.grid(padx=self._padding[0], pady=self._padding[1],
                          sticky='nsew')

    def _create_controls(self, default_zoom):
        self._control_frame = ttk.Frame(self)
        self._control_frame.grid(row=0, column=1)
        self._create_zoom_control(default_zoom)
        ttk.Separator(self._control_frame, orient='horizontal')\
           .grid(row=1, sticky='ew')
        self._create_rotation_controls()
        self._create_move_controls()
        ttk.Separator(self._control_frame, orient='horizontal')\
           .grid(row=4, sticky='ew')
        self._create_load_controls()
        self._create_screenshot_controls()

    def _create_zoom_control(self, default_zoom):
        ''' Create a slider for zooming the display. '''
        frame = ttk.Frame(self._control_frame)
        frame.grid(row=0, padx=self._padding[0],
                   pady=self._padding[1], sticky='ew')

        # don't need to refer to label later, so no need to save
        ttk.Label(frame, text='Zoom:').grid(sticky='ew')
        self._zoom_slider = ttk.Scale(frame, from_=1, to=500,
                                      orient='horizontal')
        self._zoom_slider.set(default_zoom)
        self._zoom_slider.grid(sticky='ew')

    def _create_rotation_controls(self):
        ''' Create buttons and sliders for rotating the display. '''
        frame = ttk.Frame(self._control_frame)
        frame.grid(row=2, padx=self._padding[0],
                   pady=self._padding[1], sticky='ew')

        self._rotation_sliders = {}
        for dimension in 'XYZ':
            # create a label and slider for each dimension
            ttk.Label(frame, text=f'{dimension} Rotation:').grid(sticky='ew')
            slider = ttk.Scale(frame, from_=-np.pi, to=np.pi,
                               orient='horizontal')
            slider.set(0)
            slider.grid(sticky='ew')
            self._rotation_sliders[dimension] = slider

        button_frame = ttk.Frame(frame)
        button_frame.grid()

        # create a checkbox for spinning
        self._spin = tk.IntVar()
        tk.Checkbutton(button_frame, text='Spin', variable=self._spin)\
            .grid(padx=self._padding[0])
        self._spin.set(0)

        # create a button for resetting rotation to 0
        ttk.Button(button_frame, text='Reset rotation',
                   command=self._reset_rotation).grid(row=0, column=1)

    def _create_move_controls(self):
        ''' Create buttons and keybindings for panning the display. '''
        frame = ttk.Frame(self._control_frame)
        frame.grid(row=3, padx=self._padding[0],
                   pady=self._padding[1])

        for direction, binding, row, col in (('<Up>'   , self._up   , 0, 1),
                                             ('<Left>' , self._left , 1, 0),
                                             ('<Right>', self._right, 1, 2),
                                             ('<Down>' , self._down , 2, 1)):
            text = direction[1]
            ttk.Button(frame, text=text, command=binding)\
               .grid(row=row, column=col)
            self.bind(direction, binding)
            self.bind(text, binding)

    def _create_load_controls(self):
        ''' Create a button and display widget for loading a file. '''
        frame = ttk.Frame(self._control_frame)
        frame.grid(row=5, padx=self._padding[0],
                   pady=self._padding[1])
        self._file_name = tk.StringVar()
        ttk.Label(frame, textvariable=self._file_name, width=20)\
           .grid(sticky='w')

        ttk.Button(frame, text='Import file', command=self._load_file)\
            .grid(row=0, column=1, padx=self._padding[0])

    def _create_screenshot_controls(self):
        ''' Create a button for taking screenshots of the canvas. '''
        ttk.Button(self._control_frame, text='Take a screenshot',
                   command=self._screenshot).grid(row=6, sticky='ew',
                                                  padx=self._padding[0],
                                                  pady=self._padding[1])

    def _reset_rotation(self):
        ''' Reset all rotations to 0. '''
        for slider in self._rotation_sliders.values():
            slider.set(0)

    def _load_file(self):
        ''' Call the load_file binding and update file name display. '''
        self._file_name.set(self._bindings['load_file']())

    def _screenshot(self):
        ''' Take and save a screenshot of the current canvas. '''
        # coords of top left corner of canvas
        x0 = self.winfo_rootx() + self._canvas.winfo_x()
        y0 = self.winfo_rooty() + self._canvas.winfo_y()

        # coords of bottom right corner of canvas
        x1 = x0 + self._canvas.winfo_width()
        y1 = y0 + self._canvas.winfo_height()

        # take a full screenshot and crop to size
        image = ImageGrab.grab().crop(np.array([x0,y0,x1,y1])*2)

        # open a save dialog
        save_path = filedialog.asksaveasfilename(defaultextension='.png',
                filetypes= (('PNG Files', '*.png'),
                            ('All Files', '*.*')))

        # check if actually saved, instead of exiting menu
        if save_path:
            image.save(save_path)

    def _up(self, event=None):
        self._bindings['<Up>'](event)

    def _down(self, event=None):
        self._bindings['<Down>'](event)

    def _left(self, event=None):
        self._bindings['<Left>'](event)

    def _right(self, event=None):
        self._bindings['<Right>'](event)

    def update_bindings(self, bindings):
        self._bindings.update(bindings)

    def get_canvas(self):
        return self._canvas

    def get_latest(self):
        ''' Returns the current zoom and rotation slider values. '''
        zoom = self._zoom_slider.get()
        rotation = [rot.get() for rot in self._rotation_sliders.values()]
        spin = self._spin.get()
        return zoom, np.array(rotation), spin
