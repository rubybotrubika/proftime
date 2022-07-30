from encryption import encrypt
from json import loads, dumps
from requests import post
from pathlib import Path

class clients:
	android = {"app_name" : "Main","app_version" : "2.9.8","platform" : "Android","package" : "app.rbmain.a","lang_code"   : "fa"}
	web = {"app_name" : "Main","app_version" : "4.0.7","platform" : "Web","package" : "web.rubika.ir","lang_code"   : "fa"}

class profile:
	def __init__(self, auth):
		if len(auth) != 32: print("auth must be 32 characters!"); exit()
		self.auth = auth
		self.enc = encrypt(self.auth)

	@staticmethod
	def getURL():
		return "https://messengerg2c64.iranlms.ir/"

	def requestSendFile(self,file):
	    while True:
	        try:
	            data = {"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"requestSendFile","input":{"file_name": file.split("/")[-1],"mime": file.split(".")[-1],"size": str(499999)},"client": clients.android}))}
	            return loads(self.enc.decrypt(post(json=data,url=profile.getURL()).json()["data_enc"]))["data"]
	            break
	        except:pass
	        
	def uploadFile(self,file):
	    frequest = profile.requestSendFile(self,file)
	    bytef , hash_send , file_id , url = open(file,"rb").read() , frequest["access_hash_send"] , frequest["id"] , frequest["upload_url"]
    
	    header = {"auth":self.auth,"Host":url.replace("https://","").replace("/UploadFile.ashx",""),"chunk-size":str(Path(file).stat().st_size),"file-id":str(file_id),"access-hash-send":hash_send,"content-type": "application/octet-stream","content-length": str(Path(file).stat().st_size),"accept-encoding": "gzip","user-agent": "okhttp/3.12.1"}
	        
	    if len(bytef) <= 1000000:
	        header["part-number"], header["total-part"] = "1","1"
	            
	        while True:
	           try:
	               j = post(data=bytef,url=url,headers=header).text
	               j = loads(j)['data']['access_hash_rec']
	               break
	           except Exception as e: continue
	        return [frequest, j]
	    else:
	        t = round(((len(bytef) / 1024) / 1024))
	        if len(bytef) >= 100000000:
	             f = round(len(bytef) / t + round(len(bytef) / 100000000))
	        else:
	             f = round(len(bytef) / t + 1)
	        for i in range(1,t + 1):
	           if i != t:
	               k = i - 1
	               k = k * f
	               while True:
	                   try:
	                       header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:k + f])), str(i),str(t)
	                       o = post(data=bytef[k:k + f],url=url,headers=header).text
	                       o = loads(o)['data']
	                       break
	                   except:continue
	           else:
	               k = i - 1
	               k = k * f
	               while True:
	                   try:
	                       header["chunk-size"], header["part-number"], header["total-part"] = str(len(bytef[k:k + f])), str(i),str(t)
	                       p = post(data=bytef[k:k + f],url=url,headers=header).text
	                       p = loads(p)['data']['access_hash_rec']
	                       break
	                   except:continue
	               return [frequest, p]

	def uploadAvatar(self,myguid,main,thumbnail=None):
		mainID = str(profile.uploadFile(self, main)[0]["id"])
		thumbnailID = str(profile.uploadFile(self, thumbnail or main)[0]["id"])
		data = {"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"uploadAvatar","input":{"object_guid":myguid,"thumbnail_file_id":thumbnailID,"main_file_id":mainID},"client": clients.android}))}
		return loads(self.enc.decrypt(post(json=data,url=profile.getURL()).json()["data_enc"]))

	def getAvatars(self,myguid):
		data = {"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"getAvatars","input":{"object_guid":myguid,},"client": clients.android}))}
		return loads(self.enc.decrypt(post(json=data,url=profile.getURL()).json().get("data_enc"))).get("data").get("avatars")

	def deleteAvatar(self,myguid,avatar_id):
		data = {"api_version":"5","auth": self.auth,"data_enc":self.enc.encrypt(dumps({"method":"deleteAvatar","input":{"object_guid":myguid,"avatar_id":avatar_id},"client": clients.android}))}
		return loads(self.enc.decrypt(post(json=data,url=profile.getURL()).json()["data_enc"]))