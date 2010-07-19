import zope.component
from zope.publisher.interfaces import IRequest
from ZPublisher.BaseRequest import DefaultPublishTraverse
from paste.httpexceptions import HTTPNotFound, HTTPFound
from Products.CMFCore.utils import getToolByName

from pmr2.annotation.curation.browser.interfaces import ICurationToolDisplayForm
from pmr2.annotation.curation.interfaces import ICurationTool


class CurationFlagManagerTraverser(DefaultPublishTraverse):
    """\
    Exposure traverser that catches requests for objects which are not 
    inside zope to pass it into its workspace and commit id to handle.
    """

    zope.component.adapts(ICurationToolDisplayForm, IRequest)

    def publishTraverse(self, request, name):
        # As this traverser is for a form, the parent traverser will not
        # return any object.
        return zope.component.getUtility(ICurationTool).getFlag(name)
