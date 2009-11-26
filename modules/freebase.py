# Python imports
import urllib
import urllib2

# Local imports
try:
    import simplejson
except ImportError:
    from django.utils import simplejson

import pycmds

MQLREAD_SERVICE = "http://www.freebase.com/api/service/mqlread"
WEB_SERVICE = "http://www.freebase.com/view/guid/"
SEARCH_SERVICE = "http://www.freebase.com/api/service/search?prefix="
TRANS_SERVICE = "http://www.freebase.com/api/trans/blurb/guid/"
IMAGE_SERVICE = "http://www.freebase.com/api/trans/raw/guid/"
THUMBNAIL_SERVICE = "http://www.freebase.com/api/trans/image_thumb/guid/"

def mql_read(q):
    env = {'qname':{'query':q}}
    args = urllib.urlencode({'queries':simplejson.dumps(env)}) 
    url = MQLREAD_SERVICE + '?' + args
    response = urllib2.urlopen(url).read()
    result = simplejson.loads(response)
    return result['qname']['result']

def suggest(prefix, type, limit=10):
    if prefix:
        query = [{
            "name" : None,
            "name~=": "^" + prefix + "*",
            "type" : type,
            "limit": limit
        }]
    else:
        query = [{
            "name" : None,
            "type" : type,
            "limit": limit
        }]
    
    results = mql_read(query)
    return results

def get_url(guid):
    return WEB_SERVICE + guid.lstrip('#')

def get_image_url(guid):
    return IMAGE_SERVICE + guid.lstrip('#')

def get_thumbnail_url(guid, width=50, height=60):
    return THUMBNAIL_SERVICE + guid.lstrip('#') + \
            '?mode=fillcrop&maxheight=' + str(height) + \
            '&maxwidth=' + str(width)

def get_thumbnail_url(guid, width=50, height=60):
    return THUMBNAIL_SERVICE + guid.lstrip('#')

def get_blurb_url(guid, maxlength=250):
    return TRANS_SERVICE + guid.lstrip("#") + "?maxlength=" + str(maxlength)


class FreebaseType(str):
    type = ""
    @classmethod
    def suggest(cls, prefix):
        response = suggest(prefix, cls.type)
        return [suggestion['name'] for suggestion in response]

class FilmActor(FreebaseType):
    type = "/film/actor"
    
class TVActor(FreebaseType):
    type = "/tv/tv_actor"

class CityTown(FreebaseType):
    type = "/location/citytown"
    
class Country(FreebaseType):
    type = "/location/country"
    
class ChemicalCompound(FreebaseType):
    type = "/chemistry/chemical_compound"
    
class ChemicalElement(FreebaseType):
    type = "/chemistry/chemical_element"    
    
class Musician(FreebaseType):
    type = "/music/artist"
    
class TimeZone(FreebaseType):
    type = "/time/time_zone"
    
    


def item_view(items):
    out = ""
    for item in items:
        out += '<div style="border-bottom: 1px dotted #222222; margin-bottom: 2px;">'
        out += '<a href="' + item['link'] + '">' + item['name'] + '</a>'
        out += '<div>' + item['released'] + '</div>'
        out += '</div>'
    return out

@pycmds.cmd("films starring [actor]", FilmActor)
def films_starring(actor):
    results = mql_read([{
            "guid" : None,
            "initial_release_date" : None,
            "sort": "-initial_release_date",
            "name" : None,
            "starring" : [{
                "actor" : {
                    "name" : actor
                }
            }],
            "type" : "/film/film"
        }])
    
    for film in results:
        released = film["initial_release_date"]
        film["link"] = get_url(film["guid"])
        film["released"] = released if released else ""
    return item_view(results)


@pycmds.cmd("television shows starring [actor]", TVActor)
def tv_shows_starring(actor):
    results = mql_read([{
            "name" : actor,
            "starring_roles" : [{
                "series" : {
                    "guid" : None,
                    "name" : None,
                    "air_date_of_first_episode" : None
                }
            }],
            "type" : "/tv/tv_actor"
        }])
    
    shows = []
    for role in results[0]["starring_roles"]:
        released = role["series"]["air_date_of_first_episode"]
        shows.append({
            "name": role["series"]["name"],
            "link": get_url(role["series"]["guid"]),
            "released": released if released else ""
        })
    return item_view(shows)

@pycmds.cmd("albums by [musician]", Musician)
def albums_by(musician):
    results = mql_read([{
            "album" : [{
                "guid": None,
                "name" : None,
                "release_date": None,
                "sort": "-release_date"
            }],
            "name": musician,
            "type": "/music/artist"
        }])
    
    albums = results[0]['album']
    for album in albums:
        released = album["release_date"]
        album["link"] = get_url(album["guid"])
        album["released"] = released if released else ""
    return item_view(albums)

