import os
import random
import urllib2

# Local imports
import pycmds
import utils
try:
    import simplejson
except ImportError:
    from django.utils import simplejson

@pycmds.cmd("the zen of python")
def zen():
    return """<pre>
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
</pre>"""

@pycmds.cmd("random number between 1 and 100")
@utils.nocache
def random_to_hundred():
	return random.randint(1, 100)

@pycmds.cmd("my ip address")
@utils.nocache
def my_ip_address():
    return os.environ['REMOTE_ADDR']

@pycmds.cmd("flickr images tagged with [tag]")
def flickr(tag):
    service = "http://api.flickr.com/services/feeds/photos_public.gne?tagmode=any&format=json&nojsoncallback=1&tags="
    json = urllib2.urlopen(service + urllib2.quote(tag)).read()
    results = simplejson.loads(json)
    
    out = ""
    for item in results['items']:
        out += '<img src="' + item['media']['m'] + '"/>'
    return out

@pycmds.cmd("cgi environment variables")
@utils.nocache
def cgi_environment_vars():
    out = '<table><tbody>'
    for attr, val in os.environ.iteritems():
        out += '<tr><td>' + str(attr) + '</td><td>' + str(val) +'</td></tr>'
    return out + '</tbody></table>'

@pycmds.cmd("the answer to life, the universe, and everything")
def answer_to_everything():
    return 42

@pycmds.cmd("help")
def help_cmd():
    return """
<p>To get a list of commands, type <code>list commands</code> in the
command line below and press <strong>Enter</strong>.</p>

<p>Commands which have text enclosed within <code>[square brackets]</code> can 
accept user input.  To run a command, simply replace the bracketed text with 
your own input.

<h4>Example</h4>
<p>
For a command such as: <code>films starring [actor]</code><br/>
You might type: <code>films starring [clint eastwood]</code>
</p>

<h4>Tips</h4>
<p>Suggestions are shown at every step of the way, until you have a completed 
command. If you aren't seeing any suggestions, make sure that the command exists 
and your inputs are valid.</p>

<p>The Enter key can be used to auto-complete a command. This can be 
helpful for quickly moving from one input to the next.</p>

<h4>More Examples</h4>
<pre>my ip address</pre>
<pre>films starring [clint eastwood]</pre>
<pre>albums by [led zeppelin]</pre>
<pre>translate [hello world!] to [japanese]</pre>
<pre>currency convert [100] from [U.S. Dollar (USD)] to [Canadian Dollar (CAD)]</pre>
"""
   

@pycmds.cmd("list commands")
def list_commands():
    commands = pycmds.suggest('')
    html = ''
    for command in commands:
        html += '<pre>' + command + '</pre>'
    return html
    
    
    
    
    