# Doctor Appointment Booking System

A comprehensive web-based appointment booking system with AI-powered doctor recommendations and real-time availability management.

## 🌟 Features

### 🤖 AI-Powered Doctor Recommendations
- **Multi-AI Support**: Uses Groq, Gemini, and OpenAI for symptom analysis
- **Smart Matching**: Matches patients with nearby doctors based on their condition and location
- **Priority Assessment**: Categorizes appointments as URGENT, ROUTINE, or NORMAL
- **Distance-Based Sorting**: Doctors displayed in ascending order of distance
- **Fallback Analysis**: Keyword-based analysis if AI services fail
- **Symptom Processing**: Natural language processing for medical conditions
- **Recommendation Timeline**: AI provides suggested consultation timeline
- **Medical Category Classification**: Automatic categorization of medical conditions

### 📅 Real-Time Appointment Booking
- **Extended Hours**: 30-minute slots from 9:00 AM to 9:00 PM
- **Lunch Break Management**: 12:00 PM available, 12:30-14:00 skipped
- **Live Availability**: Real-time status updates showing available, booked, unavailable, and past time slots
- **Date-Based Scheduling**: Dynamic time slot updates when changing dates
- **Double Booking Prevention**: Server-side validation with race condition protection
- **Smart Time Validation**: Prevents booking past time slots on current date
- **Time Slot Status**: Visual indicators for available/booked/unavailable/past slots
- **Real-Time Updates**: Instant availability updates across all users
- **Cancellation Integration**: Cancelled slots become immediately available

### 👥 User Management & Dashboard
- **Session-Based Authentication**: Secure user login with session management
- **Personal Dashboard**: View upcoming and past appointments
- **Smart Appointment Classification**: Automatic past/upcoming based on date AND time
- **Clickable Appointment Cards**: Direct access to appointment details
- **Professional UI**: Clean, responsive dashboard with proper spacing
- **Appointment Cancellation**: One-click cancellation with confirmation
- **Status Management**: Clear visual indicators for appointment states
- **Auto-Refresh**: Dashboard updates after actions
- **Tab Navigation**: Organized upcoming/past appointment sections
- **Empty States**: Helpful messages when no appointments exist

### 📋 Appointment Management
- **Complete Booking Workflow**: From symptom input to confirmation
- **Professional Receipts**: Detailed appointment information with unique IDs
- **Calendar Integration**: Add appointments to Google Calendar
- **Print Functionality**: Printable appointment receipts
- **Appointment Bills**: Professional information pages without payment details
- **Appointment IDs**: Unique 6-character IDs generated from ObjectId
- **Specialty Display**: Doctor specialty shown on all appointment pages
- **Symptom Recording**: Patient symptoms saved with appointments
- **Hospital Information**: Complete hospital details displayed
- **Contact Information**: Patient contact details stored securely

### 🗺️ Location-Based Services
- **Distance Calculation**: Haversine formula for accurate distance measurements
- **Nearby Doctors**: Shows doctors sorted by proximity to user's location
- **Hospital Information**: Complete details including address, phone, and availability
- **User Location**: Delhi-based coordinates for distance calculations
- **Geographic Sorting**: Closest doctors displayed first
- **Distance Badges**: Visual distance indicators on doctor cards
- **Location-Based Recommendations**: AI considers proximity in recommendations

### ☁️ Cloud Database Integration
- **MongoDB Atlas**: Cloud-based data storage for scalability
- **Real-Time Sync**: Instant updates across all users
- **Data Fallback**: Local JSON backup for offline functionality
- **Appointment Persistence**: All data stored in cloud database
- **User Data Security**: Encrypted storage of personal information
- **Scalable Architecture**: Handles multiple concurrent users
- **Real-Time Availability**: Live slot availability across all users
- **Data Consistency**: Atomic operations prevent data corruption

### � Security & Authentication
- **Session Management**: Secure 24-hour session tokens
- **User Validation**: Email-based authentication system
- **Data Protection**: Secure storage of personal health information
- **Input Validation**: Server-side validation for all user inputs
- **XSS Protection**: HTML escaping for user-generated content
- **Booking Protection**: Multiple layers prevent double booking
- **Time Validation**: Prevents booking of past time slots
- **Ownership Verification**: Users can only access their own appointments

### �📱 Modern User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Interactive UI**: Smooth animations and transitions
- **Error Handling**: User-friendly error messages and loading indicators
- **Accessibility**: Semantic HTML and ARIA compliance
- **Professional Styling**: Modern, clean interface design
- **Loading Indicators**: Visual feedback during operations
- **Toast Notifications**: Non-intrusive success/error messages
- **Confirmation Dialogs**: User confirmations for critical actions
- **Hover Effects**: Interactive button and card animations
- **Color-Coded Status**: Visual appointment status indicators

### 🏥 Medical Professional Features
- **Doctor Profiles**: Complete doctor information and specialties
- **Specialist Directory**: Browse all available specialists
- **Hospital Networks**: Multiple hospital affiliations displayed
- **Professional Information**: Doctor qualifications and experience
- **Specialty Categories**: Organized by medical specialties
- **Availability Status**: Real-time doctor availability
- **Contact Information**: Hospital phone and address details
- **Professional Photos**: Visual representation of medical staff

### 🎯 Advanced Functionality
- **Real-Time Cancellation**: Instant appointment cancellation with Atlas updates
- **Smart Time Slot Management**: Excludes cancelled appointments from availability
- **Appointment History**: Complete record of all appointments
- **Status Tracking**: Confirmed/Cancelled/Completed status management
- **Timestamp Recording**: Creation and cancellation timestamps
- **Data Integrity**: Consistent appointment categorization
- **Multi-User Support**: Concurrent booking with conflict prevention
- **Race Condition Handling**: Prevents simultaneous booking conflicts

### 📊 Technical Features
- **Flask Web Framework**: Python-based web application
- **AJAX Integration**: Dynamic content updates without page reloads
- **RESTful API**: Clean API endpoints for all operations
- **JSON Responses**: Structured data exchange
- **Error Logging**: Comprehensive error tracking
- **Performance Optimization**: Efficient database queries
- **Modular Architecture**: Clean code organization
- **Environment Configuration**: Secure environment variable management

### 🎨 Design & UI Elements
- **Bootstrap Integration**: Professional CSS framework
- **Custom Styling**: Tailored design system
- **Icon Integration**: Font Awesome icons throughout
- **Card-Based Layout**: Modern card design patterns
- **Responsive Grid**: Flexible layout system
- **Color Psychology**: Medical-appropriate color scheme
- **Typography**: Clean, readable font hierarchy
- **Interactive Elements**: Hover states and transitions
- **Mobile Optimization**: Touch-friendly interface
- **Professional Branding**: Consistent visual identity

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- MongoDB Atlas account
- Google Gemini API key

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

4. **Configure MongoDB Atlas**
   ```bash
   python atlas_setup.py
   ```

5. **Set up sample appointments**
   ```bash
   python setup_appointments.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   Navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables (.env)
```env
GEMINI_API_KEY=your_google_gemini_api_key
ATLAS_CONNECTION_STRING=your_mongodb_atlas_connection_string
```

### MongoDB Atlas Setup
1. Create a free MongoDB Atlas account
2. Create a cluster named "appointment_system"
3. Create a collection named "doctor"
4. Create a collection named "appointments"
5. Add your connection string to `.env`

## 📁 Project Structure

```
appointment-system/
├── app.py                 # Main Flask application with all features
├── atlas_setup.py         # MongoDB Atlas initialization
├── setup_appointments.py  # Sample appointment data
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── data/
│   └── doctors.json       # Doctor data (fallback)
├── static/
│   └── style.css          # Complete application styles
├── templates/
│   ├── index.html         # Home page with AI analysis
│   ├── book.html          # Symptom input form
│   ├── result.html        # AI doctor recommendations
│   ├── specialists.html   # All specialists (horizontal layout)
│   ├── booking.html       # Appointment booking with time slots
│   ├── confirmation.html  # Booking confirmation page
│   ├── appointment_bill.html # Professional appointment receipts
│   ├── dashboard.html     # User dashboard with appointments
│   ├── login.html         # User authentication
│   └── register.html      # User registration
└── flask_session/         # Session storage (auto-generated)
```

## 🎯 Usage Guide

### For Patients
1. **Enter Symptoms**: Describe your medical condition
2. **Get Recommendations**: AI suggests appropriate specialists
3. **Choose Doctor**: Select from nearby available doctors
4. **Book Appointment**: Select date and time slot
5. **Receive Confirmation**: Get appointment details with unique ID

### For Administrators
1. **Manage Doctors**: Update doctor information in MongoDB Atlas
2. **Monitor Appointments**: View booking statistics and availability
3. **System Maintenance**: Use setup scripts for data management

## 🔒 Security Features

- **Input Validation**: Server-side validation for all user inputs
- **SQL Injection Prevention**: Parameterized database queries
- **XSS Protection**: HTML escaping for user-generated content
- **Booking Protection**: Multiple layers prevent double booking
- **Time Validation**: Prevents booking of past time slots

## 🛠️ Technologies Used

### Backend
- **Flask**: Python web framework
- **Google Gemini AI**: Symptom analysis and recommendations
- **MongoDB Atlas**: Cloud database
- **PyMongo**: MongoDB Python driver
- **Python-Dotenv**: Environment variable management

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **JavaScript**: Dynamic interactions and AJAX calls
- **Responsive Design**: Mobile-first approach

### API Integrations
- **Google Gemini AI**: Natural language processing
- **MongoDB Atlas**: Real-time database operations

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
  "description": "Doctor description",
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
  "patient_phone": "Phone Number",
  "appointment_date": "YYYY-MM-DD",
  "time_slot": "HH:MM",
  "symptoms": "Patient symptoms",
  "status": "confirmed",
  "created_at": "ISO_TIMESTAMP"
}
```

## 🔄 API Endpoints

### Web Routes
- `GET /` - Home page with AI symptom analysis
- `GET /specialists` - All specialists with distance (horizontal layout)
- `GET/POST /book` - Symptom analysis and AI recommendations
- `GET /booking/<doctor_id>` - Booking page with time slots
- `POST /confirm_booking` - Process booking and save to database
- `GET /get_time_slots/<doctor_id>/<date>` - Time slots API with real-time status
- `GET /dashboard` - User dashboard with appointments
- `GET/POST /login` - User authentication
- `GET /logout` - User logout
- `GET /register` - User registration
- `GET /appointment_bill/<appointment_id>` - Professional appointment receipt

### User Management Routes
- `POST /register` - Create new user account
- `POST /login` - Authenticate user and create session
- Session management with 24-hour expiry

### API Responses
```json
{
  "time_slots": [
    {
      "time": "09:00",
      "available": false,
      "status": "booked"
    },
    {
      "time": "09:30",
      "available": true,
      "status": "available"
    },
    {
      "time": "11:30",
      "available": false,
      "status": "past"
    }
  ]
}
```

## 🧪 Testing

### Manual Testing
1. **Booking Flow**: Test complete appointment booking process
2. **Date Changes**: Verify dynamic time slot updates
3. **Double Booking**: Attempt to book same slot twice
4. **Past Times**: Try booking past time slots
5. **Mobile View**: Test responsive design

### Sample Data
Use `setup_appointments.py` to create sample appointments for testing:
```bash
python setup_appointments.py
```

## 🚀 Deployment

### Production Setup
1. **Environment Variables**: Set production values in `.env`
2. **Database**: Use MongoDB Atlas production cluster
3. **Web Server**: Use Gunicorn or similar WSGI server
4. **HTTPS**: Configure SSL certificate
5. **Domain**: Point custom domain to application

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Create an issue on GitHub
4. Contact the development team

## 🔄 Version History

- **v2.0.0** - Complete production-ready system with user authentication
  - Added user login/registration system with session management
  - Professional dashboard with appointment management
  - Multi-AI support (Groq, Gemini, OpenAI)
  - Extended hours (9 AM - 9 PM) with 12:00 PM slot
  - Distance-based doctor sorting
  - Appointment receipts and calendar integration
  - Double booking prevention with race condition protection
  - Smart time validation (date + time)
  - Professional UI/UX improvements

- **v1.0.0** - Initial release with basic booking system
  - AI-powered symptom analysis
  - Basic appointment booking
  - MongoDB Atlas integration
  - Distance calculations

- **Future versions** may include:
  - Email notifications
  - Payment processing
  - Telemedicine features
  - Mobile app development

## 📈 Performance

- **Response Time**: < 500ms for most operations
- **Database Queries**: Optimized indexes for fast lookups
- **Caching**: Browser caching for static assets
- **CDN Ready**: Static assets can be served via CDN

## 🔮 Future Enhancements

- **User Authentication**: Patient and doctor login system
- **Email Notifications**: Automated appointment reminders
- **Video Consultation**: Telemedicine integration
- **Payment Processing**: Online payment integration
- **Analytics**: Dashboard for appointment statistics
- **Mobile App**: Native iOS and Android applications
- **Multi-Language**: Support for multiple languages
- **API Versioning**: RESTful API for third-party integration
