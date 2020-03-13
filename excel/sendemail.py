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

class Mail:
    def __init__(self):
        self.mail_host = "smtp.qq.com"
        self.mail_pass = "mbbsapzkoxeedace"
        self.sender = '3375934400@qq.com'
        self.receivers = ['352619255@qq.com']


    def send(self,content):
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
    def __init__(self,page,p_job,price,area_id):
        left = '[\"'
        right = '\"]'
        self.page = page
        self.p_job = left+p_job+right
        self.price = left+price[0]+'\",\"'+price[1]+right
        self.area_id = area_id
        self.base_url = 'http://www.gmmsj.com/gatew/gmmGoodsGW/goodsList'
        self.base_good_url = 'http://www.gmmsj.com/dy/89_zh/detail_{0}.shtml'
        self.base_good_detail_url = 'http://www.gmmsj.com/gmminf/accountapi/goods/'
        self.params = {
            "book_id":''
        }
        self.good_data = {
            'src_code':7,
            'method':'GetGoodsStatus',
            'params':self.params,
        }

    # "price": "[\"{p1}}\",\"{p2}\"]"

    def dispose(self,content):
        content = json.loads(content)
        list = content['data']
        goodList = list['goodsList']
        flag = False
        if(len(goodList)):
            for item in goodList:
                title = item['goods_list_title']
                price = item['price']+'元'
                book_id = item['book_id']
                self.params['book_id'] = book_id
                params = json.dumps(self.params)
                self.good_data['params'] = params
                # res1 = requests.get(self.base_good_detail_url, params=self.good_data)
                url = self.base_good_url.format(book_id)
                mail = Mail()
                response = requests.get(url)
                html = etree.HTML(response.text)
                i = 1
                content = 'No.'+ str(i) +'\t' +title +'\t'+price
                # content = 'No.'+ str(i) +'\t' +title +'\t'+price
                path = html.xpath('string(//div[@class="tab-content"]/div[@class="tab-pane active detail"]/section[@class="desc"])')
                if title.find('变换')>=0 and (path.find('头')>=0 or path.find('脚')>=0) :
                    path = path.replace(' ', '')
                    path = path.replace('\t', '')
                    path.strip('\n')
                    content = content+path + url
                    print(content)
                    # mail.send(content)
                # mail.send(content)

if __name__ == '__main__':
    gmm = GMM(1,'24',['5001','10000'],2)
    # 搜索参数设置
    properties = {
        'p_job':gmm.p_job,
        'price':gmm.price
    }
    properties = json.dumps(properties)
    # p_new = properties.replace(' ','')
    # 区服参数调协
    area_id = {
        'area_id':gmm.area_id
    }
    area_id_list = [area_id]
    area_id_groups = json.dumps(area_id_list)
    # area_id_groups = area_id_groups.replace(' ','')
    header ={
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'Host':'www.gmmsj.com',
        'X-Requested-With':'XMLHttpRequest'
    }
    # 设置传参
    data = {
        'searchProperties':properties,
        'src_code':7,
        'order_type':'modify_time',
        'order_dir':'d',
        'goods_types':10,
        'game_id':89,
        'area_id_groups':area_id_groups
    }
    response = requests.get(gmm.base_url,params=data)
    print(response.text)
    gmm.dispose(response.text)

