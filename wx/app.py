#! -*- coding: utf-8 -*-


from flask import Flask, request
from wechatpy import WeChatClient
from wechatpy.parser import parse_message
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException


app = Flask(__name__)
wx_hook_token = 'forcemain'
wx_hook_app_id = 'wx4ba9027b49a44173'
wx_hook_secret = '2c3d0e1d6b5cd91f9926df4edd72da62'
wx_client_instance = WeChatClient(wx_hook_app_id, wx_hook_secret)


class Handler(object):
    def __init__(self, **kwargs):
        self.message = kwargs.get('message', '')
        self.client = kwargs.get('client', wx_client_instance)

    def text_handle(self):
        source = getattr(self.message, 'source')
        self.client.message.send_text(source, repr(self.message))

    def event_handle(self):
        source = getattr(self.message, 'source')
        self.client.message.send_text(source, repr(self.message))

    def default_handle(self):
        source = getattr(self.message, 'source')
        self.client.message.send_text(source, repr(self.message))

    def __call__(self, *args, **kwargs):
        print 'Got callback message: {0}'.format(self.message)
        {
            'text': self.text_handle,
            'event': self.event_handle,
            'default': self.default_handle,
        }.get(getattr(self.message, 'type'), self.default_handle)()

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@app.route('/hook/', methods=['GET', 'POST'])
def hook():
    if request.method == 'GET':
        try:
            check_signature(wx_hook_token,
                            request.args.get('signature'),
                            request.args.get('timestamp'),
                            request.args.get('nonce'))
        except InvalidSignatureException:
            return 'invalid signature', 400
        return request.args.get('echostr', ''), 200
    if request.method == 'POST':
        message = parse_message(request.data)
        handler = Handler.from_dict({'message': message})
        handler()
        return 'success', 200
    return 'method not allowed', 405


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
