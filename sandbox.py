# Python imports
import sys
import os
import urllib2
import traceback
import types

# Appengine monkey patch
sys.path.append(os.path.join(os.path.dirname(__file__), 'appengine-monkey'))
import appengine_monkey

# Appengine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template

# Django imports
from django.utils import simplejson

# Local imports
import pycmds
import main
import modules

main.CACHING = False

class PythonModule(db.Model):
    source = db.TextProperty()

def load_source(name, source):
    reload(pycmds)
    mod = types.ModuleType(str(name))
    mod.__dict__.update(modules.__dict__)
    exec source in mod.__dict__
    return mod

class SandboxIndex(webapp.RequestHandler):
    def get(self):
        mods = PythonModule.all().fetch(10)
        path = os.path.join(os.path.dirname(__file__), 'templates','sandbox.html')
        template_values = {
            "mods": [mod.key().name() for mod in mods]
        }
        self.response.out.write(template.render(path, template_values))
    
class ModuleEditor(webapp.RequestHandler):
    def get(self, name):
        mod = PythonModule.get_by_key_name(name)
        path = os.path.join(os.path.dirname(__file__), 'templates','editor.html')
        template_values = {
            "name": name,
            "source": mod.source if mod else ""
        }
        self.response.out.write(template.render(path, template_values))
    
    def post(self, name):
        source = self.request.get('source', '').replace("\r\n", "\n")
        mod = PythonModule.get_by_key_name(name)
        if not mod:
            mod = PythonModule(key_name=name)
            
        try:
            load_source(name, source)
            mod.source = source
            mod.put()
            out = "Module Saved"
        except:
            out = traceback.format_exc()
        self.response.out.write(out)

class CommandTester(main.CommandHandler):
    def get(self, name):
        data = PythonModule.get_by_key_name(name)
        source = data.source if data else ""
        mod2 = load_source(name, source)
        
        main.pycmds = pycmds
        main.CommandHandler.get(self)
        
application = webapp.WSGIApplication([
        ('/', SandboxIndex),
        ('/(.*)/commands', CommandTester),
        ('/(.*)', ModuleEditor)
    ], debug=True)

if __name__ == "__main__":
    run_wsgi_app(application)