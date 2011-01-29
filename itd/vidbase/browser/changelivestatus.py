from zope.interface import Interface
from zope.interface import implements
from Acquisition import aq_inner
import zope.event
import zope.lifecycleevent

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

class IChangeLiveStatusView(Interface):
    """Change livestatus for iphoneannounce object
    """


class ChangeLiveStatusView(BrowserView):
    """
    """
    implements(IChangeLiveStatusView)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.template = ViewPageTemplateFile("templates/changestatusview.pt")        

    def __call__(self):
        
        if self.request.get('form.submit', None) is not None:
            status = self.request.get('livestatus', None)
            obj = self.context
            self.updateLiveStatus(status, obj)
            return self.request.response.redirect(self.context.absolute_url())
        return self.template(self)
        
    def updateLiveStatus(self, status, object):
        if status:
            object.livestatus = status
        descriptions = []
        zope.event.notify(
                zope.lifecycleevent.ObjectModifiedEvent(object, *descriptions))            
        IStatusMessage(self.request).addStatusMessage((u"Changes saved"), "info")


