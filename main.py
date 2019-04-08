import subprocess
import os

FILES = {
#    'cruby': 'ruby.versions',
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
    # install_all_uninstalled_versions()

    # jruby breaks if we are not in the correct directory
    os.chdir('./optcarrot')

    for interpreter_type, versions in all_versions.items():
        versions.reverse()

        for version in versions:

            if interpreter_type == 'jruby':
                # subprocess.run(['/bin/bash', '--login'], shell=True)
                subprocess.run(f'rvm use {version}', shell=True)

            fpses = []
            for i in range(5):

                benchmark_command = command(interpreter_type)
                print(f'running result {i}')

                if interpreter_type == 'cruby':
                    result = subprocess.run(f'rvm {version} do {benchmark_command}',
                            capture_output=True,
                            shell=True)
                else:
                    result = subprocess.run(f'ruby {benchmark_command}',
                            capture_output=True,
                            shell=True)

                if result.stderr:
                    continue

                fps = [output for output in
                        result.stdout.decode('utf-8').strip('\n').split('\n')
                        if 'fps' in output][0]

                fpses.append(fps)

            print(f'Writing results back to file')
            with open(os.path.join('..', RESULTS), 'a') as f:
                f.write(','.join([interpreter_type, version, *fpses]) + '\n')

def run_jruby_specifically():
    os.chdir('optcarrot')

    jrubies = subprocess.run('rvm list strings | grep jruby', shell=True,
            capture_output=True).stdout.decode('utf-8').strip('\n').split('\n')

    # jruby < 1.7 cannot run the benchmark
    # jrubies = [version for version in jrubies
    #        if 'jruby-9.1' in version or 'jruby-9.2' in version]

    versions = {}
    for jruby_version in jrubies:
        versions[jruby_version] = []


    for i in range(5):
        print(f'running {i}')

        jrubies_results = subprocess.run(
                f'rvm {",".join(jrubies)} do '\
                'ruby -r ./tools/shim.rb -Ilib bin/optcarrot '\
                '--benchmark examples/Lan_Master.nes',
                shell=True, capture_output=True)\
                .stdout.decode('utf-8').strip('\n').split('\n')

        # assume that the output order is the same as the running order
        fps_results = [result for result in jrubies_results if 'fps' in result]

        for fps_result, version in zip(fps_results, jrubies):
            versions[version].append(fps_result)

    os.chdir('..')

    with open('jruby_results2.csv', 'w+') as f:
        for version, fps in versions.items():
            f.write(f'jruby,{version},{",".join(fps)}\n')


if __name__ == '__main__':
    # main()

    run_jruby_specifically()
