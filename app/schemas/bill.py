from pydantic import BaseModel, Field
from typing import Optional

class BillExtractionResponse(BaseModel):
    # Transaction status
    status: Optional[str] = Field(None, description="Transaction status (e.g., 'Giao dịch thành công', 'Thành công', 'Success')")
    
    # Amount and currency
    amount: Optional[float] = Field(None, description="The total amount of money transferred")
    currency: Optional[str] = Field(None, description="Currency code (e.g., 'VND', 'USD')")
    
    # Date and time
    date: Optional[str] = Field(None, description="The date of the transaction in YYYY-MM-DD format")
    time: Optional[str] = Field(None, description="The time of the transaction in HH:MM:SS format")
    
    # Sender information
    sender_name: Optional[str] = Field(None, description="Name of the sender")
    
    # Receiver information
    receiver_name: Optional[str] = Field(None, description="Name of the receiver")
    receiver_account: Optional[str] = Field(None, description="Account number of the receiver")
    receiver_bank: Optional[str] = Field(None, description="Bank name of the receiver")
    
    # Transaction details
    transaction_id: Optional[str] = Field(None, description="Transaction ID or reference code (Mã giao dịch)")
    content: Optional[str] = Field(None, description="Transfer content/description (Nội dung chuyển tiền)")
    transfer_type: Optional[str] = Field(None, description="Type of transfer (e.g., 'Chuyển tiền trong ngân hàng', 'Chuyển tiền liên ngân hàng')")
    
    # Fees
    fee: Optional[float] = Field(None, description="Transfer fee amount (0 if free)")
    fee_description: Optional[str] = Field(None, description="Fee description (e.g., 'Miễn phí', 'Free')")

class ErrorResponse(BaseModel):
    detail: str
