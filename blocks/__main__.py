import inspect
import importlib


def main(module: str):
    print(gen_md(importlib.import_module("rice.blocks." + module)))


def gen_md(module) -> str:
    return f"""# {module.title}

**Author**: {module.author}
**Category:** {module.category}
**Description:** {module.description}

# Source

```py
{inspect.getsource(module)}
```
"""


if __name__ == "__main__":
    from sys import argv

    main(argv[1])
