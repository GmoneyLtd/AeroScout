'''
helper function,get AP Message payload
'''


def get_D0_payload(pkt):
    payload = {
        'ap_mac_address': pkt[:6],
        'reserved': pkt[6:]
    }
    return payload


def get_D1_payload(pkt):
    payload = {
        'ap_mac_address': pkt[:6],
        'reserved': pkt[6:]
    }
    return payload


def get_D2_payload(pkt):
    payload = {
        'ap_mac_address': pkt[:6],
        'major_version': pkt[6:7],
        'minor_version': pkt[7:8],
        'reserved': pkt[8:]
    }
    return payload


def get_D4_payload(pkt):
    payload = {
        'ap_mac_address': pkt[:6],
        'vendor_id': pkt[6:8],
        'reserved1': pkt[8:10],
        'supported_features': pkt[10:12],
        'reserved2': pkt[12:14],
        'operational_mode': pkt[14:15],
        'reserved3': pkt[15:16],
        'bssid_g': pkt[16:22],
        'reserved4': pkt[22:24],
        'bssid_a': pkt[24:30],
        'error_code': pkt[30:31],
        'supported_radio': pkt[31:32],
        'main_g_channel': pkt[32:33],
        'main_a_channel': pkt[33:34],
        'reserved5': pkt[34:44],
        'additional_data': pkt[44:]
    }
    return payload


# Tag Reports
def get_D5_payload(pkt):
    payload = {
        'ap_mac_address': pkt[:6],
        'vendor_id': pkt[6:8],
        'reserved1': pkt[8:10],
        'bssid': pkt[10:16],
        'reserved2': pkt[16:17],
        '802.11b/g_channel': pkt[17:18],
        'timestamp': pkt[18:22],
        'resverved3': pkt[22:24],
        'rssi': pkt[24:25],
        'resverved4': pkt[25:26],
        'noise_floor': pkt[26:27],
        'resverved5': pkt[27:30],
        'data_rate': pkt[30:31],
        'resverved6': pkt[31:32],
        'tag_mac_address': pkt[32:38],
        'frame_control': pkt[38:40],
        'sequence_control': pkt[40:42],
        'resverved7': pkt[42:44],
        'tag_information': pkt[44:50],
        'extended_tag_information': pkt[50:56],
        'payload': pkt[56:]
    }
    return payload


# MU Reports
def get_D6_payload(pkt):
    payload = {
        'ap_mac_address': pkt[:6],
        'vendor_id': pkt[6:8],
        'reserved1': pkt[8:10],
        'bssid': pkt[10:16],
        'radio_type': pkt[16:17],
        'channel': pkt[17:18],
        'is_associated': pkt[18:19],
        'reserved2': pkt[19:20],
        'timestamp': pkt[20:24],
        'reserved3': pkt[24:26],
        'mu_type': pkt[26:27],
        'reserved4': pkt[27:28],
        'rssi': pkt[28:29],
        'reserved5': pkt[29:30],
        'noise_floor': pkt[30:31],
        'reserved6': pkt[31:34],
        'data_rate': pkt[34:35],
        'mpdu_flags': pkt[35:36],
        'mu_mac_address': pkt[36:42],
        'frame_control': pkt[42:44],
        'sequence_control': pkt[44:46],
        'reserved7': pkt[46:48]
    }
    return payload


def get_D7_payload(pkt):
    payload = {
        'ap_mac_address': pkt[:6],
        'vendor_id': pkt[6:8],
        'reserved1': pkt[8:10],
        'time_elapsed_since_last_debug_report': pkt[10:14],
        'supported_debug_elements': pkt[14:16],
        'reserved2': pkt[16:18],
        'number_of_tag_messages': pkt[18:22],
        'number_of_tag_adjacent_messages': pkt[22:26],
        'number_of_mu_messages': pkt[26:30],
        'number_of_tag_messages_dropped': pkt[30:34],
        'reserved3': pkt[34:144]
    }
    return payload


def get_D8_payload(pkt):
    payload = {
        'number_of_compounded_messages': pkt[:2],
        'reserved': pkt[2:4],
        'compounded_messages': pkt[4:],
        'ap_mac_address': pkt[12:18]
    }
    return payload


def get_D9_payload(pkt):
    payload = {
        'ap_mac_address': pkt[:6],
        'vendor_id': pkt[6:8],
        'reserved1': pkt[8:10],
        'flags': pkt[10:12],
        'reserved2': pkt[12:24],
        'data': pkt[24:]
    }
    return payload
