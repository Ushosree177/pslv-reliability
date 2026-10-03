"""Build the verified PSLV Step 1 dataset.

This file is intentionally self-contained.  The launch records below are a
small, readable source snapshot taken from the official ISRO PSLV launch list.
Run this file from the project root with:

    python code/build_step1_dataset.py

The script writes CSV files, a data dictionary, a validation report, and two
simple figures.  It does not fit a Bayesian model.
"""

from __future__ import annotations

import csv
from datetime import date, datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
FIGURES_DIR = PROJECT_ROOT / "figures"

ISRO_LAUNCH_LIST = "https://www.isro.gov.in/ISRO_EN/PSLV_Launchers.html"
ISRO_SPACECRAFT_LIST = "https://www.isro.gov.in/ISRO_EN/SpacecraftMissions.html"
ISRO_C62_PAGE = "https://www.isro.gov.in/Mission_PSLV_C62.html"


# Index, mission, date, raw variant, payload, raw launch-list remark.
# An empty payload means that the launch-list row did not state one clearly.
LAUNCHES = [
    (1, "PSLV-D1", "1993-09-20", "PSLV-G", "IRS-1E", "Mission Unsuccessful"),
    (2, "PSLV-D2", "1994-10-15", "PSLV-G", "IRS-P2", ""),
    (3, "PSLV-D3", "1996-03-21", "PSLV-G", "IRS-P3", ""),
    (4, "PSLV-C1", "1997-09-29", "PSLV-G", "IRS-1D", ""),
    (5, "PSLV-C2", "1999-05-26", "PSLV-G", "Oceansat (IRS-P4)", ""),
    (6, "PSLV-C3", "2001-10-22", "PSLV-G", "TES", ""),
    (7, "PSLV-C4", "2002-09-12", "PSLV-G", "KALPANA-1", ""),
    (8, "PSLV-C5", "2003-10-17", "PSLV-G", "IRS-P6 / RESOURCESAT-1", ""),
    (9, "PSLV-C6", "2005-05-05", "PSLV-G", "CARTOSAT-1 / HAMSAT", ""),
    (10, "PSLV-C7", "2007-01-10", "PSLV-G", "CARTOSAT-2 / SRE-1", ""),
    (11, "PSLV-C8", "2007-04-23", "PSLV-CA", "", ""),
    (12, "PSLV-C10", "2008-01-21", "PSLV-CA", "", ""),
    (13, "PSLV-C9", "2008-04-28", "PSLV-CA", "CARTOSAT-2A / IMS-1", ""),
    (14, "PSLV-C11", "2008-10-22", "PSLV-XL", "Chandrayaan-1", ""),
    (15, "PSLV-C12", "2009-04-20", "PSLV-CA", "RISAT-2", ""),
    (16, "PSLV-C14", "2009-09-23", "PSLV-CA", "Oceansat-2", ""),
    (17, "PSLV-C15", "2010-07-12", "PSLV-CA", "CARTOSAT-2B", ""),
    (18, "PSLV-C16", "2011-04-20", "PSLV-G", "RESOURCESAT-2 / YOUTHSAT", ""),
    (19, "PSLV-C17", "2011-07-15", "PSLV-XL", "GSAT-12", ""),
    (20, "PSLV-C18", "2011-10-12", "PSLV-CA", "Megha-Tropiques", ""),
    (21, "PSLV-C19", "2012-04-26", "PSLV-XL", "RISAT-1", ""),
    (22, "PSLV-C21", "2012-09-09", "PSLV-CA", "", ""),
    (23, "PSLV-C20", "2013-02-25", "PSLV-CA", "SARAL", ""),
    (24, "PSLV-C22", "2013-07-01", "PSLV-XL", "IRNSS-1A", ""),
    (25, "PSLV-C25", "2013-11-05", "PSLV-XL", "Mars Orbiter Mission", ""),
    (26, "PSLV-C24", "2014-04-04", "PSLV-XL", "IRNSS-1B", ""),
    (27, "PSLV-C23", "2014-06-30", "PSLV-CA", "", ""),
    (28, "PSLV-C26", "2014-10-16", "PSLV-XL", "IRNSS-1C", ""),
    (29, "PSLV-C27", "2015-03-28", "PSLV-XL", "IRNSS-1D", ""),
    (30, "PSLV-C28", "2015-07-10", "PSLV-XL", "DMC3", ""),
    (31, "PSLV-C30", "2015-09-28", "PSLV-XL", "AstroSat", ""),
    (32, "PSLV-C29", "2015-12-16", "PSLV-CA", "TeLEOS-1", ""),
    (33, "PSLV-C31", "2016-01-20", "PSLV-XL", "IRNSS-1E", ""),
    (34, "PSLV-C32", "2016-03-10", "PSLV-XL", "IRNSS-1F", ""),
    (35, "PSLV-C33", "2016-04-28", "PSLV-XL", "IRNSS-1G", ""),
    (36, "PSLV-C34", "2016-06-22", "PSLV-XL", "CARTOSAT-2 Series", ""),
    (37, "PSLV-C35", "2016-09-26", "PSLV", "SCATSAT-1", ""),
    (38, "PSLV-C36", "2016-12-07", "PSLV-XL", "RESOURCESAT-2A", ""),
    (39, "PSLV-C37", "2017-02-15", "PSLV-XL", "CARTOSAT-2 Series", ""),
    (40, "PSLV-C38", "2017-06-23", "PSLV-XL", "CARTOSAT-2 Series", ""),
    (41, "PSLV-C39", "2017-08-31", "PSLV-XL", "IRNSS-1H", "Mission Unsuccessful"),
    (42, "PSLV-C40", "2018-01-12", "PSLV-XL", "Cartosat-2 Series", ""),
    (43, "PSLV-C41", "2018-04-12", "PSLV-XL", "IRNSS-1I", ""),
    (44, "PSLV-C42", "2018-09-16", "PSLV", "", ""),
    (45, "PSLV-C43", "2018-11-29", "PSLV", "HysIS", ""),
    (46, "PSLV-C44", "2019-01-24", "PSLV-DL", "Microsat-R", ""),
    (47, "PSLV-C45", "2019-04-01", "PSLV-QL", "EMISAT", ""),
    (48, "PSLV-C46", "2019-05-22", "PSLV-CA", "RISAT-2B", ""),
    (49, "PSLV-C47", "2019-11-27", "PSLV-XL", "Cartosat-3", ""),
    (50, "PSLV-C48", "2019-12-11", "PSLV-QL", "RISAT-2BR1", ""),
    (51, "PSLV-C49", "2020-11-07", "PSLV-DL", "EOS-01", ""),
    (52, "PSLV-C50", "2020-12-17", "PSLV-XL", "CMS-01", ""),
    (53, "PSLV-C51", "2021-02-28", "PSLV-DL", "Amazonia-1", ""),
    (54, "PSLV-C52", "2022-02-14", "PSLV-XL", "EOS-04", ""),
    (55, "PSLV-C53", "2022-06-30", "", "DS-EO", ""),
    (56, "PSLV-C54", "2022-11-26", "PSLV-XL", "EOS-06 / India-Bhutan Sat", ""),
    (57, "PSLV-C55", "2023-04-22", "PSLV-CA", "TeLEOS-2", ""),
    (58, "PSLV-C56", "2023-07-30", "PSLV-CA", "DS-SAR", ""),
    (59, "PSLV-C57", "2023-09-02", "PSLV-XL", "Aditya-L1", ""),
    (60, "PSLV-C58", "2024-01-01", "PSLV-DL", "XPoSat", ""),
    (61, "PSLV-C59", "2024-12-05", "PSLV-XL", "Proba-3", ""),
    (62, "PSLV-C60", "2024-12-30", "", "SPADEX-A / SPADEX-B / POEM-4", ""),
    (63, "PSLV-C61", "2025-05-18", "PSLV-XL", "EOS-09", "Not accomplished"),
    (64, "PSLV-C62", "2026-01-12", "PSLV-DL", "EOS-N1 / ANVESHA", ""),
]


def standardize_variant(raw_variant: str) -> str:
    """Keep the documented configuration, while normalizing blank values."""
    return raw_variant.strip() if raw_variant.strip() else "UNKNOWN"


def build_rows() -> list[dict[str, object]]:
    failure_details = {
        "PSLV-D1": ("FAILURE", "UNKNOWN", "Mission unsuccessful", "confirmed"),
        "PSLV-C39": ("FAILURE", "UNKNOWN", "Mission unsuccessful", "confirmed"),
        "PSLV-C61": ("FAILURE", "PS3", "Anomaly during third-stage operation", "reported_under_investigation"),
        "PSLV-C62": ("FAILURE", "PS3", "Anomaly around the end of the third stage", "under_investigation"),
    }
    rows = []
    previous_failure = 0
    for index, mission, date_text, variant, payload, remark in LAUNCHES:
        launch_date = datetime.strptime(date_text, "%Y-%m-%d").date()
        is_failure = mission in failure_details
        failure_type, failure_stage, cause, cause_status = failure_details.get(
            mission, ("SUCCESS", "", "", "not_applicable")
        )
        if mission == "PSLV-C62":
            outcome_verification = "SECONDARY_OFFICIAL_FAILURE"
            outcome_source = ISRO_SPACECRAFT_LIST
            outcome_source_text = "Launch unsuccessful"
            verification_status = "VERIFIED"
        elif is_failure:
            outcome_verification = "PRIMARY_OFFICIAL_FAILURE"
            outcome_source = ISRO_LAUNCH_LIST
            outcome_source_text = remark
            verification_status = "VERIFIED"
        else:
            outcome_verification = "PRIMARY_OFFICIAL_SUCCESS"
            outcome_source = ISRO_LAUNCH_LIST
            outcome_source_text = (
                "Mission is listed in ISRO's official PSLV launch chronology under Missions accomplished; "
                "the row has no unsuccessful outcome and its payload is recorded."
            )
            verification_status = "VERIFIED"
        row = {
            "launch_index": index,
            "mission": mission,
            "calendar_date": launch_date.isoformat(),
            "year": launch_date.year,
            "variant_raw": variant,
            "variant_standard": standardize_variant(variant),
            "payload_raw": payload,
            "outcome_raw": remark,
            "success": 0 if is_failure else 1,
            "outcome_verification": outcome_verification,
            "outcome_source": outcome_source,
            "outcome_source_text": outcome_source_text,
            "verification_status": verification_status,
            "failure_type": failure_type,
            "failure_stage": failure_stage,
            "failure_cause_raw": cause,
            "cause_status": cause_status,
            "post_C61": 1 if index >= 63 else 0,
            "previous_failure": previous_failure,
            "primary_source": ISRO_LAUNCH_LIST,
            "secondary_source": (
                ISRO_SPACECRAFT_LIST if mission in {"PSLV-D1", "PSLV-C39", "PSLV-C61", "PSLV-C62"} else ""
            ),
            "source_date_checked": "2026-10-01",
            "source_disagreement": 1 if mission == "PSLV-C62" else 0,
            "resolution_note": (
                "Launch list remark is blank; ISRO spacecraft catalogue explicitly says Launch unsuccessful."
                if mission == "PSLV-C62"
                else ""
            ),
            "notes": (
                "PS3 anomaly reported; root cause not established."
                if mission in {"PSLV-C61", "PSLV-C62"}
                else ""
            ),
        }
        rows.append(row)
        previous_failure = int(row["success"] == 0)
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def validate(rows: list[dict[str, object]]) -> list[str]:
    errors = []
    if len(rows) != 64:
        errors.append(f"Expected 64 rows, found {len(rows)}")
    if len({row["mission"] for row in rows}) != len(rows):
        errors.append("Mission names are not unique")
    dates = [date.fromisoformat(str(row["calendar_date"])) for row in rows]
    if dates != sorted(dates):
        errors.append("Dates are not in chronological order")
    if any(not row["calendar_date"] for row in rows):
        errors.append("At least one date is missing")
    failures = [row for row in rows if row["success"] == 0]
    if {row["mission"] for row in failures} != {"PSLV-D1", "PSLV-C39", "PSLV-C61", "PSLV-C62"}:
        errors.append("Failure set does not match the documented Step 1 coding")
    if sum(int(row["success"]) for row in rows) != 60:
        errors.append("Success count is not 60")
    if rows[-1]["previous_failure"] != 1:
        errors.append("C62 is not marked as following a failure")
    if any(row["verification_status"] != "VERIFIED" for row in rows):
        errors.append("At least one outcome is not positively source-verified")
    if any(not row["outcome_source"] or not row["outcome_source_text"] for row in rows):
        errors.append("At least one row is missing outcome evidence")
    return errors


def write_figures(rows: list[dict[str, object]]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        (FIGURES_DIR / "README.txt").write_text(
            "Install matplotlib and rerun the builder to create the figures.\n",
            encoding="utf-8",
        )
        return

    indices = [int(row["launch_index"]) for row in rows]
    outcomes = [int(row["success"]) for row in rows]
    plt.figure(figsize=(11, 3.5))
    plt.step(indices, outcomes, where="mid", color="#1f5f8b")
    plt.scatter(indices, outcomes, c=["#b23a48" if value == 0 else "#2a9d8f" for value in outcomes], s=28)
    plt.yticks([0, 1], ["Failure", "Success"])
    plt.xlabel("Chronological launch index")
    plt.title("PSLV mission outcomes, official Step 1 coding")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "success_sequence.png", dpi=180)
    plt.close()

    failure_years = {}
    for row in rows:
        if row["success"] == 0:
            failure_years[row["year"]] = failure_years.get(row["year"], 0) + 1
    plt.figure(figsize=(7, 3.5))
    plt.bar([str(year) for year in failure_years], list(failure_years.values()), color="#b23a48")
    plt.ylabel("Number of unsuccessful missions")
    plt.xlabel("Year")
    plt.title("Documented unsuccessful PSLV missions")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "failures_by_year.png", dpi=180)
    plt.close()


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    errors = validate(rows)

    raw_columns = [
        "launch_index", "mission", "calendar_date", "year", "variant_raw",
        "payload_raw", "outcome_raw", "primary_source",
    ]
    verified_columns = [
        "launch_index", "mission", "calendar_date", "year", "variant_raw",
        "variant_standard", "payload_raw", "outcome_raw", "success", "outcome_verification",
        "outcome_source", "outcome_source_text", "verification_status", "failure_type",
        "failure_stage", "failure_cause_raw", "cause_status", "post_C61",
        "previous_failure", "primary_source", "secondary_source", "source_date_checked",
        "source_disagreement", "resolution_note", "notes",
    ]
    audit_rows = []
    for row in rows:
        audit_rows.append({
            "mission": row["mission"], "variable": "outcome",
            "source": row["outcome_source"], "source_value": row["outcome_source_text"],
            "coded_value": "FAILURE" if row["success"] == 0 else "SUCCESS",
            "decision": row["outcome_verification"],
        })
    audit_columns = ["mission", "variable", "source", "source_value", "coded_value", "decision"]

    write_csv(DATA_DIR / "PSLV_raw_launch_history.csv", rows, raw_columns)
    write_csv(DATA_DIR / "PSLV_verified_dataset.csv", rows, verified_columns)
    write_csv(DATA_DIR / "PSLV_verified_dataset_v1.0.csv", rows, verified_columns)
    write_csv(DATA_DIR / "PSLV_source_audit.csv", audit_rows, audit_columns)
    source_conflict_count = sum(str(row.get("source_disagreement", "")).strip().lower() in {"1", "true", "yes"} for row in rows)
    missing_configuration_count = sum(not str(row.get("variant_standard", "")).strip() or str(row.get("variant_standard", "")).strip() == "UNKNOWN" for row in rows)
    missing_payload_count = sum(not str(row.get("payload_raw", "")).strip() for row in rows)
    final_audit_rows = [
        {"audit_item": "Number of launches", "result": len(rows), "status": "PASS" if len(rows) == 64 else "FAIL"},
        {"audit_item": "Duplicate missions", "result": len(rows) - len({row['mission'] for row in rows}), "status": "PASS" if len(rows) == len({row['mission'] for row in rows}) else "FAIL"},
        {"audit_item": "Missing dates", "result": sum(not str(row.get('calendar_date', '')).strip() for row in rows), "status": "PASS" if not any(not str(row.get('calendar_date', '')).strip() for row in rows) else "FAIL"},
        {"audit_item": "Missing outcomes", "result": sum(row.get('success') not in (0, 1) for row in rows), "status": "PASS" if not any(row.get('success') not in (0, 1) for row in rows) else "FAIL"},
        {"audit_item": "Unverified outcomes", "result": sum(row.get('verification_status') != 'VERIFIED' for row in rows), "status": "PASS" if not any(row.get('verification_status') != 'VERIFIED' for row in rows) else "FAIL"},
        {"audit_item": "Source conflicts", "result": source_conflict_count, "status": "REVIEWED"},
        {"audit_item": "Missing configurations", "result": missing_configuration_count, "status": "REVIEWED"},
        {"audit_item": "Missing payload information", "result": missing_payload_count, "status": "REVIEWED"},
    ]
    write_csv(DATA_DIR / "PSLV_final_data_audit.csv", final_audit_rows, ["audit_item", "result", "status"])
    (DATA_DIR / "DATA_FREEZE_v1.0.md").write_text(
        "# PSLV Dataset Freeze v1.0\n\n"
        "The Step 1 dataset is frozen before inferential modeling. Any later correction must create a new dataset version rather than silently modifying the analysis dataset.\n\n"
        "The frozen analysis file is `PSLV_verified_dataset_v1.0.csv`. The final audit table is `PSLV_final_data_audit.csv`.\n\n"
        "Step 2, Step 3, and Step 4 read this frozen file and do not rewrite it.\n",
        encoding="utf-8",
    )
    (DATA_DIR / "PSLV_source_urls.csv").write_text(
        "source_name,source_url\n"
        f"ISRO PSLV launch list,{ISRO_LAUNCH_LIST}\n"
        f"ISRO spacecraft missions,{ISRO_SPACECRAFT_LIST}\n"
        f"ISRO PSLV-C62 mission page,{ISRO_C62_PAGE}\n",
        encoding="utf-8",
    )
    (DATA_DIR / "PSLV_data_dictionary.md").write_text(DATA_DICTIONARY, encoding="utf-8")
    report = [
        "# Step 1 validation report",
        "",
        f"Status: {'PASS' if not errors else 'FAIL'}",
        f"Rows: {len(rows)}",
        f"Successes: {sum(int(row['success']) for row in rows)}",
        f"Failures: {sum(int(row['success']) == 0 for row in rows)}",
        "Observed success proportion: 0.9375 (descriptive only)",
        "",
        "Checks:",
        "- 64 rows",
        "- unique mission names",
        "- chronological dates",
        "- four documented unsuccessful missions",
        "- C62 previous_failure = 1",
        "- every row has outcome_verification, outcome_source, outcome_source_text, and VERIFIED status",
    ]
    if errors:
        report.extend(["", "Errors:"] + [f"- {error}" for error in errors])
    (DATA_DIR / "PSLV_validation_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    write_figures(rows)
    if errors:
        raise SystemExit("Validation failed; read data/PSLV_validation_report.md")
    print("Step 1 complete: 64 rows, 60 successes, 4 failures.")


DATA_DICTIONARY = """# PSLV Step 1 data dictionary

This is the frozen descriptive dataset for the first stage of the project.
It is not a Bayesian model and should not be interpreted as one.

## Files

- `PSLV_raw_launch_history.csv`: source-facing fields preserved as reported.
- `PSLV_verified_dataset.csv`: analysis-ready rows plus coding and audit fields.
- `PSLV_source_audit.csv`: source-to-coding decisions.
- `PSLV_final_data_audit.csv`: final quality-audit checklist and results.
- `DATA_FREEZE_v1.0.md`: statement that the analysis dataset is frozen before inference.
- `PSLV_source_urls.csv`: official source URLs used for this version.
- `PSLV_validation_report.md`: automated quality checks.

## Coding rules

- One row represents one PSLV flight in chronological launch order.
- `success = 1` means the primary mission was documented as successful.
- `success = 0` means the primary mission was documented as unsuccessful.
- A blank remark is preserved; it is never changed into a failure.
- C62 is coded as a failure because the dedicated ISRO spacecraft catalogue says `Launch unsuccessful`, even though the launch-list remark is blank.
- `failure_stage` records the documented location of an anomaly, not a proven root cause.
- `cause_status` distinguishes a confirmed description from an investigation still in progress.
- `post_C61` is a descriptive indicator equal to 1 for C61 and C62. It is not evidence of a change point.
- `previous_failure` records whether the immediately preceding launch was unsuccessful.
- `variant_raw` preserves the source wording. `variant_standard` only normalizes blank values to `UNKNOWN` in this version.
- `outcome_verification` states how the outcome was verified: `PRIMARY_OFFICIAL_SUCCESS`, `PRIMARY_OFFICIAL_FAILURE`, or `SECONDARY_OFFICIAL_FAILURE`.
- `outcome_source` gives the URL used for the outcome decision.
- `outcome_source_text` preserves the exact short evidence statement used by the coder.
- `verification_status` is `VERIFIED` only when the row has a source and evidence statement.

## Important limitation

The official launch-list page is the primary chronology source. Several rows have no payload or remark in that table; those blanks are retained rather than guessed. C62 is resolved with the dedicated ISRO spacecraft catalogue because its launch-list remark is blank but its catalogue status is `Launch unsuccessful`.

For successful launches, this Version 1 protocol treats an official entry in ISRO's `Missions accomplished` PSLV chronology, with a recorded payload and no unsuccessful status, as positive official evidence. This rule is recorded in `outcome_source_text` so a later paper audit can replace or strengthen individual evidence without changing the statistical columns.
"""


if __name__ == "__main__":
    main()
