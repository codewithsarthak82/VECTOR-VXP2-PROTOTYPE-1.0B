# Implementation Plan - VXP2 Iteration-1: Universal Data Loader & Window Padding

We need to enhance the data loading capabilities of the VECTOR VXP2 prototype to handle various file formats (CSV/TXT), detect commercial headers (unit_id/cycle), and ensure that even short telemetry streams (like `scenario_nominal.csv`) can be processed immediately by padding them to the LSTM window size (50).

## User Review Required

> [!IMPORTANT]
> The "Window Padding" will be implemented by repeating the **first row** of telemetry at the beginning of the sequence for any engine unit that has fewer than 50 cycles. This ensures that the LSTM (which requires a 50-cycle window) can generate an RUL prediction from the very first cycle of the uploaded data.

## Proposed Changes

### [Component: Data Processing]

#### [MODIFY] [data_processor.py](file:///a:/12.%20Orion%20Spacetech/Vector%20Codebase/VECTOR%20VXP2%20Prototype%202.0/src/data_processor.py)
- Refine `load_data` to ensure `sep=None` and `engine='python'` are used consistently.
- Enhance the `header_map` to handle `unit_id`, `cycle`, `setting1-3`, and `s1-21` (case-insensitive or exact match).
- Implement the **Window Padding** logic within `load_data` or a new helper method. If a unit's cycle count is $< 50$, prepend copies of the first row until the count reaches 50.

### [Component: Dashboard UI]

#### [MODIFY] [app.py](file:///a:/12.%20Orion%20Spacetech/Vector%20Codebase/VECTOR%20VXP2%20Prototype%202.0/src/app.py)
- Update the data loading section to ensure it leverages the improved `load_data`.
- (Optional but recommended) Add a logging message in the Streamlit UI to inform the user when "Aero-Core Window Padding" is active for a short dataset.

---

## Verification Plan

### Automated Tests
1. **Load Test Script**: Create a temporary script `test_loader.py` that specifically loads `data/scenario_nominal.csv` using the updated `VectorSequenceProcessor` and asserts:
   - The dataframe is loaded correctly (no errors).
   - Headers like `unit_id` are mapped to `Engine_ID`.
   - The number of cycles for Unit #1 is at least 50 (after padding).
2. **Runtime Verification**: Use `streamlit run src/app.py` and upload `scenario_nominal.csv` to ensure the "ENGAGE VXP2" simulation starts and generates RUL values immediately.

### Manual Verification
1. Upload `data/scenario_nominal.csv` in the running app.
2. Observe if the RUL metric updates from Cycle 1 (which requires padding).
3. Verify that `data/test_FD002.txt` (standard space-separated) still loads correctly.
