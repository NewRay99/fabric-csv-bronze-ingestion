PS C:\repo\WMPP\wmpp> python -m pytest .\tests\test_gold_ipa_signature_contract.py
=========================================== test session starts ===========================================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\repo\WMPP\wmpp
configfile: pytest.ini
collected 14 items                                                                                         

tests\test_gold_ipa_signature_contract.py F......FFF....                                             [100%]

================================================ FAILURES =================================================
___________________________ test_gold_ipa_signature_and_closed_state[1-1-0-1-0] ___________________________

provider = 1, authority = 1, closed = 0, completed = 1, pending = 0

    @pytest.mark.parametrize('provider,authority,closed,completed,pending', [
        (1, 1, 0, 1, 0), (1, 0, 0, 0, 1), (0, 1, 0, 0, 1),
        (0, 0, 0, 0, 1), (None, 1, 0, 0, 1), (1, None, 0, 0, 1),
        (1, 1, 1, 1, 0), (1, 0, 1, 0, 0), (0, 0, 1, 0, 0),
    ])
    def test_gold_ipa_signature_and_closed_state(provider, authority, closed, completed, pending):
        with sqlite3.connect(':memory:') as connection:
            connection.execute('CREATE TABLE ipa (signed_by_provider, signed_by_local_authority, closed)')
            connection.execute('INSERT INTO ipa VALUES (?, ?, ?)', (provider, authority, closed))
            # The projection uses portable COALESCE, boolean CAST, AND and NOT operations.
            row = connection.execute('SELECT ' + SIGNATURE_PROJECTION + ' FROM ipa i').fetchone()
>           assert row == (provider or 0, authority or 0, completed, pending)
E           assert (1, 1, 0, 1) == (1, 1, 1, 0)
E             
E             At index 2 diff: 0 != 1
E             Use -v to get more diff

tests\test_gold_ipa_signature_contract.py:28: AssertionError
___________________________ test_gold_ipa_signature_and_closed_state[1-0-1-0-0] ___________________________

provider = 1, authority = 0, closed = 1, completed = 0, pending = 0

    @pytest.mark.parametrize('provider,authority,closed,completed,pending', [
        (1, 1, 0, 1, 0), (1, 0, 0, 0, 1), (0, 1, 0, 0, 1),
        (0, 0, 0, 0, 1), (None, 1, 0, 0, 1), (1, None, 0, 0, 1),
        (1, 1, 1, 1, 0), (1, 0, 1, 0, 0), (0, 0, 1, 0, 0),
    ])
    def test_gold_ipa_signature_and_closed_state(provider, authority, closed, completed, pending):
        with sqlite3.connect(':memory:') as connection:
            connection.execute('CREATE TABLE ipa (signed_by_provider, signed_by_local_authority, closed)')
            connection.execute('INSERT INTO ipa VALUES (?, ?, ?)', (provider, authority, closed))
            # The projection uses portable COALESCE, boolean CAST, AND and NOT operations.
            row = connection.execute('SELECT ' + SIGNATURE_PROJECTION + ' FROM ipa i').fetchone()
>           assert row == (provider or 0, authority or 0, completed, pending)
E           assert (1, 0, 1, 0) == (1, 0, 0, 0)
E             
E             At index 2 diff: 1 != 0
E             Use -v to get more diff

tests\test_gold_ipa_signature_contract.py:28: AssertionError
___________________________ test_gold_ipa_signature_and_closed_state[0-0-1-0-0] ___________________________

provider = 0, authority = 0, closed = 1, completed = 0, pending = 0

    @pytest.mark.parametrize('provider,authority,closed,completed,pending', [
        (1, 1, 0, 1, 0), (1, 0, 0, 0, 1), (0, 1, 0, 0, 1),
        (0, 0, 0, 0, 1), (None, 1, 0, 0, 1), (1, None, 0, 0, 1),
        (1, 1, 1, 1, 0), (1, 0, 1, 0, 0), (0, 0, 1, 0, 0),
    ])
    def test_gold_ipa_signature_and_closed_state(provider, authority, closed, completed, pending):
        with sqlite3.connect(':memory:') as connection:
            connection.execute('CREATE TABLE ipa (signed_by_provider, signed_by_local_authority, closed)')
            connection.execute('INSERT INTO ipa VALUES (?, ?, ?)', (provider, authority, closed))
            # The projection uses portable COALESCE, boolean CAST, AND and NOT operations.
            row = connection.execute('SELECT ' + SIGNATURE_PROJECTION + ' FROM ipa i').fetchone()
>           assert row == (provider or 0, authority or 0, completed, pending)
E           assert (0, 0, 1, 0) == (0, 0, 0, 0)
E             
E             At index 2 diff: 1 != 0
E             Use -v to get more diff

tests\test_gold_ipa_signature_contract.py:28: AssertionError
____________________ test_multiple_ipas_do_not_collapse_signature_counts_to_one_offer _____________________

    def test_multiple_ipas_do_not_collapse_signature_counts_to_one_offer():
        with sqlite3.connect(':memory:') as connection:
            connection.execute('CREATE TABLE ipa (offer_id, signed_by_provider, signed_by_local_authority, closed)')
            connection.executemany('INSERT INTO ipa VALUES (?, ?, ?, ?)', [
                ('offer-1', 1, 1, 0), ('offer-1', 0, 1, 0), ('offer-1', 0, 0, 1),
            ])
            rows = connection.execute('SELECT ' + SIGNATURE_PROJECTION + ' FROM ipa i').fetchall()
            assert len(rows) == 3
            assert sum(row[2] for row in rows) == 1
>           assert sum(row[3] for row in rows) == 1
E           assert 2 == 1
E            +  where 2 = sum(<generator object test_multiple_ipas_do_not_collapse_signature_counts_to_one_offer.<locals>.<genexpr> at 0x0000017D34179E50>)

tests\test_gold_ipa_signature_contract.py:40: AssertionError
========================================= short test summary info =========================================
FAILED tests/test_gold_ipa_signature_contract.py::test_gold_ipa_signature_and_closed_state[1-1-0-1-0] - assert (1, 1, 0, 1) == (1, 1, 1, 0)
FAILED tests/test_gold_ipa_signature_contract.py::test_gold_ipa_signature_and_closed_state[1-0-1-0-0] - assert (1, 0, 1, 0) == (1, 0, 0, 0)
FAILED tests/test_gold_ipa_signature_contract.py::test_gold_ipa_signature_and_closed_state[0-0-1-0-0] - assert (0, 0, 1, 0) == (0, 0, 0, 0)
FAILED tests/test_gold_ipa_signature_contract.py::test_multiple_ipas_do_not_collapse_signature_counts_to_one_offer - assert 2 == 1
====================================== 4 failed, 10 passed in 0.39s =======================================
PS C:\repo\WMPP\wmpp> 
