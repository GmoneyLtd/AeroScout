#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/7/6 5:30 PM
# @Author  : Jinlin
# @File    : main.py
# @Project : AreoScout


from message import *
from socketserver import *
import time

aps = {}


class ArubaAero(BaseRequestHandler):
    def handle(self):
        # print ap dict,get ap's request id and last message code.
        for k,v in aps.items():
            print(k.hex(),v[0],v[1].hex(),v[2],sep='|-:-|')
        try:
            while True:
                pkt = self.request[0]
                server = self.request[1]
                addr = self.client_address
                ap_msg = Msg(pkt)
                ap_msg.view()

                # update aps dict
                if aps.get(ap_msg.data_payload.get('ap_mac_address')) is None:
                    aps[ap_msg.data_payload.get('ap_mac_address')] = [addr, ap_msg.code, 0]
                elif aps[ap_msg.data_payload.get('ap_mac_address')][0] != addr:
                    aps[ap_msg.data_payload.get('ap_mac_address')] = [addr, ap_msg.code, 0]
                else:
                    pass

                # confirm send ae message
                if ap_msg.code == b'\xD9' and aps[ap_msg.data_payload.get('ap_mac_address')][1] == b'\xD9':
                    aps[ap_msg.data_payload.get('ap_mac_address')][2] += 1
                    set_msg = ap_msg.B0_pkt(aps[ap_msg.data_payload.get('ap_mac_address')][2])
                    server.sendto(set_msg, addr)
                    break

                elif ap_msg.code == b'\xD2' and aps[ap_msg.data_payload.get('ap_mac_address')][1] == b'\xD9':
                    aps[ap_msg.data_payload.get('ap_mac_address')][2] += 1
                    aps[ap_msg.data_payload.get('ap_mac_address')][1] = ap_msg.code
                    set_msg = ap_msg.B1_pkt(aps[ap_msg.data_payload.get('ap_mac_address')][2])
                    server.sendto(set_msg, addr)
                    break

                elif ap_msg.code == b'\xD4' and aps[ap_msg.data_payload.get('ap_mac_address')][1] == b'\xD2':
                    aps[ap_msg.data_payload.get('ap_mac_address')][2] += 1
                    aps[ap_msg.data_payload.get('ap_mac_address')][1] = ap_msg.code
                    set_msg = ap_msg.B2_pkt(aps[ap_msg.data_payload.get('ap_mac_address')][2])
                    server.sendto(set_msg, addr)
                    break

                elif ap_msg.code == b'\xD0' and aps[ap_msg.data_payload.get('ap_mac_address')][1] == b'\xD4':
                    aps[ap_msg.data_payload.get('ap_mac_address')][2] += 1
                    aps[ap_msg.data_payload.get('ap_mac_address')][1] = ap_msg.code
                    # MU Report start
                    set_msg = ap_msg.B4_pkt(aps[ap_msg.data_payload.get('ap_mac_address')][2])
                    # Tag Report Start,no testing ,may need to modefiy a 0xB2 code msg
                    # set_msg = ap_msg.B3_pkt(aps[ap_msg.data_payload.get('ap_mac_address')][2])
                    server.sendto(set_msg, addr)
                    break
                else:
                    aps[ap_msg.data_payload.get('ap_mac_address')][1] = ap_msg.code
                    break
        except Exception as msg:
            print(msg)


if __name__ == '__main__':
    host = ('0.0.0.0', 12092)

    server = UDPServer(host, ArubaAero)
    server.serve_forever()
