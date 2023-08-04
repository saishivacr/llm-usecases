from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.post("/queryllama")
async def query_llama_db_qa(data: QueryInput):

    try:
        query = data.query

        if not query:
            # Raise HTTP 400 Bad Request if data is invalid
            raise HTTPException(status_code=400, detail='Invalid input data')
        else:            
            from utils.retreival_qa import llama_dbqa
            llm_dbqa, llm_gen = llama_dbqa()
            start_time = time.time()
            res_dbqa = llm_dbqa({'query': query})
            res_gen = llm_gen.run(query)
            end_time = time.time()
            
            response = {
                'answer_dbqa': res_dbqa['result'],
                'answer_genqa': res_gen,
                'source_documents': [],
                'time_taken': end_time - start_time
            }

            for document in res_dbqa['source_documents']:
                response['source_documents'].append({
                    'source': document.metadata['source'],
                    'content': document.page_content,
                    'page number': document.metadata['page']
                })

        return response
    except Exception as e:
        error_msg = f"An error occured while getting response, please try again ❌: {e}"
        raise HTTPException(status_code=500, detail=str(error_msg))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
