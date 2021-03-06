import subprocess


class Key(str):
    def __add__(self, other):
        return Key("%s+%s" % (self, other))


VoidSymbol = Key('VoidSymbol')  # 0xFFFFFF	Does nothing
BackSpace = Key('BackSpace')  # 0xFF08	Erase the previous character, unlike loadkeys, Delete does not do the same thing
Tab = Key('Tab')  # 0xFF09
Linefeed = Key('Linefeed')  # 0xFF0A	Linefeed, LF
Clear = Key('Clear')  # 0xFF0B
Enter = Key('Return')  # Enter
Return = Key('Return')  # 0xFF0D	Return, enter
Pause = Key('Pause')  # 0xFF13	Pause, hold
Scroll_Lock = Key('Scroll_Lock')  # 0xFF14
Sys_Req = Key('Sys_Req')  # 0xFF15
Escape = Key('Escape')  # 0xFF1B
Delete = Key('Delete')  # 0xFFFF	Erase the character under the cursor. This is the same as Rubout in loadkeys.
Multi_key = Key('Multi_key')  # 0xFF20	Allows odd characters to be entered, in the same way as Compose in loadkeys
Codeinput = Key('Codeinput')  # 0xFF37	Kanji_Bangou is a synonym
SingleCandidate = Key('SingleCandidate')  # 0xFF3C
MultipleCandidate = Key('MultipleCandidate')  # 0xFF3D	Zen_Koho is a synonym
PreviousCandidate = Key('PreviousCandidate')  # 0xFF3E	Mae_Koho is a synonym
Home = Key('Home')  # 0xFF50
Left = Key('Left')  # 0xFF51	Move left, left arrow
Up = Key('Up')  # 0xFF52	Move up, up arrow
Right = Key('Right')  # 0xFF53	Move right, right arrow
Down = Key('Down')  # 0xFF54	Move down, down arrow
Prior = Key('Prior')  # 0xFF55	Prior, previous; Page_Up is a synonym
Next = Key('Next')  # 0xFF56	Next; Page_Down is a synonym
End = Key('End')  # 0xFF57	EOL
Begin = Key('Begin')  # 0xFF58	BOL
Select = Key('Select')  # 0xFF60	Select, mark
Print = Key('Print')  # 0xFF61
Execute = Key('Execute')  # 0xFF62	Execute, run, do
Insert = Key('Insert')  # 0xFF63	Insert, insert here
Undo = Key('Undo')  # 0xFF65	Undo, oops
Redo = Key('Redo')  # 0xFF66	redo, again
Menu = Key('Menu')  # 0xFF67
Find = Key('Find')  # 0xFF68	Find, search
Cancel = Key('Cancel')  # 0xFF69	Cancel, stop, abort, exit
Help = Key('Help')  # 0xFF6A	Help
Break = Key('Break')  # 0xFF6B
Mode_switch = Key(
    'Mode_switch')  # 0xFF7E	Shiftlevel two, giving access to the third and fourth columns of keysyms; script-, Greek-, Arabic-, kana-, Hangul- and Hebrew- _switch are synonyms
Num_Lock = Key('Num_Lock')  # 0xFF7F
KP_Space = Key('KP_Space')  # 0xFF80	space
KP_Tab = Key('KP_Tab')  # 0xFF89
KP_Enter = Key('KP_Enter')  # 0xFF8D	enter
KP_F1 = Key('KP_F1')  # 0xFF91	PF1, KP_A, ...
KP_F2 = Key('KP_F2')  # 0xFF92
KP_F3 = Key('KP_F3')  # 0xFF93
KP_F4 = Key('KP_F4')  # 0xFF94
KP_Home = Key('KP_Home')  # 0xFF95
KP_Left = Key('KP_Left')  # 0xFF96
KP_Up = Key('KP_Up')  # 0xFF97
KP_Right = Key('KP_Right')  # 0xFF98
KP_Down = Key('KP_Down')  # 0xFF99
KP_Prior = Key('KP_Prior')  # 0xFF9A	KP_Page_Up is a synonym
KP_Next = Key('KP_Next')  # 0xFF9B	KP_Page_Down is a synonym
KP_End = Key('KP_End')  # 0xFF9C
KP_Begin = Key('KP_Begin')  # 0xFF9D
KP_Insert = Key('KP_Insert')  # 0xFF9E
KP_Delete = Key('KP_Delete')  # 0xFF9F
KP_Equal = Key('KP_Equal')  # 0xFFBD	equals
KP_Multiply = Key('KP_Multiply')  # 0xFFAA
KP_Add = Key('KP_Add')  # 0xFFAB
KP_Separator = Key('KP_Separator')  # 0xFFAC	separator, often comma
KP_Subtract = Key('KP_Subtract')  # 0xFFAD
KP_Decimal = Key('KP_Decimal')  # 0xFFAE
KP_Divide = Key('KP_Divide')  # 0xFFAF
KP_0 = Key('KP_0')  # through 9	0xFFB0 through 0xFFB9
KP_1 = Key('KP_1')
KP_2 = Key('KP_2')
KP_3 = Key('KP_3')
KP_4 = Key('KP_4')
KP_5 = Key('KP_5')
KP_6 = Key('KP_6')
KP_7 = Key('KP_7')
KP_8 = Key('KP_8')
KP_9 = Key('KP_9')
F1 = Key(
    'F1')  # through 35	0xFFBE through 0xFFE0	F11 through 20 have synonyms L1 through 10; F21 through 35 have synonyms R1 through 15
F2 = Key('F2')
F3 = Key('F3')
F4 = Key('F4')
F5 = Key('F5')
F6 = Key('F6')
F7 = Key('F7')
F8 = Key('F8')
F9 = Key('F9')
F10 = Key('F10')
F11 = Key('F11')
F12 = Key('F12')
shift = Key('shift')  # shift
Shift_L = Key('Shift_L')  # 0xFFE1	Left shift
Shift_R = Key('Shift_R')  # 0xFFE2	Right shift
ctrl = Key('ctrl')  # control
control = Key('control')  # control
Control_L = Key('Control_L')  # 0xFFE3	Left control
Control_R = Key('Control_R')  # 0xFFE4	Right control
Caps_Lock = Key('Caps_Lock')  # 0xFFE5	Caps lock
Shift_Lock = Key('Shift_Lock')  # 0xFFE6	Shift lock
Meta_L = Key('Meta_L')  # 0xFFE7	Left meta
Meta_R = Key('Meta_R')  # 0xFFE8	Right meta
alt = Key('alt')  # alt
Alt_L = Key('Alt_L')  # 0xFFE9	Left alt
Alt_R = Key('Alt_R')  # 0xFFEA	Right alt
Super_L = Key('Super_L')  # 0xFFEB	Left super
Super_R = Key('Super_R')  # 0xFFEC	Right super
Hyper_L = Key('Hyper_L')  # 0xFFED	Left hyper
Hyper_R = Key('Hyper_R')  # 0xFFEE	Right hyper
dead_hook = Key('dead_hook')  # 0xFE61
dead_horn = Key('dead_horn')  # 0xFE62
space = Key('space')  # 0x020
exclam = Key('exclam')  # 0x021	!
quotedbl = Key('quotedbl')  # 0x022	"
numbersign = Key('numbersign')  # 0x023	#
dollar = Key('dollar')  # 0x024	$
percent = Key('percent')  # 0x025	%
ampersand = Key('ampersand')  # 0x026	&
apostrophe = Key('apostrophe')  # 0x027	'; quoteright is a deprecated synonym
parenleft = Key('parenleft')  # 0x028	(
parenright = Key('parenright')  # 0x029	)
asterisk = Key('asterisk')  # 0x02a	*
plus = Key('plus')  # 0x02b	+
comma = Key('comma')  # 0x02c	,
minus = Key('minus')  # 0x02d	-
period = Key('period')  # 0x02e	.
slash = Key('slash')  # 0x02f	/
_0 = Key('0')  # through 9	0x030 through 0x039
_1 = Key('1')
_2 = Key('2')
_3 = Key('3')
_4 = Key('4')
_5 = Key('5')
_6 = Key('6')
_7 = Key('7')
_8 = Key('8')
_9 = Key('9')
colon = Key('colon')  # 0x03a	:
semicolon = Key('semicolon')  # 0x03b	;
less = Key('less')  # 0x03c	<
equal = Key('equal')  # 0x03d	=
greater = Key('greater')  # 0x03e	>
question = Key('question')  # 0x03f	?
at = Key('at')  # 0x040	@
_A = Key('A')  # through Z	0x041 through 0x05a
_B = Key('B')
_C = Key('C')
_D = Key('D')
_E = Key('E')
_F = Key('F')
_G = Key('G')
_H = Key('H')
_I = Key('I')
_J = Key('J')
_K = Key('K')
_L = Key('L')
_M = Key('M')
_N = Key('N')
_O = Key('O')
_P = Key('P')
_Q = Key('Q')
_R = Key('R')
_S = Key('S')
_T = Key('T')
_U = Key('U')
_V = Key('V')
_W = Key('W')
_X = Key('X')
_Y = Key('Y')
_Z = Key('Z')
bracketleft = Key('bracketleft')  # 0x05b	[
backslash = Key('backslash')  # 0x05c	\
bracketright = Key('bracketright')  # 0x05d	]
asciicircum = Key('asciicircum')  # 0x05e	^
underscore = Key('underscore')  # 0x05f	_
grave = Key('grave')  # 0x060	`; quoteleft is a deprecated synonym
_a = Key('a')  # through z	0x061 through 0x07a
_b = Key('b')
_c = Key('c')
_d = Key('d')
_e = Key('e')
_f = Key('f')
_g = Key('g')
_h = Key('h')
_i = Key('i')
_j = Key('j')
_k = Key('k')
_l = Key('l')
_m = Key('m')
_n = Key('n')
_o = Key('o')
_p = Key('p')
_q = Key('q')
_r = Key('r')
_s = Key('s')
_t = Key('t')
_u = Key('u')
_v = Key('v')
_w = Key('w')
_x = Key('x')
_y = Key('y')
_z = Key('z')
braceleft = Key('braceleft')  # 0x07b	{
bar = Key('bar')  # 0x07c	|
braceright = Key('braceright')  # 0x07d	}
asciitilde = Key('asciitilde')  # 0x07e	~
nobreakspace = Key('nobreakspace')  # 0x0a0


def do_key(key):
    subprocess.call(["xdotool", "key", key])


def do_type(text):
    lines = str(text).split('/')
    for line in lines[:-1]:
        subprocess.call(["xdotool", "type", line])
        do_key(slash)
    subprocess.call(["xdotool", "type", lines[-1]])


def do(*args):
    for arg in args:
        if isinstance(arg, Key):
            do_key(arg)
        else:
            do_type(arg)
