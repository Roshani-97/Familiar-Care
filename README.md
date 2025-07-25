# Familiar-Care
Familiar Care is an animal healthcare app guiding pet and livestock care.

For the Backend Server:
  1.Navigate to the Backend directory:
    cd Backend
  2.Run the Flask server:
    python simple_server.py
  The backend server will run on:
    http://localhost:5000
  Endpoints available:
    GET /api/health - Health check
    GET /api/encyclopedia/search - Search encyclopedia
    GET /api/encyclopedia/pet - Get specific pet info
    POST /api/chatbot - Chatbot endpoint

For the Frontend Server:
 1.Navigate to the Frontend directory:
  cd Frontend
2.Install dependencies (only needed first time or when dependencies change):
  npm install
3.Start the development server:
  npm run dev
The frontend server will typically run on:
->>http://localhost:5173 (Vite's default port)
You need to run both servers simultaneously in separate terminal windows for the full application to work. The frontend will make API calls to the backend server running on port 5000.


# Familiar Care - Pet Health Assistant

A comprehensive pet health management system that combines AI-powered chatbot assistance, pet encyclopedia, and veterinary clinic locator services.

## 🌟 Features

### 1. AI-Powered Pet Health Chatbot
- **Technology Stack:**
  - Backend: Python, Flask
  - AI Model: Google Gemini Pro
  - Data Processing: Pandas, OpenPyXL
- **Capabilities:**
  - Symptom analysis and preliminary diagnosis
  - General pet health advice
  - Emergency situation guidance
  - Integration with custom ML model for specific conditions

### 2. Pet Encyclopedia
- **Technology Stack:**
  - Backend: Python, Flask
  - Data Storage: JSON
  - Data Processing: Pandas
- **Features:**
  - Comprehensive pet breed information
  - Species-specific care guidelines
  - Health condition database
  - Search functionality for breeds and species

### 3. Veterinary Clinic Locator
- **Technology Stack:**
  - Backend: Python, Flask
  - Geocoding: Geopy
  - Maps API: Google Places API
- **Features:**
  - Location-based veterinary clinic search
  - Distance calculation
  - Clinic ratings and reviews
  - Contact information

### 4. Modern Web Interface
- **Technology Stack:**
  - Frontend: React 18, TypeScript
  - Styling: Tailwind CSS
  - Animation: Framer Motion
  - Routing: React Router
  - Build Tool: Vite
- **Features:**
  - Responsive design
  - Real-time chat interface
  - Interactive maps
  - Smooth animations and transitions

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Navigate to the Backend directory:
   ```bash
   cd Backend
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the backend server:
   ```bash
   python api.py
   ```

### Frontend Setup
1. Navigate to the Frontend directory:
   ```bash
   cd Frontend
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 🔧 Configuration

### Backend Configuration
- API Keys:
  - Google Places API Key
  - Gemini API Key
- Data Files:
  - `encyclopedia_data.json`
  - `DTI dataset chatbot .xlsx`

### Frontend Configuration
- Environment Variables:
  - `VITE_API_URL`: Backend API endpoint (default: http://localhost:5000)

## 📚 API Endpoints

### Health Check
- `GET /api/health`
  - Returns server status

### Chatbot
- `POST /api/chatbot`
  - Accepts user messages
  - Returns AI-generated responses

### Encyclopedia
- `GET /api/encyclopedia/search`
  - Search for pet information
- `GET /api/encyclopedia/pet`
  - Get specific pet details

### Locations
- `GET /api/locations`
  - Find nearby veterinary clinics

## 🛠️ Development

### Backend Development
- Flask debug mode enabled
- Logging configured for development
- CORS enabled for frontend integration

### Frontend Development
- Hot module replacement enabled
- TypeScript strict mode
- ESLint for code quality
- Tailwind CSS for styling

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
