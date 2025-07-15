
## Installation

Install pysele with virtual env 

```bash
cp sample.env .env
```

create virtual env on python : 
```bash 
python3 -m venv env
```

Running venv On Windows:
```bash
bash .\env\Scripts\activate
```

Running venv On MacOS/Linux:
```bash
bash source env/bin/activate
```

and Then Intall Dependencies : 
```bash
pip install selenium webdriver-manager

pip install selenium
```
and Running The Sample Test With : 

```bash
python -m cobaTest.tests.test_make_appointment
```
