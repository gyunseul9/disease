import pymysql

class DBConnection:
	def __init__(self,host,user,password,database,charset,port):
		self.connection = pymysql.connect(
			host=host,
			user=user,
			password=password,
			db=database,
			charset=charset,
			port=port,
			cursorclass=pymysql.cursors.DictCursor)

	def exec_select_disease(self,dissCd,dt,znCd):
		with self.connection.cursor() as cursor:
			query = Query().get_select_disease(dissCd,dt,znCd)
			cursor.execute(query)
			for row in cursor:
				data = row.get('cnt')
		return data	

	def exec_insert_disease(self,dissCd,dt,znCd,cnt,risk,dissRiskXpln): 
		query = Query().get_insert_disease(dissCd,dt,znCd,cnt,risk,dissRiskXpln) 
		with self.connection as cur:
			cur.execute(query)

	def close(self):
		self.connection.close()

	def commit(self):
		self.connection.commit()

class Query:
	def get_select_disease(self,dissCd,dt,znCd):
		query = 'select \
		count(*) as cnt \
		from disease \
		where  dissCd=\'{}\' and dt=\'{}\' and znCd=\'{}\''.format(dissCd,dt,znCd)

		return query

	def get_insert_disease(self,dissCd,dt,znCd,cnt,risk,dissRiskXpln):
		query = 'insert into disease (dissCd,dt,znCd,cnt,risk,dissRiskXpln) \
		values (\'{}\',\'{}\',\'{}\',{},\'{}\',\'{}\')'.format(dissCd,dt,znCd,cnt,risk,dissRiskXpln)
		#print('qery:',query)
		return query		