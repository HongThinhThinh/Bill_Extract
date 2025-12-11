import base64
import json
import logging
from openai import OpenAI
from app.core.config import settings
from app.schemas.bill import BillExtractionResponse

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
            default_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": settings.PROJECT_NAME,
            }
        )

    def extract_bill_data(self, image_bytes: bytes) -> BillExtractionResponse:
        try:
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            prompt = """
            You are an AI specialized in extracting structured data from Vietnamese bank transfer receipts and bills (Vietcombank, Techcombank, MB Bank, BIDV, Momo, ZaloPay, VNPay, etc.).
            
            Extract ALL available information from the image. Return the result as a SINGLE JSON OBJECT (not an array):
            {
                "status": "Transaction status text (e.g., 'Giao dịch thành công', 'Thành công')",
                "amount": 500000.0,
                "currency": "VND",
                "date": "2025-12-09",
                "time": "12:15:00",
                "sender_name": "NGUYEN HONG THINH",
                "receiver_name": "TRAN THI B",
                "receiver_account": "04249300501",
                "receiver_bank": "TP Bank",
                "transaction_id": "12345678901",
                "content": "Transfer description/note",
                "transfer_type": "Chuyển tiền trong ngân hàng",
                "fee": 0,
                "fee_description": "Miễn phí"
            }
            
            Rules:
            - IMPORTANT: Return ONLY a single JSON object, NOT an array/list
            - amount: Extract as number, remove currency symbols and thousand separators
            - date: Convert to YYYY-MM-DD format
            - time: Convert to HH:MM:SS format (24-hour)
            - fee: Return 0 if "Miễn phí" or free, otherwise return the fee amount
            - If sender_name is not explicitly shown, infer from content/description field if possible (e.g., "TRAN GIA BAO chuyen tien" means sender is "TRAN GIA BAO")
            - If a field is not visible or illegible, set it to null
            - Do NOT include markdown formatting like ```json
            """

            response = self.client.chat.completions.create(
                model=settings.OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                response_format={"type": "json_object"} 
            )
            
            content = response.choices[0].message.content
            data = json.loads(content)
            
            # Handle case where LLM returns a list instead of dict
            if isinstance(data, list):
                if len(data) > 0 and isinstance(data[0], dict):
                    data = data[0]  # Take the first item if it's a list of dicts
                else:
                    logger.warning(f"LLM returned a list with unexpected content: {data}")
                    return BillExtractionResponse()  # Return empty response with all nulls
            
            # Handle case where data is not a dict
            if not isinstance(data, dict):
                logger.warning(f"LLM returned unexpected type: {type(data)}")
                return BillExtractionResponse()
            
            return BillExtractionResponse(**data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            return BillExtractionResponse()
        except Exception as e:
            logger.error(f"Error extracting bill data: {e}")
            return BillExtractionResponse()

llm_service = LLMService()
