import urllib2
try:
    import simplejson
except ImportError:
    from django.utils import simplejson
import pycmds

TRANSLATE_SERVICE = "http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&"

class Language(str):
    languages = {
        'chinese': 'zh', 
        'german': 'de', 
        'chinese traditional': 'zh-TW', 
        'belarusian': 'be', 
        'galician': 'gl', 
        'macedonian': 'mk', 
        'urdu': 'ur', 
        'polish': 'pl', 
        'swahili': 'sw', 
        'icelandic': 'is', 
        'vietnamese': 'vi', 
        'romanian': 'ro', 
        'oriya': 'or', 
        'uighur': 'ug', 
        'sanskrit': 'sa', 
        'khmer': 'km', 
        'hungarian': 'hu', 
        'bihari': 'bh', 
        'catalan': 'ca', 
        'laothian': 'lo', 
        'korean': 'ko', 
        'finnish': 'fi', 
        'serbian': 'sr', 
        'italian': 'it', 
        'portuguese': 'pt-PT', 
        'czech': 'cs', 
        'basque': 'eu', 
        'japanese': 'ja', 
        'amharic': 'am', 
        'persian': 'fa', 
        'tajik': 'tg', 
        'estonian': 'et', 
        'telugu': 'te', 
        'marathi': 'mr', 
        'pashto': 'ps', 
        'gujarati': 'gu', 
        'dutch': 'nl', 
        'dhivehi': 'dv', 
        'french': 'fr', 
        'armenian': 'hy', 
        'sinhalese': 'si', 
        'afrikaans': 'af', 
        'filipino': 'tl', 
        'uzbek': 'uz', 
        'albanian': 'sq', 
        'turkish': 'tr', 
        'tibetan': 'bo', 
        'latvian': 'lv', 
        'croatian': 'hr', 
        'inuktitut': 'iu', 
        'slovak': 'sk', 
        'spanish': 'es', 
        'esperanto': 'eo',  
        'hindi': 'hi', 
        'danish': 'da', 
        'bulgarian': 'bg', 
        'georgian': 'ka', 
        'malay': 'ms', 
        'bengali': 'bn', 
        'russian': 'ru', 
        'thai': 'th', 
        'tamil': 'ta', 
        'tagalog': 'tl', 
        'malayalam': 'ml', 
        'indonesian': 'id', 
        'kannada': 'kn', 
        'mongolian': 'mn', 
        'hebrew': 'iw', 
        'arabic': 'ar', 
        'swedish': 'sv', 
        'cherokee': 'chr', 
        'slovenian': 'sl', 
        'azerbaijani': 'az', 
        'sindhi': 'sd', 
        'kyrgyz': 'ky', 
        'ukrainian': 'uk', 
        'lithuanian': 'lt', 
        'norwegian': 'no', 
        'maltese': 'mt', 
        'kazakh': 'kk', 
        'chinese simplified': 'zh-CN', 
        'kurdish': 'ku', 
        'nepali': 'ne', 
        'guarani': 'gn', 
        'punjabi': 'pa', 
        'greek': 'el', 
        'burmese': 'my', 
        'english': 'en'
    }

    def __init__(self, lang):
        if lang in self.languages:
            self.abbr = self.languages[lang]
        else:
            raise TypeError

    @classmethod
    def suggest(cls, prefix):
        suggestions = []
        for lang in cls.languages:
            if lang.startswith(prefix):
                suggestions.append(lang)
        return suggestions


@pycmds.cmd("translate [text] to [language]", str, Language)
def translate(text, language):
    response = urllib2.urlopen(TRANSLATE_SERVICE + "q=" + urllib2.quote(text) + \
                "&langpair=%7C" + language.abbr).read()
    json = simplejson.loads(response)
    try:
        translated = json['responseData']['translatedText']
    except TypeError:
        return '<p>Sorry, no translation was found</p>'
    return '<p>' + translated + '</p>' + \
        'Powered by<img style="padding-left: 1px; vertical-align: middle;" src="http://www.google.com/uds/css/small-logo.png">'
    