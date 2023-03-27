# pylint: disable=no-member, unnecessary-lambda, unused-argument, import-error
# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
# SPDX-License-Identifier: GPL-3.0-only
import os
import json
import traceback
from functools import partial
from yuki_iptv.time import print_with_time
from yuki_iptv.qt import get_qt_library
from yuki_iptv.lang import _, __
from yuki_iptv.qt6compat import qaction
qt_library, QtWidgets, QtCore, QtGui, QShortcut = get_qt_library()

class YukiData: # pylint: disable=too-few-public-methods
    menubar_ready = False
    first_run = False
    first_run1 = False
    menubars = {}
    data = {}
    cur_vf_filters = []
    keyboard_sequences = []
    if qt_library == 'PyQt6':
        str_offset = ' ' * 44
    else:
        str_offset = ''

def ast_mpv_seek(secs):
    print_with_time("Seeking to {} seconds".format(secs))
    YukiData.player.command('seek', secs)

def ast_mpv_speed(spd):
    print_with_time("Set speed to {}".format(spd))
    YukiData.player.speed = spd

def ast_trackset(track, type1):
    print_with_time("Set {} track to {}".format(type1, track))
    if type1 == 'vid':
        YukiData.player.vid = track
    else:
        YukiData.player.aid = track
    YukiData.redraw_menubar()

def send_mpv_command(name, act, cmd):
    if cmd == '__AST_VFBLACK__':
        cur_window_pos = YukiData.get_curwindow_pos()
        cmd = 'lavfi=[pad=iw:iw*sar/{}*{}:0:(oh-ih)/2]'.format(
            cur_window_pos[0], cur_window_pos[1]
        )
    if cmd == '__AST_SOFTSCALING__':
        cur_window_pos = YukiData.get_curwindow_pos()
        cmd = 'lavfi=[scale={}:-2]'.format(cur_window_pos[0])
    print_with_time("Sending mpv command: \"{} {} \\\"{}\\\"\"".format(name, act, cmd))
    YukiData.player.command(name, act, cmd)

def get_active_vf_filters():
    return YukiData.cur_vf_filters

def apply_vf_filter(vf_filter, e_l):
    try:
        if e_l.isChecked():
            send_mpv_command(vf_filter.split('::::::::')[0], 'add', vf_filter.split('::::::::')[1])
            YukiData.cur_vf_filters.append(vf_filter)
        else:
            send_mpv_command(
                vf_filter.split('::::::::')[0], 'remove', vf_filter.split('::::::::')[1]
            )
            YukiData.cur_vf_filters.remove(vf_filter)
    except Exception as e_4: # pylint: disable=broad-except
        print_with_time("ERROR in vf-filter apply")
        print_with_time("")
        e4_traceback = traceback.format_exc()
        print_with_time(e4_traceback)
        YukiData.show_exception(e_4, e4_traceback, '\n\n' + _('errorvfapply'))

def get_seq():
    return YukiData.keyboard_sequences

def qkeysequence(seq):
    s_e = QtGui.QKeySequence(seq)
    YukiData.keyboard_sequences.append(s_e)
    return s_e

def kbd(k_1):
    return qkeysequence(YukiData.get_keybind(k_1))

def alwaysontop_action():
    try:
        aot_f = open(YukiData.aot_file, 'w', encoding='utf-8')
        aot_f.write(json.dumps({
            "alwaysontop": YukiData.alwaysontopAction.isChecked()
        }))
        aot_f.close()
    except: # pylint: disable=bare-except
        pass
    if YukiData.alwaysontopAction.isChecked():
        print_with_time("Always on top enabled now")
        YukiData.enable_always_on_top()
    else:
        print_with_time("Always on top disabled now")
        YukiData.disable_always_on_top()

def reload_menubar_shortcuts():
    YukiData.playlists.setShortcut(kbd("show_playlists"))
    YukiData.reloadPlaylist.setShortcut(kbd("reload_playlist"))
    YukiData.m3uEditor.setShortcut(kbd("show_m3u_editor"))
    YukiData.exitAction.setShortcut(kbd("app.quit"))
    YukiData.playpause.setShortcut(kbd("mpv_play"))
    YukiData.stop.setShortcut(kbd("mpv_stop"))
    YukiData.normalSpeed.setShortcut(kbd("(lambda: set_playback_speed(1.00))"))
    YukiData.prevchannel.setShortcut(kbd("prev_channel"))
    YukiData.nextchannel.setShortcut(kbd("next_channel"))
    YukiData.fullscreen.setShortcut(kbd("mpv_fullscreen"))
    YukiData.compactmode.setShortcut(kbd("showhideeverything"))
    YukiData.csforchannel.setShortcut(kbd("main_channel_settings"))
    YukiData.screenshot.setShortcut(kbd("do_screenshot"))
    YukiData.muteAction.setShortcut(kbd("mpv_mute"))
    YukiData.volumeMinus.setShortcut(kbd("my_down_binding_execute"))
    YukiData.volumePlus.setShortcut(kbd("my_up_binding_execute"))
    YukiData.showhideplaylistAction.setShortcut(kbd("key_t"))
    YukiData.showhidectrlpanelAction.setShortcut(kbd("lowpanel_ch_1"))
    YukiData.alwaysontopAction.setShortcut(kbd("alwaysontop"))
    YukiData.streaminformationAction.setShortcut(kbd("open_stream_info"))
    YukiData.showepgAction.setShortcut(kbd("show_tvguide_2"))
    YukiData.forceupdateepgAction.setShortcut(kbd("force_update_epg"))
    YukiData.sortAction.setShortcut(kbd("show_sort"))
    YukiData.settingsAction.setShortcut(kbd("show_settings"))
    sec_keys_1 = [
        kbd("(lambda: mpv_seek(-10))"),
        kbd("(lambda: mpv_seek(10))"),
        kbd("(lambda: mpv_seek(-60))"),
        kbd("(lambda: mpv_seek(60))"),
        kbd("(lambda: mpv_seek(-600))"),
        kbd("(lambda: mpv_seek(600))")
    ]
    sec_i_1 = -1
    for i_1 in YukiData.secs:
        sec_i_1 += 1
        i_1.setShortcut(qkeysequence(sec_keys_1[sec_i_1]))

def init_menubar(data): # pylint: disable=too-many-statements
    # File

    YukiData.playlists = qaction(_('menubar_playlists'), data)
    YukiData.playlists.setShortcut(kbd("show_playlists"))
    YukiData.playlists.triggered.connect(lambda: YukiData.show_playlists())

    YukiData.reloadPlaylist = qaction(_('updcurplaylist'), data)
    YukiData.reloadPlaylist.setShortcut(kbd("reload_playlist"))
    YukiData.reloadPlaylist.triggered.connect(lambda: YukiData.reload_playlist())

    YukiData.m3uEditor = qaction(_('menubar_m3ueditor') + YukiData.str_offset, data)
    YukiData.m3uEditor.setShortcut(kbd("show_m3u_editor"))
    YukiData.m3uEditor.triggered.connect(lambda: YukiData.show_m3u_editor())

    YukiData.exitAction = qaction(_('menubar_exit'), data)
    YukiData.exitAction.setShortcut(kbd("app.quit"))
    YukiData.exitAction.triggered.connect(lambda: YukiData.app_quit())

    # Play

    YukiData.playpause = qaction(_('menubar_playpause'), data)
    YukiData.playpause.setShortcut(kbd("mpv_play"))
    YukiData.playpause.triggered.connect(lambda: YukiData.mpv_play())

    YukiData.stop = qaction(_('menubar_stop'), data)
    YukiData.stop.setShortcut(kbd("mpv_stop"))
    YukiData.stop.triggered.connect(lambda: YukiData.mpv_stop())

    YukiData.secs = []
    sec_keys = [
        kbd("(lambda: mpv_seek(-10))"),
        kbd("(lambda: mpv_seek(10))"),
        kbd("(lambda: mpv_seek(-60))"),
        kbd("(lambda: mpv_seek(60))"),
        kbd("(lambda: mpv_seek(-600))"),
        kbd("(lambda: mpv_seek(600))")
    ]
    sec_i = -1
    for i in (
        (10, "seconds_plural", 10),
        (1, "minutes_plural", 60),
        (10, "minutes_plural", 600)
    ):
        for k in ("-", "+"):
            sec_i += 1
            sec = qaction(
                "{}{} {}".format(k, i[0], __(i[1], "", i[0])),
                data
            )
            sec.setShortcut(qkeysequence(sec_keys[sec_i]))
            sec.triggered.connect(partial(ast_mpv_seek, i[2] * -1 if k == '-' else i[2]))
            YukiData.secs.append(sec)

    YukiData.normalSpeed = qaction(_('menubar_normalspeed'), data)
    YukiData.normalSpeed.triggered.connect(partial(ast_mpv_speed, 1.00))
    YukiData.normalSpeed.setShortcut(kbd("(lambda: set_playback_speed(1.00))"))

    YukiData.spds = []

    for spd in (0.25, 0.5, 0.75, 1.25, 1.5, 1.75):
        spd_action = qaction("{}x".format(spd), data)
        spd_action.triggered.connect(partial(ast_mpv_speed, spd))
        YukiData.spds.append(spd_action)

    YukiData.prevchannel = qaction(_('menubar_previous'), data)
    YukiData.prevchannel.triggered.connect(lambda: YukiData.prev_channel())
    YukiData.prevchannel.setShortcut(kbd("prev_channel"))

    YukiData.nextchannel = qaction(_('menubar_next'), data)
    YukiData.nextchannel.triggered.connect(lambda: YukiData.next_channel())
    YukiData.nextchannel.setShortcut(kbd("next_channel"))

    # Video
    YukiData.fullscreen = qaction(_('menubar_fullscreen'), data)
    YukiData.fullscreen.triggered.connect(lambda: YukiData.mpv_fullscreen())
    YukiData.fullscreen.setShortcut(kbd("mpv_fullscreen"))

    YukiData.compactmode = qaction(_('menubar_compactmode'), data)
    YukiData.compactmode.triggered.connect(lambda: YukiData.showhideeverything())
    YukiData.compactmode.setShortcut(kbd("showhideeverything"))

    YukiData.csforchannel = qaction(
        _('menubar_videosettings') + YukiData.str_offset, data
    )
    YukiData.csforchannel.triggered.connect(lambda: YukiData.main_channel_settings())
    YukiData.csforchannel.setShortcut(kbd("main_channel_settings"))

    YukiData.screenshot = qaction(_('menubar_screenshot'), data)
    YukiData.screenshot.triggered.connect(lambda: YukiData.do_screenshot())
    YukiData.screenshot.setShortcut(kbd("do_screenshot"))

    # Video filters
    YukiData.vf_postproc = qaction(_('menubar_postproc'), data)
    YukiData.vf_postproc.setCheckable(True)

    YukiData.vf_deblock = qaction(_('menubar_deblock'), data)
    YukiData.vf_deblock.setCheckable(True)

    YukiData.vf_dering = qaction(_('menubar_dering'), data)
    YukiData.vf_dering.setCheckable(True)

    YukiData.vf_debanding = qaction(_('menubar_debanding') + YukiData.str_offset, data)
    YukiData.vf_debanding.setCheckable(True)

    YukiData.vf_noise = qaction(_('menubar_noise'), data)
    YukiData.vf_noise.setCheckable(True)

    YukiData.vf_black = qaction(_('menubar_black'), data)
    YukiData.vf_black.setCheckable(True)

    YukiData.vf_softscaling = qaction(_('menubar_softscaling'), data)
    YukiData.vf_softscaling.setCheckable(True)

    YukiData.vf_phase = qaction(_('menubar_phase'), data)
    YukiData.vf_phase.setCheckable(True)

    # Audio

    YukiData.muteAction = qaction(_('menubar_mute'), data)
    YukiData.muteAction.triggered.connect(lambda: YukiData.mpv_mute())
    YukiData.muteAction.setShortcut(kbd("mpv_mute"))

    YukiData.volumeMinus = qaction(_('menubar_volumeminus'), data)
    YukiData.volumeMinus.triggered.connect(lambda: YukiData.my_down_binding_execute())
    YukiData.volumeMinus.setShortcut(kbd("my_down_binding_execute"))

    YukiData.volumePlus = qaction(_('menubar_volumeplus'), data)
    YukiData.volumePlus.triggered.connect(lambda: YukiData.my_up_binding_execute())
    YukiData.volumePlus.setShortcut(kbd("my_up_binding_execute"))

    # Audio filters

    YukiData.af_extrastereo = qaction(_('menubar_extrastereo'), data)
    YukiData.af_extrastereo.setCheckable(True)

    YukiData.af_karaoke = qaction(_('menubar_karaoke'), data)
    YukiData.af_karaoke.setCheckable(True)

    YukiData.af_earvax = qaction(_('menubar_earvax') + YukiData.str_offset, data)
    YukiData.af_earvax.setCheckable(True)

    YukiData.af_volnorm = qaction(_('menubar_volnorm'), data)
    YukiData.af_volnorm.setCheckable(True)

    # View

    YukiData.showhideplaylistAction = qaction(_('showhideplaylist'), data)
    YukiData.showhideplaylistAction.triggered.connect(lambda: YukiData.showhideplaylist())
    YukiData.showhideplaylistAction.setShortcut(kbd("key_t"))

    YukiData.showhidectrlpanelAction = qaction(_('showhidectrlpanel'), data)
    YukiData.showhidectrlpanelAction.triggered.connect(lambda: YukiData.lowpanel_ch_1())
    YukiData.showhidectrlpanelAction.setShortcut(kbd("lowpanel_ch_1"))

    YukiData.alwaysontopAction = qaction(_('alwaysontop'), data)
    YukiData.alwaysontopAction.triggered.connect(alwaysontop_action)
    YukiData.alwaysontopAction.setCheckable(True)
    YukiData.alwaysontopAction.setShortcut(kbd("alwaysontop"))
    if qt_library == 'PyQt6':
        YukiData.alwaysontopAction.setVisible(False)

    YukiData.streaminformationAction = qaction(_('Stream Information'), data)
    YukiData.streaminformationAction.triggered.connect(
        lambda: YukiData.open_stream_info()
    )
    YukiData.streaminformationAction.setShortcut(kbd("open_stream_info"))

    YukiData.showepgAction = qaction(_('tvguide'), data)
    YukiData.showepgAction.triggered.connect(
        lambda: YukiData.show_tvguide_2()
    )
    YukiData.showepgAction.setShortcut(kbd("show_tvguide_2"))

    YukiData.forceupdateepgAction = qaction(_('menubar_updateepg'), data)
    YukiData.forceupdateepgAction.triggered.connect(
        lambda: YukiData.force_update_epg()
    )
    YukiData.forceupdateepgAction.setShortcut(kbd("force_update_epg"))

    YukiData.applogAction = qaction(_('applog'), data)
    YukiData.applogAction.triggered.connect(lambda: YukiData.show_app_log())

    YukiData.mpvlogAction = qaction(_('mpvlog'), data)
    YukiData.mpvlogAction.triggered.connect(lambda: YukiData.show_mpv_log())

    # Options

    YukiData.sortAction = qaction(_('menubar_channelsort'), data)
    YukiData.sortAction.triggered.connect(lambda: YukiData.show_sort())
    YukiData.sortAction.setShortcut(kbd("show_sort"))

    YukiData.shortcutsAction = qaction('&' + _('shortcuts'), data)
    YukiData.shortcutsAction.triggered.connect(lambda: YukiData.show_shortcuts())

    YukiData.settingsAction = qaction(_('menubar_settings'), data)
    YukiData.settingsAction.triggered.connect(lambda: YukiData.show_settings())
    YukiData.settingsAction.setShortcut(kbd("show_settings"))

    # Help

    YukiData.aboutAction = qaction(_('menubar_about'), data)
    YukiData.aboutAction.triggered.connect(lambda: YukiData.show_help())

    # Empty (track list)
    YukiData.empty_action = qaction('<{}>'.format(_('empty_sm')), data)
    YukiData.empty_action.setEnabled(False)
    YukiData.empty_action1 = qaction('<{}>'.format(_('empty_sm')), data)
    YukiData.empty_action1.setEnabled(False)

    # Filters mapping
    YukiData.filter_mapping = {
        "vf::::::::lavfi=[pp]": YukiData.vf_postproc,
        "vf::::::::lavfi=[pp=vb/hb]": YukiData.vf_deblock,
        "vf::::::::lavfi=[pp=dr]": YukiData.vf_dering,
        "vf::::::::lavfi=[gradfun]": YukiData.vf_debanding,
        "vf::::::::lavfi=[noise=alls=9:allf=t]": YukiData.vf_noise,
        "vf::::::::__AST_VFBLACK__": YukiData.vf_black,
        "vf::::::::__AST_SOFTSCALING__": YukiData.vf_softscaling,
        "vf::::::::lavfi=[phase=A]": YukiData.vf_phase,
        "af::::::::lavfi=[extrastereo]": YukiData.af_extrastereo,
        "af::::::::lavfi=[stereotools=mlev=0.015625]": YukiData.af_karaoke,
        "af::::::::lavfi=[earwax]": YukiData.af_earvax,
        "af::::::::lavfi=[acompressor]": YukiData.af_volnorm
    }
    for vf_filter in YukiData.filter_mapping:
        YukiData.filter_mapping[vf_filter].triggered.connect(
            partial(apply_vf_filter, vf_filter, YukiData.filter_mapping[vf_filter])
        )
    return YukiData.alwaysontopAction

def populate_menubar(
    i, menubar, data, track_list=None, playing_chan=None,
    get_keybind=None
): # pylint: disable=too-many-statements, too-many-arguments, too-many-locals
    #print_with_time("populate_menubar called")
    # File

    if get_keybind:
        YukiData.get_keybind = get_keybind

    aot_action = None

    if not YukiData.menubar_ready:
        aot_action = init_menubar(data)
        YukiData.menubar_ready = True

    file_menu = menubar.addMenu(_('menubar_title_file'))
    file_menu.addAction(YukiData.playlists)
    file_menu.addSeparator()
    file_menu.addAction(YukiData.reloadPlaylist)
    file_menu.addAction(YukiData.forceupdateepgAction)
    file_menu.addSeparator()
    file_menu.addAction(YukiData.m3uEditor)
    file_menu.addAction(YukiData.exitAction)

    # Play

    play_menu = menubar.addMenu(_('menubar_title_play'))
    play_menu.addAction(YukiData.playpause)
    play_menu.addAction(YukiData.stop)
    play_menu.addSeparator()
    for sec in YukiData.secs:
        play_menu.addAction(sec)
    play_menu.addSeparator()

    speed_menu = play_menu.addMenu(_('speed'))
    speed_menu.addAction(YukiData.normalSpeed)
    for spd_action1 in YukiData.spds:
        speed_menu.addAction(spd_action1)
    play_menu.addSeparator()
    play_menu.addAction(YukiData.prevchannel)
    play_menu.addAction(YukiData.nextchannel)

    # Video

    video_menu = menubar.addMenu(_('menubar_video'))
    video_track_menu = video_menu.addMenu(_('menubar_track'))
    video_track_menu.clear()
    video_menu.addAction(YukiData.fullscreen)
    video_menu.addAction(YukiData.compactmode)
    video_menu.addAction(YukiData.csforchannel)
    YukiData.video_menu_filters = video_menu.addMenu(_('menubar_filters'))
    YukiData.video_menu_filters.addAction(YukiData.vf_postproc)
    YukiData.video_menu_filters.addAction(YukiData.vf_deblock)
    YukiData.video_menu_filters.addAction(YukiData.vf_dering)
    YukiData.video_menu_filters.addAction(YukiData.vf_debanding)
    YukiData.video_menu_filters.addAction(YukiData.vf_noise)
    YukiData.video_menu_filters.addAction(YukiData.vf_black)
    YukiData.video_menu_filters.addAction(YukiData.vf_softscaling)
    YukiData.video_menu_filters.addAction(YukiData.vf_phase)
    video_menu.addSeparator()
    video_menu.addAction(YukiData.screenshot)

    # Audio

    audio_menu = menubar.addMenu(_('menubar_audio'))
    audio_track_menu = audio_menu.addMenu(_('menubar_track'))
    audio_track_menu.clear()
    YukiData.audio_menu_filters = audio_menu.addMenu(_('menubar_filters'))
    YukiData.audio_menu_filters.addAction(YukiData.af_extrastereo)
    YukiData.audio_menu_filters.addAction(YukiData.af_karaoke)
    YukiData.audio_menu_filters.addAction(YukiData.af_earvax)
    YukiData.audio_menu_filters.addAction(YukiData.af_volnorm)
    audio_menu.addSeparator()
    audio_menu.addAction(YukiData.muteAction)
    audio_menu.addSeparator()
    audio_menu.addAction(YukiData.volumeMinus)
    audio_menu.addAction(YukiData.volumePlus)

    # View

    view_menu = menubar.addMenu(_('menubar_view'))
    view_menu.addAction(YukiData.showhideplaylistAction)
    view_menu.addAction(YukiData.showhidectrlpanelAction)
    view_menu.addAction(YukiData.alwaysontopAction)
    view_menu.addAction(YukiData.streaminformationAction)
    view_menu.addAction(YukiData.showepgAction)
    view_menu.addSection(_('logs'))
    view_menu.addAction(YukiData.applogAction)
    view_menu.addAction(YukiData.mpvlogAction)

    # Options

    options_menu = menubar.addMenu(_('menubar_options'))
    options_menu.addAction(YukiData.sortAction)
    options_menu.addSeparator()
    options_menu.addAction(YukiData.shortcutsAction)
    options_menu.addAction(YukiData.settingsAction)

    # Help

    help_menu = menubar.addMenu(_('menubar_help'))
    help_menu.addAction(YukiData.aboutAction)

    YukiData.menubars[i] = [video_track_menu, audio_track_menu]

    return aot_action

# Preventing memory leak
def clear_menu(menu):
    for mb_action in menu.actions():
        if mb_action.isSeparator():
            mb_action.deleteLater()
        #elif mb_action.menu():
        #    clear_menu(mb_action.menu())
        #    mb_action.menu().deleteLater()
        else:
            if mb_action.text() != '<{}>'.format(_('empty_sm')):
                mb_action.deleteLater()

def recursive_filter_setstate(state):
    for act in YukiData.video_menu_filters.actions():
        if not act.isSeparator(): #or act.menu():
            act.setEnabled(state)
    for act1 in YukiData.audio_menu_filters.actions():
        if not act1.isSeparator(): #or act1.menu():
            act1.setEnabled(state)

def get_first_run():
    return YukiData.first_run

def update_menubar(track_list, playing_chan, m3u, file, aot_file): # pylint: disable=too-many-branches, too-many-statements
    # Filters enable / disable
    if playing_chan:
        recursive_filter_setstate(True)
        #print(playing_chan + '::::::::::::::' + m3u)
        if not YukiData.first_run:
            YukiData.first_run = True
            print_with_time("YukiData.first_run")
            try:
                file_1 = open(file, 'r', encoding='utf-8')
                file_1_out = json.loads(file_1.read())['vf_filters']
                file_1.close()
                for dat in file_1_out:
                    if dat in YukiData.filter_mapping:
                        YukiData.filter_mapping[dat].setChecked(True)
                        apply_vf_filter(dat, YukiData.filter_mapping[dat])
            except: # pylint: disable=bare-except
                pass
    else:
        recursive_filter_setstate(False)
    # Always on top
    if not YukiData.first_run1:
        YukiData.first_run1 = True
        try:
            if os.path.isfile(aot_file):
                file_2 = open(aot_file, 'r', encoding='utf-8')
                file_2_out = file_2.read()
                file_2.close()
                aot_state = json.loads(file_2_out)["alwaysontop"]
                if aot_state:
                    YukiData.alwaysontopAction.setChecked(True)
                else:
                    YukiData.alwaysontopAction.setChecked(False)
        except: # pylint: disable=bare-except
            pass
    # Track list
    for i in YukiData.menubars:
        clear_menu(YukiData.menubars[i][0])
        clear_menu(YukiData.menubars[i][1])
        YukiData.menubars[i][0].clear()
        YukiData.menubars[i][1].clear()
        if track_list and playing_chan:
            if not [x for x in track_list if x['type'] == 'video']:
                YukiData.menubars[i][0].addAction(YukiData.empty_action)
            if not [x for x in track_list if x['type'] == 'audio']:
                YukiData.menubars[i][1].addAction(YukiData.empty_action1)
            for track in track_list:
                if track['type'] == 'video':
                    trk = qaction(str(track['id']), YukiData.data)
                    if track['id'] == YukiData.player.vid:
                        trk.setIcon(YukiData.circle_icon)
                    trk.triggered.connect(partial(ast_trackset, track['id'], 'vid'))
                    YukiData.menubars[i][0].addAction(trk)
                if track['type'] == 'audio':
                    trk1 = qaction(str(track['id']), YukiData.data)
                    if track['id'] == YukiData.player.aid:
                        trk1.setIcon(YukiData.circle_icon)
                    trk1.triggered.connect(partial(ast_trackset, track['id'], 'aid'))
                    YukiData.menubars[i][1].addAction(trk1)
        else:
            YukiData.menubars[i][0].addAction(YukiData.empty_action)
            YukiData.menubars[i][1].addAction(YukiData.empty_action1)

def init_yuki_iptv_menubar(data, app, menubar):
    YukiData.data = data

def init_menubar_player( # pylint: disable=too-many-arguments, too-many-locals
    player,
    mpv_play,
    mpv_stop,
    prev_channel,
    next_channel,
    mpv_fullscreen,
    showhideeverything,
    main_channel_settings,
    show_app_log,
    show_mpv_log,
    show_settings,
    show_help,
    do_screenshot,
    mpv_mute,
    showhideplaylist,
    lowpanel_ch_1,
    open_stream_info,
    app_quit,
    redraw_menubar,
    circle_icon,
    my_up_binding_execute,
    my_down_binding_execute,
    show_m3u_editor,
    show_playlists,
    show_sort,
    show_exception,
    get_curwindow_pos,
    force_update_epg,
    get_keybind,
    show_tvguide_2,
    enable_always_on_top,
    disable_always_on_top,
    reload_playlist,
    show_shortcuts,
    aot_file
):
    for func in locals().items():
        setattr(YukiData, func[0], func[1])
