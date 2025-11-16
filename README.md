# 🎯 Simple Typing Application

**Measure and Improve Your Typing Performance with AI-Powered Practice**

![GitHub top language](https://img.shields.io/github/languages/top/hmasdev/simple_typing_application)
![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/hmasdev/simple_typing_application?sort=semver)
![GitHub](https://img.shields.io/github/license/hmasdev/simple_typing_application)
![GitHub last commit](https://img.shields.io/github/last-commit/hmasdev/simple_typing_application)

![Scheduled Tests](https://github.com/hmasdev/simple_typing_application/actions/workflows/tests-on-schedule.yaml/badge.svg)

![application image](./pics/application.png)

## ✨ Features

- 🤖 **AI-Powered Sentence Generation**: Use OpenAI's GPT models or HuggingFace models to generate dynamic typing targets
- 📊 **Performance Tracking**: Detailed recording of your typing performance with timestamps and accuracy metrics
- 🌐 **Multi-Language Support**: Full support for Japanese (Hiragana, Katakana, Kanji) and English
- ⌨️ **Flexible Input**: Multiple correct input patterns (e.g., both 'ti' and 'chi' for 'ち')
- 🎨 **Console Interface**: Clean, distraction-free typing practice environment
- 📈 **Data Analysis Ready**: Export records in JSON format for detailed analysis with pandas/matplotlib

## Requirements

- **Python >= 3.10** (Python 3.10, 3.11, 3.12, and 3.13 are supported)

- **Dependencies** (automatically installed):
  - `click`
  - `langchain` (>= 1.0)
  - `langchain_openai`
  - `openai`
  - `pydantic` (>= 2.0)
  - `pynput`
  - `python-dotenv`
  - `requests`
  - `sshkeyboard`
  - `types-pynput`
  - `types-requests`

- **OpenAI API Key** (required for AI-generated typing targets)

See [`pyproject.toml`](./pyproject.toml) for detailed information.

## Installation

### Quick Install (Recommended)

The recommended way to install is using [uv](https://docs.astral.sh/uv/), a fast Python package installer:

```bash
# Clone the repository
git clone https://github.com/hmasdev/simple_typing_application.git
cd simple_typing_application

# Install with uv (recommended)
uv sync
```

This will install all dependencies and set up the application for use.

### Alternative Installation Methods

#### Using pip

```bash
pip install git+https://github.com/hmasdev/simple_typing_application.git
```

#### Install with Optional Dependencies

You can specify the following optional dependencies:

- **`[extra]`**: Data analysis packages (`pandas`, `matplotlib`, `jupyterlab`, `seaborn`)
- **`[huggingface]`**: HuggingFace models support (`torch`, `transformers`, etc.)
- **`[dev]`**: Development tools (`pytest`, `mypy`, `ruff`, etc.)

**Using uv** (recommended):

```bash
git clone https://github.com/hmasdev/simple_typing_application.git
cd simple_typing_application

# Install with specific optional dependencies
uv sync --extra extra --extra huggingface
```

**Using pip**:

```bash
git clone https://github.com/hmasdev/simple_typing_application.git
cd simple_typing_application

# Install with optional dependencies
pip install ".[extra,huggingface]"
```

For more details, see [`./pyproject.toml`](./pyproject.toml).

## 🚀 Quick Start

1. **Clone and install**:
   ```bash
   git clone https://github.com/hmasdev/simple_typing_application.git
   cd simple_typing_application
   uv sync
   ```

2. **Set up your OpenAI API key**:
   ```bash
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

3. **Run the application**:
   ```bash
   python -m simple_typing_application
   ```

4. **Start typing!** Follow the on-screen prompts and improve your typing skills.

## Usage

### ⚙️ Configuration

You can specify some parameters with '.json'.

For example, the following `.json` files are valid:

- [`./sample_config.json`](./sample_config.json)
- [`./sample_config_huggingface.json`](./sample_config_huggingface.json)
- [`./sample_config_static.json`](./sample_config_static.json)

The content of `./sample_config.json` is as follows:

```json
{
    "sentence_generator_type": "OPENAI",
    "sentence_generator_config": {
        "model": "gpt-5-nano",
        "temperature": 0.7,
        "openai_api_key": "HERE_IS_YOUR_API_KEY",
        "memory_size": 0,
        "max_retry": 5
    },
    "user_interface_type": "CONSOLE",
    "user_interface_config": {},
    "key_monitor_type": "PYNPUT",
    "key_monitor_config": {},
    "record_direc": "./record"
}
```

As default, the contents of 'sample_config.json' are used except `openai_api_key`.
In this case, you should add an environment variable `OPENAI_API_KEY` which contains your API key or create `.env` file like

```bash
OPENAI_API_KEY={HERE_IS_YOUR_API_KEY}
```

#### 🤖 Sentence Generator

You can specify the following as `sentence_generator_type`:

- **`OPENAI`**: Use OpenAI API to generate typing targets (recommended: `gpt-5-nano`, `gpt-4o`, or `gpt-4-turbo`)
- **`HUGGINGFACE`**: Use models available on HuggingFace to generate typing targets
- **`STATIC`**: Use predefined typing targets that you have specified

For each `sentence_generator_type`, you can specify the detailed parameters as `sentence_generator_config`:

- `OPENAI`
  - `model`: See [langchain.chat_models.openai.ChatOpenAI](#langchain.chat_models.openai.ChatOpenAI)
  - `temperature`: See [langchain.chat_models.openai.ChatOpenAI](#langchain.chat_models.openai.ChatOpenAI)
  - `openai_api_key`: See [langchain.chat_models.openai.ChatOpenAI](#langchain.chat_models.openai.ChatOpenAI)
  - `memory_size`: See [langchain.memory.buffer.ConversationBufferMemory](#langchain.memory.buffer.ConversationBufferMemory)
  - `max_retry`: Maximum number of times to rerun when an error occurs

- `HUGGINGFACE`
  - `model`: Model name. For example, "line-corporation/japanese-large-lm-3.6b", "rinna/japanese-gpt-neox-3.6b", "rinna/bilingual-gpt-neox-4b" and "cyberagent/open-calm-7b" are available as Japanese LLM. For details, See [huggingface.co/models](#huggingface_models_available_text_generation).
  - `do_sample`: `true` or `false`. See [huggingface.co/docs/transformers/pipeline_tutorial](#huggingface_pipeline_tutorial).
  - `max_length`: int. See [huggingface.co/docs/transformers/pipeline_tutorial](#huggingface_pipeline_tutorial).
  - `top_k`: int. See [huggingface.co/docs/transformers/pipeline_tutorial](#huggingface_pipeline_tutorial).
  - `top_p`: float between 0 and 1. See [huggingface.co/docs/transformers/pipeline_tutorial](#huggingface_pipeline_tutorial).
  - `device`: `cpu` or `cuda`

- `STATIC`
  - `text_kana_map`: key-value pairs whose keys are row typing targets and values are typing targets which do not include kanjis;
  - `is_random`: whether typing targets are randomly selected or sequentially displayed.

To see the default values, see [`./simple_typing_application/models/config_models/sentence_generator_config_model.py`](./simple_typing_application/models/config_models/sentence_generator_config_model.py).

> **💡 Tip**: For best results, we recommend using `gpt-5-nano` (fast and cost-effective) or `gpt-4o` (most capable) for OpenAI models.

#### 🖥️ User Interface

You can specify the followings as `user_interface_type`:

- `CONSOLE`: CUI

For each `user_interface_type`, you can specify the detailed parameters as `user_interface_config`:

- `CONSOLE`
  - No parameters

To see the default values, see [`./simple_typing_application/models/config_models/user_interface_config_model.py`](./simple_typing_application/models/config_models/user_interface_config_model.py).

#### ⌨️ Key Monitor

You can specity the followings as `key_monitor_type`:

- `PYNPUT`: `pynput`-based local key monitor
- `SSHKEYBOARD`: `sshkeyboard`-based key monitor

For each `key_monitor_type`, you can specify the detailed parameters as `key_monitor_config`:

- `PYNPUT`
  - No parameters
- `SSHKEYBOARD`
  - No parameters

To see the default values, see [`./simple_typing_application/models/config_models/key_monitor_config_model.py`](./simple_typing_application/models/config_models/key_monitor_config_model.py).

### 🎮 Launch the Application

You can launch this application with the following command:

```bash
python -m simple_typing_application -c HERE_IS_YOUR_CONFIG_FILE
```

If you want to launch this application with debug mode, run the following command:

```bash
python -m simple_typing_application -c HERE_IS_YOUR_CONFIG_FILE --debug
```

For more details, run `python -m simple_typing_application --help`.

### ✍️ Typing Practice

`simple_typing_application` shows typing targets through the interface which you have specified.
Type correct keys.

> **📝 Note**: The `Typing Target (Romaji)` displayed in your interface is one of the correct typing patterns. For example, when `Typing Target (Hiragana)` is 'ち', both 'ti' and 'chi' are correct, although only one of them is displayed.

**Available keyboard shortcuts**:

- `Esc` or `Ctrl+c`: Quit the application
- `Tab`: Skip the current typing target

### 📊 Analyze Your Typing Performance

The application records your typing in the following format in the directory specified in you config file for each typing target.

```json
{
    "timestamp": "HERE IS TIMESTAMP THE TYPING START WITH FORMAT %Y-%m-%dT%H:%M:%S.%f",
    "typing_target": {
        "text": "HERE IS TYPING TARGET",
        "text_hiragana_alphabet_symbol": "HERE IS TRANSFORMED STRING WHICH CONTAINS ONLY HIRAGANA, ALPHABET AND SYMBOLS",
        "typing_target": [["CORRECT PATTERN. TYPICALLY ROMANIZED STRING", ...], ...]
    },
    "records": [
        {
            "timestamp": "HERE IS TIMESTAMP WHEN YOU TYPE %Y-%m-%dT%H:%M:%S.%f",
            "pressed_key": "WHICH KEY YOU HAVE PRESSED",
            "correct_keys": ["", ...],
            "is_correct": true or false
        },
        ...
    ]
}
```

Refer to [`./sample_record.json`](./sample_record.json) for an example.

## 🛠️ Development

1. Fork this repository:
   - [https://github.com/hmasdev/simple_typing_application/fork](https://github.com/hmasdev/simple_typing_application/fork)

2. Clone your forked repository:

   ```bash
   git clone https://github.com/hmasdev/simple_typing_application
   cd simple_typing_application
   ```

3. Create your feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

4. Setup your development environment (uv recommended):

   ```bash
   uv sync
   ```

   If you want to include optional dependencies for development (e.g., `huggingface`, `pandas`, etc.), run:

   ```bash
   uv sync --extra huggingface --extra extra
   ```

   To know which option is available, see [`./pyproject.toml`](./pyproject.toml).

5. Develop your feature and add tests.

6. Test your feature:

   ```bash
   uv run pytest  # Unit test
   uv run pytest -m integrate  # integration test
   ```

7. Check the code style and static type:

   ```bash
   uv run ruff check simple_typing_application
   uv run ruff check tests
   uv run mypy simple_typing_application
   uv run mypy tests
   ```

8. Commit your changes:

   ```bash
   git add .
   git commit -m "Add your feature"
   ```

9. Push to the branch:

   ```bash
   git push -u origin feature/your-feature
   ```

10. Create a new Pull Request:
    - [https://github.com/hmasdev/simple_typing_application/compare](https://github.com/hmasdev/simple_typing_application/compare)

Thank you for your contribution! 🙏

## 📄 LICENSE

`simple_typing_application` is licensed under the [MIT](./LICENSE) License. See the LICENSE file for more details.

## 📚 References

- [1] <a id="langchain.chat_models.openai.ChatOpenAI"></a> https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.openai.ChatOpenAI.html
- [2] <a id="langchain.memory.buffer.ConversationBufferMemory"></a> https://api.python.langchain.com/en/latest/memory/langchain.memory.buffer.ConversationBufferMemory.html
- [3] <a id="huggingface_models_available_text_generation"></a> https://huggingface.co/models?pipeline_tag=text-generation
- [4] <a id="huggingface_pipeline_tutorial"></a> https://huggingface.co/docs/transformers/pipeline_tutorial

## 👨‍💻 Authors

- [hmasdev](https://github.com/hmasdev)
