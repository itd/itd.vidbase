from Products.Five import BrowserView
from zope.interface import Interface
from zope.interface import implements
from zope.component import getMultiAdapter
from urllib import quote
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName

class IXMLByShowDateView(Interface):
    """Marker interface identifying XMLByShowDateView View.
    """

class IXMLByFolderOrderView(Interface):
    """Marker interface identifying XMLByFolderOrderView View.
    """

class IXMLByFolderOrderReversedView(Interface):
    """Marker interface identifying XMLByFolderOrderReversedView View.
    """

class ITDBaseXML(BrowserView):
    """ Base class for XML generating
    """

    def folderName(self):
        return self.context.title

    def getTargetURL(self):
        return self.context.targeturl

    def getTargetURLSuffix(self):
        suff = self.context.targeturlsuffix
        if suff == None:
            suff = ''
        return suff.strip()

    def getUploadFileName(self, video_id):
        """ Returns the exact file name of itdvideo object
        """
        video_obj = getattr(self.context, video_id, None)
        try:
            if video_obj != None:
                return quote(video_obj.itdvideofile.filename)
        except:
            return None


class XMLByShowDateView(ITDBaseXML):
    """
    """
    implements(IXMLByShowDateView)

    def subItems(self):
        """ Returns set of published itdvideo sorted by showdate
        """
        context = aq_inner(self.context)
        itdFilter = {'portal_type':['itd.vidbase.itdvideo'],
                     'review_state':'published',
                     'sort_on':'showdate',
                     'sort_order':'descending',
                     }
        items = self.context.getFolderContents(contentFilter=itdFilter)
        if self.context.limit > 0:
            items = items[:self.context.limit]
        return items


class XMLByFolderOrderView(ITDBaseXML):
    """
    """
    implements(IXMLByFolderOrderView)

    def subItems(self):
        """ Returns set of published itdvideo by folder order
        """
        itdFilter = {'portal_type':['itd.vidbase.itdvideo'],
                     'review_state':'published',}
        items = self.context.getFolderContents(contentFilter=itdFilter)
        if self.context.limit > 0:
            items = items[:self.context.limit]
        return items


class XMLByFolderOrderReversedView(ITDBaseXML):
    """
    """
    implements(IXMLByFolderOrderReversedView)

    def subItems(self):
        """ Returns set of published itdvideo reverved to normal order
        """
        itdFilter = {'portal_type':['itd.vidbase.itdvideo'],
                     'review_state':'published',
                     'sort_order':'descending'}
        items = self.context.getFolderContents(contentFilter=itdFilter)
        if self.context.limit > 0:
            items = items[:self.context.limit]
        return items

