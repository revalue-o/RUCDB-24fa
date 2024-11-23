---
license: cc-by-sa-4.0
metrics:
- accuracy
pipeline_tag: text-generation
tags:
- code
---

A capable language model for text to SQL generation for Postgres, Redshift and Snowflake that is on-par with the most capable generalist frontier models.

![image/png](https://cdn-uploads.huggingface.co/production/uploads/603bbad3fd770a9997b57cb6/h52Z_OKYBaDDQMFZyU5pF.png)

## Model Description

Developed by: Defog, Inc
Model type: [Text to SQL]
License: [CC-by-SA-4.0]
Finetuned from model: [Meta-Llama-3-8B-Instruct]

## Demo Page
[https://defog.ai/sqlcoder-demo/](https://defog.ai/sqlcoder-demo/)

## Ideal prompt and inference parameters
Set temperature to 0, and do not do sampling.

### Prompt
```
<|begin_of_text|><|start_header_id|>user<|end_header_id|>

Generate a SQL query to answer this question: `{user_question}`
{instructions}

DDL statements:
{create_table_statements}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

The following SQL query best answers the question `{user_question}`:
```sql

```

## Evaluation
This model was evaluated on SQL-Eval, a PostgreSQL based evaluation framework developed by Defog for testing and alignment of model capabilities.

You can read more about the methodology behind SQLEval [here](https://defog.ai/blog/open-sourcing-sqleval/).

## Contact
Contact us on X at [@defogdata](https://twitter.com/defogdata), or on email at founders@defog.ai