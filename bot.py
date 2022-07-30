from Creation import cr_image, del_image, get_time
from client import profile
from confing import info
from time import sleep

self = profile(info.auth)

ps_time, guid = "", info.guid_me

while True:
	try:
		if not ps_time == get_time():
			ct_time = get_time()
			ps_time = ct_time
			
			cr_image(ct_time)
			
			test = self.getAvatars(guid)
			
			if test != []:
				
				while True:
					try:
						avatar_id = self.getAvatars(guid)[0]["avatar_id"]
						break
					except:continue
			
			while True:
				try:
					self.uploadAvatar(guid, 'time_image.jpg')
					break
				except:continue
			
			if test != []:
				while True:
					try:
						self.deleteAvatar(guid, avatar_id)
						break
					except:continue

			del_image()
			sleep(1)

	except:continue 