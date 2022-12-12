.. currentmodule:: pyrfc

.. _intro:

============
Introduction
============


The Python connector (a synonym for the :mod:`pyrfc` package) wraps the existing *SAP NW RFC Library*,
often colloquially called *SAP C connector* or *SAP NW RFC SDK*. To start using :mod:`pyrfc`
and similar connectors effectively, we highly recommend reading a series of insightful articles
about RFC communication and *SAP NW RFC Library*, published in the SAP Professional Journal (SPJ),
in 2009, by Ulrich Schmidt and Guangwei Li: *Improve communication between your C/C++ applications
and SAP systems with SAP NetWeaver RFC SDK*
`Part 1: RFC Client Programming <https://scn.sap.com/docs/DOC-52886>`_,
`Part 2: RFC Server Programming <https://scn.sap.com/docs/DOC-52887>`_,
`Part 3: Advanced Topics <https://scn.sap.com/docs/DOC-52888>`_.

The lecture of these articles and `NW RFC SDK Guide (SAP Help) <http://help.sap.com/saphelp_nw73ehp1/helpdata/en/48/a88c805134307de10000000a42189b/content.htm?frameset=/en/48/a994a77e28674be10000000a421937/frameset.htm>`_
are recommended as an introduction into RFC communication and programming, while :mod:`pyrfc` documentation is
focused merely on technical aspects of :mod:`pyrfc` API.


Example usage
=============

In order to call remote enabled ABAP function module, we need to open a connection with
valid logon credentials.

.. code-block:: python

    from pyrfc import Connection
    conn = Connection(user='me', passwd='secret', ashost='10.0.0.1', sysnr='00', client='100')

Using an open connection we can call remote enabled ABAP function modules from Python.

.. code-block:: python

    result = conn.call('STFC_CONNECTION', REQUTEXT=u'Hello SAP!')
    print result
    {u'ECHOTEXT': u'Hello SAP!',
     u'RESPTEXT': u'SAP R/3 Rel. 702   Sysid: ABC   Date: 20121001   Time: 134524   Logon_Data: 100/ME/E'}

Finally, the connection is closed automatically when the instance is deleted by the garbage collector.
As this may take some time, we may either call the :meth:`~Connection.close` method explicitly
or use the connection as a context manager:

.. code-block:: python

     with Connection(user='me', ...) as conn:
        conn.call(...)
     # connection automatically closed here


Functional coverage
===================

The goal of the Python connector development was to provide a package for interacting with
SAP ABAP systems on an intuitive and adequate abstract level. Not each and every available
function provided by *SAP NW RFC Library* is therefore wrapped into Python, but classes and
methods are implemented, covering the most of the use cases relevant for projects done so far.
The drawback of this approach is that fine-grained RFC manipulation is not possible sometimes
but coverage can be extended if needed.

In line with this approach, we distinguish between two basic scenarios:

* Client, Python client calls ABAP server
* Server, ABAP client calls Python server

The coverage is as follows:

+------------------------------+---------------+--------------+
|                              |   Client      |   Server (1) |
+==============================+===============+==============+
| Standard functionality,      |   yes         |    no        |
| e.g. invoking arbitrary      |               |              |
| RFC                          |               |              |
+------------------------------+---------------+--------------+
| Transactions (tRFC/qRFC)     |   yes         |     no       |
+------------------------------+---------------+--------------+
| Background RFC               |   yes (2)     |     no       |
+------------------------------+---------------+--------------+
| RFC Callbacks                |   no          |     no       |
+------------------------------+---------------+--------------+
| Secure network connect (SNC) |   yes         |     no       |
+------------------------------+---------------+--------------+
| Single Sign on (SSO)         |   no          |     no       |
+------------------------------+---------------+--------------+

.. note::
   (1) Server functionality is currently not implemented
   (2) Background RFC is currently not working.

