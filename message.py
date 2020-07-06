#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/6 5:30 PM
# @Author  : Jinlin
# @File    : message.py
# @Project : AreoScout


from helper import *
import struct
from tabulate import tabulate

_code = {
    # AE Messages
    0xB0: {'val': 'Request LBS Protocol Version', 'sub_code': {0x00: None}},
    0xB1: {'val': 'Request AP Status', 'sub_code': {0x00: None}},
    0xB2: {'val': 'Set Configuration', 'sub_code': {0x00: None}},
    0xB3: {'val': 'Set Tags Mode',
           'sub_code': {0x01: 'Start reporting AeroScout Tag messages', 0x02: 'Stop reporting AeroScout Tag messages', 'other': 'Reserved'}},
    0xB4: {'val': 'Set MUs Mode', 'sub_code': {0x01: 'Start reporting MU messages', 0x02: 'Stop reporting MU messages', 'other': 'Reserved'}},
    0xB5: {'val': 'Request Debug Information', 'sub_code': {0x00: None}},

    # AP Messages
    0xD0: {'val': 'ACK', 'sub_code': {0x00: None}},
    0xD1: {'val': 'NACK', 'sub_code': {0x01: 'General Error', 0x02: 'Reserved', 0x03: 'Unknown Incoming AE Message', 0x04: 'Unsupported Request',
                                       0x05: 'Corrupted Message', 'other': 'Reserved'}},
    0xD2: {'val': 'LBS Protocol Version Report', 'sub_code': {0x00: None}},
    0xD4: {'val': 'AP Status Report', 'sub_code': {0x00: None}},
    0xD5: {'val': 'Tag Report', 'sub_code': {0x00: None}},
    0xD6: {'val': 'MU Report', 'sub_code': {0x00: None}},
    0xD7: {'val': 'AP Debug Report', 'sub_code': {0x00: None}},
    0xD8: {'val': 'Compounded Reports Message', 'sub_code': {0x00: None}},
    0xD9: {'val': 'Generic AP Notification', 'sub_code': {0x00: None}}
}

class Msg:
    name = 'AeroScout Protocol Data Unit Structure'

    def __init__(self, pkt):
        self.header = pkt[:2]
        self.request_id = pkt[2:4]
        self.code = pkt[4:5]
        self.sub_code = pkt[5:6]
        self.data_length = pkt[6:8]
        self.reports = None

        if self.code == b'\xD0':
            self.data_payload = get_D0_payload(pkt[8:])
        elif self.code == b'\xD1':
            self.data_payload = get_D1_payload(pkt[8:])
        elif self.code == b'\xD2':
            self.data_payload = get_D2_payload(pkt[8:])
        elif self.code == b'\xD4':
            self.data_payload = get_D4_payload(pkt[8:])
        elif self.code == b'\xD5':
            self.data_payload = get_D5_payload(pkt[8:])
        elif self.code == b'\xD6':
            self.data_payload = get_D6_payload(pkt[8:])
        elif self.code == b'\xD7':
            self.data_payload = get_D7_payload(pkt[8:])
        elif self.code == b'\xD8':
            self.data_payload = get_D8_payload(pkt[8:])
            self.reports = self.data_payload.get('compounded_messages')
            self.data_payload['compounded_messages'] = b''
        elif self.code == b'\xD9':
            self.data_payload = get_D9_payload(pkt[8:])
        else:
            self.data_payload = None

    def view(self):
        code_int, = struct.unpack('!B', self.code)
        sub_code_int, = struct.unpack('!B', self.sub_code)
        print('\033[1;35m{}  {}\033[0m'.format(_code.get(code_int).get('val'), _code.get(code_int).get('sub_code').get(sub_code_int)))

        tb_header = ['Header', 'Request ID', 'Code', 'Sub Code', 'Data Length']

        for key in self.data_payload.keys():
            if not key.startswith('reserved'):
                tb_header.append(key)

        # tb_header.extend(self.data_payload.keys())

        tb_data = [self.header, self.request_id, self.code, self.sub_code, self.data_length]

        for key in tb_header[5:]:
            tb_data.append(self.data_payload.get(key))

        tb_data = [data.hex() for data in tb_data]
        print(tabulate([tb_data], headers=tb_header, tablefmt='psql'))

        if self.reports != None:
            tb_mu_header = ['Header', 'Request ID', 'Code', 'Sub Code', 'Data Length']
            tb_tag_header = ['Header', 'Request ID', 'Code', 'Sub Code', 'Data Length']
            tb_mu_data = []
            tb_tag_data = []
            while self.reports:
                msg_length, = struct.unpack('!H', self.reports[6:8])
                msg_length += 8
                if self.reports[4:5] == b'\xD6':
                    mu_data = get_D6_payload(self.reports[8:msg_length])
                    mu = [self.reports[:2], self.reports[2:4], self.reports[4:5], self.reports[5:6], self.reports[6:8]]
                    mu.extend(mu_data.values())
                    mu = [val.hex() for val in mu]
                    tb_mu_data.append(mu)
                    self.reports = self.reports[msg_length:]
                else:
                    tag_data = get_D5_payload(self.reports[8:msg_length])
                    tag = [self.reports[:2], self.reports[2:4], self.reports[4:5], self.reports[5:6], self.reports[6:8]]
                    tag.extend(tag_data.values())
                    tag = [val.hex() for val in tag]
                    tb_tag_data.append(tag)
                    self.reports = self.reports[msg_length:]
            print('MU Reports....')
            try:
                tb_mu_header.extend(mu_data.keys())
                print(tabulate(tb_mu_data, headers=tb_mu_header, tablefmt='psql'))
            except:
                print('MU Reports NUll')
            print('Tag Reports....')
            try:
                tb_tag_header.extend(tag_data.keys())
                print(tabulate(tb_tag_data, headers=tb_tag_header, tablefmt='psql'))
            except:
                print('Tag Reports NUll')

    def B0_pkt(self, request_id):
        pkt = b''
        pkt += self.header
        pkt += struct.pack('!H', request_id)
        pkt += b'\xB0'
        pkt += b'\x00'
        pkt += b'\x00\x10'
        pkt += self.data_payload.get('ap_mac_address')
        pkt += bytes(2)
        pkt += bytes(4)
        pkt += bytes(2)
        pkt += bytes(2)

        return pkt

    def B1_pkt(self, request_id):
        pkt = b''
        pkt += self.header
        pkt += struct.pack('!H', request_id)
        pkt += b'\xB1'
        pkt += b'\x00'
        pkt += b'\x00\x10'
        pkt += self.data_payload.get('ap_mac_address')
        pkt += bytes(2)
        pkt += bytes(4)
        pkt += bytes(2)
        pkt += bytes(2)

        return pkt

    def B2_pkt(self, request_id):
        pkt = b''
        pkt += self.header
        pkt += struct.pack('!H', request_id)
        pkt += b'\xB2'
        pkt += b'\x00'
        pkt += b'\x00\x10'
        pkt += self.data_payload.get('ap_mac_address')
        pkt += bytes(2)
        pkt += bytes(4)
        pkt += bytes(2)
        pkt += bytes(6)     # Tag report multicas addr
        pkt += b'\x00\x0A'  # 1s update
        pkt += bytes(2)

        return pkt

    def B3_pkt(self, request_id, sub_code=1):
        pkt = b''
        pkt += self.header
        pkt += struct.pack('!H', request_id)
        pkt += b'\xB3'
        pkt += struct.pack('!B', sub_code)
        pkt += b'\x00\x10'
        pkt += self.data_payload.get('ap_mac_address')
        pkt += bytes(2)
        pkt += bytes(4)
        pkt += bytes(2)
        pkt += bytes(2)

        return pkt

    def B4_pkt(self, request_id, sub_code=1):
        pkt = b''
        pkt += self.header
        pkt += struct.pack('!H', request_id)
        pkt += b'\xB4'
        pkt += struct.pack('!B', sub_code)
        pkt += b'\x00\x18'
        pkt += self.data_payload.get('ap_mac_address')
        pkt += bytes(2)
        pkt += bytes(4)
        pkt += bytes(2)
        pkt += bytes(2)
        pkt += b'\x00\x00\x00\x64'
        pkt += b'\x00\x05'
        pkt += bytes(2)

        return pkt

    def B5_pkt(self, request_id):
        pkt = b''
        pkt += self.header
        pkt += struct.pack('!H', request_id)
        pkt += b'\xB5'
        pkt += b'\x00'
        pkt += b'\x00\x14'
        pkt += self.data_payload.get('ap_mac_address')
        pkt += bytes(2)
        pkt += bytes(4)
        pkt += bytes(2)
        pkt += bytes(6)

        return pkt
