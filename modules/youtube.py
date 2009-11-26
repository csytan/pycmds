# Python imports
import urllib2

# Django imports
try:
    import simplejson
except ImportError:
    from django.utils import simplejson

# Local imports
import pycmds
import lib
import gdata
import gdata.youtube.service


client = gdata.youtube.service.YouTubeService()
query = gdata.youtube.service.YouTubeVideoQuery()


def commafy(num):
    if len(num) <= 3:
        return num
    else:
        return commafy(num[:-3]) + ',' + num[-3:]



class GoogleSuggestQuery(str):
    service = "http://suggestqueries.google.com/complete/search?nolabels=t&hl=en&ds=yt&client=suggest&json=t&q="
    cache = {}
    
    @classmethod
    def suggest(cls, prefix):
        if not prefix:
            return ["term"]
        if prefix in cls.cache:
            return cls.cache[prefix]
        prefix = urllib2.quote(prefix)
        json = urllib2.urlopen(cls.service + prefix).read()
        response = simplejson.loads(json)
        return cls.cache.setdefault(prefix, response[1])


@pycmds.cmd("youtube search for [term]", GoogleSuggestQuery)
def youtube_search(term):
    query.vq = term
    query.max_results = '10'
    feed = client.YouTubeQuery(query)

    out = ''
    for entry in feed.entry:
        img_url = entry.media.thumbnail[0].url
        title = entry.title.text
        link = entry.link[0].href
        description = entry.media.description.text
        if len(description) > 200:
            description = description[:200] + '...'
        views = 'Views: ' + commafy(entry.statistics.view_count)
        rating = 'Rating: ' + (entry.rating.average if entry.rating else "Unrated")
        
        out += '<div style="clear:left; margin-top:5px;">'
        out += '<img src="' + img_url + '" style="float:left"/>'
        out += '<div style="float:right;height:97px;padding-left:5px;border-left:2px solid grey;width:100px">' + views + '<br/>' + rating + '</div>'
        out += '<div style="height:97px;overflow:hidden; padding:0px 5px;">'
        out += '<a href="' + link + '">' + title + '</a><br/>' + description + '</div>'

        out += '</div>'
    return out
