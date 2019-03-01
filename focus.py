from time import sleep
from onvif import ONVIFCamera


# Definition of focus(x, s) function
# Function params:
# x - Focus Move Position/Direction
# s - Focus Move Speed
def focus(x, s):

    # Connecting to Camera
    mycam = ONVIFCamera('192.168.15.43', 80, 'admin', 'Supervisor',
                        'C:\Users\komar\Documents\python-onvif-master\wsdl')

    # Creation of Media Service
    media = mycam.create_media_service()

    # Getting of Media Profile
    media_profile = media.GetProfiles()[0]

    # Creation of Imaging Service
    img = mycam.create_imaging_service()

    # Creation of Request for supported Focus Move modes with Video Source Token
    request = img.create_type('GetMoveOptions')
    request.VideoSourceToken = media_profile.VideoSourceConfiguration.SourceToken

    # Getting Focus Move options
    move_options = img.GetMoveOptions(request)
    print move_options

    # Getting Current Focus Status
    # status = img.GetStatus({'VideoSourceToken': media_profile.VideoSourceConfiguration.SourceToken})
    # print status

    # Creation of Request for Focus Move with Video Source Token
    request = img.create_type('Move')
    request.VideoSourceToken = media_profile.VideoSourceConfiguration.SourceToken

    # Setting Focus Move Params
    # Absolute Move
    # request.Focus.Absolute.Position = x
    # request.Focus.Absolute.Speed = s

    # Continuous Move
    request.Focus.Continuous.Speed = s

    # Relative Move
    # request.Focus.Relative.Distance = x
    # request.Focus.Relative.Speed = s

    # Calling Move Method of Imaging Service with request as a param
    img.Move(request)

    # Stopping any movement after 5 seconds delay
    sleep(5)
    img.Stop({'VideoSourceToken': media_profile.VideoSourceConfiguration.SourceToken})


# Calling focus() Function
# For Absolute Mode
# focus(1, 1)
# focus(0, 1)

# For Continuous Mode
focus(0, 1)
focus(0, -1)

# For Relative Mode
# focus(1, 1)
# focus(-1, 1)
