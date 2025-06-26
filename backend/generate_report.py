from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(37, 99, 235)
        self.cell(0, 10, 'FreelanceScope Project Report', ln=True, align='C')
        self.ln(4)
    def section_title(self, title):
        self.set_font('Arial', 'B', 13)
        self.set_text_color(33, 37, 41)
        self.cell(0, 8, title, ln=True)
        self.ln(1)
    def section_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(55, 65, 81)
        self.multi_cell(0, 7, body)
        self.ln(2)

def main():
    pdf = PDF()
    pdf.add_page()

    # Project Overview
    pdf.section_title('Project Overview')
    pdf.section_body('FreelanceScope is a professional data analysis dashboard for freelancer earnings and performance, built with a React frontend and a Flask backend. The dashboard visualizes and analyzes freelancer data, providing insights into hourly rates, earnings trends, skill-based earnings, job success scores, and forecasted earnings.')

    # Architecture
    pdf.section_title('Architecture')
    pdf.section_body('Backend (Flask):\n- Location: backend/app.py, backend/utils.py\n- Data Source: freelancer_earnings_bd.csv\n- API Endpoints: /api/earnings-summary, /api/hourly-rate-distribution, /api/earnings-trend, /api/skill-earnings, /api/job-success-scores, /api/forecast-earnings, /api/skills\n\nFrontend (React):\n- Location: frontend/src/App.js and related files\n- UI Libraries: Recharts for charts, react-icons for icons\n- Design: Modern, responsive, and themeable (light/dark mode)\n- Main Features: Sidebar navigation, header, dashboard screens for all analyses, search bar, theme toggle, responsive design')

    # Features
    pdf.section_title('Main Features')
    pdf.section_body('- Sidebar Navigation: Vertical, fixed sidebar with icons and section names\n- Header: Fixed top header with branding, search bar, and theme toggle\n- Dashboard Screens: Hourly Rate Distribution, Earnings Trend, Earnings by Skill, Job Success Scores, Forecasted Earnings\n- Search Bar: Filters data on the current screen\n- Theme Toggle: Switch between dark and light mode\n- Responsiveness and Accessibility: Layout adapts to different screen sizes, keyboard accessible')

    # Recent Enhancements
    pdf.section_title('Recent Enhancements')
    pdf.section_body('1. Modern UI/UX Redesign\n2. Per-Skill and Per-Platform Analysis\n3. Search Functionality\n4. Theme Toggle\n5. Responsiveness and Accessibility')

    # User Flow
    pdf.section_title('How It Works (User Flow)')
    pdf.section_body('1. Navigation: Use the sidebar to switch between dashboard sections\n2. Filtering: Use dropdowns to filter by skill or platform\n3. Searching: Use the search bar in the header\n4. Theme: Toggle between dark and light mode\n5. Visualization: View interactive charts and summary statistics')

    # Technologies Used
    pdf.section_title('Technologies Used')
    pdf.section_body('- Frontend: React, Recharts, react-icons, CSS-in-JS\n- Backend: Flask, pandas, scikit-learn, CSV data\n- Other: Modern ES6+ JavaScript, responsive design, RESTful API')

    # Summary
    pdf.section_title('Summary')
    pdf.section_body('FreelanceScope is a feature-rich, professional dashboard for analyzing freelancer data. It provides interactive, filterable, and visually appealing insights into earnings, skills, and performance, with a modern and accessible user interface. All recent changes have focused on improving usability, interactivity, and visual consistency, making the dashboard both powerful and user-friendly.')

    pdf.output('FreelanceScope_Project_Report.pdf')

if __name__ == '__main__':
    main() 