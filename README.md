# Doctor Appointment Booking System

A comprehensive web-based appointment booking system with AI-powered doctor recommendations and real-time availability management.

## 🌟 Features

### 🤖 AI-Powered Doctor Recommendations
- **Symptom Analysis**: Uses Google Gemini AI to analyze symptoms and recommend appropriate medical specialties
- **Smart Matching**: Matches patients with nearby doctors based on their condition and location
- **Priority Assessment**: Categorizes appointments as URGENT, ROUTINE, or NORMAL

### 📅 Real-Time Appointment Booking
- **Time Slot Management**: 30-minute slots from 9:00 AM to 5:00 PM
- **Live Availability**: Real-time status updates showing available, booked, and past time slots
- **Date-Based Scheduling**: Dynamic time slot updates when changing dates
- **Double Booking Prevention**: Server-side validation prevents duplicate appointments

### 🗺️ Location-Based Services
- **Distance Calculation**: Haversine formula for accurate distance measurements
- **Nearby Doctors**: Shows doctors sorted by proximity to user's location
- **Hospital Information**: Complete details including address, phone, and availability

### ☁️ Cloud Database Integration
- **MongoDB Atlas**: Cloud-based data storage for scalability
- **Real-Time Sync**: Instant updates across all users
- **Data Fallback**: Local JSON backup for offline functionality

### 📱 Modern User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Interactive UI**: Smooth animations and transitions
- **Error Handling**: User-friendly error messages and loading indicators
- **Accessibility**: Semantic HTML and ARIA compliance

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
├── app.py                 # Main Flask application
├── atlas_setup.py         # MongoDB Atlas initialization
├── setup_appointments.py  # Sample appointment data
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── data/
│   └── doctors.json       # Doctor data (fallback)
├── static/
│   └── style.css          # Application styles
└── templates/
    ├── index.html         # Home page
    ├── book.html          # Symptom input
    ├── result.html        # Doctor recommendations
    ├── specialists.html   # All specialists
    ├── booking.html       # Appointment booking
    ├── confirmation.html  # Booking confirmation
    └── booking_error.html # Booking error page
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
- `GET /` - Home page
- `GET /specialists` - All specialists with distance
- `GET/POST /book` - Symptom analysis
- `GET /booking/<doctor_id>` - Booking page
- `POST /confirm_booking` - Process booking
- `GET /get_time_slots/<doctor_id>/<date>` - Time slots API

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

- **v1.0.0** - Initial release with complete booking system
- Future versions will include:
  - User authentication
  - Email notifications
  - Calendar integration
  - Payment processing
  - Telemedicine features

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
