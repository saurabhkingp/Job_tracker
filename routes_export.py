from fasthtml.common import *
from app import rt
from database import jobs
from components import df_to_markdown
import pandas as pd
import datetime
from starlette.responses import Response

# Download CSV Export
@rt('/export/csv', methods=['GET'])
def export_csv(sess):
    try:
        user_id = sess.get('auth')
        rows = list(jobs.rows_where("user_id = ?", [user_id]))
        if not rows:
            return Response("No job data to export.", status_code=400)
        
        df = pd.DataFrame(rows)
        df = df[['id', 'company', 'title', 'status', 'date_applied', 'url', 'notes']]
        csv_content = df.to_csv(index=False)
        
        return Response(
            csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=job_applications.csv"}
        )
    except Exception as e:
        return Response(f"CSV Export Error: {str(e)}", status_code=500)

# Download Markdown Summary
@rt('/export/markdown', methods=['GET'])
def export_markdown(sess):
    try:
        user_id = sess.get('auth')
        rows = list(jobs.rows_where("user_id = ?", [user_id]))
        if not rows:
            return Response("No job data to export.", status_code=400)
        
        df = pd.DataFrame(rows)
        df = df[['company', 'title', 'status', 'date_applied', 'url', 'notes']]
        md_table = df_to_markdown(df)
        
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"# Job Applications Report\nGenerated: {date_str}\n\n{md_table}"
        
        return Response(
            report,
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=job_applications_report.md"}
        )
    except Exception as e:
        return Response(f"Markdown Export Error: {str(e)}", status_code=500)
