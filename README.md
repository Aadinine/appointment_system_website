# Doctor Appointment Booking System

A comprehensive web-based appointment booking system with AI-powered doctor recommendations and real-time availability management.

## 🌟 Features

### 🤖 AI-Powered Doctor Recommendations
- **Multi-AI Support**: Advanced AI integration using Groq Llama 3.3, Google Gemini, and OpenAI GPT models for comprehensive symptom analysis with fallback mechanisms ensuring reliability
- **Smart Matching**: Intelligent patient-to-doctor matching algorithm that considers medical condition severity, geographic proximity, and doctor specialty to provide optimal recommendations
- **Priority Assessment**: Automated triage system that categorizes medical conditions as URGENT (immediate attention needed), ROUTINE (standard consultation), or NORMAL (general checkup) based on AI analysis
- **Distance-Based Sorting**: Geographic optimization using Haversine distance calculations to display doctors in ascending order of proximity, prioritizing convenience for patients
- **Fallback Analysis**: Robust keyword-based analysis system that activates when AI services are unavailable, ensuring continuous functionality with basic medical condition matching
- **Symptom Processing**: Natural language processing engine that interprets patient-described symptoms in plain language and extracts relevant medical information for accurate analysis
- **Recommendation Timeline**: AI-generated consultation timeframe suggestions based on condition urgency, ranging from "within 24 hours" for urgent cases to "within 1-2 weeks" for routine checkups

### 📅 Real-Time Appointment Booking
- **Extended Hours**: Comprehensive scheduling system with 30-minute appointment slots from 9:00 AM to 9:00 PM, maximizing patient convenience and doctor availability
- **Lunch Break Management**: Intelligent scheduling that keeps 12:00 PM available for appointments while automatically skipping 12:30-2:00 PM lunch break, respecting doctor schedules
- **Live Availability**: Real-time status system with four distinct slot states (available/booked/unavailable/past) that update instantly across all connected users
- **Date-Based Scheduling**: Dynamic calendar system that automatically refreshes time slot availability when patients change dates, providing accurate real-time booking options
- **Double Booking Prevention**: Multi-layered server-side validation with race condition protection using database atomic operations to prevent simultaneous bookings of the same slot
- **Smart Time Validation**: Intelligent time filtering that automatically prevents booking of past time slots on the current date while allowing future date bookings
- **Cancellation Integration**: Seamless cancellation system that immediately releases cancelled time slots back to the available pool, enabling instant rebooking
- **Real-Time Updates**: WebSocket-like instant synchronization across all user sessions, ensuring that when one patient books or cancels, all others see updated availability immediately

### 👥 User Management & Dashboard
- **Session-Based Authentication**: Enterprise-grade security system with 24-hour session tokens, automatic session expiration, and secure logout functionality protecting patient data
- **Personal Dashboard**: Comprehensive appointment management interface with separate tabs for upcoming and past appointments, featuring intuitive navigation and professional medical interface design
- **Smart Appointment Classification**: Intelligent categorization algorithm that considers both appointment date and time to accurately classify appointments as upcoming or past, ensuring precise dashboard organization
- **Appointment Cancellation**: One-click cancellation system with confirmation dialogs, instant database updates, and automatic dashboard refresh for seamless user experience
- **Status Management**: Visual status system with color-coded badges (green for confirmed, red for cancelled, gray for completed) providing instant appointment state recognition
- **Auto-Refresh**: Automatic dashboard refresh system that updates the interface immediately after booking or cancellation actions, ensuring users always see current information
- **Clickable Appointment Cards**: Interactive appointment cards with hover effects and click functionality that provide direct access to detailed appointment information and receipts
- **Professional UI**: Medical-grade interface design with proper spacing, professional color scheme, and healthcare-appropriate typography ensuring trust and usability

### 📋 Appointment Management
- **Complete Booking Workflow**: End-to-end appointment system guiding patients from symptom input through AI analysis, doctor selection, time slot booking, to final confirmation with unique appointment ID
- **Professional Receipts**: Detailed appointment information pages with medical-grade formatting, including doctor credentials, hospital information, appointment details, and professional presentation suitable for medical records
- **Calendar Integration**: One-click Google Calendar integration that automatically adds appointment details to patients' personal calendars with reminders and location information
- **Print Functionality**: Browser-optimized print styles that generate professional appointment receipts suitable for medical records and insurance purposes with clean formatting
- **Appointment IDs**: Unique 6-character identification system generated from MongoDB ObjectId using the last 6 characters in uppercase format for easy reference and tracking
- **Specialty Display**: Comprehensive doctor specialty information prominently displayed across all appointment-related pages ensuring patients know their medical specialist's expertise
- **Symptom Recording**: Secure storage of patient-described symptoms linked to appointments, enabling medical history tracking and continuity of care
- **Hospital Information**: Complete hospital details including address, phone number, and location information displayed with appointment details for patient convenience

### 🗺️ Location-Based Services
- **Distance Calculation**: Precise geographic distance calculations using the Haversine formula accounting for Earth's curvature, providing accurate distance measurements between patient and doctor locations
- **Nearby Doctors**: Location-aware doctor recommendation system that sorts and displays medical specialists based on proximity to the patient's specified location (default: Delhi coordinates)
- **Geographic Sorting**: Intelligent distance-based ordering that prioritizes closer doctors first while maintaining quality and specialty relevance in the recommendation algorithm
- **Distance Badges**: Visual distance indicators displayed on doctor cards showing approximate distance in kilometers with color coding (green for nearby, yellow for moderate, red for distant)
- **Location-Based Recommendations**: AI-powered recommendation system that incorporates geographic proximity as a key factor in doctor selection, balancing medical needs with convenience
- **User Location**: Flexible location system with Delhi-based default coordinates (28.6139° N, 77.2090° E) that can be customized for different geographic regions

### ☁️ Cloud Database Integration
- **MongoDB Atlas**: Enterprise-grade cloud database solution providing scalable, secure, and reliable data storage with automatic backups and global distribution capabilities
- **Real-Time Sync**: Instant data synchronization across all connected users ensuring that appointment bookings, cancellations, and updates are immediately reflected system-wide
- **Data Fallback**: Robust local JSON backup system that activates when cloud database is unavailable, ensuring continuous operation and data integrity during connectivity issues
- **Appointment Persistence**: Comprehensive data storage system that maintains complete appointment records including patient information, doctor details, timestamps, and status changes
- **Scalable Architecture**: Cloud-native design supporting multiple concurrent users with automatic scaling capabilities handling peak usage periods without performance degradation
- **Data Consistency**: Atomic database operations with transaction-like consistency ensuring that appointment bookings and cancellations are complete and reliable without data corruption

### 🔒 Security & Authentication
- **Session Management**: Secure session handling with encrypted tokens, automatic expiration after 24 hours, and server-side session validation protecting against unauthorized access
- **User Validation**: Email-based authentication system with secure password storage, user verification, and account management ensuring only authorized patients access their medical data
- **Data Protection**: Healthcare-grade data security with encrypted storage of personal health information (PHI) following medical data protection best practices
- **Input Validation**: Comprehensive server-side validation for all user inputs including symptom descriptions, personal information, and appointment details preventing malicious data injection
- **XSS Protection**: Cross-site scripting prevention with HTML escaping for all user-generated content ensuring safe display of patient-provided information
- **Booking Protection**: Multi-layered security system preventing unauthorized appointment bookings, modifications, or cancellations through ownership verification
- **Ownership Verification**: Strict access control ensuring patients can only view, modify, or cancel their own appointments with no access to other patients' medical information

### 📱 Modern User Experience
- **Responsive Design**: Mobile-first responsive design that seamlessly adapts to desktop, tablet, and mobile devices with optimized layouts and touch-friendly interfaces
- **Interactive UI**: Smooth animations, transitions, and micro-interactions providing professional user experience with loading indicators, progress bars, and visual feedback
- **Error Handling**: Comprehensive error management system with user-friendly error messages, graceful degradation, and recovery options for all system operations
- **Toast Notifications**: Non-intrusive notification system for success messages, errors, and important updates that appear temporarily without disrupting user workflow
- **Confirmation Dialogs**: User confirmation prompts for critical actions like appointment cancellation, ensuring intentional actions and preventing accidental modifications
- **Professional Styling**: Medical-grade interface design with healthcare-appropriate color psychology, clean typography, and professional visual hierarchy
- **Loading Indicators**: Visual feedback systems including spinners, progress bars, and skeleton screens providing clear indication of system processing during operations

### 🏥 Medical Professional Features
- **Doctor Profiles**: Comprehensive medical professional profiles including education, experience, specialties, hospital affiliations, and professional credentials
- **Specialist Directory**: Organized medical specialty directory with 12+ specialties including Cardiology, Dermatology, Neurology, Orthopedics, and more with detailed descriptions
- **Hospital Networks**: Multi-hospital affiliation system displaying all hospitals where doctors practice, including contact information and location details
- **Professional Information**: Detailed doctor qualifications including medical degrees, certifications, years of experience, and specialized training
- **Specialty Categories**: Organized medical specialty categorization system enabling patients to easily find appropriate specialists for their specific medical conditions
- **Availability Status**: Real-time doctor availability indicators showing which doctors are currently accepting new patients and their scheduling availability

### 🎯 Advanced Functionality
- **Real-Time Cancellation**: Instant appointment cancellation system with immediate database updates, availability restoration, and user notification ensuring seamless cancellation experience
- **Smart Time Slot Management**: Intelligent slot management that excludes cancelled appointments from availability calculations while maintaining booking history and audit trails
- **Appointment History**: Complete chronological record of all patient appointments including bookings, cancellations, and status changes with timestamp tracking
- **Status Tracking**: Comprehensive appointment lifecycle management with status tracking through confirmed, cancelled, and completed states with automatic status transitions
- **Timestamp Recording**: Detailed timestamp system recording creation time, cancellation time, and modification times for audit trails and medical record compliance
- **Multi-User Support**: Concurrent user handling with proper session management ensuring multiple patients can use the system simultaneously without conflicts
- **Race Condition Handling**: Advanced database locking and atomic operations preventing simultaneous booking conflicts when multiple users attempt to book the same time slot

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
