# _*_ coding:utf-8 _*_
import web
import web.db
import sae.const
 
 
db = web.database(
    dbn='mysql',
    host=sae.const.MYSQL_HOST,
    port=int(sae.const.MYSQL_PORT),
    user=sae.const.MYSQL_USER,
    passwd=sae.const.MYSQL_PASS,
    db=sae.const.MYSQL_DB
)
  
def addDream(username, saySomething, dreamContact):
    db.insert('dream', dreamCo=saySomething, userName=username, rank=1, contact = dreamContact)
    results = db.query("SELECT * FROM dream ORDER BY id DESC LIMIT 1")
    return results[0].id
  
def getNumb(yo):
    strc = "id="+yo
    results = db.select('dream', where = strc)
    return results

def getDream():
    results = db.query("SELECT * FROM dream ORDER BY RAND() LIMIT 1")
    
    return results

def deleDream(yo, formUser):
    strg = "id="+yo
    results = db.select('dream', where = strg)
    if results[0].userName == formUser:
       db.delete('dream', where = strg)
       return "通过身份验证，并删除"
    else:
        return "无法通过身份认证，只能由许愿人本人进行删除，请再次确认愿望ID"
def storyInsert(username, userstory):
	db.insert('story', userName = username, userStory = userstory )
	return "感谢你的分享"
