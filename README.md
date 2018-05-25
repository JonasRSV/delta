## Server for delta

Working with submodules: https://git-scm.com/book/en/v2/Git-Tools-Submodules

Download Postgres
1. initdb on db/ (To initialize DB)
2. Run postgres -D db/ (To start DB)
3. createdb delta (To create delta DB) 
4. psql -f schema.psql -d delta (To implement the schema)

