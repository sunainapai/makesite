Contribution Guidelines
=======================

Please take care of the following points while sending a pull request to
this project:

 1. Ensure that the pull request does not add major features or increase
    the scope of the project. Bug fixes and minor improvements are okay
    and might be accepted. But major features or changes that increase
    the complexity of the code will not be accepted.

 2. Follow [PEP 8][CODING-GUIDE] while editing [makesite.py].

 3. Use only Makefile syntax, shell syntax, commands, and options that
    are specified in [POSIX][POSIX-HOME] as much as possible while
    editing [Makefile]. Avoid Bash-specific and GNU-specific features.
    See documentation on [POSIX Shell Command Language][POSIX-SCL],
    [POSIX Utilities][POSIX-UTIL], and [POSIX Make][POSIX-MAKE] for
    reference.

 4. Follow [Erlang/OTP commit message guidelines][COMMIT-GUIDE] while
    writing Git commit messages.


[makesite.py]: makesite.py
[Makefile]: Makefile
[POSIX-HOME]: https://pubs.opengroup.org/onlinepubs/9699919799/
[POSIX-SCL]: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html
[POSIX-UTIL]: https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html
[POSIX-MAKE]: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/make.html
[CODING-GUIDE]: https://www.python.org/dev/peps/pep-0008/
[COMMIT-GUIDE]: https://github.com/erlang/otp/wiki/Writing-good-commit-messages
