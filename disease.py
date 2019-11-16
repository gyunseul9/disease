
# -*- coding: utf-8 -*- 

import os, glob
import requests
import time
import datetime
import sys
from config import Configuration
from db import DBConnection,Query
from slacker import Slacker
from PIL import Image, ImageDraw, ImageFont
from xml.etree import ElementTree as et

class Disease:

	def __init__(self,dissCd,platform):
		#print('init')
		self.dissCd = dissCd
		self.platform = platform

	def set_params(self):
		#print('set_params')
		self.dissCd = sys.argv[1]
		self.platform = sys.argv[2]

	def validate(self):
		default	= {
			'dissCd':'1',
			'platform':'mac'
		}

		self.dissCd = default.get('dissCd') if self.dissCd == '' else self.dissCd
		self.platform = default.get('platform')	if self.platform == '' else self.platform.lower()

	def table_disease(self,value):

		if value == '-':
			result = '-'
		else:
			if int(value) < 0:
				result = '미측정'	
			elif int(value) == 1:
				result = '관심'
			elif int(value) == 2:
				result = '주의'
			elif int(value) == 3:
				result = '경고'				
			elif int(value) == 4:
				result = '위험'
			else:
				result = '-'

		return result				

	def table_znCd(self,value):

		print('table_area:value:',value)

		area = {
			'11':'서울특별시',
			'26':'부산광역시',
			'27':'대구광역시',
			'28':'인천광역시',
			'29':'광주광역시',
			'30':'대전광역시',
			'31':'울산광역시',
			'41':'경기도',
			'42':'강원도',
			'43':'충청북도',
			'44':'충청남도',
			'45':'전라북도',
			'46':'전라남도',
			'47':'경상북도',
			'48':'경상남도',
			'49':'제주특별자치도',
			'99':'전국'
		}

		result = area.get(value)

		return result		

	def send_slack(self,channel,text):
		attachments_dict = dict()
		attachments_dict['text'] = text
		attachments = [attachments_dict]

		token = 'TOKEN'
		slack = Slacker(token)
		slack.chat.post_message(channel=channel, text=None, attachments=attachments, as_user=True)

	def make_message(self,src,dissCd,dt,znCd,cnt,risk,dissRiskXpln):

		area = self.table_znCd(znCd)		
		risk = self.table_disease(risk)

		text = '피부염예측진료정보\n\n출처:{}\n지역:{}\n측정일:{}\n예측진료건수:{}\n예측위험도:{}\n지침:{}\n'.format(src,area,dt,cnt,risk,dissRiskXpln)	
		
		self.send_slack('#disease', text)		
		
	def api(self):

		#print('crawling')
		self.validate()

		try:
			
			configuration = Configuration.get_configuration(self.platform)
			_host = configuration['host']
			_user = configuration['user']
			_password = configuration['password']
			_database = configuration['database']
			_port = configuration['port']
			_charset = configuration['charset']

			conn = DBConnection(host=_host,
				user=_user,
				password=_password,
				database=_database,
				port=_port,
				charset=_charset)

			dissCd = []
			dt = []
			znCd = []
			cnt = []
			risk = []
			dissRiskXpln = []

			url = ''

			if self.dissCd == '5': #피부염
				url = 'http://apis.data.go.kr/B550928/dissForecastInfoSvc/getDissForecastInfo?serviceKey=SERICEKEY&numOfRows=17&pageNo=1&type=xml&dissCd=5'			

			area = {
				'11':'서울특별시',
				'26':'부산광역시',
				'27':'대구광역시',
				'28':'인천광역시',
				'29':'광주광역시',
				'30':'대전광역시',
				'31':'울산광역시',
				'41':'경기도',
				'42':'강원도',
				'43':'충청북도',
				'44':'충청남도',
				'45':'전라북도',
				'46':'전라남도',
				'47':'경상북도',
				'48':'경상남도',
				'49':'제주특별자치도',
				'99':'전국'
			}

			response = requests.get(url)

			directory = '/home/ubuntu/refactoring/disease/xml/'

			filename = '{}{}.xml'.format(directory,self.dissCd)

			with open(filename,'w') as file:
				file.write(response.text)

			tree = et.parse(filename)
			root = tree.getroot()

			for response in root:
				for body in response:
					for items in body:
						for item in items:
							if item.tag == 'dissCd':
								dissCd.append(item.text)
								#print('dissCd:',dissCd)
							elif item.tag == 'dt':
								dt.append(item.text)
								#print('dt:',dt)
							elif item.tag == 'znCd':
								znCd.append(item.text)
								#print('znCd:',znCd)
							elif item.tag == 'cnt':
								cnt.append(item.text)
								#print('cnt:',cnt)
							elif item.tag == 'risk':
								risk.append(item.text)
								#print('risk:',risk)
							elif item.tag == 'dissRiskXpln':
								dissRiskXpln.append(item.text)
								#print('dissRiskXpln:',dissRiskXpln)	

			for i in range(0,int(len(area))):
				#print(dissCd[i],dt[i],znCd[i],cnt[i],risk[i],dissRiskXpln[i])
		
				src = '공공데이터'	
				
				count = conn.exec_select_disease(dissCd[i],dt[i],znCd[i])

				if count:
					print('overlap seq: ',i,count)
				else:	
					print('does not overlap seq: ',i,count)

					conn.exec_insert_disease(dissCd[i],dt[i],znCd[i],int(cnt[i]),risk[i],dissRiskXpln[i])

					self.make_message(src,dissCd[i],dt[i],znCd[i],cnt[i],risk[i],dissRiskXpln[i])	

		except Exception as e:
			with open('./disease.log','a') as file:
				file.write('{} You got an error: {}\n'.format(datetime.datetime.now().strtime('%Y-%m-%d %H:%M:%S'),str(e)))

def run():
	disease = Disease('','')
	disease.set_params()
	disease.api()

if __name__ == "__main__":
	run()
