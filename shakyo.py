#!/usr/bin/env python
# -*- coding: utf-8 -*-

import curses
import locale
import time
import click


FRAME = [
    u'┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓',
    u'┃ ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │  │ ┃',
    u'┃ └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘ ┃',
    u'┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
]

HANNYA_SHINGYO = [
    u'摩訶般若波羅蜜多心経',
    u'観自在菩薩行深般若波羅蜜多時照見五',
    u'蘊皆空度一切苦厄舎利子色不異空空不',
    u'異色色即是空空即是色受想行識亦復如',
    u'是舎利子是諸法空相不生不滅不垢不浄',
    u'不増不減是故空中無色無受想行識無眼',
    u'耳鼻舌身意無色声香味触法無眼界乃至',
    u'無意識界無無明亦無無明尽乃至無老死',
    u'亦無老死尽無苦集滅道無智亦無得以無',
    u'所得故菩提薩埵依般若波羅蜜多故心無',
    u'罣礙無罣礙故無有恐怖遠離一切顛倒夢',
    u'想究竟涅槃三世諸仏依般若波羅蜜多故',
    u'得阿耨多羅三藐三菩提故知般若波羅蜜',
    u'多是大神咒是大明咒是無上咒是無等等',
    u'咒能除一切苦真実不虚故説般若波羅蜜',
    u'多咒即説咒曰',
    u'掲諦　掲諦　波羅掲諦　波羅僧掲諦',
    u'菩提薩婆訶　般若心経'
]
# quoted from : http://www.geocities.jp/tubamedou/Tandoku/Shinngyou2.htm


OVERALL_X = 4
OVERALL_Y = 1
INTERVAL = 0.07   # default (this can be overwritten by --interval option)
AFTER_SLEEP = 2
MOKUGYO = [u'Ω＼ζﾟ)', u'Ω |ζﾟ)']
MESSAGE = u'ﾁｰﾝ'
MOKUGYO_X = 60
MOKUGYO_Y = 21

locale.setlocale(locale.LC_ALL,'')
code = locale.getpreferredencoding()


def draw_frame(scr):
    y = 0
    for line in FRAME:
        scr.addstr(OVERALL_Y + y, OVERALL_X + 0, line.encode(code))
        y += 1
    scr.refresh()


def curses_main(scr, interval, typing, escape, noframe):
    curses.start_color()
    curses.use_default_colors()  # use default colors
    curses.curs_set(0)  # make the cursor invisible
    if not escape:
        curses.raw()

    if interval == None:
        interval = INTERVAL

    if typing:
        global OVERALL_Y
        global OVERALL_X
        scr.addstr(OVERALL_Y + MOKUGYO_Y, OVERALL_X + 26, 'Typing anythig...')
        scr.refresh()

    if not noframe:
        draw_frame(scr)

    MOKUGYO[0].encode(code)
    scr.addstr(OVERALL_Y + MOKUGYO_Y, OVERALL_X + MOKUGYO_X, \
      MOKUGYO[0].encode(code))
    scr.refresh()

    x = 60
    y = 2
    cnt = 1
    prev_key = None
    for s in HANNYA_SHINGYO:
        for uc in s:
            try:
                if typing:
                    curr_key = scr.getkey()
                    while prev_key == curr_key:
                        curr_key = scr.getkey()
                    prev_key = curr_key
                else:
                    time.sleep(interval)
                if uc != u'　':
                    scr.addstr(OVERALL_Y + y, OVERALL_X + x, uc.encode(code))
                    scr.addstr(OVERALL_Y + MOKUGYO_Y, OVERALL_X + MOKUGYO_X, \
                      MOKUGYO[cnt % len(MOKUGYO)].encode(code))
                scr.refresh()
                y += 1
                cnt += 1

            except KeyboardInterrupt:
                return  # exit

        x -= 3
        y = 2


    scr.addstr(OVERALL_Y + MOKUGYO_Y, OVERALL_X + MOKUGYO_X, \
      MOKUGYO[0].encode(code))
    msg_x = MOKUGYO_X
    while msg_x > 0:
        scr.addstr(OVERALL_Y + MOKUGYO_Y, msg_x, MESSAGE.encode(code))
        scr.refresh()
        time.sleep(float(AFTER_SLEEP) / float(MOKUGYO_X))
        scr.addstr(OVERALL_Y + MOKUGYO_Y, msg_x, ' ' * len(MESSAGE))
        msg_x -= 1

    curses.flushinp()



@click.command(help = 'Do "Shakyo" in your terminal.')
@click.option('--interval', '-i', type = float, help = 'Set the interval of \
outputting a character. (Default:' + str(INTERVAL) + ')')
@click.option('--typing', '-t', is_flag = True, help = 'Require typing any key \
to do shakyo.')
@click.option('--escape', '-e', is_flag = True, help = 'Allow you to exit by \
pushing Ctrl+C.')
@click.option('--noframe', '-n', is_flag = True, help = 'Do shakyo without \
frames.')
def main(interval, typing, escape, noframe):
    curses.wrapper(curses_main, interval, typing, escape, noframe)


if __name__ == '__main__':
    main()
