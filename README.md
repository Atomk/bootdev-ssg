# bootdev-ssg

A static site generator.

Converts all Markdown files in the `content` directory into HTML by filling `template.html`. The generated pages will be stored into a `public` directory.

Tested with Python 3.12 on WSL (Ubuntu).

This is the third Python project in [Boot.dev](https://www.boot.dev/)'s curriculum.


## Run tests

From the repo's root directory:
```bash
./test.sh
```


## View the output

1. Run the SSG
```bash
./main.sh
```
2. Navigate to `http://localhost:8888`


## TODO

- [ ] Move tests to a `test` dir?
- [ ] Create new tests that use markdown files and assert that the conversion result is identical to the expected HTML file
- [ ] Support nested bullet lists
- [ ] Error for block that starts with "```" but has no corresponding closing delimiter
- [ ] Allow code blocks to contain empty lines
- [ ] Convert sequences of 3+ dashes to horizontal lines
- [ ] Convert newlines to `<br />`
- [ ] Remove all TODOs in code by fixing or documenting