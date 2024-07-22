from openai import OpenAI
import stock_data as sd
import requests
from pprint import pprint   
import os
from dotenv import load_dotenv


load_dotenv()


client = OpenAI()

def chat_call(context):
    
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=context,
        tools = tools,
        tool_choice="auto",
        temperature=0
    )

tools = [
    {
        "type": "function",
        "function": {
            "name": "make_recommendation",
            "description": "Make recommendation on stock based on sentiment analysis and historical data",
            "parameters": {
                "type": "object",
                "properties": {
                    "market_data": {
                        "type": "object",
                        "description": "Timeseries data for the ticker symbol"
                    },
                    "current_events": {
                        "type": "string",
                        "description": "Collection of news articles related to the stock"
                    },
                    "reccomendation": {
                        "type": "string",
                        "description": "Return 'BUY', 'SELL', or 'HOLD' based on analysis"
                    },
                    "confidence": {
                        "type": "integer",
                        "description": "Confidence level of the recommendation (1 - 10)"
                    },
                    "rationale": {
                        "type": "string",
                        "description": "Explanation for the recommendation; must refer to market_data and current_events"
                    }

                },
                "required": ["reccomendation", "confidence", "rationale"]
            }
        }
    }
]


ticker = "AAPL"

news = sd.get_stock_news("AAPL")


descriptions = [item['description'] for item in news['data']]


data  = sd.get_weekly_stock_data("AAPL")



prompt = f"""Give a recommendation based on the following data:
            - Market data: {data}  
            - Current events: {descriptions}"""

# pprint(prompt)

context = [{"role": "user", "content": prompt}]

response = chat_call(context)

res_data = response.choices[0].message
res_tools = res_data.tool_calls

tool_id = res_tools[0].id
tool_function_name = res_tools[0].function.name
res_args = eval(res_tools[0].function.arguments)

print(tool_id)
print(tool_function_name)
pprint(res_args)
# print(res_args["reccomendation"])
# print(res_args["confidence"])
# print(res_args["rationale"])
