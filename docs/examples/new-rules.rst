New clean rules script
======================

.. literalinclude:: ../../examples/new_rules.py
    :language: python3
    :caption: This script is an example of a purge to replace all existing rules with new ones.
    :linenos:

.. danger::
    This script is cleaning all the rules from a domain.
    It is used if you want to replicate the rules from a domain to another one.

    Be careful when using :func:`cf.Cloudflare.purge_rules` method.
