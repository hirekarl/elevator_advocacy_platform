# SoQL Query Parameters (Lead: Kiran)

The project queries the NYC SODA API (Dataset `kqwi-7ncn`) using Socrata Query Language (SoQL).

## Dataset Information
- **ID:** `kqwi-7ncn` (Elevator Complaints)
- **Base URL:** `https://data.cityofnewyork.us/resource/kqwi-7ncn.json`

## Elevator-Specific Filters
To ensure we only track relevant elevator issues, we filter by `complaint_category`:
- **`6S`**: Elevator complaints (active, 2018–present)
- **`6M`**: Elevator/escalator complaints (active, 2018–present)
- **`81`**, **`63`**: Retired historical categories (used ONLY for all-time historical syncs).

## Common Query Patterns

### 1. Fetching by BIN
Used to retrieve history for a specific building.
```python
unique_key = report.get("unique_key") or report.get("complaint_number") # Use complaint_number fallback
```

### 2. Fetching Recent Outages (Lookback Window)
Because SODA `date_entered` is MM/DD/YYYY text (not ISO), we cannot use SoQL `>` for date filtering. Instead, we:
1.  Order by `complaint_number DESC`.
2.  Fetch in batches of 5,000.
3.  Parse and filter for `threshold` (e.g., last 24 hours) in Python.

```python
params = {
    "$order": "complaint_number DESC",
    "$limit": 5000,
    "$offset": offset,
}
```

### 3. Historical Ingestion (Pagination)
For all-time syncs (e.g. 75k+ records for Bronx), we use `$offset` pagination to capture the full dataset.
