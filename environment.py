# handles declaration/assignment/access of variables
# also tracks scopes

def char(value): # an 'initializer' for char, since it's not a python datatype
    try: return str(value[0])
    except: raise TypeError

class Environment:

    def __init__(self):
        self.variable_types = {'int': int, 'double': float, 'char': char, 'string': str, 'bool': bool, 'list': list} # associates each YAPL datatype with a python datatype
        self.defaults = {'int': 0, 'double': 0.0, 'char': 'a', 'string': "", 'bool': False, 'list': []} # value assigned when a variable is declared without initializing
        self.env = [{}]

    def declare(self, variable_type, identifier, initial_value = None):
        for scope in self.env:
            if identifier in scope:
                raise Exception('RedeclarationError')

        if initial_value == None:
            self.env[-1][identifier] = {'value': self.defaults[variable_type], 'type': self.variable_types[variable_type]}
        else:
            try:
                self.env[-1][identifier] = {'value': self.variable_types[variable_type](initial_value), 'type': self.variable_types[variable_type]}
            except: raise TypeError

    def assign(self, identifier, value):
        for i, scope in enumerate(self.env):
            if identifier in scope:
                try:
                    self.env[i][identifier]['value'] = self.env[i][identifier]['type'](value)
                except: raise TypeError
                return
        raise NameError

    def access(self, identifier):
        for i, scope in enumerate(self.env):
            if identifier in scope:
                value = self.env[i][identifier]['value']
                return value
        raise NameError

    def push(self):
        self.env.append({})

    def pop(self):
        self.env.pop()