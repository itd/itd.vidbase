from StringIO import StringIO

from zope.component import getUtility
from zope.component import getMultiAdapter

from Products.CMFCore.utils import getToolByName

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from itd.vidbase.config import GLOBALS
from itd.vidbase.config import LAYER_NAME
from itd.vidbase.config import PROJECT_NAME


def install(context):
    """Install CMFNotification.

    Most of the job is done by a Generic Setup profile.
    """
    out = StringIO()

    ## I do not know how (and if it is possible) to define that an
    ## import step is a dependency of the 'rolemap' step.
    addPermissions(context)

    ## Import GenericSetup default profile
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-itd.vidbase:default')

    print >> out, "Successfully installed %s." % PROJECT_NAME
    return out.getvalue()


def uninstall(context):
    """Uninstall itd.vidbase."""
    portal = getToolByName(context, 'portal_url').getPortalObject()

    ## Remove skin layer
    skins_tool = getToolByName(portal, 'portal_skins')
    selections = skins_tool._getSelections()
    for skin, layers in selections.items():
        layers = layers.split(',')
        if LAYER_NAME in layers:
            layers.remove(LAYER_NAME)
        layers = ','.join(layers)
        selections[skin] = layers
