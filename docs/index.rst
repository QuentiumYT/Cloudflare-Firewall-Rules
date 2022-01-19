*****************************************************
Welcome to Cloudflare's Firewall Rules documentation!
*****************************************************

.. currentmodule:: cf

.. toctree::
    :maxdepth: 4
    :caption: Introduction:

    self

Cloudflare Firewall Rules is a wrapper library that aims to easily modify, create and import, export new rules in your domain's firewall.

If you have a single rule that you want to duplicate among your domains, you can simply write 3 lines to do that :)

Note: You can also import several rules into several domains at once!

Installation:
-------------

.. code-block:: bash

    git clone https://github.com/QuentiumYT/Cloudflare-Firewall-Rules.git
    cd Cloudflare-Firewall-Rules/

.. code-block:: python3
    
    from cf import Cloudflare

    cf = Cloudflare()
    cf.auth(email, password)

    ...

.. toctree::
    :maxdepth: 2
    :caption: Module:

    cf

.. toctree::
    :maxdepth: 2
    :glob:
    :caption: Classes:

    classes/*

.. toctree::
    :maxdepth: 4
    :glob:
    :caption: Examples:

    examples/*

Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`