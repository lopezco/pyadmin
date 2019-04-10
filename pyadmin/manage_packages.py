import os
import pandas as pd
from pyadmin.cmd import subprocess_cmd, handle_cmd_output


def get_pip_path(env_dir=None, env_name=None):
    pip_path = None
    if env_dir is not None:
        pip_path = os.path.join(env_dir, 'bin', 'pip')
    else:
        env_dir = os.getenv('PYENV_DIR')
        if env_dir is None:
            ValueError('`PYENV_DIR` variable needs to be declared before using this module')
        else:
            pip_path = os.path.join(env_dir, '{env_name}'.format(env_name=env_name), 'bin', 'pip')

    if pip_path is None:
        ValueError('Either specify the env. path with `env_dir` parameter or the env. name with `env_name` and declaring `PYENV_DIR`')
    else:
        return pip_path


def install_package(package_path, update=False, path='', env_name=None):
    update = '-U' if update else ''
    path = '--install-option="--prefix={}"'.format(path) if path else ''
    options = ' '.join((update, path))
    
    pip_to_use = get_pip_path(env_name=env_name)
    bash_command = "{pip} install {options} {package_path}".format(pip=pip_to_use, package_path=package_path,
                                                                   options=options)
    handle_cmd_output(subprocess_cmd(bash_command))
    
    
def uninstall_package(package_name, env_name=None, auto_proceed=True):
    pip_to_use = get_pip_path(env_name=env_name)
    bash_command = "{pip} uninstall {auto_proceed}{package}".format(pip=pip_to_use, package=package_name,
                                                                    auto_proceed='-y ' if auto_proceed else '')
    handle_cmd_output(subprocess_cmd(bash_command))
    
    
def show_package(package_name, env_name=None):
    pip_to_use = get_pip_path(env_name=env_name)
    bash_command = "{pip} show {package}".format(pip=pip_to_use, package=package_name)
    handle_cmd_output(subprocess_cmd(bash_command))
    
    
def pip_freeze(env_name=None):
    pip_to_use = get_pip_path(env_name=env_name)
    tmp = subprocess_cmd('{} freeze'.format(pip_to_use))
    df = pd.DataFrame({'package': tmp[0].split('\n')})
    df = df['package'].str.split('==', expand=True)
    df.columns = ['package', 'version']
    return df
