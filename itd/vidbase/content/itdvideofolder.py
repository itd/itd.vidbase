from five import grok
from zope import schema
from plone.namedfile import field as namedfile

from plone.directives import form, dexterity

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from itd.vidbase.content.itdvideo import IITDVideo

from itd.vidbase import _

class IITDVideoFolder(form.Schema):
    """
    A folder to hold itdvideos
    """

    # -*- Your Zope schema definitions here ... -*-
    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"A descriptive title of the collection"),
        required=True,
    )
    targeturl = schema.TextLine(
        title=_(u"Target Stream URL"),
        description=_(u"The URL prepended to the video file names for playback, \
                       e.g., 'http://media1.lotteryvideo.com/kyod/mp4:'  "),
        required=True,
    )
    targeturlsuffix = schema.TextLine(
        title=_(u"Stream URL suffix"),
        description=_(u"If needed, the URL suffix to each file for playback, \
                       e.g., '/playlist.m3u8'  "),
        required=True,
    )
    limit = schema.Int(
        title=_(u"Item limitation"),
        description=(u"Limit the number of items of folder's feeds. Enter 0 or leave blank for disable limitation."),
    )

#
class View(grok.View):
    grok.context(IITDVideoFolder)
    grok.require('zope2.View')

    #import pdb; pdb.set_trace()
    def vids(self):
        """Return a catalog search result of vids to show
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        res = catalog(object_provides=IITDVideo.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='sortable_title')

        #import pdb; pdb.set_trace()

        return  [brain.getObject() for brain in res]
