
from astroid_miner.utilities import dict_to_kwargs, kwargs_to_dict


class TestUtilities:

    def test_dict_to_kwargs(self):

        src_in = """
{
    "name": "Alice",
    "age": 30,
    "address": {
        'state': "New York",
        'city': "New York City",
    },
}
"""
        expected = "\n".join([
            "name='Alice',",
            "age=30,",
            "address={'state': 'New York', 'city': 'New York City'},",
        ])

        assert expected == dict_to_kwargs(src_in)

    def test_dict_to_kwargs__expr_is_not_dict(self):
        """Test to see if ValueError is raised"""
        assert False

    def test_dict_to_kwargs__indent_nested_structures(self):
        """Function should indent nested dicts, lists, sets, and tuples"""
        assert False

    def test_kwargs_to_dict(self):
        assert False, "Implement this method first"