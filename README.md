# nexus-maven-upload

a simple tool upload maven dependency to nexus server

## Usage

* upload whole repository(defalut)

you can upload your whole local repository to nexus server, just set **[specified=False]** in config.ini.

* upload the specified repository

when you need upload some specified dependency to nexus(don't scan the entire repository). you should put the specified dependeny's local path into dependencies.txt(split by line), then set **[specified=True]** in config.ini.
