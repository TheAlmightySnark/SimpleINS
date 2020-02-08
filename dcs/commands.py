#ASCII decimal characters > to display
CIVACharDict = {
    0.0: ' ',
    32.0:' ',
    46.0:'.', #decimal character, always same spot, not always on
    48.0:'0',
    49.0:'1',
    50.0:'2',
    51.0:'3',
    52.0:'4',
    53.0:'5',
    54.0:'6',
    55.0:'7',
    56.0:'8',
    57.0:'9',
    65.0:'A', #special char
}

commandDict = {
    '1': 'cdu/1',
    '2': 'cdu/2',
    '3': 'cdu/3',
    '4': 'cdu/4',
    '5': 'cdu/5',
    '6': 'cdu/6',
    '7': 'cdu/7',
    '8': 'cdu/8',
    '9': 'cdu/9',
    '0': 'cdu/0',
    '+': 'cdu/wayp_inc',
    '-': 'cdu/wayp_dec',
    'WPTCHG': 'cdu/wayp_change',
    'INSERT': 'cdu/insert',
    'CLEAR': 'cdu/clear',
    'REMOTE': 'cdu/remote',
    '>': 'cdu/data_inc',
    '<': 'cdu/data_dec',
    'modeinc': 'msu/mode_inc',
    'modedec': 'msu/mode_dec',
}
RREF = b"RREF\x00"
datarefs = [
    #("sim/cockpit/radios/nav1_freq_hz"), #8 bytes, <f l'ittle endian in unpack 00 00 00 00 70 2d 46 becomes 11100(111.00nav1)
    ("de/philippmuenzel/xciva/cdu/display_right[0]", 0, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_right[1]", 1, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_right[2]", 2, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_right[3]", 3, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_right[4]", 4, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_right[5]", 5, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_right[6]", 6, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_right[7]", 7, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_left[0]", 8, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_left[1]", 9, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_left[2]", 10, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_left[3]", 11, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_left[4]", 12, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_left[5]", 13, 1, str), #string dataref
    ("de/philippmuenzel/xciva/cdu/display_left[6]", 14, 1, str), #string dataref
    # ("de/philippmuenzel/xciva/cdu/display_waypoint[0]", 15, 1, str), #
    # ("de/philippmuenzel/xciva/cdu/display_waypoint[1]", 16, 1, str), #
    # ("de/philippmuenzel/xciva/cdu/display_waypoint[2]", 17, 1, str), #
    # ("de/philippmuenzel/xciva/cdu/data_selector", 18, 1, int), #
    # ("de/philippmuenzel/xciva/msu/mode_selector", 19, 1, int),
    #CIVA datarefs
]


class Commands:
    def __init(self):
        print('[Commands.py] initialized')
