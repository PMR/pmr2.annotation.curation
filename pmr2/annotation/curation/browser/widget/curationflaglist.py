import zope.component
import zope.interface

from zope.pagetemplate.interfaces import IPageTemplate

from z3c.form.interfaces import IFormLayer, IFieldWidget, ISubformFactory
from z3c.form.interfaces import IDataManager, IObjectFactory, NO_VALUE
from z3c.form.field import Fields

from z3c.form.converter import BaseDataConverter

from z3c.form.object import ObjectSubForm, makeDummyObject, SubformAdapter

from z3c.form.browser.widget import HTMLFormElement
from z3c.form.browser.multi import MultiWidget
from z3c.form.browser.object import ObjectWidget
from z3c.form.widget import Widget, FieldWidget
from z3c.form.browser import widget

from pmr2.annotation.curation.schema.interfaces import IBasicCurationDict
from pmr2.annotation.curation.browser.widget.interfaces import \
    ICurationFlagListWidget

from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.tool import buildSchemaInterface


# Object based widget and support classes.

class CurationFlagListSubForm(ObjectSubForm):

    def setupFields(self):
        # should provide method or something
        ct = zope.component.getUtility(ICurationTool)
        schema = buildSchemaInterface(ct.all_flags)
        self.fields = Fields(schema)


class CurationFlagListConverter(BaseDataConverter):
    """Data converter for IObjectWidget."""

    zope.component.adapts(
        IBasicCurationDict, ICurationFlagListWidget)

    @property
    def schema(self):
        ct = zope.component.queryUtility(ICurationTool)
        flags = ct is not None and ct.all_flags or []
        schema = buildSchemaInterface(flags)
        return schema

    def toWidgetValue(self, value):
        """Just dispatch it."""
        if value is self.field.missing_value:
            return NO_VALUE

        retval = {}
        for name in zope.schema.getFieldNames(self.schema):
            dm = zope.component.getMultiAdapter(
                (value, self.schema[name]), IDataManager)
            retval[name] = dm.query()

        return retval

    def createObject(self, value):
        #keep value passed, maybe some subclasses want it
        #value here is the raw extracted from the widget's subform
        #in the form of a dict key:fieldname, value:fieldvalue

        name = getIfName(self.schema)
        creator = zope.component.queryMultiAdapter(
            (self.widget.context, self.widget.request,
             self.widget.form, self.widget),
            IObjectFactory,
            name=name)
        if creator:
            obj = creator(value)
        else:
            raise ValueError("No IObjectFactory adapter registered for %s" %
                             name)

        return obj

    def toFieldValue(self, value):
        """field value is an Object type, that provides schema"""
        if value is NO_VALUE:
            return self.field.missing_value

        if self.widget.subform is None:
            #creepy situation when the widget is hanging in nowhere
            obj = self.createObject(value)
        else:
            if self.widget.subform.ignoreContext:
                obj = self.createObject(value)
            else:
                dm = zope.component.getMultiAdapter(
                    (self.widget.context, self.field), IDataManager)
                try:
                    obj = dm.get()
                except KeyError:
                    obj = {} # self.createObject(value)
                except AttributeError:
                    obj = {} # self.createObject(value)

        if obj is None or obj == self.field.missing_value:
            #if still None create one, otherwise following will burp
            obj = {}

        # don't need to adapt our schema since the dictionary converter
        # will deal with that (never mind how dict do not get adapted).

        # obj = self.schema(obj)

        names = []
        for name in zope.schema.getFieldNames(self.schema):
            try:
                dm = zope.component.getMultiAdapter(
                    (obj, self.schema[name]), IDataManager)
                oldval = dm.query()
                if (oldval != value[name]
                    or zope.schema.interfaces.IObject.providedBy(
                        self.schema[name])
                    ):
                    dm.set(value[name])
                    names.append(name)
            except KeyError:
                pass

        if names:
            zope.event.notify(
                zope.lifecycleevent.ObjectModifiedEvent(obj,
                    zope.lifecycleevent.Attributes(self.schema, *names)))
        return obj


class CurationFlagListWidget(ObjectWidget):
    zope.interface.implements(ICurationFlagListWidget)

    @property
    def schema(self):
        ct = zope.component.queryUtility(ICurationTool)
        flags = ct is not None and ct.all_flags or []
        schema = buildSchemaInterface(flags)
        return schema

    def _getForm(self, content):
        form = getattr(self, 'form', None)
        schema = self.schema

        self.subform = zope.component.getMultiAdapter(
            (content, self.request, self.context,
             form, self, self.field, makeDummyObject(schema)),
            ISubformFactory)()

    @apply
    def value():
        """
        This invokes updateWidgets on any value change e.g. update/extract.
        """

        def get(self):
            #value (get) cannot raise an exception, then we return insane values
            try:
                self.setErrors=True
                return self.extract()
            except MultipleErrors:
                value = {}
                for name in zope.schema.getFieldNames(self.schema):
                    value[name] = self.subform.widgets[name].value
                return value
        def set(self, value):
            self._value = value
            self.updateWidgets()

            # ensure that we apply our new values to the widgets
            if value is not NO_VALUE:
                for name in zope.schema.getFieldNames(self.schema):
                    self.applyValue(self.subform.widgets[name],
                                    value.get(name, NO_VALUE))

        return property(get, set)

    def render(self):
        """See z3c.form.interfaces.IWidget."""
        template = self.template
        schema = self.schema

        if template is None:
            template = zope.component.queryMultiAdapter(
                (self.context, self.request, self.form, self.field, self,
                 makeDummyObject(schema)),
                IPageTemplate, name=self.mode)
            if template is None:
                #return super(ObjectWidget, self).render()
                return Widget.render(self)
        return template(self)


class CurationFlagListSubformAdapter(SubformAdapter):
    """Most basic-default subform factory adapter"""

    zope.component.adapts(zope.interface.Interface, #widget value
                          IFormLayer,    #request
                          zope.interface.Interface, #widget context
                          zope.interface.Interface, #form
                          ICurationFlagListWidget, #widget
                          zope.interface.Interface, #field
                          zope.interface.Interface) #field.schema

    factory = CurationFlagListSubForm




@zope.interface.implementer(IFieldWidget)
def BasicCurationDictFieldWidget(field, request):
    """IFieldWidget factory for BasicCurationDict."""
    # While I could get the BasicCurationDict to implement IObject,
    # doing this additional step may allow finer control later.
    return FieldWidget(field, CurationFlagListWidget(request))
