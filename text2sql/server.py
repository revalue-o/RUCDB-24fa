import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import sqlparse
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn

prompt = """<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Generate a SQL query to answer this question: `{question}`
DDL statements:
CREATE TABLE products (
  product_id INTEGER PRIMARY KEY, -- Unique ID for each product
  name VARCHAR(50), -- Name of the product
  price DECIMAL(10,2), -- Price of each unit of the product
  quantity INTEGER  -- Current quantity in stock
);
CREATE TABLE customers (
   customer_id INTEGER PRIMARY KEY, -- Unique ID for each customer
   name VARCHAR(50), -- Name of the customer
   address VARCHAR(100) -- Mailing address of the customer
);
CREATE TABLE salespeople (
  salesperson_id INTEGER PRIMARY KEY, -- Unique ID for each salesperson
  name VARCHAR(50), -- Name of the salesperson
  region VARCHAR(50) -- Geographic sales region
);
CREATE TABLE sales (
  sale_id INTEGER PRIMARY KEY, -- Unique ID for each sale
  product_id INTEGER, -- ID of product sold
  customer_id INTEGER,  -- ID of customer who made purchase
  salesperson_id INTEGER, -- ID of salesperson who made the sale
  sale_date DATE, -- Date the sale occurred
  quantity INTEGER -- Quantity of product sold
);
CREATE TABLE product_suppliers (
  supplier_id INTEGER PRIMARY KEY, -- Unique ID for each supplier
  product_id INTEGER, -- Product ID supplied
  supply_price DECIMAL(10,2) -- Unit price charged by supplier
);
-- sales.product_id can be joined with products.product_id
-- sales.customer_id can be joined with customers.customer_id
-- sales.salesperson_id can be joined with salespeople.salesperson_id
-- product_suppliers.product_id can be joined with products.product_id<|eot_id|><|start_header_id|>assistant<|end_header_id|>
The following SQL query best answers the question `{question}`:
```sql
"""



def model_init(model_name : str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    available_memory = torch.cuda.get_device_properties(0).total_memory
    if available_memory > 20e9:
        # if you have atleast 20GB of GPU memory, run load the model in float16
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
            use_cache=True,
        )
    else:
        # else, load in 4 bits – this is slower and less accurate
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            # torch_dtype=torch.float16,
            load_in_4bit=True,
            device_map="auto",
            use_cache=True,
        )
    return tokenizer, model



def generate_query(question):
    updated_prompt = prompt.format(question=question)
    inputs = tokenizer(updated_prompt, return_tensors="pt").to("cuda")
    print("finish")
    
    generated_ids = model.generate(
        **inputs,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=400,
        do_sample=False,
        num_beams=1,
        temperature=0.0,
        top_p=1,
    )
    outputs = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)
    print("finish")
 
    torch.cuda.empty_cache()
    torch.cuda.synchronize()
    # empty cache so that you do generate more results w/o memory crashing
    # particularly important on Colab – memory management is much more straightforward
    # when running on an inference service
    # return sqlparse.format(outputs[0].split("[SQL]")[-1], reindent=True)
    std_sql = sqlparse.format(outputs[0].split("```sql")[1].split(";")[0], reindent=True) 
    return {'response' : std_sql}

valid_api_keys = {
      "4f484d4324b66bdbb835415c454fab772a14d126555d5a0df897b4a22c38706b": "test_0",  # API Key: 使用者信息
  }

if __name__ == "__main__":
  model_name = "./llama-3-sqlcoder-8b"
  tokenizer, model = model_init(model_name)
  
  app = FastAPI()
  class ModelInput(BaseModel):
      input_data: str

  @app.post("/predict")
  async def get_prediction(input: ModelInput, request: Request):
      api_key = request.headers.get("Authorization")
  
      # 这里您可以检查 API Key 是否有效
      if not api_key or api_key not in valid_api_keys:
          raise HTTPException(status_code=401, detail="Invalid API Key")
  
      # 模型预测
      result = generate_query(input.input_data)
      return result
  
  uvicorn.run(app, host="10.77.40.36", port=9080)
