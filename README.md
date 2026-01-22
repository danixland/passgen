# Random Password Generator

This Python script generates strong, easy to memorize passwords using random words from a dictionary file.

## Installation

1. Ensure Python 3.x is installed on your system.
2. Clone the repository to your local machine:

```bash
   git clone https://github.com/yourusername/random-password-generator.git
```
3. Navigate to the project directory:
```bash
cd random-password-generator
```

## Usage

The script can be run directly from the command line specifying the number of words to use and optionally, some other options:

```bash
python generate_password.py <num_words> [options]
```

### Options

- `-s, --separator SEPARATOR`: Specify a custom separator symbol from our list (default: `@`). See [Separators](#separators).
- `-r, --random-separator`: Use a random separator from a predefined list.
- `-0, --no-numerals`: Disable numbers in the password.
- `-A, --no-capitals`: Disable capitalized words in the output.

### Examples

1. Generate a 3-word password (the default if no argument is passed) with default settings:
   ```bash
   python generate_password.py
   ```

2. Generate a 6-word password with a custom separator `!`:
   ```bash
   python generate_password.py 6 -s !
   ```

3. Generate a 7-word password using a random separator and no numbers:
   ```bash
   python generate_password.py 7 --random-separator -0
   ```

4. Generate an 8-word password with capitalized words disabled:
   ```bash
   python generate_password.py 8 -A
   ```

## Separators

The script uses this list of separators:

```python
["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", "{", "}", "[", "]", "|", ":", ";", "<", ">", ",", ".", "?"]
```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a pull request.

## License

This project is licensed under the GPLv2 License - see the [LICENSE](LICENSE) file for details.

## Author

 - [danix](https://danix.xyz) - it's just me, really...