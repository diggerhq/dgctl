import pytest

from dgctl.utils import get_bundle_id

class TestUtils:
    @pytest.mark.parametrize(
        "dir_name,exp",[
            ('myEnvName-2022-11-16-12-55', 'myEnvName'),
            ('my-env-name-2022-11-16-12-55', 'my-env-name'),
            ('env-3000-2022-11-16-12-55', 'env-3000'),
        ]
    )
    def test_bundle_regex(self, exp, dir_name, monkeypatch):
        monkeypatch.setattr("os.getcwd", lambda: dir_name)
        assert get_bundle_id() == exp
