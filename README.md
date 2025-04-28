# SmolDocling OCR Streamlit app
Streamlit app to perform OCR using SmolDocling model.

Note:- uses the SmolDocling model from [DS4SD/SmolDocling-256M-preview](**https://huggingface.co/ds4sd/SmolDocling-256M-preview**).
More models may be added, just ask! 

The app extracts text, tables, code, chart etc from doc images. 
Produces outputs in Markdown, DocTags, Text and HTML format. 
_Note: As of 28Apr only single image upload and extraction is tested._ 
## Setup

### Clone the repository
git clone git@github.com:ananyalahiri2003/smoldocling-ocr-streamlit.git
cd src

### Create .env 
Under src/ create `.env` file with 

HF_TOKEN={your_hf_token}

### Install dependencies 
`poetry lock --no-update`

`poetry install` 

All dependencies in pyproject.toml file. 


## Start the app
`streamlit run src/app.py`
This opens up streamlit interface on port 8501 and allows you to process. 

#### NOTE 
CPU is ok to use, things will be slow.  

## License
MIT License 

## Future Plans 
Add new models. 

Add support for multi-page pdf docs. 

_Pls add your wish list._ 

  
