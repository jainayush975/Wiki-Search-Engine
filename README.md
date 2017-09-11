# Wiki Search Engine

This Search Engine first need to make index from wikipedia dump.
Engine also provide search query for the index generated by it.
Engine provides searching of field queries for titles, external links, and body.

Index can be generated using:
```sh
  python  indexgenerator.py  path_to_wiki_dump
```
For Searching:
```sh
  python search.py "query"
```
>Query for different fields should be separated using ';' for different query and ':' for separating field type from query <br />
example: "C:Dog;B:Dog" or can be plain query <br />
example: "Dog"

You can download a small dump to test run from [here](https://drive.google.com/file/d/0B9o5ykSODCIlOEJsUFZPbVVLU3c/view?usp=sharing).