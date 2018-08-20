import http.client
import random
import string
import re

from urllib.parse import urlencode

"""
curl -i --insecure -X POST --data 'aimsid=001.2041048095.2218922818:744192305&t=a.galtsin%40corp.mail.ru&r=3jkjl23423424424&message="HelloWorld"' https://botapi.icq.net/im/sendIM
"""


class BotException(Exception):

    def __str__(self):
        return "Something is wrong ..."


class Bot:
    """
    Agent Mail.Ru Bot uses for internal communication
    """
    def __init__(self, token):
        self.url = 'https://botapi.icq.net/im/sendIM'
        self.debug = 0
        self.conn = http.client.HTTPSConnection("botapi.icq.net")

        self.data = {
            'aimsid':   token,
            't':        None,
            'message':  None,
            'mentions': None,
            'r':        None
        }

    def set_debug(self, debug=0):
        self.debug = debug

    def send_msg(self, to, message):
        self.data['r'] = self._get_request_sequence()
        self.data['message'] = message
        self.data['t'] = to

        mentions = re.findall('@\[(\w+)\]', message)

        if len(mentions):
            self.data['mentions'] = mentions[0]

        if self.debug:
            self.conn.set_debuglevel(1)

        self.conn.request("POST", self.url, urlencode(self.data),
                          {"Content-Type": "application/x-www-form-urlencoded"})
        resp = self.conn.getresponse()

        if resp.status != 200:
            raise BotException(resp.read().decode())

        if self.debug:
            print(resp.read().decode())

    def _get_request_sequence(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

    def work_bitch(self, to, uin):
        return self.send_msg(to, "@[" + str(uin) + "] Do something!")

