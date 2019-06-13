# encoding: utf-8
'''
desc: U校园模拟登录&刷题
'''
import sys
sys.path.append("../")
import requests
from copy import deepcopy
import json
from bs4 import BeautifulSoup
import os   
import re
import hmac
import time
import hashlib
import random
from urllib.parse import quote
import config
import traceback
from urllib.request import urlretrieve
from fateadm_api import FateadmApi
import logging
path = os.path.dirname(__file__)
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(path+"\\log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Unipus:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }

    def __init__(self, app, username, password):
        self.logger = app.logger
        #self.logger = app 
        self.username = username
        self.password = password

        user_info_file_dir = os.path.join(os.path.dirname(__file__), 'user_info')
        if not os.path.exists(user_info_file_dir):
            os.makedirs(user_info_file_dir)
        user_info_file_templation = os.path.join(user_info_file_dir, '{}.json')
        self.user_info_file = user_info_file_templation.format(self.username)
        self.answer_data_file_templation = os.path.join(os.path.dirname(__file__), config.ANSWER_DATA_FILE)

    def login(self):
        '''
        desc: 登录
        '''
        self.logger.info('username: %s' % self.username)

        session = requests.Session()

        login_url = 'https://sso.unipus.cn/sso/0.1/sso/login'
        login_headers = deepcopy(self.headers)
        extend_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/json',
            'Origin': 'https://sso.unipus.cn',
            'Referer': 'https://sso.unipus.cn/sso/login?service=https%3A%2F%2Fu.unipus.cn%2Fuser%2Fcomm%2Flogin%3Fschool_id%3D',
        }
        login_headers = dict(self.headers, **extend_headers)
        data = {
            "service":"https://u.unipus.cn/user/comm/login?school_id=",
            "username":self.username,
            "password":self.password,
            "captcha":"",
            "rememberMe":"on",
            "captchaCode":""
        }
        login_req = session.post(login_url, headers=login_headers, data=json.dumps(data))
        if login_req.status_code<300 and 'Set-Cookie' in login_req.headers:

            self.logger.info('登录成功')

            login_json_data = json.loads(login_req.text)
            ticket = login_json_data['rs']['serviceTicket']
            self.openid = login_json_data['rs']['openid']

            # sso单点登陆

            self.logger.info('sso单点登录')

            sso_login_url = 'https://u.unipus.cn/user/comm/login?school_id=&ticket=%s' % ticket
            sso_login_headers = deepcopy(self.headers)
            sso_login_headers['Host'] = 'u.unipus.cn'
            sso_login_headers['Referer'] = 'https://sso.unipus.cn/sso/login?service=https%3A%2F%2Fu.unipus.cn%2Fuser%2Fstudent%3Fschool_id%3D'
            sso_login_req = session.get(sso_login_url, headers=sso_login_headers, allow_redirects=False)      
            
            sso_login_url = sso_login_req.headers['Location']
            sso_login_req = session.get(sso_login_url, headers=sso_login_headers, allow_redirects=False)
            user_index_url = sso_login_req.headers['Location']

            self.logger.info('sso单点登录成功')
            
            self.cookies = session.cookies.get_dict()  

            # 获取token和openid

            self.logger.info('获取token和openid')

            token_url = 'https://u.unipus.cn/user/data/getToken?_=%s' % (int(time.time()*1000))
            token_headers = deepcopy(self.headers)
            token_headers['Host'] = 'u.unipus.cn'
            token_headers['Referer'] = 'https://u.unipus.cn/user/student?school_id='
            token_req = requests.get(token_url, headers=token_headers, cookies=self.cookies, 
                allow_redirects=False)
            if token_req.status_code==200:
                json_data = json.loads(token_req.text)
                self.token = json_data['token']
                self.openid = json_data['openId']
                self.save_user_info()

                return True

            else:
                self.logger.error('未知错误，%s' % (
                        self.username, self.password, user_index_req.text
                    )
                )
                self.logger.error(traceback.format_exc())

                return False

        else:
            self.logger.error('登录失败，用户名或者密码错误') 

            return False

    def test_username_password(self):
        '''
        desc: 判断用户名、密码是否正确
        '''
        if not os.path.exists(self.user_info_file):
            self.logger.info('user_info不存在')
            return self.login()
        else:
            self.logger.info('加载user_info')
            with open(self.user_info_file, encoding='utf-8', mode='r') as fp:
                data = fp.read()
                user_info = json.loads(data)
                self.cookies = user_info['cookies']
                self.token = user_info['token']
                self.openid = user_info['openid']

            if self.test_user_info():
                self.logger.info('user_info可用')
                return True
            else:
                self.logger.error('user_info不可用')
                return self.login()

    def save_user_info(self):
        '''
        desc: 保存用户cookies、token、openid
        '''

        self.logger.info('保存用户cookies、token、openid')

        user_info = {
            'cookies': self.cookies,
            'token': self.token,
            'openid': self.openid
        }

        with open(self.user_info_file, encoding='utf-8', mode='w') as fp:
            fp.write(json.dumps(user_info))

    def load_user_info(self):
        '''
        desc: 加载用户cookies、token、openid
        '''

        self.logger.info('加载用户cookies、token、openid')

        if not os.path.exists(self.user_info_file):
            self.logger.warn('user_info不存在')
            self.login()
        else:
            self.logger.info('加载user_info')
            with open(self.user_info_file, encoding='utf-8', mode='r') as fp:
                data = fp.read()
                user_info = json.loads(data)
                self.cookies = user_info['cookies']
                self.token = user_info['token']
                self.openid = user_info['openid']

            if self.test_user_info():
                self.logger.info('user_info可用')
            else:
                self.logger.error('user_info不可用')
                self.login()

    def test_user_info(self):
        '''
        desc: 检验用户登陆信息可用性
        '''

        self.logger.info('检验用户登陆信息可用性')

        user_index_url = 'https://u.unipus.cn/user/student?school_id='
        user_index_headers = deepcopy(self.headers)
        user_index_headers['Host'] = 'u.unipus.cn'
        user_index_req = requests.get(user_index_url, headers=user_index_headers, cookies=self.cookies, 
            allow_redirects=False)
        if user_index_req.status_code<300:
            return True
        elif user_index_req.status_code==302:
            return False
        else:
            return False

    def get_course_list(self):
        '''
        desc: 获取所有课程信息，返回两个list，已激活课程list和未激活课程list
        '''

        self.logger.info('获取课程列表')

        while True:
            user_index_url = 'https://u.unipus.cn/user/student?school_id='
            user_index_headers = deepcopy(self.headers)
            user_index_headers['Host'] = 'u.unipus.cn'
            #user_index_req = requests.get(user_index_url, headers=user_index_headers, cookies=self.cookies, 
            #    allow_redirects=False)
            user_index_req = self.request_with_verification(user_index_url, headers=user_index_headers, cookies=self.cookies, 
                 allow_redirects=False)
            if user_index_req.status_code==200:
                break
            elif user_index_req.status_code==302:
                self.logger.warn('账号在另一台设备登录，重新登录')
                self.login()
                continue
            else:
                self.logger.error('username: %s, password: %s, 未知错误，%s' % (
                        self.username, self.password, user_index_req.text
                    )
                )
                self.logger.error(traceback.format_exc())
                return
        soup = BeautifulSoup(user_index_req.text, 'html.parser')
        my_course_lists = soup.find_all('div', attrs={'class': 'my_course_list'})
        if my_course_lists:
            my_course_list = my_course_lists[0]
            course_items = my_course_list.find_all('div', attrs={'class':'ite'})
            activated_course_list = []
            not_activated_course_list = []
            for course_item in course_items:
                course_info = {}
                if course_item.attrs.get('hastch', '')=='1':
                    course_info['status'] = 1
                    course_url = 'https://u.unipus.cn%s' % (
                            course_item.select('.hideurl')[0].text.replace(';', '')
                        )
                    course_id = self.get_course_id(course_url)
                    if course_id:
                        course_info['id'] = course_id
                        course_info['units'] = self.get_course_unit_list(course_id) 
                        course_info['name'] = course_item.select('.my_course_name')[0].text
                        activated_course_list.append(course_info)
                elif course_item.attrs.get('hastch', '')=='0':
                    course_info['status'] = 0
                    course_info['url'] = 'https://u.unipus.cn%s' % (
                            course_item.select('.hideurl')[0].text.replace(';', '')
                        )
                    course_info['name'] = course_item.select('.my_course_name')[0].text
                    not_activated_course_list.append(course_info)

        self.logger.info('获取课程列表成功')
        return activated_course_list, not_activated_course_list

    def get_course_id(self, course_url):
        '''
        desc: 获取course_id
        '''
        self.logger.info('获取课程id')
        
        course_headers = deepcopy(self.headers)
        
        retry_count=0
        while True:
            try:
                course_req = requests.get(course_url, headers=course_headers, cookies=self.cookies)
                if  'some thing not loaded' in course_req.text :
                    if retry_count>=3:
                        return None
                    retry_count=retry_count+1
                    self.logger.info('获取course_id: 出现验证码')
                    time.sleep(1)
                    captcha_req = requests.get('https://captcha.unipus.cn/captcha/v1/', headers=course_headers, cookies=self.cookies)
                    captcha_json=json.loads(captcha_req.text)
                    os.makedirs('./image/', exist_ok=True)
                    captcha_path=captcha_json['path']
                    IMAGE_URL = 'https://captcha.unipus.cn'+captcha_path
                    IMAGE_NAME='./image/'+captcha_path.replace('/','')+'.jpg'
                    urlretrieve(IMAGE_URL, IMAGE_NAME)
                    pd_id           = "111751"     
                    pd_key          = "LA4ut4p3fcC65MX/6MHiEklQyVj+us0W"
                    app_id          = "311751"     
                    app_key         = "PTcYetLt5PeW3kJtlacYf9fVUPq+b8Ge"
                    pred_type       = "50100"
                    api             = FateadmApi(app_id, app_key, pd_id, pd_key)
                    balance         = api.QueryBalcExtend()   # 直接返余额
                    if balance<1:
                        self.logger.info('打码平台余额不足' )
                        return None
                    else:
                        self.logger.info('上传验证码图片')
                        rsp             = api.PredictFromFileExtend(pred_type, IMAGE_NAME)  
                        self.logger.info('获取验证码图片打码结果: %s' % rsp)
                        duration_data = {
                            'answer': rsp
                        }
                        duration_req = requests.post(IMAGE_URL, headers=course_headers,data=json.dumps(duration_data),cookies=self.cookies)
                        print(duration_req.text)
                        if '成功' in duration_req.text:
                            self.logger.info('提交验证码成功')
                            time.sleep(1)
                            course_req = requests.get(course_url, headers=course_headers, cookies=self.cookies)
                            course_id = re.findall(r'course_id\s*\=\s*\"(.*?)\"', course_req.text)[0]
                            print('获取course_id:'+course_id)
                            self.logger.info('获取course_id: %s' % course_id)
                            return course_id
                else:
                    course_id = re.findall(r'course_id\s*\=\s*\"(.*?)\"', course_req.text)[0]
                    self.logger.info('获取course_id: %s' % course_id)
                    return course_id

            except Exception as e:

                self.logger.error('username: %s, password: %s, 获取course_id失败，exception: %s，course_url: %s，return_data: %s' % (
                        self.username, self.password, e, course_url, course_req.text
                    )
                )
                self.logger.error(traceback.format_exc())
                return None

    def get_course_unit_list(self, course_id):
        '''
        desc: 获取课程目单元列表
        '''
        self.logger.info('获取课程目录, course_id: %s' % course_id)

        course_catalog_url = 'https://ucontent.unipus.cn/course/api/course/%s/default/?jwtToken=%s' % (
                course_id,
                self.token
            )
        course_catalog_headers = deepcopy(self.headers)
        while True:
            try:
                #course_catalog_req = requests.get(course_catalog_url, headers=course_catalog_headers, 
                #    cookies=self.cookies)
                course_catalog_req = self.request_with_verification(course_catalog_url,headers=course_catalog_headers,
                    cookies=self.cookies)
                course_catalog_json_data = json.loads(json.loads(course_catalog_req.text)['course'])
                course_units_info = json.loads(json.loads(course_catalog_req.text)['course'])['units']
                course_units_list = []
                for course_unit_info in course_units_info:
                    course_units_list.append({
                            'unitName': '%s %s' % (
                                    course_unit_info.get('caption', ''),
                                    course_unit_info.get('name', ''),
                                ),
                            'unitId': course_unit_info.get('url', '')
                        })
                return course_units_list

            except Exception as e:
                self.logger.error('username: %s, password: %s,course_id: %s, exception: %s' % (
                        self.username, self.password, course_id, e
                    )
                )
                self.logger.error(traceback.format_exc())
                return []

    def get_course_unit_task_list(self, course_id, unit_id):
        '''
        desc: 获取课程单元的学习任务
        '''

        self.logger.info('获取课程单元的学习任务, course_id: %s, unit_id: %s' % (
                course_id,
                unit_id
            )
        )

        # 获取exercise_id
        course_catalog_url = 'https://ucontent.unipus.cn/course/api/course/%s/default/?jwtToken=%s' % (
                course_id,
                self.token
            )
        course_catalog_headers = deepcopy(self.headers)
        exercise_id_dict = {}
        while True:
            self.logger.info('获取具体课程单元的学习任务')
            time.sleep(3)
            try:
                #course_catalog_req = requests.get(course_catalog_url, headers=course_catalog_headers, 
                #    cookies=self.cookies,timeout=(3,7))
                course_catalog_req = self.request_with_verification(course_catalog_url,headers=course_catalog_headers,
                     cookies=self.cookies,timeout=(3,7))
                return_data = course_catalog_req.text.replace('\\\\\\n', '').replace('\\\\n', '').replace('\\', '')
                exercise_id_list = re.findall(r'[\'\"]exerciseId[\'\"]\s*:\s*[\'\"](\d+)[\'\"]', return_data)
                for i, exercise_id in enumerate(exercise_id_list):
                    exercise_id_dict['u%s'%(i+1)] = exercise_id
                break
            except Exception as e:
                self.logger.error('username: %s, password: %s,course_id: %s, exception: %s' % (
                        self.username, self.password, course_id, e
                    )
                )
                self.logger.error(traceback.format_exc())

        # 获取任务
        task_list = []
        course_unit_task_url = 'https://ucontent.unipus.cn/course/api/v2/course_progress/%s/%s/%s/default/?jwtToken=%s' % (
                course_id,
                unit_id,
                self.openid,
                self.token
            )
        course_unit_task_headers = deepcopy(self.headers)
        course_unit_task_headers['host'] = 'ucontent.unipus.cn'
        while True:
            try:
                #course_unit_task_req = requests.get(course_unit_task_url, headers=course_unit_task_headers,
                #    cookies=self.cookies)
                course_unit_task_req = self.request_with_verification(course_unit_task_url, headers=course_unit_task_headers,
                    cookies=self.cookies)
                course_unit_task_json_data = json.loads(course_unit_task_req.text)
                leafs = course_unit_task_json_data['rt']['leafs']
                for key, value in leafs.items():
                    if value['tab_type'] != 'ut':
                        task_list.append({
                                'task_id': key,
                                'task_type': value['tab_type']
                            })
                    elif exercise_id_dict.get(unit_id):
                        task_list.append({
                                'task_id': key,
                                'task_type': value['tab_type'],
                                'exercise_id': exercise_id_dict[unit_id]
                            })
                return task_list

            except Exception as e:
                self.logger.error('username: %s, password: %s, url: %s, return_data: %s, exception: %s' % (
                        self.username, self.password, course_unit_task_url, course_unit_task_req.text, e
                    )
                )
                self.logger.error(traceback.format_exc())
                return []

    def get_encrypt_str(self, to_encrypt_str):
        # sha256加密参数
        secret = b'y2WyF1*HP*5oEw@Pe37rqeeT7Ns3z1rqtwI!u9NsDncHHssJcAQ4WAjSXANDX4B5'
        encrypt_str = hmac.new(secret, bytes(str(to_encrypt_str), 'utf-8'), digestmod=hashlib.sha256).hexdigest()
        return encrypt_str

    def do_task(self, course_id, task, study_time):
        '''
        desc: 刷指定课程部分的题目，传入course_id为课程id，task包含url和name属性，study_time为学习时间
        '''
        task_id = task['task_id']
        task_type = task['task_type']

        def get_content_json_data(course_id, task_id):
            content_url = 'https://ucontent.unipus.cn/course/api/content/%s/%s/default/' % (
                    course_id, task_id
                )
            print('get_content_json_data for url '+content_url)
            extend_headers = {
                'Host': 'ucontent.unipus.cn',
                'Origin': 'https://ucontent.unipus.cn',
                'x-annotator-auth-token': self.token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Content-Type':'application/json',
                'Referer': 'https://ucontent.unipus.cn/_pc_default/pc.html?cid=',
            }
            content_headers = deepcopy(self.headers)
            content_headers = dict(content_headers, **extend_headers)
            while True:
                try:
                    #content_req = requests.get(content_url, headers=content_headers, cookies=self.cookies,timeout=(3,7))
                    content_req = self.request_with_verification(content_url, headers=content_headers, cookies=self.cookies,timeout=(3,7))
                    self.logger.info('get_content_json_data for content %s' % content_req.text)
                    #self.logger.info('get_content_json_data for content')
                    content_json_data = json.loads(content_req.text)
                    return json.loads(content_json_data['content'])
                except Exception as e:
                    self.logger.error('username: %s, password: %s, exception: %s, return_data: %s' % (
                                self.username, self.password, e, content_req.text
                            )
                        )
                    time.sleep(3)

        def get_summary_json_data(course_id, task_id):
            summary_url = 'https://ucontent.unipus.cn/course/api/pc/summary/%s/%s/default/' % (
                    course_id, task_id
                )
            extend_headers = {
                'Host': 'ucontent.unipus.cn',
                'Origin': 'https://ucontent.unipus.cn',
                'x-annotator-auth-token': self.token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Content-Type':'application/json',
                'Referer': 'https://ucontent.unipus.cn/_pc_default/pc.html?cid=',
            }
            print('get_summary_json_data for url '+summary_url)
            summary_headers = deepcopy(self.headers)
            summary_headers = dict(summary_headers, **extend_headers)
            while True:
                try:
                    #summary_req = requests.get(summary_url, headers=summary_headers, cookies=self.cookies,timeout=(3,7))
                    summary_req = self.request_with_verification(summary_url, headers=summary_headers, cookies=self.cookies,timeout=(3,7))
                    self.logger.info('get_summary_json_data for content %s' % summary_req.text)
                    ret = re.search('score',summary_req.text,re.I)
                    summary_json_data = json.loads(summary_req.text)
                    return summary_json_data['summary']
                except Exception as e:
                    self.logger.error('username: %s, password: %s, exception: %s, return_data: %s' % (
                                self.username, self.password, e, summary_req.text
                            )
                        )
                    time.sleep(3)

        def update_duration(course_id, task_id, delta, delta_consistency):
            '''
            desc: 伪造学习时长,由于1分钟只能请求3次，所以出现异常时sleep 1分钟
            '''
            duration_url = 'https://ucontent.unipus.cn/api/mobile/user_module/%s/%s/duration/' % (
                    course_id,
                    task_id
                )
            duration_headers = deepcopy(self.headers)
            extend_headers = {
                'Host': 'ucontent.unipus.cn',
                'Origin': 'https://ucontent.unipus.cn',
                'x-annotator-auth-token': self.token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Content-Type':'application/json',
                'Referer': 'https://ucontent.unipus.cn/_pc_default/pc.html?cid=',
            }
            duration_headers = dict(duration_headers, **extend_headers)
            duration_data = {
                'delta': delta,
                'deltaConsistency': delta_consistency,
                'version': 'default'
            }
            duration_req = requests.post(duration_url, headers=duration_headers, data=json.dumps(duration_data),
                cookies=self.cookies,verify=False,timeout=(3,7))
            self.logger.info('提交学习时长  %s' % duration_req.text)
            duration = 0
            if duration_req.status_code==503:
                self.logger.warn('请求受限，sleep 3秒')
                time.sleep(3)
                pass

            elif duration_req.text.strip() != 'failed':
                    try:
                        duration_json_data = json.loads(duration_req.text)
                        if duration_json_data['success']:
                            duration = duration_json_data['data']['duration']
                            if duration:
                                return True, duration
                    except Exception as e:
                        time
                        self.logger.error('username: %s, password: %s, exception: %s, return_data: %s' % (
                                self.username, self.password, e, duration_req.text
                            )
                        )
                        self.logger.error(traceback.format_exc())
            return False, duration


        # 刷学习时间

        self.logger.info('刷学习时长：%s秒' % study_time)

        #while True:
            #delta = study_time
            #delta_consistency = self.get_encrypt_str(delta)
            #flag, duration = update_duration(course_id, task_id, delta, delta_consistency)
            #self.logger.info('目前学习时长：%s秒' % duration)
            #if flag and duration>=study_time:
                # self.logger.info('目前学习时长：%s秒' % duration)
            #break

        
        if task_type != 'ut':   # 课程学习
            # 请求对应课程题目和答案

            self.logger.info('请求题目和答案')
            
            content_json_data = get_content_json_data(course_id, task_id)
            summary_json_data = get_summary_json_data(course_id, task_id)
                  
            # 直接构造分数请求
            extend_headers = {
                'Host': 'ucontent.unipus.cn',
                'Origin': 'https://ucontent.unipus.cn',
                'x-annotator-auth-token': self.token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                'Content-Type':'application/json',
                'Referer': 'https://ucontent.unipus.cn/_pc_default/pc.html?cid=',
            }
            submit_answer_headers = deepcopy(self.headers)
            submit_answer_headers = dict(submit_answer_headers, **extend_headers)
            # 分数概率
            score_rate = 0.9
            if task_type=='task' and summary_json_data['questionsList'] != []:
                submit_answer_url = 'https://ucontent.unipus.cn/api/mobile/user_group/%s/%s/progress/v2/' % (
                    course_id,
                    task_id
                )
                score_list = []
                for question in summary_json_data['questionsList']:
                    score_list.append(question['score'])
                score_consistency = self.get_encrypt_str(','.join(['%s.000' % score for score in score_list]))
                submit_answer_data = {
                        'courseSummary': {},
                        'score': score_list,
                        'scoreConsistency': score_consistency,
                        'signature': ['']*len(score_list),
                        'specificScores': [None]*len(score_list),
                        'version': 'default'
                    }
            else:
                submit_answer_url = 'https://ucontent.unipus.cn/api/mobile/user_group/%s/%s/progress/' % (
                    course_id,
                    task_id
                )
                submit_answer_data = {
                        'groupId': task_id,
                        'rid': "flowengine:studyStatus:2:%s" % task_id,
                        'status': 2,
                        'version': "default",
                    }
            self.logger.info('提交学习')
            while True:
                submit_answer_req = requests.post(submit_answer_url, headers=submit_answer_headers, 
                    data=json.dumps(submit_answer_data), cookies=self.cookies)
                if submit_answer_req.status_code==200:
                    submit_answer_json_data = json.loads(submit_answer_req.text)
                    if submit_answer_json_data.get('success'):
                        self.logger.info('学习完成')
                        break 
                    else:
                        self.logger.error('username: %s, password: %s, 学习失败，return_data: %s' % (
                            self.username, self.password, submit_answer_json_data
                        )
                    )
                        self.logger.error(traceback.format_exc())
                        time.sleep(2)
                # try:
                #     submit_answer_json_data = json.loads(submit_answer_req.text)
                #     if submit_answer_json_data.get('success'):
                #         self.logger.info('学习完成')
                #     else:
                #         self.logger.error('username: %s, password: %s, 学习失败，return_data: %s' % (
                #                 self.username, self.password, submit_answer_json_data
                #             )
                #         )
                # except Exception as e:
                #     self.logger.error('username: %s, password: %s, 学习失败, exception: %s, return_data: %s' % (
                #             self.username, self.password, e, submit_answer_req.text
                #         )
                #     ) 

        else:   # 课后习题
            task_id = task['task_id']
            exercise_id = task['exercise_id']
            answer_data_file = self.answer_data_file_templation.format(quote(course_id), task_id)
            if not os.path.exists(answer_data_file):
                self.logger.warn('test模块对应答案不存在')
                return

            target_cookies_dict = {}
            login_req_cookies = {}
            for key in ['SSOExpireTime', 'TGC', 'Y1vJ4IdorMglXdNk']:
                login_req_cookies[key] = self.cookies[key]

            # exercise
            self.logger.info('exercise')
            exercise_id = task['exercise_id']
            exercise_login_url = 'https://sso.unipus.cn/sso/login?service=%s' % \
                quote('https://uexercise.unipus.cn/itest/login?userId=null&_rp=%s' % \
                    quote('/uexercise/api/v2/enter_unit_test?exerciseId=%s&forwardUrl=%s&openId=%s&callbackUrl=%s' % (
                            exercise_id,
                            '%2F%2Fucontent.unipus.cn%2F_pc_default%2FUTCallback.html',
                            self.openid,
                            quote('http://ucontent.unipus.cn/course/api/utscore/%s/%s/default/&ntc=1&nad=1&sms=1&lcs=1&plf=0&sf=1' % (course_id, task_id))
                        )
                    )
                )
            exercise_login_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                'host': 'sso.unipus.cn'
            }
            #exercise_login_req = requests.get(exercise_login_url, headers=exercise_login_headers, cookies=login_req_cookies, allow_redirects=False)
            exercise_login_req = self.request_with_verification(exercise_login_url, headers=exercise_login_headers, cookies=login_req_cookies, allow_redirects=False)
            exercise_login_req_cookies = exercise_login_req.cookies.get_dict()
            for key in ['SSOExpireTime', 'Y1vJ4IdorMglXdNk', 'JSESSIONID', 'iTSsiD']:
                if key in exercise_login_req_cookies:
                    target_cookies_dict[key] = exercise_login_req_cookies[key]

            # ticket
            self.logger.info('ticket')
            ticket_url = exercise_login_req.headers['Location']
            ticket_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
                'host': 'uexercise.unipus.cn'
            }
            #ticket_req = requests.get(ticket_url, headers=ticket_headers, cookies=exercise_login_req_cookies, allow_redirects=False)
            ticket_req = self.request_with_verification(ticket_url, headers=ticket_headers, cookies=exercise_login_req_cookies, allow_redirects=False)
            ticket_req_cookies = ticket_req.cookies.get_dict()
            for key in ['SSOExpireTime', 'Y1vJ4IdorMglXdNk', 'JSESSIONID', 'iTSsiD']:
                if key in ticket_req_cookies:
                    target_cookies_dict[key] = ticket_req_cookies[key]

            # dataid
            self.logger.info('dataid')
            enter_unit_test_url = 'https://uexercise.unipus.cn/uexercise/api/v2/enter_unit_test?exerciseId={}&forwardUrl=%2F%2Fucontent.unipus.cn%2F_pc_default%2FUTCallback.html&openId={}&callbackUrl=http%3A%2F%2Fucontent.unipus.cn%2Fcourse%2Fapi%2Futscore%2F{}%2F{}%2Fdefault%2F&ntc=0&nad=0&sms=1&lcs=0&plf=0&sf=1'.format(
                    exercise_id, self.openid, quote(course_id), task_id
                )
            enter_unit_test_headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
            }

            enter_unit_test_cookies = dict(target_cookies_dict, **login_req_cookies)

            #enter_unit_test_req = requests.get(enter_unit_test_url, headers=enter_unit_test_headers, cookies=enter_unit_test_cookies)
            enter_unit_test_req = self.request_with_verification(enter_unit_test_url, headers=enter_unit_test_headers, cookies=enter_unit_test_cookies)
            soup1 = BeautifulSoup(enter_unit_test_req.text, 'html.parser')
            dataid_obj = soup1.find('input', attrs={'id': 'dataid'})
            # if not dataid_obj:
            #     self.logger.error('username: %s, password: %s, 刷test模块失败，获取dataid失败' % (
            #             self.username, self.password
            #         ))
            #     return

            dataid = dataid_obj.get('value')
            self.logger.info('dataid-%s' % dataid)

            # 获取题目、答案、构造答案完成test模块
            def get_origin_answer(answer_url):
                # 获取试卷答案
                self.logger.info('get_origin_answer')
                answer_headers = deepcopy(self.headers)
                #answer_req = requests.get(answer_url, headers=answer_headers, cookies=target_cookies_dict)
                answer_req = self.request_with_verification(answer_url, headers=answer_headers, cookies=target_cookies_dict)
                soup1 = BeautifulSoup(answer_req.text, 'html.parser')
                all_answer_list = []
                for test_div in soup1.find_all('div', attrs={'class': 'Test'}):
                    answer_list = []
                    opt_list = [chr(ord('A')+i) for i in range(0, 26)]
                    for answer_tag in test_div.find_all(text='参考答案：'):
                        # a_answer_list = re.split(r'\s*\d+\)\s*', re.sub(r'\s+', '', answer_tag.parent.parent.next_sibling.text))
                        a_answer_list = re.split(r'\s*\d+\)\s*', answer_tag.parent.parent.next_sibling.text)
                        a_answer_list = [item.strip() for item in a_answer_list]
                        if a_answer_list:
                            a_answer_list = [ord(a_answer_list[i])-ord('A') if a_answer_list[i] in opt_list \
                                else a_answer_list[i] for i in range(1, len(a_answer_list))]
                            answer_list.append(a_answer_list)
                    all_answer_list.append(answer_list)
                return all_answer_list

            def get_ut(dataid, all_answer_list):
                self.logger.info('get_ut')
                # 获取题目，构造答案参数，传入all_answer_list为空时答案全都为0
                correct_rate = 0.9  # 90%正确性
                load_ut_url = 'https://uexercise.unipus.cn/itest/s/clsanswer/loadUT'
                load_ut_headers = deepcopy(self.headers)
                load_ut_headers['Origin'] = 'https://uexercise.unipus.cn'
                load_ut_data = {
                    'dataid': dataid
                }
                load_ut_req = requests.post(load_ut_url, headers=load_ut_headers, cookies=target_cookies_dict, data=load_ut_data)
                load_ut_json_data = json.loads(load_ut_req.text)
                answer_data_al_list = []
                answer_data_sl_list = []
                if load_ut_json_data.get('code')==1:
                    soup2 = BeautifulSoup(load_ut_json_data['data']['C_HTML'], 'html.parser')
                    itest_section_list = soup2.find_all('div', attrs={'class': 'itest-section'})
                    for i, itest_section in enumerate(itest_section_list):
                        # answer_data_sl
                        answer_data_sl_list.append({
                            'sid': itest_section.get('sectionid', ''),
                            'rnp': '1'
                        })

                        # answer_data_al
                        for j, itest_ques_set in enumerate(itest_section.find_all('div', attrs={'class', 'itest-ques-set'})):
                            answer_data_al_d = []
                            answer_data_al_o = []
                            question_list = itest_ques_set.find_all(qid=re.compile('\d+'))
                            tmp_list = []
                            index = 0
                            while index < len(question_list):
                                question = question_list[index]
                                q_type = question.get('type')
                                qid = question.get('qid')
                                qoo = json.loads(question.get('qoo', '[]'))
                                tmp_list.append({
                                    'qid': qid,
                                    'qoo': qoo
                                })
                                if q_type=='radio':
                                    index += len(qoo)
                                elif q_type=='text':
                                    index += 1

                            if all_answer_list: # 答案不为空
                                for answer, item in zip(all_answer_list[i][j], tmp_list):
                                    if random.random()<correct_rate:
                                        answer_data_al_d.append([answer])
                                    else:
                                        answer_data_al_d.append([0])
                                    answer_data_al_o.append([item['qoo']])
                                    answer_data_al_q = item['qid']
                            else:   # 答案为空
                                for item in tmp_list:
                                    answer_data_al_d.append([0])
                                    answer_data_al_o.append([item['qoo']])
                                    answer_data_al_q = item['qid']


                            answer_data_al_list.append({
                                'q': answer_data_al_q,
                                'rnp': 1,
                                'f': '',
                                'vl': '',
                                'd': answer_data_al_d,
                                'o': answer_data_al_o
                            })
                answer_data = {
                    'al': answer_data_al_list,
                    'sl': answer_data_sl_list,
                    'ut':0
                }
                return answer_data

            def submit_ut(dataid, exercise_id, answer_data, is_get_answer):
                self.logger.info('submit_ut')
                # 提交答案, is_get_answer为true则返回答案链接，若为false则直接提交答案
                submit_ut_url = 'https://uexercise.unipus.cn/itest/s/clsanswer/submitUT'
                submit_ut_headers = {}
                submit_ut_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
                submit_ut_data = {
                    "ansData": json.dumps(answer_data),
                    "act": 'save',
                    "sppid": dataid,
                    "exerciseId": exercise_id,
                }
                submit_ut_req = requests.post(submit_ut_url, headers=submit_ut_headers, cookies=target_cookies_dict, data=submit_ut_data)
                submit_ut_json_data = json.loads(submit_ut_req.text)
                if submit_ut_json_data.get('code')==1 and '本次共完成' in submit_ut_json_data.get('msg'):
                    if not is_get_answer:
                        self.logger.info('获取答案链接')
                        soup2 = BeautifulSoup(submit_ut_json_data.get('msg'), 'html.parser')
                        answer_url = 'https://uexercise.unipus.cn' + soup2.find("div", attrs={"class": "ckdaSubmit"}).get('qa')
                        return answer_url
                    else:
                        soup2 = BeautifulSoup(submit_ut_json_data.get('msg'), 'html.parser')
                        self.logger.info(soup2.find('span', attrs={'class': 'green'}).text)
                        self.logger.info('test模块完成')
                else:
                    self.logger.info('test模块失败, %s' % submit_ut_json_data)
                    return None

            # 从本地加载答案并提交
            self.logger.info('本地加载答案')
            with open(answer_data_file, encoding='utf-8', mode='r') as fp:
                origin_answer_data = json.loads(fp.read())
                answer_data = get_ut(dataid, origin_answer_data)
                submit_ut(dataid, exercise_id, answer_data, True)

    def learn_for_unit(self, course_id, unit_id, study_time):
        '''
        desc: 完成单元学习
        '''

        self.logger.info('完成单元学习, course_id: %s, unit_id: %s, study_time: %s' % (
                course_id,
                unit_id,
                study_time
            )
        )

        try:
            task_list = self.get_course_unit_task_list(course_id, unit_id)
            average_study_time = int(study_time/len(task_list))
            flag = True
            for i,task in enumerate(task_list):
                self.logger.info('【%s/%s】' % (i+1, len(task_list)))
                retry_times = 3
                while retry_times:
                    try:
                        self.do_task(course_id, task, average_study_time+random.randint(-10, 10))
                        break
                    except Exception as e:
                        self.logger.error(e)
                        self.logger.error(traceback.format_exc())
                        retry_times -= 1
                        self.login()
                        continue
                if not retry_times:
                    flag = False
            return flag

        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
            return False

    def learn_for_all_unit(self, course_id, study_time):
        '''
        desc: 完成整个课程学习
        '''
        print('完成整个课程学习')
        self.logger.info('完成整个课程学习')
        try:
            all_task_list = []
            unit_list = self.get_course_unit_list(course_id)
            for unit in unit_list:
                unit_id = unit['unitId']
                task_list = self.get_course_unit_task_list(course_id, unit_id)
                for task in task_list:
                    all_task_list.append(task)
            average_study_time = int(study_time/len(all_task_list))
            flag = True
            for i,task in enumerate(all_task_list):
                self.logger.info('【%s/%s】' % (i+1, len(all_task_list)))
                retry_times = 3
                while retry_times:
                    try:
                        self.do_task(course_id, task, average_study_time+random.randint(-10, 10))
                        break
                    except Exception as e:
                        self.logger.error(e)
                        self.logger.error(traceback.format_exc())
                        retry_times -= 1
                        self.login()
                        continue
                if not retry_times:
                    flag = False
            return flag

        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
            return False

    def download_test_answer_for_course(self, course_id):
        '''
        desc: 下载指定课程所有test模块的答案
        '''
        self.logger.info('完成course_id:%s课程test模块答案下载' % course_id)

        try:
            all_task_list = []
            unit_list = self.get_course_unit_list(course_id)
            for unit in unit_list:
                unit_id = unit['unitId']
                task_list = self.get_course_unit_task_list(course_id, unit_id)
                for task in task_list:
                    if task['task_type'] == 'ut':
                        all_task_list.append(task)
            # 不存在test模块
            if not all_task_list:
                return 0, '不存在test模块'
            code = 1
            for i,task in enumerate(all_task_list):
                self.logger.info('【%s/%s】' % (i+1, len(all_task_list)))
                self.logger.info('download_test_answer')
                flag, msg = self.download_test_answer(course_id, task)
                if not flag:
                    code = 0
            if code==1:
                return 1, '下载test模块答案成功'
            else:
                return 0, 'test模块答案部分下载失败'

        except Exception as e:
            self.logger.error(e)
            self.logger.error(traceback.format_exc())
            return -1, str(e)

    def download_test_answer(self, course_id, task):
        '''
        desc: 下载指定课程指定test模块答案
        '''
        task_id = task['task_id']
        exercise_id = task['exercise_id']

        answer_data_file = self.answer_data_file_templation.format(quote(course_id), task_id)
        if os.path.exists(answer_data_file):
            self.logger.info('test模块答案已存在')
            return True, 'test模块答案已存在'

        target_cookies_dict = {}
        login_req_cookies = {}
        for key in ['SSOExpireTime', 'TGC', 'Y1vJ4IdorMglXdNk']:
            login_req_cookies[key] = self.cookies[key]

        # exercise
        self.logger.info('exercise')
        exercise_id = task['exercise_id']
        exercise_login_url = 'https://sso.unipus.cn/sso/login?service=%s' % \
            quote('https://uexercise.unipus.cn/itest/login?userId=null&_rp=%s' % \
                quote('/uexercise/api/v2/enter_unit_test?exerciseId=%s&forwardUrl=%s&openId=%s&callbackUrl=%s' % (
                        exercise_id,
                        '%2F%2Fucontent.unipus.cn%2F_pc_default%2FUTCallback.html',
                        self.openid,
                        quote('http://ucontent.unipus.cn/course/api/utscore/%s/%s/default/&ntc=1&nad=1&sms=1&lcs=1&plf=0&sf=1' % (course_id, task_id))
                    )
                )
            )
        exercise_login_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'host': 'sso.unipus.cn'
        }
        #exercise_login_req = requests.get(exercise_login_url, headers=exercise_login_headers, cookies=login_req_cookies, allow_redirects=False)
        exercise_login_req = self.request_with_verification(exercise_login_url, headers=exercise_login_headers, cookies=login_req_cookies, allow_redirects=False)
        exercise_login_req_cookies = exercise_login_req.cookies.get_dict()
        for key in ['SSOExpireTime', 'Y1vJ4IdorMglXdNk', 'JSESSIONID', 'iTSsiD']:
            if key in exercise_login_req_cookies:
                target_cookies_dict[key] = exercise_login_req_cookies[key]

        # ticket
        self.logger.info('ticket')
        ticket_url = exercise_login_req.headers['Location']
        ticket_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'host': 'uexercise.unipus.cn'
        }
        #ticket_req = requests.get(ticket_url, headers=ticket_headers, cookies=exercise_login_req_cookies, allow_redirects=False)
        ticket_req = self.request_with_verification(ticket_url, headers=ticket_headers, cookies=exercise_login_req_cookies, allow_redirects=False)
        ticket_req_cookies = ticket_req.cookies.get_dict()
        for key in ['SSOExpireTime', 'Y1vJ4IdorMglXdNk', 'JSESSIONID', 'iTSsiD']:
            if key in ticket_req_cookies:
                target_cookies_dict[key] = ticket_req_cookies[key]

        # dataid
        self.logger.info('dataid')
        enter_unit_test_url = 'https://uexercise.unipus.cn/uexercise/api/v2/enter_unit_test?exerciseId={}&forwardUrl=%2F%2Fucontent.unipus.cn%2F_pc_default%2FUTCallback.html&openId={}&callbackUrl=http%3A%2F%2Fucontent.unipus.cn%2Fcourse%2Fapi%2Futscore%2F{}%2F{}%2Fdefault%2F&ntc=0&nad=0&sms=1&lcs=0&plf=0&sf=1'.format(
                exercise_id, self.openid, quote(course_id), task_id
            )
        enter_unit_test_headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        }

        enter_unit_test_cookies = dict(target_cookies_dict, **login_req_cookies)

        #enter_unit_test_req = requests.get(enter_unit_test_url, headers=enter_unit_test_headers, cookies=enter_unit_test_cookies)
        enter_unit_test_req = self.request_with_verification(enter_unit_test_url, headers=enter_unit_test_headers, cookies=enter_unit_test_cookies)
        soup1 = BeautifulSoup(enter_unit_test_req.text, 'html.parser')
        dataid_obj = soup1.find('input', attrs={'id': 'dataid'})
        if not dataid_obj:
            self.logger.error('username: %s, password: %s, 刷test模块失败，获取dataid失败' % (
                    self.username, self.password
                ))
            self.logger.error(traceback.format_exc())
            return

        dataid = dataid_obj.get('value')
        self.logger.info('dataid-%s' % dataid)

        # 获取题目、答案、构造答案完成test模块
        def get_origin_answer(answer_url):
            # 获取试卷答案
            self.logger.info('get_origin_answer')
            answer_headers = deepcopy(self.headers)
            #answer_req = requests.get(answer_url, headers=answer_headers, cookies=target_cookies_dict)
            answer_req = self.request_with_verification(answer_url, headers=answer_headers, cookies=target_cookies_dict)
            soup1 = BeautifulSoup(answer_req.text, 'html.parser')
            all_answer_list = []
            for test_div in soup1.find_all('div', attrs={'class': 'Test'}):
                answer_list = []
                opt_list = [chr(ord('A')+i) for i in range(0, 26)]
                for answer_tag in test_div.find_all(text='参考答案：'):
                    # a_answer_list = re.split(r'\s*\d+\)\s*', re.sub(r'\s+', '', answer_tag.parent.parent.next_sibling.text))
                    a_answer_list = re.split(r'\s*\d+\)\s*', answer_tag.parent.parent.next_sibling.text)
                    a_answer_list = [item.strip() for item in a_answer_list]
                    if a_answer_list:
                        a_answer_list = [ord(a_answer_list[i])-ord('A') if a_answer_list[i] in opt_list \
                            else a_answer_list[i] for i in range(1, len(a_answer_list))]
                        answer_list.append(a_answer_list)
                all_answer_list.append(answer_list)
            return all_answer_list

        def get_ut(dataid, all_answer_list):
            self.logger.info('get_ut')
            # 获取题目，构造答案参数，传入all_answer_list为空时答案全都为0
            correct_rate = 0.9  # 90%正确性
            load_ut_url = 'https://uexercise.unipus.cn/itest/s/clsanswer/loadUT'
            load_ut_headers = deepcopy(self.headers)
            load_ut_headers['Origin'] = 'https://uexercise.unipus.cn'
            load_ut_data = {
                'dataid': dataid
            }
            load_ut_req = requests.post(load_ut_url, headers=load_ut_headers, cookies=target_cookies_dict, data=load_ut_data)
            load_ut_json_data = json.loads(load_ut_req.text)
            answer_data_al_list = []
            answer_data_sl_list = []
            if load_ut_json_data.get('code')==1:
                soup2 = BeautifulSoup(load_ut_json_data['data']['C_HTML'], 'html.parser')
                itest_section_list = soup2.find_all('div', attrs={'class': 'itest-section'})
                for i, itest_section in enumerate(itest_section_list):
                    # answer_data_sl
                    answer_data_sl_list.append({
                        'sid': itest_section.get('sectionid', ''),
                        'rnp': '1'
                    })

                    # answer_data_al
                    for j, itest_ques_set in enumerate(itest_section.find_all('div', attrs={'class', 'itest-ques-set'})):
                        answer_data_al_d = []
                        answer_data_al_o = []
                        question_list = itest_ques_set.find_all(qid=re.compile('\d+'))
                        tmp_list = []
                        index = 0
                        while index < len(question_list):
                            question = question_list[index]
                            q_type = question.get('type')
                            qid = question.get('qid')
                            qoo = json.loads(question.get('qoo', '[]'))
                            tmp_list.append({
                                'qid': qid,
                                'qoo': qoo
                            })
                            if q_type=='radio':
                                index += len(qoo)
                            elif q_type=='text':
                                index += 1

                        if all_answer_list: # 答案不为空
                            for answer, item in zip(all_answer_list[i][j], tmp_list):
                                if random.random()<correct_rate:
                                    answer_data_al_d.append([answer])
                                else:
                                    answer_data_al_d.append([0])
                                answer_data_al_o.append([item['qoo']])
                                answer_data_al_q = item['qid']
                        else:   # 答案为空
                            for item in tmp_list:
                                answer_data_al_d.append([0])
                                answer_data_al_o.append([item['qoo']])
                                answer_data_al_q = item['qid']


                        answer_data_al_list.append({
                            'q': answer_data_al_q,
                            'rnp': 1,
                            'f': '',
                            'vl': '',
                            'd': answer_data_al_d,
                            'o': answer_data_al_o
                        })
            answer_data = {
                'al': answer_data_al_list,
                'sl': answer_data_sl_list,
                'ut':0
            }
            return answer_data

        def submit_ut(dataid, exercise_id, answer_data, is_get_answer):
            self.logger.info('submit_ut')
            # 提交答案, is_get_answer为true则返回答案链接，若为false则直接提交答案
            submit_ut_url = 'https://uexercise.unipus.cn/itest/s/clsanswer/submitUT'
            submit_ut_headers = {}
            submit_ut_headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            submit_ut_data = {
                "ansData": json.dumps(answer_data),
                "act": 'save',
                "sppid": dataid,
                "exerciseId": exercise_id,
            }
            submit_ut_req = requests.post(submit_ut_url, headers=submit_ut_headers, cookies=target_cookies_dict, data=submit_ut_data)
            submit_ut_json_data = json.loads(submit_ut_req.text)
            if submit_ut_json_data.get('code')==1 and '本次共完成' in submit_ut_json_data.get('msg'):
                if not is_get_answer:
                    self.logger.info('获取答案链接')
                    soup2 = BeautifulSoup(submit_ut_json_data.get('msg'), 'html.parser')
                    self.logger.info(soup2)
                    for submit in soup2.find_all('div', attrs={"class": "submit"}):
                        self.logger.info(soup2.find_all('div', attrs={"class": "submit"}))
                        if '/itest/t/clsExam/rate/detail' in submit.get('qa'):
                            answer_url = 'https://uexercise.unipus.cn' + submit.get('qa')
                            self.logger.info(answer_url)
                            return answer_url
                    return None
                else:
                    soup2 = BeautifulSoup(submit_ut_json_data.get('msg'), 'html.parser')
                    self.logger.info(soup2.find('span', attrs={'class': 'green'}).text)
                    self.logger.info('test模块完成')
            else:
                self.logger.info('test模块失败, %s' % submit_ut_json_data)
                return None

        # 提交默认答案，获取答案链接
        origin_answer_data = []
        answer_data = get_ut(dataid, origin_answer_data)
        answer_url = submit_ut(dataid, exercise_id, answer_data, False)
        if answer_url:
            # 根据答案链接获取答案并保存
            self.logger.info('保存test模块答案')
            origin_answer_data = get_origin_answer(answer_url)

            with open(answer_data_file, encoding='utf-8', mode='w') as fp:
                fp.write(json.dumps(origin_answer_data))
            return True, '下载答案成功'
        else:
            return False, '下载答案失败'
    def request_with_verification(self,url,headers=None,cookies=None,timeout=None,allow_redirects=None):
        retry_count = 0
        while True:
            req = requests.get(url, headers=headers, cookies=cookies,timeout=timeout,allow_redirects=allow_redirects)
            if  'some thing not loaded' in req.text :
                if retry_count>=3:
                    return None
                retry_count=retry_count+1
                self.logger.info('获取course_id: 出现验证码')
                time.sleep(1)
                get_count = 0
                while get_count <4:
                    captcha_req = requests.get('https://captcha.unipus.cn/captcha/v1/', headers=self.headers, cookies=self.cookies)
                    try:
                        captcha_json=json.loads(captcha_req.text)
                        break
                    except:
                        with open(path +"\\verify.txt","w+") as fo:
                            fo.write("error:\n"+captcha_req.text) 
                    time.sleep(1)
                    get_count = get_count + 1
                if get_count >= 4:
                    continue 
                os.makedirs('./image/', exist_ok=True)
                captcha_path=captcha_json['path']
                IMAGE_URL = 'https://captcha.unipus.cn'+captcha_path
                IMAGE_NAME='./image/'+captcha_path.replace('/','')+'.jpg'
                urlretrieve(IMAGE_URL, IMAGE_NAME)
                pd_id           = "111751"     
                pd_key          = "LA4ut4p3fcC65MX/6MHiEklQyVj+us0W"
                app_id          = "311751"     
                app_key         = "PTcYetLt5PeW3kJtlacYf9fVUPq+b8Ge"
                pred_type       = "50100"
                api             = FateadmApi(app_id, app_key, pd_id, pd_key)
                balance         = api.QueryBalcExtend()   # 直接返余额
                if balance<1:
                    self.logger.info('打码平台余额不足' )
                    return None
                else:
                    self.logger.info('上传验证码图片')
                    rsp             = api.PredictFromFileExtend(pred_type, IMAGE_NAME)  
                    self.logger.info('获取验证码图片打码结果: %s' % rsp)
                    duration_data = {
                        'answer': rsp
                    }
                    duration_req = requests.post(IMAGE_URL, headers=self.headers,data=json.dumps(duration_data),cookies=self.cookies)
                    print(duration_req.text)
                    if '成功' in duration_req.text:
                        self.logger.info('提交验证码成功')
                        time.sleep(1)
                        req = requests.get(url, headers=headers, cookies=cookies)
                        return req  
            else:
                return req
if __name__ == '__main__':
    unipus = Unipus(logger,'13015265988', 'wq19980506')
    unipus.login()
    activated_course_list, not_activated_course_list = unipus.get_course_list()
    for course in [activated_course_list]:
        logger.info(str(course))
    # unipus.learn_for_unit('course-v1:Unipus+nhce_3_vls_1+2018_03', 'u2', 1000)
    #unipus.learn_for_all_unit(course['id'], 10000)
