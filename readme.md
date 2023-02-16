# BOT_ITE_DOG

## Overview

A software that provides sentence generation using an N-gram model generated from sentences as a Discord bot

## 使用方法

- Prepare the source text
  - The text should be stored in a file separated by a line break (LF).
  - Multiple files are acceptable.
  - Escape newline characters to `\n`.
  - Write the text in `/text/src/tweets_20230203235233.txt` (We will change it to scan the directory.)
- Prepare Bot token
  - Write it in `/credentials/token.txt`.
- Execute the following command
  ```sh
  $docker compose build prod
  $docker compose up prod
  ```

## Use only for sentence generation

All functions are available in the `dev` stage image

```sh
$docker compose build dev
$docker compose up dev
```

- `/src/creageNGRam.py`: Generate N-gram model
- `/src/generate.py`: Generate sentences from the generated N-gram model
