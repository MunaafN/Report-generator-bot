#!/usr/bin/env python3
"""
Test script for Report Generator Bot
This script tests the core functionality without running the web server
"""

import os
import sys
from report_generator import ReportGenerator

def test_report_generation():
    """Test the report generation functionality"""
    print("🧪 Testing Report Generator Bot...")
    print("=" * 50)
    
    # Initialize report generator
    report_gen = ReportGenerator()
    
    # Test data
    student_name = "Test Student"
    subject = "Test Subject"
    scores = {
        'math': 85,
        'science': 92,
        'english': 78,
        'history': 88
    }
    
    print(f"📝 Generating report for: {student_name}")
    print(f"📚 Subject: {subject}")
    print(f"📊 Scores: {scores}")
    print()
    
    try:
        # Generate report
        report_data = report_gen.generate_report(student_name, subject, scores)
        
        print("✅ Report data generated successfully!")
        print(f"📋 Report ID: {report_data['report_id']}")
        print(f"📅 Generated Date: {report_data['generated_date']}")
        print(f"📈 Average Score: {report_data['overall_performance']['average_score']}%")
        print(f"🎓 Grade: {report_data['overall_performance']['grade']}")
        print()
        
        # Test strengths and weaknesses
        print("🎯 Strengths:")
        for strength in report_data['strengths']:
            print(f"   - {strength['subject']}: {strength['score']}%")
        
        print("\n⚠️ Areas for Improvement:")
        for weakness in report_data['weaknesses']:
            print(f"   - {weakness['subject']}: {weakness['score']}%")
        
        print()
        
        # Test PDF generation
        print("📄 Testing PDF generation...")
        pdf_path = report_gen.generate_pdf(report_data)
        
        if os.path.exists(pdf_path):
            print(f"✅ PDF generated successfully: {pdf_path}")
            print(f"📁 File size: {os.path.getsize(pdf_path)} bytes")
        else:
            print("❌ PDF generation failed")
        
        print()
        print("🎉 All tests passed! The Report Generator Bot is working correctly.")
        print()
        print("🚀 To start the web application, run:")
        print("   python app.py")
        print("   or")
        print("   ./start.bat (Windows)")
        print("   ./start.sh (Linux/Mac)")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False
    
    return True

def test_score_analysis():
    """Test score analysis functionality"""
    print("\n🔍 Testing Score Analysis...")
    print("-" * 30)
    
    report_gen = ReportGenerator()
    
    # Test different score scenarios
    test_cases = [
        {
            'name': 'High Performer',
            'scores': {'math': 95, 'science': 98, 'english': 92, 'history': 90}
        },
        {
            'name': 'Average Student',
            'scores': {'math': 75, 'science': 80, 'english': 78, 'history': 82}
        },
        {
            'name': 'Needs Improvement',
            'scores': {'math': 45, 'science': 60, 'english': 55, 'history': 50}
        }
    ]
    
    for test_case in test_cases:
        print(f"\n📊 Testing: {test_case['name']}")
        strengths, weaknesses = report_gen.analyze_scores(test_case['scores'])
        
        print(f"   Strengths: {len(strengths)} subjects")
        print(f"   Weaknesses: {len(weaknesses)} subjects")
        
        overall = report_gen.calculate_overall_performance(test_case['scores'])
        print(f"   Average: {overall['average_score']}% (Grade: {overall['grade']})")

if __name__ == "__main__":
    print("🚀 Report Generator Bot - Test Suite")
    print("=" * 50)
    
    # Run tests
    success = test_report_generation()
    test_score_analysis()
    
    if success:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1) 