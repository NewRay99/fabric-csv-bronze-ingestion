PS C:\repo\WMPP\wmpp> python -m pytest tests --ignore-glob=tests/test_wmpp_*.py
=========================================== test session starts ===========================================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\repo\WMPP\wmpp
configfile: pytest.ini
collected 331 items                                                                                        

tests\test_active_notebook_validation.py ....                                                        [  1%]
tests\test_archive_pipeline_modes.py ......................F..                                       [  8%]
tests\test_category_location_etl.py .......................F..                                       [ 16%]
tests\test_data_domain_history.py .............                                                      [ 20%]
tests\test_fabric_notebooks.py ..........................                                            [ 28%]
tests\test_gold_ipa_signature_contract.py ................                                           [ 33%]
tests\test_gold_referral_journey_status.py .....F................................FF.....FF......     [ 49%]
tests\test_gold_referral_source_reference.py ..............                                          [ 53%]
tests\test_gold_referral_source_status.py ....................................F                      [ 64%]
tests\test_live_pipeline_final_refresh.py ................                                           [ 69%]
tests\test_notebooks_v16_contract.py ......                                                          [ 71%]
tests\test_pipeline_utc_timestamps.py F..........s....                                               [ 76%]
tests\test_provider_registry_etl.py ...................................................              [ 91%]
tests\test_schema_capture_system_columns.py ....                                                     [ 92%]
tests\test_validation_scripts.py ..F................F....                                            [100%]

================================================ FAILURES =================================================
_____________ test_archive_children_do_not_repeat_setup_with_injected_parent[00_archive_load] _____________

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000002A04188D7F0>, name = '00_archive_load'

    @pytest.mark.parametrize("name", ["00_archive_load", "01a_cfg_schema_capture_archive"])
    def test_archive_children_do_not_repeat_setup_with_injected_parent(monkeypatch, name):
        calls = []
        monkeypatch.setitem(sys.modules, "notebookutils", SimpleNamespace(
            mssparkutils=SimpleNamespace(notebook=SimpleNamespace(run=lambda *args: calls.append(args))),
        ))
        scope = execute_parameters(name, {"JOB_RUN_ID": "synthetic-parent"})
>       assert "IS_ORCHESTRATED_RUN" not in scope
E       assert 'IS_ORCHESTRATED_RUN' not in {'__builtins__': {'__name__': 'builtins', '__doc__': "Built-in functions, types, exceptions, and other objects.\n\nThi...port-birmingham/archive', 'EXTRACT_ROOT': 'Files/archive_unzipped', 'ARCHIVE_FILE_ROOT': 'Files/archive_unzipped', ...}

tests\test_archive_pipeline_modes.py:185: AssertionError
________________________ test_referral_etl_simulation_sql_matches_current_notebook ________________________

    def test_referral_etl_simulation_sql_matches_current_notebook():
        source = code("04_gold_model")
        marker = "CREATE OR REPLACE TABLE gold.fact_referral AS"
        query = marker + source.split(marker, 1)[1].split('""")', 1)[0]
>       assert query.strip() == (PROJECT / "tests/_gold_fact_sql.sql").read_text(encoding="utf-8").strip()
E       AssertionError: assert 'CREATE OR RE...rence_profile' == 'CREATE OR RE...rence_profile'
E         
E         Skipping 1082 identical leading characters in diff, use -v to show
E           
E         -     AND (export_date IS NULL OR TO_DATE(export_date) <= {AS_OF_SQL})
E         ?          -----------------------
E         +     AND (TO_DATE(export_date) <= {AS_OF_SQL})
E           ),...
E         
E         ...Full output truncated (319 lines hidden), use '-vv' to show

tests\test_category_location_etl.py:140: AssertionError
_______________________________________ test_all_journey_stages[6] ________________________________________

db = <sqlite3.Connection object at 0x000002A0416775B0>, stage = 6

    @pytest.mark.parametrize("stage", range(1, 9))
    def test_all_journey_stages(db, stage):
        raw = "CANCELLED" if stage == 7 else "OPEN"
        referral(db, raw)
        if stage in (2, 3, 4, 5, 6, 8):
            assignment(db)
        if stage == 3:
            offer(db, "OFFER_MADE")
        if stage == 4:
            offer(db, "OFFER_SUCCESSFUL")
        if stage in (5, 6):
            ipa(db, provider=1, authority=int(stage == 6))
        if stage == 8:
            offer(db, "UNRECOGNISED")
>       assert_stage(db, stage, raw)

tests\test_gold_referral_journey_status.py:127: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

db = <sqlite3.Connection object at 0x000002A0416775B0>, stage = 6, raw = 'OPEN'

    def assert_stage(db, stage, raw="OPEN"):
        rows = db.execute(portable_sql()).fetchall()
        assert len(rows) == 1
        row = rows[0]
        assert row["current_status"] == raw
>       assert row["journey_stage_order"] == stage
E       assert 5 == 6

tests\test_gold_referral_journey_status.py:107: AssertionError
____________________________ test_active_ipa_and_signature_precedence[1-1-0-6] ____________________________

db = <sqlite3.Connection object at 0x000002A041677E20>, provider = 1, authority = 1, closed = 0, stage = 6

    @pytest.mark.parametrize("provider,authority,closed,stage", [
        (1, 1, 0, 6), (1, 1, None, 6), (1, 0, 0, 5), (0, 1, 0, 5),
        (None, 1, 0, 5), (1, None, 0, 5), (None, None, None, 5), (1, 1, 1, 4),
    ])
    def test_active_ipa_and_signature_precedence(db, provider, authority, closed, stage):
        referral(db)
        assignment(db)
        offer(db, "accepted")
        ipa(db, provider, authority, closed)
>       assert_stage(db, stage)

tests\test_gold_referral_journey_status.py:189: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

db = <sqlite3.Connection object at 0x000002A041677E20>, stage = 6, raw = 'OPEN'

    def assert_stage(db, stage, raw="OPEN"):
        rows = db.execute(portable_sql()).fetchall()
        assert len(rows) == 1
        row = rows[0]
        assert row["current_status"] == raw
>       assert row["journey_stage_order"] == stage
E       assert 5 == 6

tests\test_gold_referral_journey_status.py:107: AssertionError
__________________________ test_active_ipa_and_signature_precedence[1-1-None-6] ___________________________

db = <sqlite3.Connection object at 0x000002A0416748B0>, provider = 1, authority = 1, closed = None
stage = 6

    @pytest.mark.parametrize("provider,authority,closed,stage", [
        (1, 1, 0, 6), (1, 1, None, 6), (1, 0, 0, 5), (0, 1, 0, 5),
        (None, 1, 0, 5), (1, None, 0, 5), (None, None, None, 5), (1, 1, 1, 4),
    ])
    def test_active_ipa_and_signature_precedence(db, provider, authority, closed, stage):
        referral(db)
        assignment(db)
        offer(db, "accepted")
        ipa(db, provider, authority, closed)
>       assert_stage(db, stage)

tests\test_gold_referral_journey_status.py:189: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

db = <sqlite3.Connection object at 0x000002A0416748B0>, stage = 6, raw = 'OPEN'

    def assert_stage(db, stage, raw="OPEN"):
        rows = db.execute(portable_sql()).fetchall()
        assert len(rows) == 1
        row = rows[0]
        assert row["current_status"] == raw
>       assert row["journey_stage_order"] == stage
E       assert 5 == 6

tests\test_gold_referral_journey_status.py:107: AssertionError
____________________________ test_active_ipa_and_signature_precedence[1-1-1-4] ____________________________

db = <sqlite3.Connection object at 0x000002A0419D4220>, provider = 1, authority = 1, closed = 1, stage = 4

    @pytest.mark.parametrize("provider,authority,closed,stage", [
        (1, 1, 0, 6), (1, 1, None, 6), (1, 0, 0, 5), (0, 1, 0, 5),
        (None, 1, 0, 5), (1, None, 0, 5), (None, None, None, 5), (1, 1, 1, 4),
    ])
    def test_active_ipa_and_signature_precedence(db, provider, authority, closed, stage):
        referral(db)
        assignment(db)
        offer(db, "accepted")
        ipa(db, provider, authority, closed)
>       assert_stage(db, stage)

tests\test_gold_referral_journey_status.py:189: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

db = <sqlite3.Connection object at 0x000002A0419D4220>, stage = 4, raw = 'OPEN'

    def assert_stage(db, stage, raw="OPEN"):
        rows = db.execute(portable_sql()).fetchall()
        assert len(rows) == 1
        row = rows[0]
        assert row["current_status"] == raw
>       assert row["journey_stage_order"] == stage
E       assert 6 == 4

tests\test_gold_referral_journey_status.py:107: AssertionError
___________________________ test_signatures_on_different_ipas_are_not_combined ____________________________

db = <sqlite3.Connection object at 0x000002A0419D44F0>

    def test_signatures_on_different_ipas_are_not_combined(db):
        referral(db)
        ipa(db, 1, 0, ipa_id="one")
        ipa(db, 0, 1, ipa_id="two")
        ipa(db, 1, 1, closed=1, ipa_id="closed")
>       assert_stage(db, 5)

tests\test_gold_referral_journey_status.py:197: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

db = <sqlite3.Connection object at 0x000002A0419D44F0>, stage = 5, raw = 'OPEN'

    def assert_stage(db, stage, raw="OPEN"):
        rows = db.execute(portable_sql()).fetchall()
        assert len(rows) == 1
        row = rows[0]
        assert row["current_status"] == raw
>       assert row["journey_stage_order"] == stage
E       assert 6 == 5

tests\test_gold_referral_journey_status.py:107: AssertionError
__________________ test_separate_gold_journey_classifier_and_fixture_matches_production ___________________

    def test_separate_gold_journey_classifier_and_fixture_matches_production():
        assert "r.referral_status AS current_status" in FACT_SQL
        assert "END AS journey_stage_order" in FACT_SQL
        assert "END AS journey_stage," in FACT_SQL
>       assert ("CREATE OR REPLACE TABLE gold.fact_referral AS" + FACT_SQL).strip() == (
            PROJECT / "tests/_gold_fact_sql.sql"
        ).read_text(encoding="utf-8").strip()
E       AssertionError: assert 'CREATE OR RE...rence_profile' == 'CREATE OR RE...rence_profile'
E         
E         Skipping 1082 identical leading characters in diff, use -v to show
E           
E         -     AND (export_date IS NULL OR TO_DATE(export_date) <= {AS_OF_SQL})
E         ?          -----------------------
E         +     AND (TO_DATE(export_date) <= {AS_OF_SQL})
E           ),...
E         
E         ...Full output truncated (319 lines hidden), use '-vv' to show

tests\test_gold_referral_source_status.py:189: AssertionError
_______________ test_notebook_clocks_are_warning_free_and_explicit_utc[00_archive_load.py] ________________

name = '00_archive_load.py'

    @pytest.mark.parametrize("name", CLOCK_NOTEBOOKS)
    def test_notebook_clocks_are_warning_free_and_explicit_utc(name):
>       for value in clock_values(name):
                     ^^^^^^^^^^^^^^^^^^

tests\test_pipeline_utc_timestamps.py:61: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests\test_pipeline_utc_timestamps.py:56: in clock_values
    return [eval(compile(ast.Expression(call), name, "eval"), scope) for call in calls]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

>   ???
E   TypeError: datetime.utcnow() takes no arguments (1 given)

00_archive_load.py:21: TypeError
________________________ test_validator[validate_archive_snapshot_and_enrichment] _________________________

validator = WindowsPath('C:/repo/WMPP/WMPP/tests/validate_archive_snapshot_and_enrichment.py')

    @pytest.mark.parametrize("validator", VALIDATORS, ids=lambda path: path.stem)
    def test_validator(validator):
        """Each opted-in Python validator must pass from the repository root."""
        result = subprocess.run(
            [sys.executable, str(validator)],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print(f"PASS: {validator.name}")
            return
    
        print(f"FAIL: {validator.name}")
>       assert result.returncode == 0, (
            f"{validator.name} failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
E       AssertionError: validate_archive_snapshot_and_enrichment.py failed:
E         STDOUT:
E         PASS Fabric notebook cells and Python syntax
E         PASS ARCH-ETL-001 runner allows 9,200 seconds; nested DQ/Gold allow two hours
E         PASS ARCH-ETL-002 and LIVE-ETL-001 replace, rather than accumulate, the active month
E         PASS SI-018/SI-019 derived Silver enrichment and Gold promotion are present
E         PASS GLD-009/011/012/014 open, awaiting-offer, provider-derived spot and is_engaged logic is present
E         PASS GLD-013 provider-count, emergency, overdue, draft-age and IPA flags are present
E         PASS full fact_referral shape, snapshot promotion and Offer/IPA facts are present
E         PASS enrichment DQ rules and bidirectional date-order support are configured
E         
E         STDERR:
E         Traceback (most recent call last):
E           File "C:\repo\WMPP\WMPP\tests\validate_archive_snapshot_and_enrichment.py", line 240, in <module>
E             text = document.read_text(encoding="utf-8")
E           File "C:\Users\tmpaarmh\AppData\Local\Python\pythoncore-3.14-64\Lib\pathlib\__init__.py", line 787, in read_text
E             with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
E                  ~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           File "C:\Users\tmpaarmh\AppData\Local\Python\pythoncore-3.14-64\Lib\pathlib\__init__.py", line 771, in open
E             return io.open(self, mode, buffering, encoding, errors, newline)
E                    ~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E         FileNotFoundError: [Errno 2] No such file or directory: 'C:\\repo\\WMPP\\WMPP\\client documentation\\03_Architecture_and_Design\\Proposed_Solution_Architecture.md'
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['C:\\Users\\tmpaarmh\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe', 'C:\\repo\\WMPP\...\\repo\\\\WMPP\\\\WMPP\\\\client documentation\\\\03_Architecture_and_Design\\\\Proposed_Solution_Architecture.md\'\n').returncode

tests\test_validation_scripts.py:59: AssertionError
------------------------------------------ Captured stdout call -------------------------------------------
FAIL: validate_archive_snapshot_and_enrichment.py
____________________________ test_validator[validate_schema_drift_dimensions] _____________________________

validator = WindowsPath('C:/repo/WMPP/WMPP/tests/validate_schema_drift_dimensions.py')

    @pytest.mark.parametrize("validator", VALIDATORS, ids=lambda path: path.stem)
    def test_validator(validator):
        """Each opted-in Python validator must pass from the repository root."""
        result = subprocess.run(
            [sys.executable, str(validator)],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print(f"PASS: {validator.name}")
            return
    
        print(f"FAIL: {validator.name}")
>       assert result.returncode == 0, (
            f"{validator.name} failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
E       AssertionError: validate_schema_drift_dimensions.py failed:
E         STDOUT:
E         
E         STDERR:
E         Traceback (most recent call last):
E           File "C:\repo\WMPP\WMPP\tests\validate_schema_drift_dimensions.py", line 124, in <module>
E             assert archive_runbook.exists(), "Archive runbook is missing"
E                    ~~~~~~~~~~~~~~~~~~~~~~^^
E         AssertionError: Archive runbook is missing
E         
E       assert 1 == 0
E        +  where 1 = CompletedProcess(args=['C:\\Users\\tmpaarmh\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe', 'C:\\repo\\WMPP\...ts(), "Archive runbook is missing"\n           ~~~~~~~~~~~~~~~~~~~~~~^^\nAssertionError: Archive runbook is missing\n').returncode

tests\test_validation_scripts.py:59: AssertionError
------------------------------------------ Captured stdout call -------------------------------------------
FAIL: validate_schema_drift_dimensions.py
========================================= short test summary info =========================================
FAILED tests/test_archive_pipeline_modes.py::test_archive_children_do_not_repeat_setup_with_injected_parent[00_archive_load] - assert 'IS_ORCHESTRATED_RUN' not in {'__builtins__': {'__name__': 'builtins', '__doc__': "Built-in func...
FAILED tests/test_category_location_etl.py::test_referral_etl_simulation_sql_matches_current_notebook - AssertionError: assert 'CREATE OR RE...rence_profile' == 'CREATE OR RE...rence_profile'
FAILED tests/test_gold_referral_journey_status.py::test_all_journey_stages[6] - assert 5 == 6
FAILED tests/test_gold_referral_journey_status.py::test_active_ipa_and_signature_precedence[1-1-0-6] - assert 5 == 6
FAILED tests/test_gold_referral_journey_status.py::test_active_ipa_and_signature_precedence[1-1-None-6] - assert 5 == 6
FAILED tests/test_gold_referral_journey_status.py::test_active_ipa_and_signature_precedence[1-1-1-4] - assert 6 == 4
FAILED tests/test_gold_referral_journey_status.py::test_signatures_on_different_ipas_are_not_combined - assert 6 == 5
FAILED tests/test_gold_referral_source_status.py::test_separate_gold_journey_classifier_and_fixture_matches_production - AssertionError: assert 'CREATE OR RE...rence_profile' == 'CREATE OR RE...rence_profile'
FAILED tests/test_pipeline_utc_timestamps.py::test_notebook_clocks_are_warning_free_and_explicit_utc[00_archive_load.py] - TypeError: datetime.utcnow() takes no arguments (1 given)
FAILED tests/test_validation_scripts.py::test_validator[validate_archive_snapshot_and_enrichment] - AssertionError: validate_archive_snapshot_and_enrichment.py failed:
FAILED tests/test_validation_scripts.py::test_validator[validate_schema_drift_dimensions] - AssertionError: validate_schema_drift_dimensions.py failed:
=============================== 11 failed, 319 passed, 1 skipped in 11.30s ================================
PS C:\repo\WMPP\wmpp> 
