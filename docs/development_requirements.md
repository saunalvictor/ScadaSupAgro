Development requirements
=========================

Installation of MkDocs
----------------------

Documentation of the SCADA is in MkDocs format (https://www.mkdocs.org/).

The documentation displays on github needs to install MkDocs and some extensions:

```sh
sudo apt install python3-pip
python3 -m pip install mkdocs
python3 -m pip install python-markdown-math
python3 -m pip install mkdocs-material
```

Displaying documentation locally
--------------------------------

Type one of these commands: 

```sh
mkdocs serve
python3 -m mkdocs serve
```

Deploying documentation on github
---------------------------------

After committing the source of the doc to the master branch of the github repository, type one of these commands: 

```sh
mkdocs gh-deploy
python3 -m mkdocs gh-deploy
```

The URL of the documentation is: https://ddorch.github.io/Scada_DDorch/

