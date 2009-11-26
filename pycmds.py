"""
Pycmds - A simple command line interpreter.

The `cmd` decorator is used to register functions as commands.  It takes a 
schema string which will be displayed to the user:

    >>> @cmd("hello world!")
    ... def hello_world():
    ...     return "hi there!"
    ...     

The `suggest` function is used to get a list of commands that start with a 
given prefix.  To find commands that start with "h", type:

    >>> suggest('h')
    ['hello world!']

To run the command, use the `dispatch` function:

    >>> dispatch('hello world!')
    'hi there!'

Commands can take user input, by enclosing inputs within square brackets.  
During command dispatch, the inputs are passed to the function as keyword 
arguments stripped of their non-alphanumeric characters.

The `cmd` decorator may be called with additional type classes, which will be 
initialized with a string before being passed to the function:

    >>> @cmd("sum of [x] and [y]", int, int)
    ... def summizer(x, y):
    ...     return x + y
    ...     
    >>> dispatch("sum of [14] and [23]")
    37

Types are bound to the function arguments in the same order listed in the 
decorator call. If no type classes are specified, it defaults to a string.

Types may provide suggestions to the user if they have a `suggest` function.
The `suggest` function is called with a `prefix` string, and returns a list of 
possible completions:

    >>> class Fruit(str):
    ...     @staticmethod
    ...     def suggest(prefix):
    ...         fruits = ['apple', 'apricot', 'banana', 'pear']
    ...         return [fruit for fruit in fruits if fruit.startswith(prefix)]
    ...     
    >>> @cmd("my favorite fruit is [fruit]", Fruit)
    ... def fav_fruit(fruit):
    ...     return "wow! my favorite fruit is " + fruit + " too!"
    ...     

    >>> suggest('my ')
    ['my favorite fruit is [fruit]']
    >>> suggest('my favorite fruit is [')
    ['my favorite fruit is [apple]', 'my favorite fruit is [apricot]', 'my favorite fruit is [banana]', 'my favorite fruit is [pear]']
    >>> suggest('my favorite fruit is [a')
    ['my favorite fruit is [apple]', 'my favorite fruit is [apricot]']
    
    >>> dispatch('my favorite fruit is [berry]')
    'wow! my favorite fruit is berry too!'
    
Note that the suggest function is called directly from the type, and not an 
instance of the type, so the use of @staticmethod or @classmethod is recommended.
"""
import re

_TRIE = {}
_TOKEN_RE = re.compile("""
(           # start group
\[.*?\]     # input string
|           # or
[^\[^\]]+   # non input string
|           # or
\[[^\]]*$   # incomplete input
)           # end group
""", flags=re.VERBOSE)

class Error(Exception):
    pass

class CommandNotFound(Error):
    pass

def cmd(schema, *types):
    """Decorator for registering a command.
    
    schema:
        A schema is a string describing what the function does and what inputs
        it can accept.  Inputs may be specified, by enclosing them within 
        square brackets.  
        
    types:
        Types are classes which are bound to the function arguments in the 
        same order listed in the decorator call.  On command dispatch, they are
        initialized with an input string before being passed to the function.  
        
        Invalid inputs should raise a TypeError on initialization.  
        
        In Python 3.0, function annotations may be used instead of the 
        `types` parameter.
    """
    def decorator(func):
        if not hasattr(func, 'func_annotations'):
            func.func_annotations = {}
        
        if types:
            args = func.func_code.co_varnames
            for arg, type in zip(args, types):
                func.func_annotations[arg] = type
        add_command(schema, func)
        return func
    return decorator

def add_command(schema, func, node=_TRIE):
    func.schema = schema
    for token in _TOKEN_RE.findall(schema):
        if token.startswith('['):
            # input token
            arg = token.strip('[').rstrip(']')
            func_arg = re.sub('\W', '', arg)
            type = func.func_annotations.get(func_arg, str)
            args = node.setdefault('args', {})
            node = args.setdefault((arg, type), {})
        else:
            # non-input token
            for char in token:
                node = node.setdefault(char, {})
    node["func"] = func
    
    
def _matches(tokens, node=_TRIE, kwargs={}):
    """Depth first search for the node matching the tokens
    
    Yields:
        a tuple containing the node, and the keyword arguments, respectively
    """
    if tokens:
        token = tokens.pop(0)
    else:
        yield node, kwargs
        return
    
    if token.startswith('['):
        # validate inputs
        input = token.strip('[').rstrip(']')
        if 'args' not in node: return
        args = node['args'].iteritems()
        for (arg, type), node in args:
            kwargs = kwargs.copy()
            func_arg = re.sub('\W', '', arg)
            try:
                kwargs[func_arg] = type(input)
            except (TypeError, ValueError):
                continue
            for match in _matches(tokens, node, kwargs):
                yield match
    else:
        # validate non-input chars
        for char in token:
            try:
                node = node[char]
            except KeyError:
                return
        for match in _matches(tokens, node, kwargs):
            yield match
  
def find(command):
    """Finds the first matching command.
    Returns the function and keyword arguments
    """
    tokens = _TOKEN_RE.findall(command)
    for node, kwargs in _matches(tokens):
        if 'func' in node:
            return (node['func'], kwargs)
    raise CommandNotFound

def dispatch(command):
    func, kwargs = find(command)
    return func(**kwargs)

def _complete(prefix, node, suggestions):
    """Completes the prefix by recursively traversing all possible suffixes 
    starting from the given node"""
    for key in node:
        if key == 'func':
            # end of command
            suggestions.append(prefix)
        elif key == 'args':
            # argument
            args = node['args'].iteritems()
            for (arg, type), node in args:
                _complete(prefix + '[' + arg + ']', node, suggestions)
        else:
            # character
            _complete(prefix + key, node[key], suggestions)
    return suggestions

def suggest(prefix):
    """Returns a list of possible completions for a given command prefix"""
    tokens = _TOKEN_RE.findall(prefix)
    
    # look for incomplete input
    input = None
    if tokens:
        end = tokens[-1]
        if end.startswith('[') and not end.endswith(']'): 
            input = tokens.pop().strip('[')
            prefix = ''.join(tokens)
        
    suggestions = []
    for node, kwargs in _matches(tokens):
        if input is None:
            _complete(prefix, node, suggestions)
        else:
            if 'args' not in node: continue
            args = node['args'].iteritems()
            for (arg, type), node in args:
                if hasattr(type, 'suggest'):
                    # get suggestions
                    for suggestion in type.suggest(input):
                        _complete(prefix + '[' + suggestion + ']', node, suggestions)
                elif input:
                    # validate input
                    try:
                        type(input)
                    except (TypeError, ValueError):
                        continue
                    _complete(prefix + '[' + input + ']', node, suggestions)
                else:
                    _complete(prefix + '[' + arg + ']', node, suggestions)
    return suggestions

if __name__ == "__main__":
    import doctest
    doctest.testmod()
