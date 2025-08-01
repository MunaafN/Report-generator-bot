from flask_mail import Message
import os

class EmailService:
    def __init__(self, mail):
        self.mail = mail

    def send_report_email(self, email, report_data, pdf_path):
        """Send report via email"""
        try:
            subject = f"Academic Performance Report - {report_data['student_name']}"
            
            body = f"""
Dear {report_data['student_name']},

Your academic performance report has been generated and is attached to this email.

Summary:
- Average Score: {report_data['overall_performance']['average_score']}%
- Grade: {report_data['overall_performance']['grade']}
- Subject: {report_data['subject']}

Please review the attached PDF for detailed analysis including:
- Performance breakdown by subject
- Strengths and areas for improvement
- Visual performance chart

Best regards,
Report Generator Bot
            """
            
            msg = Message(
                subject=subject,
                sender=os.environ.get('MAIL_USERNAME', 'noreply@example.com'),
                recipients=[email],
                body=body
            )
            
            # Attach PDF
            with open(pdf_path, 'rb') as pdf_file:
                msg.attach(
                    filename=f"report_{report_data['report_id']}.pdf",
                    content_type='application/pdf',
                    data=pdf_file.read()
                )
            
            self.mail.send(msg)
            return True
            
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            return False 