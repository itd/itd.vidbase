from five import grok
from zope import schema
from plone.namedfile import field as namedfile

from plone.directives import form, dexterity
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName

from datetime import datetime

from itd.vidbase import _

class IITDVideo(form.Schema):
    """
    M4V video file to be served-up to an iP** type device.
    """

    # -*- Your Zope schema definitions here ... -*-


    title = schema.TextLine(
        title=_(u"Title of show"),
        description=_(u"A descriptive title of the video that will be played"),
        required=False,
    )

    itdvideofile = namedfile.NamedBlobFile(
        title=_(u"Video File"),
        description=_(u"The finished mp4 file to be played on iwhatever devices"),
        required=True,
    )

    showdate = schema.Date(
        title=_("Show Date"),
    )

@form.default_value(field=IITDVideo['showdate'])
def showdateDefaultValue(data):
    return datetime.today()

@form.default_value(field=IITDVideo['title'])
def titleDefaultValue(data):
    today = datetime.today()
    return today.strftime('%B, %d, %Y')
    
@grok.subscribe(IITDVideo, IObjectAddedEvent)
def autoPublish(itdvideo, event):
    portal_workflow = getToolByName(itdvideo, 'portal_workflow')
    portal_workflow.doActionFor(itdvideo, 'publish')

# the view class def
#class View(grok.View):
#    grok.context(IITDVideo)
#    grok.require('zope2.View')
