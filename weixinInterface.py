# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
import model
import random
import webbrowser
from lxml import etree
 
class WeixinInterface:
 
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
 
    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        #自己的token
        token="waikai" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法        
 
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
    def POST(self):        
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
       # content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if msgType == "text": 
            content=xml.find("Content").text#获得用户所输入的内容
            if content.startswith('Wish'):
                info = content.split('@')
                if info[1]:
                    if not info[2]:
                    		#strx = "sssss"
                            dreamID = model.addDream(fromUser,info[1].encode('utf-8'), "暂未提供联系方式")
                            return self.render.reply_text(fromUser,toUser,int(time.time()),u"已经记录你的许愿" + "\n这是愿望编号 " +str(dreamID))
                    else:
                        model.addDream(fromUser,info[1].encode('utf-8'),info[2].encode('utf-8'))
                        
                        return self.render.reply_text(fromUser,toUser,int(time.time()),u"已经记录你的许愿")
                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()),u"无法记录愿望为空")
            elif content == 'Lucky':
                res=list(model.getDream())
                nub=res[0].id
                dream = res[0].dreamCo
                contact = res[0].contact
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"这是愿望编号为"+" "+str(nub)+ "  "+dream + " " +contact)
            elif content.startswith('Done'):
                argsForDone = content.split('@')
                numb = argsForDone[1]
                res = model.deleDream(numb, fromUser)
                return self.render.reply_text(fromUser,toUser,int(time.time()),res)
            elif content.startswith('Get'):
                #Get@编号
                args = content.split('@')
                numb = args[1]
                theInfo = list(model.getNumb(numb))
                msgForUser = args[2]
                dreamHold = theInfo[0].userName
                return self.render.reply_text(fromUser,toUser,int(time.time()),u"感谢你的帮助："+dreamHold)
            elif content.startswith('Story'):
                sooo = model.storyInsert(fromUser, content[5:].encode('utf-8'))
                return self.render.reply_text(fromUser,toUser,int(time.time()),sooo)
          
            elif content == 'Tw':
                reurl = "http://www.baidu.com"
                return self.render.reply_m(fromUser,toUser, int(time.time()), reurl)
                
            else:
            	return self.render.reply_text(fromUser,toUser,int(time.time()),u"输入Wish@你的愿望@联系方式（可以为空），可以进行许愿。\n\n输入Lucky，可以随机获取别人的愿望和联系方式。\n\n输入Done@愿望编号，可以删除你的愿望。\n\n输入Story@你的故事，可以和我们分享任何内容。")

        else:
        	
        
        
        	return self.render.reply_text(fromUser,toUser,int(time.time()),u"输入Wish@你的愿望@联系方式（可以为空），可以进行许愿。\n\n输入Lucky，可以随机获取别人的愿望和联系方式。\n\n输入Done@愿望编号，可以删除你的愿望。\n\n输入Story@你的故事，可以和我们分享任何内容。")


