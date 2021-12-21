Update rules script
===================

.. literalinclude:: ../../examples/update_rules.py
    :language: python3
    :caption: This script is a lightweight example of how to update the same firewall rule on all your domains.
    :linenos:

.. note::
    If you export the rules from a domain, you will not be able to update them again if the text file hasn't changed.
    This is a Cloudflare limitation.
