"""
  Copyright 2016 Dominik Madarasz
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

##################################################################################
#                                                                                #
#  LIBRARY LOADER                                                                #
#                                                                                #
##################################################################################

mods = {}


class LibLoader(object):


    def __init__(self):
        import libs
        self.localmods = {}

        for module in libs.__all__:
            self.imp("libs." + module)

    @staticmethod
    def error(name):
        raise NameError("Undefined method: " + name)

    @staticmethod
    def error_var(name):
        raise NameError("Undefined variable: " + name)

    def cook(self):
        import builtins
        p = globals().copy()
        p.update(locals())
        p.update(builtins.__dict__)
        p.update(mods)
        p.update(self.localmods)
        return p

    def call(self, name, args, env):
        if '.' in name:
            parts = name.split('.')
            module = parts[:-1]
            name = parts[-1]
            import importlib
            impmod = importlib.import_module(module[0]).__dict__
            p = impmod
        else:
            p = self.cook()

        m = p.get(name)
        if m is None:
            self.error(name)

        if args is None:
            return m

        nargs = []
        varargs = {}
        for x in args:
            if type(x) is list:
                if x[0] == 'VARARG':
                    key, val = x[1:]
                    varargs.update({key: val})
                else:
                    nargs.append(x)
            else:
                nargs.append(x)

        # HACK!
        if name.lower() == "extern":
            nargs.append(env)

        return m(*nargs, **varargs)

    def getname(self, name):
        p = self.cook()
        m = p.get(name)

        if m is None:
            self.error_var(name)

        return m

    def objcall(self, obj, name, args):
        call = getattr(obj, name)

        if args is None:
            return call
        return call(*args)

    def objname(self, obj, name):
        n = getattr(obj, name)
        return n

    def imp(self, name, local=False):
        import importlib
        if '*' in name:
            n = '.'.join(name.split('.')[:-1])
            m = name.split('.')[-1]
            pak = importlib.import_module(n)
            import pkgutil

            for imp, mod, ispkg in pkgutil.iter_modules(pak.__path__):
                if mod == "__main__":
                    continue
                im = importlib.import_module(n+"."+mod, pak)
                self.localmods.update(im.__dict__)
        else:
            impmod = importlib.import_module(name)
            self.localmods.update(impmod.__dict__)

        if local is False:
            mods.update(self.localmods)

"""        for mod in self.mods:
            module = mod[0]
            methods = mod[1:]

            for m in methods:
                if m.upper() != name.upper():
                    continue

                cls = getattr(module, m)
                obj = cls()
                return obj.call(args)
"""