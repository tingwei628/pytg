## Venv

- create a virtual env and activate
```
python3 -m venv [virtual_env_name]
source [virtual_env_name]/bin/activate

```

- detactive and delete a virtual env

```
detactive
rm -r [virtual_env_name]
```

- install a package in virtual env
```
python3 -m pip install [package_name]
```

## Poetry

- create a virtual env in vscode 
```
poetry shell
```

- delete venv created by poetry
```
cd [folder where pyproject.toml is]
poetry env list // (this will show you the venv for that project)
poetry env remove [virtual_env_name]
```


## Test

```
sample_package/
├── __init__.py
├── sample_module.py
└── sample_module_import.py
```

```
import [module]
```

```
from [module] import [name1, name2, ...]
```

```
package
├── __init__.py
├── subpackage1
│   ├── __init__.py
│   ├── moduleX.py
│   └── moduleY.py
├── subpackage2
│   ├── __init__.py
│   └── moduleZ.py
└── moduleA.py
```


### Reference
- [Python projects with Poetry and VSCode. Part 1](https://www.pythoncheatsheet.org/blogpython-projects-with-poetry-and-vscode-part-1/)

- [Python projects with Poetry and VSCode. Part 3](https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-3/)

