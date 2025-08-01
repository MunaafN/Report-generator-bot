from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from flask_mail import Mail, Message
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from report_generator import ReportGenerator
from email_service import EmailService
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')

mail = Mail(app)
email_service = EmailService(mail)
report_generator = ReportGenerator()

# Store reports in memory (in production, use a database)
reports_db = {}

@app.route('/')
def index():
    """Main page with quiz/survey form"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_report():
    """Generate report from quiz/survey data"""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Extract form data
        student_name = data.get('name', 'Student')
        subject = data.get('subject', 'General')
        
        # Extract scores
        scores = {}
        for key, value in data.items():
            if key.endswith('_score') and value:
                try:
                    scores[key.replace('_score', '')] = int(value)
                except ValueError:
                    return jsonify({'error': f'Invalid score for {key}'}), 400
        
        if not scores:
            return jsonify({'error': 'No valid scores provided'}), 400
        
        # Generate report
        report_data = report_generator.generate_report(student_name, subject, scores)
        
        # Generate PDF
        pdf_path = report_generator.generate_pdf(report_data)
        
        # Store report
        report_id = str(uuid.uuid4())
        reports_db[report_id] = {
            'data': report_data,
            'pdf_path': pdf_path,
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'report_id': report_id,
            'report_data': report_data,
            'message': 'Report generated successfully!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/report/<report_id>')
def view_report(report_id):
    """View generated report"""
    if report_id not in reports_db:
        return jsonify({'error': 'Report not found'}), 404
    
    report_data = reports_db[report_id]['data']
    return render_template('report_view.html', report=report_data)

@app.route('/download/<report_id>')
def download_pdf(report_id):
    """Download PDF report"""
    if report_id not in reports_db:
        return jsonify({'error': 'Report not found'}), 404
    
    pdf_path = reports_db[report_id]['pdf_path']
    if not os.path.exists(pdf_path):
        return jsonify({'error': 'PDF file not found'}), 404
    
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"report_{report_id}.pdf",
        mimetype='application/pdf'
    )

@app.route('/email/<report_id>', methods=['POST'])
def email_report(report_id):
    """Email report to student"""
    if report_id not in reports_db:
        return jsonify({'error': 'Report not found'}), 404
    
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email address required'}), 400
        
        report_data = reports_db[report_id]['data']
        pdf_path = reports_db[report_id]['pdf_path']
        
        success = email_service.send_report_email(email, report_data, pdf_path)
        
        if success:
            return jsonify({'success': True, 'message': 'Report sent successfully!'})
        else:
            return jsonify({'error': 'Failed to send email'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/bulk', methods=['POST'])
def bulk_generate():
    """Generate reports in bulk from CSV data"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Please upload a CSV file'}), 400
        
        # Read CSV and generate reports
        import pandas as pd
        df = pd.read_csv(file)
        
        generated_reports = []
        for _, row in df.iterrows():
            try:
                # Extract scores from CSV columns
                scores = {}
                for col in row.index:
                    if col.endswith('_score') and pd.notna(row[col]):
                        scores[col.replace('_score', '')] = int(row[col])
                
                if scores:
                    student_name = row.get('name', 'Student')
                    subject = row.get('subject', 'General')
                    
                    report_data = report_generator.generate_report(student_name, subject, scores)
                    pdf_path = report_generator.generate_pdf(report_data)
                    
                    report_id = str(uuid.uuid4())
                    reports_db[report_id] = {
                        'data': report_data,
                        'pdf_path': pdf_path,
                        'created_at': datetime.now().isoformat()
                    }
                    
                    generated_reports.append({
                        'student_name': student_name,
                        'report_id': report_id
                    })
                    
            except Exception as e:
                continue
        
        return jsonify({
            'success': True,
            'generated_count': len(generated_reports),
            'reports': generated_reports
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports')
def list_reports():
    """List all generated reports"""
    reports = []
    for report_id, report_info in reports_db.items():
        reports.append({
            'id': report_id,
            'student_name': report_info['data']['student_name'],
            'subject': report_info['data']['subject'],
            'created_at': report_info['created_at']
        })
    
    return jsonify({'reports': reports})

if __name__ == '__main__':
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    os.makedirs('static/charts', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 