# Rice generators

A generator module defines a config file generator for a given application. They usually have generic constuctors that let you customize the config on a very direct and low level, meaning everything is changable. However generators should also provide a higher level constructors for creating them:

```py
from dataclasses import dataclass


@dataclass
class Example(ConfigFile):
    @classmethod
    def some_specific(_, ...):
        pass
```

If the consturctor is too specific consider making it a block.
