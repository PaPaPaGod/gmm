import smtplib
import urllib
from email.mime.text import MIMEText
from email.header import Header
from urllib import parse
from lxml import etree
from fake_useragent import UserAgent
import requests
import json

# fake_ua = UserAgent()


url = 'http://www.gmmsj.com/dy/89_zh.shtml'

area_url = 'http://www.gmmsj.com/gatew/CfgGW/getGameAreaGroupList?app_version=1.0.0.53327&device_id=K4lW2WaCuP0eYzY69THfpdCZxiGkuA0e&system_deviceId=K4lW2WaCuP0eYzY69THfpdCZxiGkuA0e&app_channel=chrome&src_code=7&game_id=89&type=area&count=1000'
base_goods_url = 'http://www.gmmsj.com/dy/89_zh/detail_{}.shtml'


class Mail:
    def __init__(self):
        self.mail_host = "smtp.qq.com"
        self.mail_pass = "mbbsapzkoxeedace"
        self.sender = '3375934400@qq.com'
        self.receivers = ['352619255@qq.com']


    def send(self):
        content = 'dn'
        message = MIMEText(content,'plain','utf-8')
        message['From'] = Header("cao",'utf-8')
        message['To'] = Header('heh','utf-8')
        subject =  'xxx'
        message['Subject'] = Header(subject,'utf-8')
        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host,465)
            smtpObj.login(self.sender,self.mail_pass)
            smtpObj.sendmail(self.sender,self.receivers,message.as_string())
            smtpObj.quit()
            print("发送成功")
        except smtplib.SMTPException as e:
            print("发送失败")


class GMM:
    def __init__(self):
        self.page = '1'
        self.p_job = '48'
        self.base_url = 'http://www.gmmsj.com/gatew/gmmGoodsGW/goodsList'




if __name__ == '__main__':
    gmm = GMM()
    # 搜索参数设置
    properties = {
        'p_job':gmm.p_job
    }
    properties = json.dumps(properties)
    p_new = properties.replace(' ','')
    # 区服参数调协
    area_id = {
        'area_id':gmm.area_id
    }
    area_id_list = [area_id]
    area_id_groups = json.dumps(area_id_list)
    area_id_groups = area_id_groups.replace(' ','')
    header ={
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Host':'www.gmmsj.com',
        'X-Requested-With':'XMLHttpRequest'
    }
    # 设置传参
    data = {
        'searchProperties':p_new,
        'src_code':7,
        'order_type':'modify_time',
        'order_dir':'d',
        'goods_types':10,
        'game_id':89,
        'area_id_groups':area_id_groups
    }
    response = requests.get(gmm.base_url,params=data)
    print(response.url)
