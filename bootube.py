#!/usr/bin/env python3

import webbrowser, pyautogui, pygetwindow as gw
from typing import Callable
from pynput.keyboard import Listener, Key
from time import sleep
import pyperclip

class ShortCutListener (Listener):

    def __init__(self, shortcut_keys: tuple[Key|str], callback: Callable, *args, **kwargs):

        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.keys_pressed = set()
        self.shortcut_keys = set()

        # set all short_keys to lower
        for k in shortcut_keys:
            if type(k) is str:
                self.shortcut_keys.add(k.lower())
            else:
                self.shortcut_keys.add(k)

        # initialize listener
        super().__init__(on_press=self.on_press, on_release=self.on_release)

        # directly start listening
        with self as listener:
            listener.join()

    def on_press (self, key: Key):

        # try to extract char
        try:
            key = key.char.lower()
        except AttributeError:
            pass
        
        # add keys to pressed keys
        if key not in self.shortcut_keys:
            return
        self.keys_pressed.add(key)

        # check for combination
        for k in self.shortcut_keys:
            if k not in self.keys_pressed:
                return
        
        sleep(.5)
        
        # handle if condition is fulfilled 
        self.callback(*self.args, **self.kwargs)

    def on_release (self, key: Key):

        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        else:
            try:
                key = key.char.lower()
            except AttributeError:
                pass
        
        

        try:
            self.keys_pressed.remove(key)
        except:
            pass
        
        if key == Key.esc: 
            return exit()

def nsfw ():

    parsed_url: str

    pyautogui.press('f6')

    # copy url to clipboard, then write to variable
    title = gw.getActiveWindowTitle()
    pyautogui.hotkey('ctrl', 'c')
    sleep(.05)
    parsed_url = pyperclip.paste()
    nsfw_url = parsed_url.replace('www.', 'www.nsfw')

    # inspect the parsed url
    if not 'youtube' in parsed_url:
        print(f'{parsed_url} is not a youtube link!')
        return

    # stdout
    print(f'NSFW Redirect ---> {title}')

    # call the video with nsfw in new tab
    webbrowser.open_new_tab(nsfw_url)
    sleep(1)

    # ---- autoplay ----
    # Get the active window (current web browser window)
    for window in gw.getAllWindows():
        if 'NSFW' in window.title:
            active_window = window
            break
    
    active_window.activate()

    # Get the window's position and size
    window_x, window_y, window_width, window_height = active_window.left, active_window.top, active_window.width, active_window.height

    # Calculate the scaling factors 
    scaling_factor_x = 1 #window_width / screen_width 
    scaling_factor_y = 1 #window_height / screen_height

    # Calculate the center coordinates
    center_x = window_x + (window_width // 2) * scaling_factor_x 
    center_y = window_y + (window_height // 2) * scaling_factor_y

    # Move the mouse to the center and click to autoplay
    # print('SCREEN', screen_width, screen_height)
    # print('WINDOW', window_x, window_y, window_width, window_height)
    # print('CENTER', center_x, center_y)
    pyautogui.click(center_x, center_y)

if __name__ == '__main__':
    
    ShortCutListener((Key.ctrl_l, 'y'), nsfw)