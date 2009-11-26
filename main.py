# Python imports
import sys
import os
import traceback

# Appengine monkey patch
sys.path.append(os.path.join(os.path.dirname(__file__), 'appengine-monkey'))
import appengine_monkey

# Appengine imports
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache
from google.appengine.ext.webapp import template

# Django imports
from django.utils import simplejson

# Local imports
import pycmds
import modules

CACHING = True

class MainHandler(webapp.RequestHandler):
    path = os.path.join(os.path.dirname(__file__), 'templates','index.html')
    def get(self):
        self.response.out.write(template.render(self.path, None))

class CommandHandler(webapp.RequestHandler):   
    def get(self):
        action = self.request.get('action')
        if action == 'suggest':
            prefix = self.request.get('prefix').encode('utf8')
            suggestions = self.suggest(prefix)
            out = simplejson.dumps(suggestions, ensure_ascii=False)
        elif action == 'dispatch':
            try:
                cmd = self.request.get('cmd').encode('utf8')
                out = self.dispatch(cmd)
            except:
                out = "<h3>Oops! You found a bug. Here's the skinny:</h3>" +\
                '<pre>' + traceback.format_exc() + '</pre>'
        self.response.out.write(out)
        
    def suggest(self, prefix):
        if CACHING:
            suggestions = memcache.get('suggest:' + prefix)
            if suggestions:
                return suggestions
        suggestions = pycmds.suggest(prefix)
        if CACHING:
            memcache.add('suggest:' + prefix, suggestions, time=6000)
        return suggestions
        
    def dispatch(self, cmd):
        if CACHING:
            out = memcache.get('dispatch:' + cmd)
            if out:
                return out
        
        try:
            func, kwargs = pycmds.find(cmd)
        except pycmds.CommandNotFound:
            return """<p><img src="/static/question_mark.png"/> Command not found</p>
        <h4>Tip</h4>
        <p>User inputs should be enclosed within <code>[square brackets]</code></p>
        
        <h4>Example</h4>
        <p>
        For a command such as: <code>films starring [actor]</code><br/>
        You might type: <code>films starring [clint eastwood]</code>
        </p>
        """
        out = func(**kwargs)
        
        if CACHING and not hasattr(func, 'nocache'):
            memcache.add('dispatch:' + cmd, out, time=3600)
        return out
        
application = webapp.WSGIApplication([
        ('/commands', CommandHandler),
        ('/', MainHandler)
    ], debug=False)


def main():
    run_wsgi_app(application)

def profile_main():
    import cProfile, pstats, StringIO, logging
    prof = cProfile.Profile()
    prof = prof.runctx("main()", globals(), locals())
    stream = StringIO.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("time")  # Or cumulative
    stats.print_stats(80)  # 80 = how many to print
    logging.info("Profile data:\n%s", stream.getvalue())


if __name__ == "__main__":
    main()
    #profile_main()