from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='log2notify',
      version='0.1',
      description='Provides file changes to tray notification',
      long_description=readme(),
      url='http://github.com/meatbot/log2notify',
      author='Aleksei Egorov',
      author_email='egorov.lexer@yandex.ru',
      license='MIT',
      packages=['log2notify'],
      install_requires=[
          'pyinotify',
          'plyer',
      ],
      entry_points={
          'console_scripts': ['log2notify=log2notify:main'],
      },
      include_package_data=True,
      zip_safe=False)
