from five import grok
from zLOG import LOG, ERROR

from itd.vidbase.content.iphoneannounce import Iiphoneannounce
from itd.vidbase.interfaces import IIphoneAnnounceAdapter

class IphoneAnnounceAdapter(grok.Adapter):
    """Adapter for iphoneannounce
    """
    grok.context(Iiphoneannounce)
    grok.implements(IIphoneAnnounceAdapter)
    def push_ua(self):
        """Send payload to UA service
        """    
        obj = self.context
        key = obj.appkey
        master_key = obj.appmaster 
        app_secret = obj.appsecret 
        ua_json = obj.ua_json()
        try:
            airship = urbanairship.Airship(key, master_key)
            airship.push(ua_json)
        except:
            LOG('itd.vidbase:', ERROR, '%s - Failure to push payload to UA' %self.context.id)
   
   
   
