# Meltano

https://meltano.com/

A **data integration engine**

- **sources** to **destinations**
- YAML file + CLI, version controlled, open source
- fivetran in open source (?)
---
# Meltano under the hood

- Python wrapper around "Singer taps" https://www.singer.io/
- open source standard for scripts that move data
	- *Taps* extract data from any source and write it to a **standard stream** in a **JSON-based format**.
	- *Targets* consume data from taps and do something with it, like load it into a file, API or database.
	- applications to load / store data
	- connected with pipes
	- communicate via JSON
	- ... some state logic?

---
# Get started
- find data to extract: https://scores.frisbeesportverband.de/?view=ext/export
- `pip install meltano`
- `meltano init`
- `meltano add extractor tap-spreadsheets-anywhere`

---
# Configure
- `meltano config tap-spreadsheets-anywhere set --interactive`
- `meltano config tap-spreadsheets-anywhere test`
Live Demo!

---
# Load data
- `meltano add loader target-duckdb`
- `meltano invoke target-duckdb --help`
- ... configure the loader
- `meltano run tap-spreadsheets-anywhere target-duckdb`

---
# Other stuff (untested)

**orchestrate** (airflow / cron)
- `meltano schedule add run-some-stuff tap-spreadsheets-anywhere target-duckdb @daily`
- `meltano add orchestrator airflow`
- `meltano invoke airflow scheduler -D`

**transform** https://hub.meltano.com/transformers/
- `meltano add transformer dbt-duckdb` 
