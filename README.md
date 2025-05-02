# bootdev-ssg

A static site generator. Converts all Markdown files in the `content` directory into HTML by filling `template.html`.

Tested with Python 3.12 on WSL (Ubuntu).

[Live demo](https://github.com/Atomk/bootdev-ssg/) - Uses placeholder contents provided by Boot.dev, the generated HTML lives [in the gh-pages branch](https://github.com/Atomk/bootdev-ssg/tree/gh-pages/docs).

This is the third Python project in [Boot.dev](https://www.boot.dev/)'s curriculum.


## Usage

All commands below assume you are in the `bootdev-ssg` directory.

```bash
python3 src/main.py <output_dir_name> [base_url]
```

- A directory called `output_dir_name` will be created with the generated output. If it already exists, it will be deleted and recreated.
- `base_url` (optional) is useful to add a prefix to all internal links, useful for hosting the website with Github Pages, which serves pages from a subdirectory and not directly from the domain's root.
    - Currently, for this to work properly, all internal links in Markdown must start with the `/` character.


#### View the output locally

1. Run the SSG
```bash
./main.sh
```
2. Navigate to `http://localhost:8888`


#### Run tests

```bash
./test.sh
```

#### Build for use with Github Pages

```bash
./build.sh
```

## TODO

- [ ] Move tests to a `test` dir?
- [ ] Create new tests that use markdown files and assert that the conversion result is identical to the expected HTML file
- [ ] Support nested bullet lists
- [ ] Error for block that starts with "```" but has no corresponding closing delimiter
- [ ] Allow code blocks to contain empty lines
- [ ] Convert sequences of 3+ dashes to horizontal lines
- [ ] Convert newlines to `<br />`
- [ ] Remove all TODOs in code by fixing or documenting