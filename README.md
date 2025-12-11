# 🧾 Bill Extractor API

A high-performance FastAPI service that extracts structured data from Vietnamese bank transfer receipts and bills using AI (OpenRouter/Gemini).

## ✨ Features

- 🖼️ **Image Processing**: Extract data from bill images (JPG, PNG, etc.)
- 🏦 **Multi-Bank Support**: Vietcombank, Techcombank, MB Bank, BIDV, Momo, ZaloPay, VNPay, and more
- 🤖 **AI-Powered**: Uses Google Gemini 2.0 Flash via OpenRouter for accurate extraction
- 📊 **Structured Output**: Returns clean JSON with all transaction details
- 🐳 **Docker Ready**: Easy deployment with Docker Compose

## 📋 Extracted Fields

| Field | Description |
|-------|-------------|
| `status` | Transaction status (e.g., "Giao dịch thành công") |
| `amount` | Transaction amount (number) |
| `currency` | Currency code (e.g., "VND") |
| `date` | Transaction date (YYYY-MM-DD) |
| `time` | Transaction time (HH:MM:SS) |
| `sender_name` | Name of the sender |
| `receiver_name` | Name of the receiver |
| `receiver_account` | Receiver's account number |
| `receiver_bank` | Receiver's bank name |
| `transaction_id` | Transaction reference code |
| `content` | Transfer description/note |
| `transfer_type` | Type of transfer |
| `fee` | Transfer fee (0 if free) |
| `fee_description` | Fee description (e.g., "Miễn phí") |

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenRouter API Key ([Get one here](https://openrouter.ai/))

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd BIll_Extract
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Open API docs**
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📡 API Usage

### Extract Bill Data

**Endpoint:** `POST /api/v1/extract`

**Request:**
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_bill.jpg;type=image/jpeg'
```

**Response:**
```json
{
  "status": "Giao dịch thành công",
  "amount": 500000.0,
  "currency": "VND",
  "date": "2025-12-09",
  "time": "12:15:00",
  "sender_name": "NGUYEN HONG THINH",
  "receiver_name": "LUU HOANG PHUONG",
  "receiver_account": "1051637718",
  "receiver_bank": "Vietcombank",
  "transaction_id": "12067338631",
  "content": "NGUYEN HONG THINH chuyen tien",
  "transfer_type": "Chuyển tiền trong Vietcombank",
  "fee": 0,
  "fee_description": "Miễn phí"
}
```

## 📁 Project Structure

```
BIll_Extract/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── extract.py    # API endpoint
│   ├── core/
│   │   └── config.py             # Configuration
│   ├── schemas/
│   │   └── bill.py               # Pydantic models
│   ├── services/
│   │   └── llm_service.py        # LLM integration
│   └── main.py                   # FastAPI app
├── .env.example                  # Environment template
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## ⚙️ Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | ✅ Yes |
| `OPENROUTER_MODEL` | AI model to use (default: `google/gemini-2.0-flash-001`) | No |
| `PROJECT_NAME` | Project name for API docs | No |

## 🔧 Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- BMP
- WebP

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
