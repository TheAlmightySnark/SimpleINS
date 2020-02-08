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
    1: 'de/philippmuenzel/xciva/cdu/1',
    2: 'de/philippmuenzel/xciva/cdu/1',
    3: 'de/philippmuenzel/xciva/cdu/2',
    4: 'de/philippmuenzel/xciva/cdu/3',
    6: 'de/philippmuenzel/xciva/cdu/4',
    7: 'de/philippmuenzel/xciva/cdu/5',
    8: 'de/philippmuenzel/xciva/cdu/6',
    10: 'de/philippmuenzel/xciva/cdu/7',
    11: 'de/philippmuenzel/xciva/cdu/8',
    12: 'de/philippmuenzel/xciva/cdu/9',
    15: 'de/philippmuenzel/xciva/cdu/0',
    '+': 'de/philippmuenzel/xciva/cdu/wayp_inc',
    '-': 'de/philippmuenzel/xciva/cdu/wayp_dec',
    'WPTCHG': 'de/philippmuenzel/xciva/cdu/wayp_change',
    16: 'de/philippmuenzel/xciva/cdu/insert',
    14: 'de/philippmuenzel/xciva/cdu/clear',
    'REMOTE': 'de/philippmuenzel/xciva/cdu/remote',
    '>': 'de/philippmuenzel/xciva/cdu/data_inc',
    '<': 'de/philippmuenzel/xciva/cdu/data_dec',
    'modeinc': 'de/philippmuenzel/xciva/msu/mode_inc',
    'modedec': 'de/philippmuenzel/xciva/msu/mode_dec',
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
