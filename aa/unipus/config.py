#encoding: utf-8
'''
desc: flask配置文件
'''
import os

PLATEFORM_ID_NAME_DICT = {
	'1': {
		'name': 'xxx',
		'desc': '随行课堂'
	},
	'2': {
		'name': 'xxx',
		'desc': '好策'
	},
	'3': {
		'name': 'unipus',
		'desc': 'u校园'
	},
	'4': {
		'name': 'xxx',
		'desc': '优学院'
	},
}

LOGIN_CODE_MSG_DICT = {
	1: '成功',
	2: '账号或密码错误，登录失败',
	3: '缺少必要参数，或参数取值有误',
	4: '其他'
}

ANWSER_CODE_MSG_DICT = {
	1: '请求接收成功',
	2: '账号或密码错误，登录失败',
	3: '缺少必要参数，或参数取值有误',
	4: '其他'
}
DOWNLOAD_ANWSER_CODE_MSG_DICT = {
	1: '成功',
	2: '账号或密码错误，登录失败',
	3: '缺少必要参数，或参数取值有误',
	4: '其他'
}

ANSWER_DATA_FILE = 'answer/courseid_{}_taskid_{}.json'