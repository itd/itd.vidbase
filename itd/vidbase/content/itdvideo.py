from five import grok
from zope import schema
from plone.namedfile import field as namedfile

from plone.directives import form, dexterity

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


# the view class def
#class View(grok.View):
#    grok.context(IITDVideo)
#    grok.require('zope2.View')
