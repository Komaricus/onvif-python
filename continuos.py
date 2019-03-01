from time import sleep
from onvif import ONVIFCamera

# Definition of default values for minimums and maximum of Pan and Tilt
XMAX = 1
XMIN = -1
YMAX = 1
YMIN = -1


# Definition of Function custom_move() with params:
# ptz - PTZ Service Onvif object
# request - input request for command
# x, y, z - Pan, Tilt and Zoom velocities
# tx, ty, tz - timeout for moving operations according to coordinate
def custom_move(ptz, request, x, y, z, tx, ty, tz):

    print ("Moving with speed: ({0}, {1}, {2})".format(x, y, z))
    print ("Moving time: ({0}, {1}, {2})".format(tx, ty, tz))

    # Moving Pan
    request.Velocity.PanTilt._x = x
    perform_move(ptz, request, tx)

    # Moving Tilt
    request.Velocity.PanTilt._y = y
    perform_move(ptz, request, ty)

    # Changing Zoom
    request.Velocity.Zoom._x = z
    perform_move(ptz, request, tz)

    request.Velocity.Zoom._x = 0


# Definition of Function perform_move() with params:
# ptz - PTZ Service Onvif object
# request - input request for move command
# timeout - time for Continuous Move
# Uses for performing every continuous move with request
def perform_move(ptz, request, timeout):

    # Starting continuous move
    ptz.ContinuousMove(request)

    # Waiting a certain time
    sleep(timeout)
    request.PanTilt = 1

    # Stop continuous move
    ptz.Stop(request)


# Definition of Functions move_up(), move_down(),
# move_right(), move_left() with params:
# ptz - PTZ Service Onvif object
# request - input request for move command
# timeout - time for Continuous Move
# Uses for continuous move in one particular direction
def move_up(ptz, request, timeout):
    print 'move up...'
    request.Velocity.PanTilt._x = 0
    request.Velocity.PanTilt._y = YMAX
    perform_move(ptz, request, timeout)


def move_down(ptz, request, timeout):
    print 'move down...'
    request.Velocity.PanTilt._x = 0
    request.Velocity.PanTilt._y = YMIN
    perform_move(ptz, request, timeout)


def move_right(ptz, request, timeout):
    print 'move right...'
    request.Velocity.PanTilt._x = XMAX
    request.Velocity.PanTilt._y = 0
    perform_move(ptz, request, timeout)


def move_left(ptz, request, timeout):
    print 'move left...'
    request.Velocity.PanTilt._x = XMIN
    request.Velocity.PanTilt._y = 0
    perform_move(ptz, request, timeout)


# Main function with Camera Initialisation and
# Other functions calls
def continuous_move():
    mycam = ONVIFCamera('192.168.15.42', 80, 'admin', 'Supervisor', 'C:\Users\komar\Documents\python-onvif-master\wsdl')

    # Create media service object
    media = mycam.create_media_service()
    # Create ptz service object
    ptz = mycam.create_ptz_service()

    # Get target profile
    media_profile = media.GetProfiles()[0];
    print media_profile

    # Get PTZ configuration options for getting continuous move range of Pan and Tilt
    request = ptz.create_type('GetConfigurationOptions')
    request.ConfigurationToken = media_profile.PTZConfiguration._token
    ptz_configuration_options = ptz.GetConfigurationOptions(request)

    # Get range of Pan and Tilt
    # X and Y are velocity vector
    global XMAX, XMIN, YMAX, YMIN
    XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
    XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
    YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
    YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min

    # Creating continuous move request with media_profile token
    request = ptz.create_type('ContinuousMove')
    request.ProfileToken = media_profile._token

    # Stops all other movement
    ptz.Stop({'ProfileToken': media_profile._token})

    # custom move
    custom_move(ptz, request, -0.1, -0.2, -0.05, 2, 1, 0.5)
    sleep(3)

    # custom move
    custom_move(ptz, request, 0.1, 0.2, 0.05, 2, 3, 2)
    sleep(3)
    # move right
    move_right(ptz, request, 1)
    sleep(2)

    # move left
    move_left(ptz, request, 1)
    sleep(2)

    # Move up
    move_up(ptz, request, 1)
    sleep(2)

    # move down
    move_down(ptz, request, 1)
    sleep(2)


continuous_move()
