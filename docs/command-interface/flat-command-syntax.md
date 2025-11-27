---
title: Flat command syntax
---

This is the syntax used in input.conf, and referred to "input.conf
syntax" in a number of other places.

  
`<command>  ::= [<prefixes>] <command_name> (<argument>)*`  
`` <argument> ::= (<unquoted> | " <double_quoted> " | ' <single_quoted> ' | `X <custom_quoted> X`) ``

`command_name` is an unquoted string with the command name itself. See
[List of Input Commands](list-of-input-commands.md) for a list.

Arguments are separated by whitespaces even if the command expects only
one argument. Arguments with whitespaces or other special characters
must be quoted, or the command cannot be parsed correctly.

Double quotes interpret JSON/C-style escaping, like `\t` or `\"` or
`\\`. JSON escapes according to RFC 8259, minus surrogate pair escapes.
This is the only form which allows newlines at the value - as `\n`.

Single quotes take the content literally, and cannot include the
single-quote character at the value.

Custom quotes also take the content literally, but are more flexible
than single quotes. They start with ``<span class="title-ref">
(back-quote) followed by any ASCII character, and end at the first
occurrence of the same pair in reverse order, e.g.
</span>`-foo-`<span class="title-ref"> or
</span>`` `bar ```. The final pair sequence is not allowed at the value - in these examples`-`` ` and ````
respectively. In the second example the last character of the value also
can't be a back-quote.

Mixed quoting at the same argument, like `'foo'"bar"`, is not supported.

Note that argument parsing and property expansion happen at different
stages. First, arguments are determined as described above, and then,
where applicable, properties are expanded - regardless of argument
quoting. However, expansion can still be prevented with the `raw` prefix
or `$>`. See [Input Command Prefixes](input-command-prefixes.md) and
[Property Expansion](property-expansion.md).

