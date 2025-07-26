# PubMed Citation Fields Data Dictionary

## Basic Identifiers

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **pmid** | PubMed ID | Unique identifier for the article in PubMed | Integer | Primary key |
| **jid** | Journal ID | Unique identifier for the journal in NLM catalog | Integer | Links to journal database |
| **pmc** | PMC ID | PubMed Central identifier | String | Format: PMCxxxxxxx |
| **mid** | Manuscript ID | Manuscript identifier | String | Publisher-specific |

## Article Information

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **ti** | Title | Article title | Text | Main title of the publication |
| **tt** | Transliterated Title | Transliterated version of non-English title | Text | For non-Latin script titles |
| **ab** | Abstract | Article abstract | Text | Full abstract text |
| **oab** | Other Abstract | Additional abstract in another language | Text | Secondary abstracts |
| **oabl** | Other Abstract Language | Language of the other abstract | String | ISO language codes |
| **la** | Language | Publication language | String | Multiple values separated by semicolon |
| **so** | Source | Complete bibliographic citation | Text | Journal. Year Mon Day;Vol(Issue):Pages |

## Journal Information

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **jt** | Journal Title | Full journal name | Text | Official journal title |
| **ta** | Title Abbreviation | Abbreviated journal title | Text | Standard NLM abbreviation |
| **issn_electronic** | Electronic ISSN | ISSN for electronic version | String | Format: xxxx-xxxx |
| **issn_print** | Print ISSN | ISSN for print version | String | Format: xxxx-xxxx |
| **issn_linking** | Linking ISSN | ISSN designated by ISSN centers | String | Format: xxxx-xxxx |
| **vi** | Volume | Journal volume number | String | Can include letters |
| **ip** | Issue | Journal issue number | String | Can include letters/supplements |
| **pg** | Pagination | Page numbers | String | Format varies (e.g., 123-456, e12345) |

## Authors and Contributors

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **au** | Author | Author names (last name, initials) | Text | Multiple authors separated by semicolon |
| **fau** | Full Author Name | Full author names (last, first middle) | Text | Multiple authors separated by semicolon |
| **auid** | Author Identifier | Author identifiers (ORCID, etc.) | Text | Multiple IDs separated by semicolon |
| **ad** | Affiliation/Address | Author institutional affiliations | Text | Multiple affiliations separated by semicolon |
| **cn** | Corporate Name | Corporate/collective author names | Text | Organizational authors |
| **ir** | Investigator Name | Investigator names | Text | For multi-center studies |
| **fir** | Full Investigator Name | Full investigator names | Text | Complete investigator names |

## Publication Dates

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **dp** | Date of Publication | Publication date | Date | Format: YYYY Mon DD |
| **dep** | Date of Electronic Publication | Electronic publication date | Date | Epub date |
| **edat** | Entrez Date | Date added to Entrez | DateTime | Format: YYYY/MM/DD HH:MM |
| **crdt** | Create Date | Date record was created | DateTime | Format: YYYY/MM/DD HH:MM |
| **dcom** | Date Completed | Date indexing completed | Date | Format: YYYYMMDD |
| **lr** | Last Revision Date | Date of last revision | Date | Format: YYYYMMDD |
| **mhda** | MeSH Date | Date MeSH terms were added | DateTime | Format: YYYY/MM/DD HH:MM |
| **pmcr** | PMC Release Date | PMC release date | Date | When available in PMC |

## Publication History Status (PHST)

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **phst_received** | Received Date | Date manuscript was received | DateTime | Publisher workflow |
| **phst_accepted** | Accepted Date | Date manuscript was accepted | DateTime | Publisher workflow |
| **phst_pubmed** | PubMed Date | Date added to PubMed | DateTime | Same as EDAT |
| **phst_medline** | Medline Date | Date added to Medline | DateTime | When indexed |
| **phst_entrez** | Entrez Date | Date added to Entrez | DateTime | Database entry |
| **phst_pmc_release** | PMC Release Date | PMC availability date | DateTime | Open access release |
| **phst_other** | Other History | Other publication history events | DateTime | Various other dates |

## Indexing and Classification

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **mh** | MeSH Terms | Medical Subject Headings | Text | Multiple terms separated by semicolon |
| **ot** | Other Term | Non-MeSH subject terms | Text | Publisher or author keywords |
| **oto** | Other Term Owner | Owner of other terms | String | Source of keywords |
| **pt** | Publication Type | Type of publication | Text | Multiple types separated by semicolon |
| **sb** | Subset | Database subset classifications | String | Special collections |
| **si** | Secondary Source ID | Secondary source identifiers | Text | Other database IDs |

## Grant and Funding

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **gr** | Grant Number | Grant/funding information | Text | Multiple grants separated by semicolon |

## Article Identifiers

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **aid** | Article Identifier | Various article identifiers | Text | DOI, PII, etc. separated by semicolon |
| **lid** | Location Identifier | Location identifiers | Text | DOI, page ranges |
| **rn** | Registry Number | Chemical registry numbers | Text | CAS numbers |

## Status and Metadata

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **stat** | Status | Processing status | String | MEDLINE, PubMed-not-MEDLINE, etc. |
| **own** | Owner | Database owner | String | Usually NLM |
| **pst** | Publication Status | Publication status | String | ppublish, epublish, aheadofprint |
| **pl** | Place of Publication | Publication location | String | Country/city of publication |

## Related Articles and Comments

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **cin** | Comment In | Comment in reference | Text | Related commentary articles |
| **con** | Comment On | Comment on reference | Text | Articles this comments on |
| **ein** | Erratum In | Erratum in reference | Text | Correction articles |
| **efr** | Erratum For | Erratum for reference | Text | Articles this corrects |
| **uin** | Update In | Update in reference | Text | Updated versions |
| **uof** | Update Of | Update of reference | Text | Previous versions |

## Copyright and Legal

| Field | Name | Description | Data Type | Notes |
|-------|------|-------------|-----------|-------|
| **ci** | Copyright Information | Copyright statement | Text | Publisher copyright notice |
| **cois** | Conflict of Interest Statement | Conflict of interest disclosure | Text | Author disclosures |

## Notes

- **Multiple Values**: Fields with multiple values are separated by semicolons (;)
- **Date Formats**: Various date formats are used depending on the field
- **Text Fields**: Most text fields can contain special characters and formatting
- **Missing Values**: Empty cells indicate the field was not present in the original citation
- **Case Sensitivity**: Field values maintain original case from PubMed
- **Special Characters**: Some fields may contain Unicode characters for international content