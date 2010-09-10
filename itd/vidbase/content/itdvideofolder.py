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
        description=_(u"The URL where the video files will be sourced, \
                       e.g., rtmp://stream.mandsworks.com/kyod/news/"),
        required=True,
    )

#
class View(grok.View):
    grok.context(IITDVideoFolder)
    grok.require('zope2.View')

    def vids(self):
        """Return a catalog search result of vids to show
        """

        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(object_provides=IITDVideo.__identifier__,
                       path='/'.join(context.getPhysicalPath()),
                       sort_on='sortable_title')
