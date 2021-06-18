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
pytest
```

## Publish

- local build 
```
poetry build
```
- local publish to GitHub repo
```
poetry config repositories.[my_repository_name] https://github.com/tingwei628/[my_repository_name].git


// set env in .poetry env and source env !!
export POETRY_USERNAME=[your_username]
export POETRY_PASSWORD=[your_github_personal_access_token]

poetry config http-basic.[my_repository_name] $POETRY_USERNAME $POETRY_PASSWORD
poetry publish -r [my_repository_name]

// after publishing it, i can't find my package (?) on my repo.
```

- install from GitHub
```
poetry add git+https://github.com/tingwei628/[my_python_package].git@v[version_number]
```
or
```
pip install git+ssh://git@github.com/tingwei628/[my_python_package].git@v[version_number]
```

## CI/CD
- GitHub Actions (Lint/Format/Test/Build/Publish/Deploy to Docker(?))

on: push (branch: main, path: src/ or tests/ or pyproject.toml)
how not to preinstall package each time and cache it ?

how to run job on different runner at the same time ?

- git tag
```
git tag -a [tag_name] -m [tag_message]
git push origin [tag_name]

```


### Reference


