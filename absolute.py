from time import sleep
from onvif import ONVIFCamera


# Definition of Function perform_absolute_move() with params:
# ptz - PTZ Service Onvif object
# request - input request for command
# Uses for performing absolute move with request
def perform_absolute_move(ptz, request):

    # Starting absolute move
    ptz.AbsoluteMove(request)

    print('Absolute move completed')

    # Five seconds delay
    sleep(5)


# Definition of Function absolute_move() with params:
# x, y, z - Pan, Tilt and Zoom coordinates
# Moves camera to coordinates in absolute mode
def absolute_move(x, y, z):

    # Connecting to Camera
    mycam = ONVIFCamera('192.168.15.42', 80, 'admin', 'Supervisor', 'C:\Users\komar\Documents\python-onvif-master\wsdl')

    # Create media service object
    media = mycam.create_media_service()
    # Create ptz service object
    ptz = mycam.create_ptz_service()

    # Get target profile
    media_profile = media.GetProfiles()[0]

    # Creating absolute move request with media_profile token
    request = ptz.create_type('AbsoluteMove')
    request.ProfileToken = media_profile._token

    # Stops all other movement to get status
    ptz.Stop({'ProfileToken': media_profile._token})

    # Getting camera status with information about coordinates
    status = ptz.GetStatus({'ProfileToken': media_profile._token})
    print status

    # Setting status object coordinates to function params
    status.Position.PanTilt._x = x
    status.Position.PanTilt._y = y
    status.Position.Zoom._x = z

    # Setting request position to status object position
    request.Position = status.Position

    # Stops all other movement to perform move
    ptz.Stop({'ProfileToken': media_profile._token})

    # Performing move with PTZ Service Onvif Object
    # and move request as arguments
    perform_absolute_move(ptz, request)


# Move to Starting Position
absolute_move(0, 0, 0.5)
sleep(3)

# Move Right
absolute_move(0.5, 0, 0.3)
sleep(5)

# Go back to Starting Position
absolute_move(0, 0, 0.5)
sleep(3)

# Move Left
absolute_move(-0.5, 0, 0.1)
sleep(5)

# Move Down
absolute_move(0, 1, 0.5)
sleep(3)

# Move Up
absolute_move(0, -1, 0.5)
sleep(3)
