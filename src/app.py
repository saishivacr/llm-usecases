from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.retreival_qa import llama_dbqa
import time

llama_dbqa = llama_dbqa()

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
            start_time = time.time()
            res = llama_dbqa({'query': query})
            end_time = time.time()
            
            response = {
                'answer': res['result'],
                'source_documents': [],
                'time_taken': end_time - start_time
            }

            for document in res['source_documents']:
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
