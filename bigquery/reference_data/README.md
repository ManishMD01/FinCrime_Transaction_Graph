# Reference Data Files for ETL Process

This folder contains reference/lookup/master data files used by the ETL process for data enrichment, validation, and standardization.

## Purpose

Reference data files are used to:
- **Validate** incoming data (country codes, currency codes)
- **Enrich** transactions (high-risk countries, channels)
- **Standardize** addresses and names
- **Support AML detection** (high-risk entities, sanctions lists)
- **Categorize** amounts and risk scores

## Folder Structure

```
bigquery/reference_data/
├── README.md
├── country_codes.csv
├── currency_codes.csv
├── high_risk_countries.csv
├── channel_types.csv
├── transaction_types.csv
├── id_types.csv
├── sanctions_list_sample.csv
├── reporting_thresholds.json
└ mapping files...
```

## Usage

Reference data can be loaded into BigQuery using:
```bash
python bigquery/etl/load_reference_data.py
```

## Adding New Reference Data
1. Create CSV/JSON in this folder
2. Add schema in `bigquery/schemas/`
3. Add DDL in `bigquery/ddl/`
4. Load via `load_reference_data.py`

## Notes
- Keep reference data small (usually < 10MB)
- Use UTF-8 encoding
- Include effective dates for time-varying reference data
