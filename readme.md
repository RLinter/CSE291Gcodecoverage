## LLM integrate test coverage checker 

### Go throught the workflow step by step
run experiment.ipynb step by step


### Get gradio UI ready in your environment
```
conda create -n coveragetest python=3.9
conda activate coveragetest
pip install openai
pip install gradio
```
### Activate server
```
python ./gradio_UI.py
```
use local address http://127.0.0.1:7860/ to open the server