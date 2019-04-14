import pysftp

sftpConnect = pysftp.Connection(host="xxx", username="xxx", private_key="zzz", password=None, port=nn, private_key_pass="fff", ciphers=None, log=False)

data = sftpConnect.listdir('/xx/')

print ('Does path /xx/ exisit ? :', sftpConnect.lexists('/xx/')) #Tests if path exisits
print ('Does file personalizedRecommend_RP.json exist ? :', sftpConnect.lexists('/xx/personalizedRecommend_RP.json')) #Tests if file exists
print ('Files on path /xx/recommendationJson/ are:', sftpConnect.listdir('/xx/recommendationJson/')) # List files in the given path

sftpConnect.close()
