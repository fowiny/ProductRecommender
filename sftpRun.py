import pysftp

sftpConnect = pysftp.Connection(host="xxx", username="xxx", private_key="zzz", password=None, port=22, private_key_pass="fff", ciphers=None, log=False)

data = sftpConnect.listdir('/home/converse/recommendationJson/')

print ('Does path /home/converse/recommendationJson/ exisit ? :', sftpConnect.lexists('/home/converse/recommendationJson/')) #Tests if path exisits
print ('Does file personalizedRecommend_RP.json exist ? :', sftpConnect.lexists('/home/converse/recommendationJson/personalizedRecommend_RP.json')) #Tests if file exists
print ('Files on path /home/converse/recommendationJson/ are:', sftpConnect.listdir('/home/converse/recommendationJson/')) # List files in the given path

sftpConnect.close()
