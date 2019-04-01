import subprocess
import os

FILES = {
    'cruby': 'ruby.versions',
    'jruby': 'jruby.versions',
}

RESULTS = 'results.csv'

all_versions = {}
for interpreter, file_name in FILES.items():
    with open(file_name, 'r') as f:
        versions = f.read()

    all_versions.update({interpreter: versions.strip('\n').split('\n')})

def command(interpreter_type):
    if interpreter_type == 'cruby':
        return 'bin/optcarrot --benchmark examples/Lan_Master.nes'
    if interpreter_type == 'jruby':
        return '-r ./tools/shim.rb -Ilib bin/optcarrot --benchmark examples/Lan_Master.nes'

def install_all_uninstalled_versions():
    output = subprocess.run('rvm list strings', capture_output=True, shell=True)
    installed_versions = set(output.stdout.decode('utf-8').strip('\n').split('\n'))

    all_required_versions = set()
    [all_required_versions.update(v) for v in all_versions.values()]

    uninstalled_versions = all_required_versions - installed_versions

    for version in uninstalled_versions:
        print(f'installing version {version}')
        subprocess.run(f'rvm install {version}', shell=True)

def main():
    install_all_uninstalled_versions()

    # jruby breaks if we are not in the correct directory
    os.chdir('./optcarrot')

    for interpreter_type, versions in all_versions.items():
        for version in versions:
            fpses = []
            for i in range(5):

                benchmark_command = command(interpreter_type)
                print(f'running result {i}')
                result = subprocess.run(f'rvm {version} do {benchmark_command}', capture_output=True, shell=True)

                if result.stderr:
                    continue

                fps, checksum = result.stdout.decode('utf-8').strip('\n').split('\n')
                fpses.append(fps)

            print(f'Writing results back to file')
            with open(os.path.join('..', RESULTS), 'a') as f:
                f.write(','.join([interpreter_type, version, *fpses]) + '\n')

if __name__ == '__main__':
    main()
