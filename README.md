#  Base Converter (ManimGL)

A **visual base conversion tool** built with [ManimGL](https://github.com/3b1b/manim) to **demonstrate how integers are converted between different number bases** through engaging **animated visualizations**.

---

##  Features

-  Convert integers between **any bases (2–16)**  
-  **Step-by-step visual breakdown** of the division/remainder conversion method  
-  Supports **power-of-two bases** (2, 4, 8, 16)  
-  Includes **binary logic operations**: `AND`, `OR`, `XOR`  
-  Uses **ManimGL animations** for clear and intuitive demonstrations  

---

##  Requirements

- **Python 3.8+**
- **[ManimGL](https://github.com/3b1b/manim)**
- **LaTeX compiler:** [MikTeX](https://miktex.org/download)
- *(Optional)* [virtualenv](https://pypi.org/project/virtualenv/)

### Installation

```bash
pip install manimgl
```

## ⚙️ Setup

1. Clone the repository:

```bash
git clone https://github.com/5ache3/base-converter.git
cd base-convertor
```


##  Usage

The project now features a CLI for easy interaction. You can perform base conversions and logic operations directly from your terminal.

### Base Conversion
Convert numbers between any bases from 2 to 16.

**Syntax:**
```bash
python main.py convert <number> <source_base> <target_base> [options]
```

**Common Options:**
- `--no-animate`: Skip the animation and produce an image instead.
- `--no-table`: Hide the conversion/truth table.

**Example:**
```bash
python main.py convert 1251 10 2
```

### Logic Operations
Perform bitwise logic operations (`AND`, `OR`, `XOR`) on two numbers.

**Syntax:**
```bash
python main.py logic <a> <b> <base> <operation> [options]
```

**Example:**
```bash
python main.py logic 76F2 543F 16 OR --no-animate
```

---

## ⚡ Caching System

To avoid redundant rendering, the project includes an automatic caching system.
- Computed scenes (videos or images) are tracked in `scene_cache.json`.
- If you run a command with parameters that have already been computed, the CLI will skip rendering and return the path to the existing file.
- If an output file is deleted, the cache will automatically re-render it on the next run.

---

##  Examples

### Base Conversion (Decimal to Binary)
```bash
python main.py convert 1251 10 2
```
![1251-B10_to_B2](assets/1251-B10_to_B2.png)

### Hexadecimal Conversion
```bash
python main.py convert 3F1B 16 10 --no-animate
```
![3F1B-B16_to_B10](assets/3F1B-B16_to_B10.png)

### Logic Operation (OR in Hex)
```bash
python main.py logic 76F2 543F 16 OR --no-animate
```
![OR76F2-543F-B16](assets/OR76F2-543F-B16.png)

---

##  Inspiration
Created to help students and educators visualize base conversion algorithms and binary logic in an intuitive and interactive way.

**Made with love for math, logic, and visualization 🙃.**
