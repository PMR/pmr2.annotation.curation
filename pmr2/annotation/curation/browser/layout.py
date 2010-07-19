import zope.interface
from zope.publisher.interfaces import IPublishTraverse
from plone.z3cform.layout import FormWrapper


class TraverseFormWrapper(FormWrapper):
    """\
    This wrapper implements IPublishTraverse and passes invocation of
    the publishTraverse method into the form_instance.
    """

    zope.interface.implements(IPublishTraverse)

    def publishTraverse(self, request, name):
        # should this be an assert?
        if IPublishTraverse.providedBy(self.form_instance):
            self.form_instance.publishTraverse(request, name)
        return self
