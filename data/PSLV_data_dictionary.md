# PSLV Step 1 data dictionary

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
