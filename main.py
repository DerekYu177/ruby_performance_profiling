import subprocess
import os

FILES = {
    'cruby': 'ruby.versions'
    'jruby': 'jruby.versions',
}

RESULTS = 'results.csv'

all_versions = {}
for interpreter, file_name in FILES.items():
    with open(file_name, 'r') as f:
        versions = f.read()

    versions.strip('\n').split('\n')
    all_versions.update({interpreter: versions})

def command(interpreter_type):
    if interpreter_type == 'cruby':
        return 'ruby bin/optcarrot --benchmark examples/Lan_Master.nes'
    if interpreter_type == 'jruby':
        return 'jruby -r ./tools/shim.rb -Ilib bin/optcarrot --benchmark examples/Lan_Master.nes'

def install_all_uninstalled_versions():
    output = subprocess.run('rvm list strings', capture_output=True, shell=True)
    installed_versions = set(output.strip('\n').split('\n'))

    all_required_versions = set()
    [all_required_versions.update(v) for v in all_versions.values()]

    uninstalled_versions = all_required_versions - installed_versions

    for version in uninstalled_versions:
        subprocess.run(f'rvm install {version}', shell=True)

def main():
    install_all_uninstalled_versions()

    # jruby breaks if we are not in the correct directory
    subprocess.run('cd optcarrot', shell=True)

    for interpreter_type, versions in all_versions.items():
        for version in versions:
            subprocess.run(f'rvm use {version}', shell=True)

            fpses = []
            for i in range(5):

                benchmark_command = command(interpreter_type)
                result = subprocess.run(benchmark_command, capture_output=True, shell=True)

                fps, checksum = result.strip('\n').split('\n')
                fpses.append(fps)

            with open(os.path.join('..', RESULTS), 'w+') as f
                f.write(','.join([interpreter_type, version, *[fpses]]))

    subprocess.run('cd ..')

if __name__ == '__main__':
    main()
