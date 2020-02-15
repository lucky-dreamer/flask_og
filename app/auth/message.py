import urllib.request,  sys
import ssl

#  短信验证码接口api

def check_number(code,phone):
    host = 'https://smsmsgs.market.alicloudapi.com'
    path = '/sms/'
    appcode = '6f3fa56e4a6745d98cc02c351610981b'
    querys = 'code='+str(code)+'&phone='+phone+'&skin=18&sign=175622'
    url = host + path + '?' + querys

    request = urllib.request.Request(url)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(request, context=ctx)
    content = response.read()
    if (content):
        return '验证码已发送，请注意查收，若未接受到，60秒后可再次发送'