import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
from datetime import datetime
from jinja2 import Template
# Use xhtml2pdf instead of weasyprint to avoid GTK+ dependency issues
weasyprint = None

class ReportGenerator:
    def __init__(self):
        self.score_thresholds = {
            'excellent': 90,
            'good': 80,
            'average': 70,
            'below_average': 60,
            'needs_improvement': 50
        }

    def analyze_scores(self, scores):
        strengths = []
        weaknesses = []
        
        for subject, score in scores.items():
            if score >= 80:
                strengths.append({
                    'subject': subject.title(),
                    'score': score
                })
            else:
                weaknesses.append({
                    'subject': subject.title(),
                    'score': score
                })
        
        return strengths, weaknesses

    def generate_chart(self, scores):
        plt.figure(figsize=(10, 6))
        subjects = list(scores.keys())
        score_values = list(scores.values())
        
        colors = ['#28a745' if score >= 80 else '#dc3545' for score in score_values]
        
        bars = plt.bar(subjects, score_values, color=colors, alpha=0.7)
        plt.xlabel('Subjects')
        plt.ylabel('Scores')
        plt.title('Performance Analysis')
        plt.ylim(0, 100)
        
        for bar, score in zip(bars, score_values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    str(score), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        chart_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return chart_base64

    def calculate_overall_performance(self, scores):
        if not scores:
            return {}
        
        average_score = sum(scores.values()) / len(scores)
        
        if average_score >= 90:
            grade = 'A+'
        elif average_score >= 80:
            grade = 'A'
        elif average_score >= 70:
            grade = 'B'
        elif average_score >= 60:
            grade = 'C'
        else:
            grade = 'D'
        
        return {
            'average_score': round(average_score, 1),
            'grade': grade
        }

    def generate_report(self, student_name, subject, scores):
        strengths, weaknesses = self.analyze_scores(scores)
        overall_performance = self.calculate_overall_performance(scores)
        chart_base64 = self.generate_chart(scores)
        
        report_data = {
            'student_name': student_name,
            'subject': subject,
            'scores': scores,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'overall_performance': overall_performance,
            'chart_base64': chart_base64,
            'generated_date': datetime.now().strftime('%B %d, %Y'),
            'report_id': f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        }
        
        return report_data

    def generate_pdf(self, report_data):
        html_template = self.get_html_template()
        template = Template(html_template)
        html_content = template.render(**report_data)
        
        pdf_path = f"reports/report_{report_data['report_id']}.pdf"
        
        try:
            if weasyprint:
                weasyprint.HTML(string=html_content).write_pdf(pdf_path)
            else:
                # Fallback to xhtml2pdf
                from xhtml2pdf import pisa
                with open(pdf_path, 'wb') as pdf_file:
                    pisa_status = pisa.CreatePDF(html_content, pdf_file)
                    if pisa_status.err:
                        raise Exception("PDF generation failed")
        except Exception as e:
            # Final fallback - create simple text file
            txt_path = pdf_path.replace('.pdf', '.txt')
            with open(txt_path, 'w') as f:
                f.write(f"Report for {report_data['student_name']}\n")
                f.write(f"Subject: {report_data['subject']}\n")
                f.write(f"Average Score: {report_data['overall_performance']['average_score']}%\n")
                f.write(f"Grade: {report_data['overall_performance']['grade']}\n")
            return txt_path
        
        return pdf_path

    def get_html_template(self):
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Academic Performance Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .section { margin: 20px 0; }
        .strengths { background: #d4edda; padding: 10px; border-radius: 5px; }
        .weaknesses { background: #f8d7da; padding: 10px; border-radius: 5px; }
        .chart { text-align: center; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Academic Performance Report</h1>
        <p>Generated on {{ generated_date }}</p>
    </div>
    
    <div class="section">
        <h2>Student: {{ student_name }}</h2>
        <h3>Subject: {{ subject }}</h3>
        <p>Average Score: {{ overall_performance.average_score }}%</p>
        <p>Grade: {{ overall_performance.grade }}</p>
    </div>
    
    <div class="chart">
        <h2>Performance Chart</h2>
        <img src="data:image/png;base64,{{ chart_base64 }}" alt="Performance Chart">
    </div>
    
    {% if strengths %}
    <div class="section">
        <h2>Strengths</h2>
        <div class="strengths">
            {% for strength in strengths %}
            <p>{{ strength.subject }}: {{ strength.score }}%</p>
            {% endfor %}
        </div>
    </div>
    {% endif %}
    
    {% if weaknesses %}
    <div class="section">
        <h2>Areas for Improvement</h2>
        <div class="weaknesses">
            {% for weakness in weaknesses %}
            <p>{{ weakness.subject }}: {{ weakness.score }}%</p>
            {% endfor %}
        </div>
    </div>
    {% endif %}
</body>
</html>
        """ 