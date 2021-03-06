import os
from string import Template

from five import grok
from zope import schema
from plone.namedfile import field as namedfile

from plone.directives import form, dexterity
from zope.app.container.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from Products.CMFCore.utils import getToolByName
from zLOG import LOG, INFO, ERROR
from datetime import datetime
from os.path import join
from Acquisition import aq_inner

from itd.vidbase import _
from itd.vidbase.config import ITDVIDEO_STORAGE_PATH

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
    write2FS(itdvideo, None)

@grok.subscribe(IITDVideo, IObjectModifiedEvent)
def write2FS(itdvideo, event):
    """ This trigger method writes the video file to file system under path
        specified in config.py
    """
    parent_path = '/'.join(itdvideo.aq_inner.aq_parent.getPhysicalPath()[2:])
    video_obj = itdvideo.itdvideofile
    path_prefix= '/'.join([ITDVIDEO_STORAGE_PATH, parent_path])
    file_path = '/'.join([path_prefix, video_obj.filename])
    #from pdb import set_trace; set_trace()
    if not os.access(path_prefix, 1):
        try:
            os.makedirs(path_prefix)
        except OSError:
            msg = 'Error occured creating dir: %s for %s' % (path_prefix, video_obj.filename )
            LOG('itd.vidbase', ERROR, msg)

    try:
        vf = open(file_path, 'w')
        try:
            vf.write(video_obj.data)
        except IOError:
            msg = 'Error occurs when writing file %s to disk' % \
                  video_obj.filename
            LOG('itd.vidbase', ERROR, msg)
        finally:
            vf.close()
    except IOError:
        LOG('itd.vidbase', ERROR, 'Error occurs when creating file on disk '+video_obj.filename)

    #write the .smil file, too.
    smil_data='''<smil><head></head>
    <body>
        <switch>
            <video src="mp4:${vid}" system-bitrate="500000"/>
            <video src="mp4:${vid}" system-bitrate="64000">
                <param name="audioOnly" value="TRUE" valuetype="data"/>
            </video>
        </switch>
    </body></smil>
    '''
    smil_template = Template(smil_data)
    strdict = {'vid': video_obj.filename,}
    smildata = smil_template.substitute(strdict)
    sf = open(file_path+'.smil', 'w')
    sf.write(smildata)
    sf.close()


# the view class def
#class View(grok.View):
#    grok.context(IITDVideo)
#    grok.require('zope2.View')
