from five import grok
from zLOG import LOG, ERROR

from itd.vidbase.content.iphoneannounce import Iiphoneannounce
from itd.vidbase.interfaces import IIphoneAnnounceAdapter
import urbanairship

class IphoneAnnounceAdapter(grok.Adapter):
    """Adapter for iphoneannounce
    """
    grok.context(Iiphoneannounce)
    grok.implements(IIphoneAnnounceAdapter)

    def push_ua(self):
        """Send payload to UA service
        """
        obj = self.context

        appkey = obj.appkey
        appmaster = obj.appmaster
        sound = obj.sound or ""
        alert = obj.alert
        liveurl = obj.liveurl
        payload = {"aps": {"alert": alert, "sound": sound}, "url": liveurl}

        try:
            airship = urbanairship.Airship(appkey, appmaster)
            airship.broadcast(payload)

        except:
            LOG('itd.vidbase:', ERROR, '%s - Failure to push payload to UA' %self.context.id)

