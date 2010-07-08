from StringIO import StringIO
from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.tool import CurationTool

def add_curation_tool(site):
    """Add the curation tool to site manager"""
    out = StringIO()
    sm = site.getSiteManager()
    if not sm.queryUtility(ICurationTool):
        print >> out, 'PMR2 Curation Tool registered'
        sm.registerUtility(ICurationTool(site), ICurationTool)
    return out.getvalue()

def remove_curation_tool(site):
    """Remove the curation tool from the site manager"""
    out = StringIO()
    sm = site.getSiteManager()
    u = sm.queryUtility(ICurationTool)
    if u:
        print >> out, 'PMR2 Curation Tool unregistered'
        sm.unregisterUtility(u, ICurationTool)
    return out.getvalue()

def importVarious(context):
    """Manually register the require parts."""

    site = context.getSite()
    print add_curation_tool(site)
