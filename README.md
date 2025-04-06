# 🐰 Easter Bunny Optimised Planning Tool 🐰

![Slides](2025-04-01_OptimisingEaster_DavidSmith.gif)
Talk Slides

### Setup 

#### Install Python
Python 3.11 (just the version I used)

#### Setup Virtual Environment  
Setup python virtual environment called ".venv"
```
python -m venv .venv
```

Activte .venv 
(I'm on windows if you aren't, look up how to activate python virtual environment)
```
source .venv/Scripts/activate
```

#### Install Packages
```
pip install -r requirements.txt

```

#### Running Streamlit
To run streamlit 

```
streamlit run app/Home.py

```
View on port [localhost:8051](http://localhost:8501/)



## Running streamlit with Docker 

```
docker compose -f 'docker-compose.yml' up -d --build

```

View on port [localhost:8081](http://localhost:8081/)





## Exporting Model Documentation to file
NOTE: you will need to install Pandoc 

**Exporting to Word**
```
pandoc --toc  --standalone --mathjax -f markdown -t docx  ./documentation/model_documentation.md -o ./documentation/model_documentation.docx --reference-doc ./documentation/reference.docx

```
