# 📊 Report Generator Bot

A comprehensive academic performance report generator that analyzes quiz scores and survey responses to create detailed 1-page reports highlighting strengths, weaknesses, and improvement areas.

## 🚀 Features

- **📝 Quiz/Survey Input**: Easy-to-use form for entering student scores
- **📊 Performance Analysis**: Automatic categorization of strengths and weaknesses
- **📈 Visual Charts**: Matplotlib-generated performance charts
- **📄 PDF Generation**: Professional PDF reports using WeasyPrint
- **📧 Email Delivery**: Send reports directly to students via email
- **💾 Report Storage**: Store and retrieve generated reports
- **🔄 Bulk Processing**: Generate multiple reports from CSV files

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask**: Lightweight web framework
- **Jinja2**: HTML templating engine
- **WeasyPrint**: PDF generation from HTML
- **Matplotlib**: Data visualization and charts
- **Flask-Mail**: Email functionality

### Frontend
- **HTML5 + CSS3**: Modern, responsive design
- **Bootstrap 5**: UI framework for beautiful interfaces
- **JavaScript**: Interactive functionality
- **Chart.js**: Additional chart capabilities

### Storage
- **In-Memory Storage**: For development (can be replaced with SQLite/PostgreSQL)

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or download the project**
   ```bash
   git clone https://github.com/MunaafN/Report-generator-bot
   cd report-generator-bot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (Optional)
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and go to: `http://localhost:5000`

## 📋 Usage

### 1. Generate Individual Report

1. **Fill out the form**:
   - Enter student name
   - Specify subject/topic
   - Input quiz scores (0-100) for different subjects

2. **Submit the form** to generate the report

3. **View options**:
   - View report in browser
   - Download as PDF
   - Email to student

### 2. Bulk Report Generation

1. **Prepare CSV file** with columns:
   ```
   name,subject,math_score,science_score,english_score,history_score
   John Doe,General,85,92,78,88
   Jane Smith,Science,90,95,82,85
   ```

2. **Upload CSV** using the bulk upload feature

3. **Download all generated reports**

### 3. Email Configuration

To enable email functionality:

1. **Gmail Setup**:
   - Enable 2-factor authentication
   - Generate an App Password
   - Use the App Password in your `.env` file

2. **Other Email Providers**:
   - Update SMTP settings in `app.py`
   - Modify `MAIL_SERVER`, `MAIL_PORT`, etc.

## 📁 Project Structure

```
report-generator-bot/
│
├── app.py                 # Main Flask application
├── report_generator.py    # Core report generation logic
├── email_service.py       # Email functionality
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/            # HTML templates
│   ├── index.html       # Main form page
│   └── report_view.html # Report display page
│
├── reports/             # Generated PDF reports (auto-created)
├── static/             # Static files (CSS, JS, images)
└── .env                # Environment variables (create this)
```

## 🔧 Configuration

### Score Thresholds
Modify the scoring logic in `report_generator.py`:

```python
self.score_thresholds = {
    'excellent': 90,    # 90+ = Excellent
    'good': 80,         # 80-89 = Good
    'average': 70,      # 70-79 = Average
    'below_average': 60, # 60-69 = Below Average
    'needs_improvement': 50 # <50 = Needs Improvement
}
```

### Email Settings
Update email configuration in `app.py`:

```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

## 📊 Report Features

### Generated Reports Include:
- **Student Information**: Name, subject, date
- **Performance Summary**: Average score, grade, total subjects
- **Visual Chart**: Bar chart showing performance by subject
- **Strengths Analysis**: Subjects with scores ≥80%
- **Improvement Areas**: Subjects with scores <80%
- **Professional Layout**: Clean, printable design

### PDF Features:
- **High-quality output** with embedded charts
- **Professional formatting** suitable for printing
- **Responsive design** that works on all devices

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Use a production WSGI server**:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set up a reverse proxy** (nginx/Apache)

3. **Use a proper database** (SQLite/PostgreSQL) instead of in-memory storage

4. **Configure environment variables** for production

## 🔒 Security Considerations

- **Input Validation**: All scores are validated (0-100 range)
- **File Upload Security**: CSV files are validated
- **Email Security**: Use App Passwords for Gmail
- **Environment Variables**: Store sensitive data in `.env` files

## 🐛 Troubleshooting

### Common Issues:

1. **PDF Generation Fails**:
   - Install system dependencies for WeasyPrint
   - On Windows: Install GTK+ runtime
   - On Linux: `sudo apt-get install libcairo2-dev`

2. **Email Not Sending**:
   - Check Gmail App Password setup
   - Verify SMTP settings
   - Check firewall/network settings

3. **Charts Not Displaying**:
   - Ensure matplotlib is properly installed
   - Check for display backend issues

## 📈 Future Enhancements

- [ ] **Database Integration**: SQLite/PostgreSQL for persistent storage
- [ ] **User Authentication**: Login system for teachers/administrators
- [ ] **Advanced Analytics**: Trend analysis, progress tracking
- [ ] **Custom Templates**: Multiple report styles and formats
- [ ] **API Endpoints**: RESTful API for integration
- [ ] **Real-time Updates**: WebSocket support for live updates
- [ ] **Mobile App**: React Native or Flutter mobile application

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact: [your-email@example.com]

---

**Happy Report Generating! 📊✨** 
