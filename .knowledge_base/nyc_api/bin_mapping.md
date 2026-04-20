# BIN to SODA Mapping (Lead: Kiran)

The Building Identification Number (BIN) is the primary key for all data integration across the platform.

## Address to BIN Mapping
Geoclient maps raw street addresses to a unique 7-digit BIN.

### 1. Retrieval
- **Tool:** `GeoclientService` (via the `address.json` endpoint).
- **Field:** `buildingIdentificationNumber`

## BIN as Integration Key
All external data sources are joined using the BIN.

### 1. SODA (Elevator Complaints)
The SODA API for elevator complaints (`kqwi-7ncn`) is queried using the BIN as a filter:
- **Query:** `bin='{bin_id}'`

### 2. District Data
Political districts are also derived from the BIN via Geoclient, ensuring that elevator outages are mapped to the correct City Council, State Assembly, and State Senate districts.

## The Two-Hop District Resolution Protocol
For automated, district-wide advocacy reports, we resolve all buildings *before* querying SODA, reducing geocoding overhead by >80%.

### Hop 1: District to BBLs (MapPLUTO)
We query the MapPLUTO dataset (`64uk-42ks`) using the `council` field to retrieve all Tax Lot identifiers (BBLs) in the district.

### Hop 2: BBL to BINs (Building Footprints)
We map these BBLs to Building Identification Numbers (BINs) using the Footprints dataset (`5zhs-2jue`) and the `mappluto_bbl` field.

## Management Data Mapping
Once a BIN is resolved, we use PLUTO `ownername` as the primary legal entity for advocacy targets.
- **BIN** → **BBL** (via Footprints)
- **BBL** → **Owner** (via PLUTO)

## Data Normalization
The platform uses the BIN as the primary key for its local `Building` model, ensuring a stable and unique identifier regardless of street name variations (e.g., `57th St` vs `57 Street`).
