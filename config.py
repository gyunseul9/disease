'''
use mysql
create database gyunseul9 default character set utf8;
create user 'gyunseul9'@'localhost' identified by 'gyunseul9';
create user 'gyunseul9'@'127.0.0.1' identified by 'gyunseul9';
grant all privileges on gyunseul9.* to 'gyunseul9'@'localhost';
grant all privileges on gyunseul9.* to 'gyunseul9'@'127.0.0.1';
flush privileges;
quit;

LOAD DATA LOCAL INFILE '/home/20180119_living_weather_location.csv'
INTO TABLE living_location
CHARACTER SET UTF8 FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(area,depth01,depth02,depth03);

CREATE TABLE disease (
  num int(11) NOT NULL AUTO_INCREMENT,
  dissCd char(1) NOT NULL,
  dt char(8) NOT NULL,
  znCd char(2) NOT NULL,
  cnt int(11) NOT NULL,
  risk char(1) NOT NULL,
  dissRiskXpln varchar(255) NOT NULL,
  posted datetime DEFAULT NOW(),
  primary key (num)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
END'''

class Configuration:

  def get_configuration(choose):

    if(choose == 'local'):
      connect_value = dict(host='HOST',
        user='USERID',
        password='PASSWORD',
        database='DATABASE',
        port=3307,
        charset='utf8')
      
    elif(choose == 'ubuntu'):
      connect_value = dict(host='HOST',
        user='USERID',
        password='PASSWORD',
        database='DATABASE',
        port=3307,
        charset='utf8')

    else:
      print('Not Selected')
      connect_value = ''

    return connect_value
  