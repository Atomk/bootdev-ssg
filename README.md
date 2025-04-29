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

- [ ] Move tests to a `test` dir
