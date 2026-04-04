# Doctor Appointment Booking System

A comprehensive web-based appointment booking system with AI-powered doctor recommendations and real-time availability management.

## 🌟 Features

### 🤖 AI-Powered Doctor Recommendations
- **Multi-AI Support**: Uses Groq, Gemini, and OpenAI for symptom analysis
- **Smart Matching**: Matches patients with nearby doctors based on condition and location
- **Priority Assessment**: Categorizes appointments as URGENT, ROUTINE, or NORMAL
- **Distance-Based Sorting**: Doctors displayed in ascending order of distance
- **Fallback Analysis**: Keyword-based analysis if AI services fail
- **Symptom Processing**: Natural language processing for medical conditions
- **Recommendation Timeline**: AI provides suggested consultation timeline

### 📅 Real-Time Appointment Booking
- **Extended Hours**: 30-minute slots from 9:00 AM to 9:00 PM
- **Lunch Break Management**: 12:00 PM available, 12:30-14:00 skipped
- **Live Availability**: Real-time status updates (available/booked/unavailable/past)
- **Date-Based Scheduling**: Dynamic time slot updates when changing dates
- **Double Booking Prevention**: Server-side validation with race condition protection
- **Smart Time Validation**: Prevents booking past time slots on current date
- **Cancellation Integration**: Cancelled slots become immediately available
- **Real-Time Updates**: Instant availability updates across all users

### 👥 User Management & Dashboard
- **Session-Based Authentication**: Secure user login with session management
- **Personal Dashboard**: View upcoming and past appointments
- **Smart Appointment Classification**: Automatic past/upcoming based on date AND time
- **Appointment Cancellation**: One-click cancellation with confirmation
- **Status Management**: Clear visual indicators (Confirmed/Cancelled/Completed)
- **Auto-Refresh**: Dashboard updates after actions
- **Clickable Appointment Cards**: Direct access to appointment details
- **Professional UI**: Clean, responsive dashboard with proper spacing

### 📋 Appointment Management
- **Complete Booking Workflow**: From symptom input to confirmation
- **Professional Receipts**: Detailed appointment information with unique IDs
- **Calendar Integration**: Add appointments to Google Calendar
- **Print Functionality**: Printable appointment receipts
- **Appointment IDs**: Unique 6-character IDs generated from ObjectId
- **Specialty Display**: Doctor specialty shown on all appointment pages
- **Symptom Recording**: Patient symptoms saved with appointments
- **Hospital Information**: Complete hospital details displayed

### 🗺️ Location-Based Services
- **Distance Calculation**: Haversine formula for accurate measurements
- **Nearby Doctors**: Shows doctors sorted by proximity to user's location
- **Geographic Sorting**: Closest doctors displayed first
- **Distance Badges**: Visual distance indicators on doctor cards
- **Location-Based Recommendations**: AI considers proximity in recommendations
- **User Location**: Delhi-based coordinates for distance calculations

### ☁️ Cloud Database Integration
- **MongoDB Atlas**: Cloud-based data storage for scalability
- **Real-Time Sync**: Instant updates across all users
- **Data Fallback**: Local JSON backup for offline functionality
- **Appointment Persistence**: All data stored in cloud database
- **Scalable Architecture**: Handles multiple concurrent users
- **Data Consistency**: Atomic operations prevent data corruption

### 🔒 Security & Authentication
- **Session Management**: Secure 24-hour session tokens
- **User Validation**: Email-based authentication system
- **Data Protection**: Secure storage of personal health information
- **Input Validation**: Server-side validation for all user inputs
- **XSS Protection**: HTML escaping for user-generated content
- **Booking Protection**: Multiple layers prevent double booking
- **Ownership Verification**: Users can only access their own appointments

### 📱 Modern User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Interactive UI**: Smooth animations and transitions
- **Error Handling**: User-friendly error messages and loading indicators
- **Toast Notifications**: Non-intrusive success/error messages
- **Confirmation Dialogs**: User confirmations for critical actions
- **Professional Styling**: Modern, clean interface design
- **Loading Indicators**: Visual feedback during operations

### 🏥 Medical Professional Features
- **Doctor Profiles**: Complete doctor information and specialties
- **Specialist Directory**: Browse all available specialists
- **Hospital Networks**: Multiple hospital affiliations displayed
- **Professional Information**: Doctor qualifications and experience
- **Specialty Categories**: Organized by medical specialties
- **Availability Status**: Real-time doctor availability

### 🎯 Advanced Functionality
- **Real-Time Cancellation**: Instant appointment cancellation with Atlas updates
- **Smart Time Slot Management**: Excludes cancelled appointments from availability
- **Appointment History**: Complete record of all appointments
- **Status Tracking**: Confirmed/Cancelled/Completed status management
- **Timestamp Recording**: Creation and cancellation timestamps
- **Multi-User Support**: Concurrent booking with conflict prevention
- **Race Condition Handling**: Prevents simultaneous booking conflicts

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MongoDB Atlas account
- AI API keys (Groq, Gemini, OpenAI)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aadinine/appointment_system_website.git
   cd appointment_system_website
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables (.env)
```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
ATLAS_CONNECTION_STRING=your_mongodb_atlas_connection_string
```

### MongoDB Atlas Setup
1. Create a free MongoDB Atlas account
2. Create a cluster named "appointment_system"
3. Create collections: "doctor" and "appointments"
4. Add your connection string to `.env`

## 📁 Project Structure

```
appointment-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment configuration
├── .env                  # Environment variables
├── data/
│   └── doctors.json      # Doctor data (fallback)
├── static/
│   └── style.css         # Application styles
├── templates/
│   ├── index.html        # Home page with AI analysis
│   ├── book.html         # Symptom input form
│   ├── result.html       # AI doctor recommendations
│   ├── specialists.html  # All specialists
│   ├── booking.html      # Appointment booking
│   ├── confirmation.html # Booking confirmation
│   ├── appointment_bill.html # Appointment receipts
│   ├── dashboard.html    # User dashboard
│   ├── login.html        # User authentication
│   └── register.html     # User registration
└── flask_session/        # Session storage (auto-generated)
```

## 🎯 Usage Guide

### For Patients
1. **Register/Login**: Create account or login with email
2. **Enter Symptoms**: Describe your medical condition
3. **Get Recommendations**: AI suggests appropriate specialists
4. **Choose Doctor**: Select from nearby available doctors
5. **Book Appointment**: Select date and time slot
6. **Manage Appointments**: View, cancel, or get appointment details

### Key Features
- **AI Analysis**: Multi-AI symptom analysis with priority assessment
- **Real-Time Booking**: Live availability with instant updates
- **Smart Dashboard**: Organized appointment management
- **Location-Based**: Find nearest doctors with distance calculations
- **Professional Receipts**: Detailed appointment information
- **Cancellation**: One-click cancellation with immediate updates

## 🛠️ Technologies Used

### Backend
- **Flask**: Python web framework
- **MongoDB Atlas**: Cloud database
- **Multi-AI Integration**: Groq, Gemini, OpenAI
- **Session Management**: Flask-Session

### Frontend
- **HTML5/CSS3**: Modern styling with animations
- **JavaScript**: Dynamic interactions and AJAX calls
- **Bootstrap**: Professional UI framework
- **Font Awesome**: Icon integration

### API Integrations
- **Groq AI**: Llama model for symptom analysis
- **Google Gemini AI**: Medical recommendations
- **OpenAI**: GPT model for analysis
- **MongoDB Atlas**: Real-time database operations

## 🔄 API Endpoints

### Main Routes
- `GET /` - Home page with AI symptom analysis
- `GET/POST /book` - Symptom analysis and AI recommendations
- `GET /booking/<doctor_id>` - Booking page with time slots
- `POST /confirm_booking` - Process booking
- `GET /get_time_slots/<doctor_id>/<date>` - Time slots API
- `GET /dashboard` - User dashboard
- `POST /cancel_appointment/<id>` - Cancel appointment
- `GET /appointment_bill/<id>` - Appointment receipt
- `GET /health` - Health check for deployment

### User Management
- `GET/POST /login` - User authentication
- `GET/POST /register` - User registration
- `GET /logout` - User logout

## 🚀 Deployment

### Railway Deployment
1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy - Railway will automatically detect the Flask app
4. Health check endpoint: `/health`

### Environment Variables Required
- `GROQ_API_KEY`
- `GEMINI_API_KEY` 
- `OPENAI_API_KEY`
- `ATLAS_CONNECTION_STRING`

## 📊 Database Schema

### Doctors Collection
```javascript
{
  "_id": ObjectId,
  "name": "Dr. Name",
  "specialty": "Medical Specialty",
  "hospital": "Hospital Name",
  "location": {
    "address": "Full Address",
    "lat": latitude,
    "lng": longitude,
    "phone": "Phone Number"
  },
  "conditions": ["condition1", "condition2"],
  "available": true
}
```

### Appointments Collection
```javascript
{
  "_id": ObjectId,
  "appointment_id": "UNIQUE_ID",
  "doctor_id": "doctor_object_id",
  "doctor_name": "Dr. Name",
  "hospital": "Hospital Name",
  "specialty": "Medical Specialty",
  "patient_name": "Patient Name",
  "patient_email": "email@example.com",
  "appointment_date": "YYYY-MM-DD",
  "time_slot": "HH:MM",
  "symptoms": "Patient symptoms",
  "status": "confirmed/cancelled",
  "created_at": "ISO_TIMESTAMP",
  "cancelled_at": "ISO_TIMESTAMP"
}
```

## 🔄 Version History

- **v2.0.0** - Complete production-ready system
  - User authentication and dashboard
  - Multi-AI support (Groq, Gemini, OpenAI)
  - Real-time appointment booking and cancellation
  - Location-based doctor recommendations
  - Professional UI/UX with responsive design
  - Railway deployment ready

- **v1.0.0** - Initial release
  - Basic appointment booking
  - AI-powered symptom analysis
  - MongoDB Atlas integration

## 📝 License

This project is licensed under the MIT License.

## 🔗 Repository

https://github.com/Aadinine/appointment_system_website
