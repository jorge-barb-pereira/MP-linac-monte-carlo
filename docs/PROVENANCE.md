# Provenance and publication decisions

Source directory: `Original Codes/Metodos Computacionais em FM/Projeto` in the private working collection. Raw files were left unchanged.

| Evidence | Date supported |
| --- | --- |
| `exe01.i` filesystem modification | 12 July 2021 |
| `10e8.i`, `novo.i` modifications | 21 July 2021 |
| `last.i` modification and mesh problem identifier | 23 July 2021; run identifier 19:21:49 |
| Planning notebook and energy image modifications | 25 July 2021 |
| Saved mesh and particle balance | Run continued to 27 July 2021 |
| Maintained Python code and English documentation | October 2026 |

Filesystem dates can change during copying; the embedded July 2021 run identifier is stronger independent evidence. Commits use the actual publication date, not backdated development dates.

`archive/manifest.json` records SHA-256 hashes, source mapping and available modification times. All five input decks, the selected complete mesh, the particle balance and original energy figure are byte-preserved. The planning notebook retains every original cell source; outputs, execution counts and notebook/cell metadata were removed. Its original and published hashes are both recorded. Historical Portuguese comments remain in the archive; maintained code and documentation are English.

`data/historical/run-diagnostics.json` records selected warning/version/termination lines from `outw`, their original line numbers and the full original file hash. It is an extract, not a full output or a new simulation. The mesh contains 100,320,422 histories; the final summary's source electron count agrees.

Excluded from publication: 829 MB binary restart, redundant intermediate outputs and meshes, command logs, IDE settings, local history, ZIP duplicate and the unrelated November 2023 R project/report/presentation/images. All four R files were compared byte-for-byte with the statistics project's original folder and are duplicates. This prevents presenting the same coursework as a new independent project.

No patient data or private configuration was needed for the published analysis. No original development date is inferred from the 2026 import folder timestamp. Original notebook code was reviewed rather than blindly executed.
