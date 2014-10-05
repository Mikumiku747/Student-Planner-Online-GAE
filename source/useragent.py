# UserAgent
# Lets me check if a user is using the site on mobile or on desktop.
# Also lets you check kind of precisely what device the user is
# Viewing the site on

def checkMobile(request):
    "Lets you check to see if the user is on a mobile device."
    agent = request.headers["User-Agent"]
    deviceInfo = agent[agent.find('(')+1:agent.find(')')]
    if "Android" in deviceInfo:
        if "U;" in deviceInfo:
            return True
        else:
            return False
    elif "iPhone OS" in deviceInfo:
        return True
    else:
        return False

def checkDevice(request):
    "Tries to guess the user's device, may be wrong in some cases."
    agent = request.headers["User-Agent"]
    deviceInfo = agent[agent.find('(')+1:agent.find(')')]
    if "Android" in deviceInfo:
        if "U;" in deviceInfo:
            return "Android Phone"
        else:
            return "Android Tablet"
    elif "iPhone;" in deviceInfo:
        return "Apple iPhone"
    elif "iPad;" in deviceInfo:
        return "Apple iPad"
    elif "iPod;" in deviceInfo:
        return "Apple iPod"
    elif "Windows" in deviceInfo:
        if "Touch" in deviceInfo:
            return "Windows Tablet"
        else:
            return "Windows"
    elif "Macintosh;" in deviceInfo:
        return "Macintosh"
    elif "Linux;" in deviceInfo:
        return "Linux"
    else:
        return "Unknown Device"
