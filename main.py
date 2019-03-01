from onvif import ONVIFCamera

# Connecting to Camera
mycam = ONVIFCamera('192.168.15.42', 80, 'admin', 'Supervisor', 'C:\Users\komar\Documents\python-onvif-master\wsdl')

# Get Camera Hostname
resp = mycam.devicemgmt.GetHostname()
print 'My camera`s hostname: ' + str(resp.Name)

print '\n#############################################\n'

# Get Camera Information
print('Device information: ' + str(mycam.devicemgmt.GetDeviceInformation()))

print '\n#############################################\n'

# Get system date and time

dt = mycam.devicemgmt.GetSystemDateAndTime()
tz = dt.TimeZone
year = dt.UTCDateTime.Date.Year
hour = dt.UTCDateTime.Time.Hour

print('Timezone: ' + str(tz))
print('Year: ' + str(year))
print('Hour: ' + str(hour))

print '\n#############################################\n'

# Getting Services
response = mycam.devicemgmt.GetServices({'IncludeCapability': True})

print response
print '\n#############################################\n'

# Creating Media Service
media_service = mycam.create_media_service()

# Getting Profiles
profiles = media_service.GetProfiles()
media_profile = profiles[0]

print("Profiles: " + str(profiles))
print '\n#############################################\n'

# Getting Token
token = media_profile._token

print("Token: " + str(token))
print '\n#############################################\n'

# Creating PTZ service
ptz = mycam.create_ptz_service()

# Checking Modes
print("Modes: " + str(mycam.ptz.GetNodes()))
print '\n#############################################\n'

# Getting available PTZ services
request = ptz.create_type('GetServiceCapabilities')
service_capabilities = ptz.GetServiceCapabilities(request)

print("Service capabilities: " + str(service_capabilities))
print '\n#############################################\n'

# Getting PTZ status
status = ptz.GetStatus({'ProfileToken': token})

print("PTZ status: " + str(status))
print '\n#############################################\n'
print('Pan position: ' + str(status.Position.PanTilt._x))
print('Tilt position: ' + str(status.Position.PanTilt._y))
print('Zoom position: ' + str(status.Position.Zoom._x))
# print('Pan/Tilt Moving?: ' + str(status.MoveStatus.PanTilt))
print '\n#############################################\n'

# # Getting PTZ configuration options for getting option ranges
# request = ptz.create_type('GetConfigurationOptions')
# request.ConfigurationToken = media_profile.PTZConfiguration._token
# ptz_configuration_options = ptz.GetConfigurationOptions(request)
#
# print('PTZ configuration options: ' + str(ptz_configuration_options))
