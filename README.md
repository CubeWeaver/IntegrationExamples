## CubeWeaver Integration Samples

[CubeWeaver](https://cubeweaver.com/) is a multidimensional spreadsheet designed for financial modelling, planning, budgeting and reporting.

This repository contains CubeWeaver API usage examples. Docs for the API can be found [here](https://cubeweaver.com/docs_documentation#developer-api).

Table of content:

- [cw_psql_stage.py](cw_psql_stage.py) - the Python script will export a CubeWeaver model to a PostgreSQL database. Tables are truncated and refilled every time. Change the connection parameters in the main part at the end of the file or import the file as a module from your own script.
- [pdi_import_dimension](pdi_import_dimension) - the folder contains a sample job for the PDI (Pentaho Data Integration) ETL Tool, which imports a table from a PostgreSQL database into a CubeWeaver list. The import report returned by CubeWeaver is saved to a file (output.txt). Don't forget to update the query inside the transformation and rename the columns if you use this example.
