Usage
=====

Pattern matching for Pages
--------------------------
Why is it needed? Pattern matching checks URL and understands which page(s)
logic we need to apply for concrete case.

Simplified wild cards are used for this task. Syntax is listed bellow:

=======  ==============  =============================
Symbol   Translates to   Explanation
=======  ==============  =============================
\%        .*?             Matches N random symbols
\*        .               Matches single random symbol
=======  ==============  =============================

Path matching for data retrieval
--------------------------------
It is used to extract data from page.
Simplified xpath-alike expressions are used for this task.

General syntax looks like:

<TAG>[<ATTRIBUTE>="<VALUE>"]/<TAG>[<ATTRIBUTE>="<VALUE>"]/...

Each "/" symbolizes new child matching, part inside "[<...>]" is optional, it 
can be skipped if you have no intention to query inside these tags
, eg.: if you want to get *all* links in the page.

For selecting concrete  element from matches array, use "{#n}" syntax, eg.
if we have :

.. code-block:: html

  <div class="menu">
    <a href=#1>Link1</a>
    <a href=#2>Link2</a>
    <a href=#3>Link3</a>
  </div>

following query can be used to retrieve "Link2":
div[class="menu"]/a{1}
where "a{1}" indicates that we want to retrieve all links, and get 2nd link from that array

To select concrete data from element, attribute selector can be used. 
Notation starts with a '.' followed by attribute name (eg. href, class, src etc.)
Retrieving concrete link would look like:
div[class="menu"]/a{1}.href
