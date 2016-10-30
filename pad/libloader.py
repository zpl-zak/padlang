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


class LibLoader(object):
    def __init__(self):
        import inspect
        import pkgutil
        import libs
        import importlib
        import sys
        self.mods = []

        for module in libs.__all__:
            impmod = importlib.import_module('libs.'+module)
            data = [impmod]
            for name, obj in inspect.getmembers(impmod):
                if inspect.isclass(obj):
                    data.append(name)
            self.mods.append(data)

    @staticmethod
    def error(name):
        raise NameError("Undefined method: " + name)

    def call(self, name, args):
        p = globals().copy()
        p.update(locals())
        m = p.get(name)

        if m is None:
            import builtins
            m = builtins.__dict__[name]

            if m is None:
                self.error(name)

        return m(*args)


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