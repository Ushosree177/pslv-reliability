# PSLV Dataset Freeze v1.0

The Step 1 dataset is frozen before inferential modeling. Any later correction must create a new dataset version rather than silently modifying the analysis dataset.

The frozen analysis file is `PSLV_verified_dataset_v1.0.csv`. The final audit table is `PSLV_final_data_audit.csv`.

Step 2, Step 3, and Step 4 read this frozen file and do not rewrite it.
