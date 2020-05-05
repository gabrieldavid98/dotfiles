# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List  # noqa: F401


mod = "mod4"

home = os.path.expanduser('~')
qtile_root_path = f'{home}/.config/qtile'

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen([f'{qtile_root_path}/autostart.sh'])


keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("alacritty")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # dmenu
    Key([mod], "p", lazy.spawn("dmenu_run -p 'Run: '")),

    # Sound
    Key([], 'XF86AudioMute', lazy.spawn(f'bash {qtile_root_path}/audio_toggle.sh')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -c 1 sset Master 1-')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -c 1 sset Master 1+')),

    # Mic
    Key([], 'XF86AudioMicMute', lazy.spawn('amixer -c 1 sset Mic toggle')),

    # Brightness
    Key([], 'XF86MonBrightnessUp', lazy.spawn(f'python {qtile_root_path}/brightness.py inc 55')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn(f'python {qtile_root_path}/brightness.py dec 55')),
]

group_names = [
    ('DEV', { 'layout': 'monadtall' }),
    ('WWW', { 'layout': 'monadtall' }),
    ('GENERAL', { 'layout': 'monadtall' }),
    ('VIDEO', { 'layout': 'monadtall' }),
    ('SPOTIFY', { 'layout': 'monadtall' }),
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], str(i), lazy.group[name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        # Key([mod, "shift"], str(i), lazy.window.togroup(name, switch_group=True)),
        # Or, use below if you prefer not to switch to that group.
        # # mod1 + shift + letter of group = move focused window to group
        Key([mod, "shift"], str(i), lazy.window.togroup(name)),
    ])

colors = {
    'panel_bg': '282828',
    'current_screen_tab_bg': '504945',
    'group_names_fg': 'ebdbb2',
    'group_names_fg_inactive': 'bdae93',
    'window_name_fg': 'b16286',
    'highlight_line_color': '458588'
}

layout_theme = {
    'border_width': 1,
    'margin': 2,
    'border_focus': '458588',
    'border_normal': '076678'
}

layouts = [
    layout.xmonad.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=False, **layout_theme),
    layout.Stack(num_stacks=2),
    layout.Floating(**layout_theme),
]

widget_defaults = dict(
    font = 'Ubuntu Mono Bold',
    fontsize = 14,
    padding = 2,
)

extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widget_list = [
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors['group_names_fg'],
            background = colors['panel_bg']
        ),
        widget.GroupBox(
            font = 'Ubuntu Bold',
            fontsize = 11,
            margin_y = 3,
            margin_x = 0,
            padding_y = 5,
            padding_x = 5,
            borderwidth = 3,
            active = colors['group_names_fg'],
            inactive = colors['group_names_fg_inactive'],
            rounded = False,
            highlight_color = colors['current_screen_tab_bg'],
            highlight_method = 'line',
            this_current_screen_border = colors['highlight_line_color'],
            this_screen_border = colors['highlight_line_color'],
            other_current_screen_border = colors['panel_bg'],
            other_screen_border = colors['panel_bg'],
            foreground = colors['group_names_fg'],
            background = colors['panel_bg'],
        ),
        widget.Sep(
            linewidth = 0,
            padding = 27,
            foreground = colors['group_names_fg'],
            background = colors['panel_bg']
        ),
        widget.WindowName(
            foreground = colors['window_name_fg'],
            background = colors['panel_bg'],
            padding = 0
        ),
        widget.Battery(
            battery = 0,
            format = 'Bat1: {percent:2.0%}',
            foreground = colors['group_names_fg'],
            background = colors['panel_bg'],
        ),
        widget.Sep(
            linewidth = 0,
            padding = 5,
            foreground = colors['group_names_fg'],
            background = colors['panel_bg']
        ),
        widget.Battery(
            battery = 1,
            format = 'Bat2: {percent:2.0%}',
            foreground = colors['group_names_fg'],
            background = colors['panel_bg'],
        ),
        widget.Net(
            interface = 'wlp3s0',
            format = '{down} ↓↑ {up}',
            foreground = colors['group_names_fg'],
            background = colors['panel_bg'],
            padding = 5
        ),
        widget.Clock(
            foreground = colors['group_names_fg'],
            background = colors['panel_bg'],
            format = '%a %d/%m/%Y %H:%M:%S'
        ),
        widget.Sep(
            linewidth = 0,
            padding = 6,
            foreground = colors['group_names_fg'],
            background = colors['panel_bg']
        ),
    ]

    return widget_list

def init_widgets_screen1():
    return init_widgets_list()

def init_widgets_screen2():
    return init_widgets_list()

def init_screens():
    return [
        Screen(
            bottom = bar.Bar(
                widgets = init_widgets_screen1(),
                opacity = 0.15,
                size = 24
            )
        ),
        Screen(
            bottom = bar.Bar(
                widgets = init_widgets_screen2(),
                opacity = 0.95,
                size = 24
            )
        )
    ]

if __name__ in ['config', '__main__']:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
