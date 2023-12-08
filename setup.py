from setuptools import setup

class CONFIG:
    VERSION = 'v0.1'
    platform = 'darwin-x86_64'
    executable_stub = '/opt/anaconda3/envs/Personal/lib/libpython3.11.dylib' # this is important, check where is your Python framework and get the `dylib`
    APP_NAME = f'Tidy Tune'
    APP = ['GUIViewer.py']
    DATA_FILES = [
        # 'config.json',
        # 'countries_list.txt',
        # ('modules', ['modules/app.ico']),
        # this modules are automatically added if you use __init__.py in your folder
        # ('modules', ['modules/scraper_module.py']),
        # ('modules', ['modules/gui_module.py']),
        #From: https://stackoverflow.com/questions/74619476/how-to-compile-tkinter-as-an-executable-for-macos
    ]

    OPTIONS = {
        'argv_emulation': False,
        'iconfile': '/Users/connorforsythe/Documents/GitHub/TidyTune/res/AppIcon.ico',
        'plist': {
            'CFBundleName': APP_NAME,
            'CFBundleDisplayName': APP_NAME,
            'CFBundleGetInfoString': APP_NAME,
            'CFBundleVersion': VERSION,
            'CFBundleShortVersionString': VERSION,
            'PyRuntimeLocations': [
                executable_stub,
                # also the executable can look like this:
                #'@executable_path/../Frameworks/libpython3.4m.dylib',
            ]
        }
    }

def main():
    setup(
        name=CONFIG.APP_NAME,
        app=CONFIG.APP,
        data_files=CONFIG.DATA_FILES,
        options={'py2app': CONFIG.OPTIONS},
        setup_requires=['py2app'],
        maintainer='Connor R. Forsythe, Ph.D.',
        author_email='connorrforsythe@gmail.com',
    )

if __name__ == '__main__':
    main()