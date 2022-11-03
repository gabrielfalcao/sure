import os


from sure.version import version


def entrypoint():
    print(f"sure version {version}\n")
    print("Example usage in Python:\n\033[1;32m")
    print(
        """
import sure


def test_something():
    # Then instead of

    assert x.upper() == 'FOO'

    x = "foo"

    # you can write assertions like:
    x.upper().should.equal('FOO')
""".strip()
    )

    print("\033[0m\n----\n\033[1;33m")
    print("Full documentation: \033[1;34mhttps://sure.readthedocs.io/")
    print("\033[0m")
