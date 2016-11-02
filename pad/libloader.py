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
        return p

    def call(self, name, args):
        p = self.cook()
        m = p.get(name)

        if m is None:
            self.error(name)

        return m(*args)

    def getname(self, name):
        p = self.cook()
        m = p.get(name)

        if m is None:
            self.error_var(name)

        return m

    def objcall(self, obj, name, args):
        call = getattr(obj, name)
        return call(*args)

    def objname(self, obj, name):
        n = getattr(obj, name)
        return n

    def imp(self, name):
        import importlib
        impmod = importlib.import_module(name)
        mods.update(impmod.__dict__)

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