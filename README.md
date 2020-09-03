Sphinx Viewer
=============

A side by side viewer for Sphinx to allow editing in 'real time'. Helpful
for when actively working on docs. Motivated by needing to write documentation
and wanting to see what it looks like right away. 

Installation
------------

:: 

    git clone git@github.com:badisa/sphinx-viewer.git
    cd sphinx-viewer
    pip install -e .


Running
-------

::

    cd my-doc-repo/
    sphinx-viewer  # Will launch a browser window


Limitations
-----------

* Having multiple tabs open can result in unexpected modifications
* Doesn't support fragments (#some-id-on-page) in the iframe
* Not super responsive
* Never tested on Windozes
* Ace and Bootstrap are served by CDN