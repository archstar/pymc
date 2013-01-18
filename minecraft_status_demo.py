import minecraft_status

status = minecraft_status.GetMCStatus('my_server_hostname')
if status[0]:
  print 'Server is online'
  print 'MOTD is: %s' % status[1]
  print 'Currently %s/%s players online' % (status[2], status[3])
else:
  print 'Server is offline'
