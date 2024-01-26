*******************************************************
Welcome to Cloudflare's WAF Custom rules documentation!
*******************************************************

.. currentmodule:: cf

.. toctree::
    :maxdepth: 4
    :caption: Introduction:

    self

This library is a wrapper that aims to easily create, modify, delete rules. It also provides a way to import & export new rules in your domain's firewall.

If you have a single rule that you want to duplicate among your domains, you can simply write 3 lines to do that :)
(See examples for more info)

Note: You can also import several rules into several domains at once!

Installation:
-------------

.. code-block:: bash

    pip install cf_rules

    # OR

    git clone https://github.com/QuentiumYT/Cloudflare-Firewall-Rules.git
    cd Cloudflare-Firewall-Rules/
    pip install .

.. code-block:: python3
    
    from cf_rules import Cloudflare

    cf = Cloudflare()
    cf.auth_key(email, password)

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
