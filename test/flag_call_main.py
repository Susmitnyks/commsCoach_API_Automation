import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from email.utils import formataddr
from idlelib.iomenu import errors

import pyodbc
from flag_call_dict import final_method,initialize_db
def final_dict():
    conn = initialize_db()
    cursor = conn.cursor()
    flag_details = final_method(cursor)
    return flag_details

# def test_demo_mail():
#     flag_Details_mail = final_dict()
#     print(flag_Details_mail)
def test_send_mail():
    formattedys_date = (datetime.today() - timedelta(days=1)).strftime("%d/%m/%Y")
    flag_Details_mail=final_dict()
    link = "https://gbr01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1M8KTD5LfP18C-d5MQAMZr-WEcYGxoBKb%2Fedit%3Fusp%3Dsharing%26ouid%3D115835696802054521040%26rtpof%3Dtrue%26sd%3Dtrue&data=05%7C02%7CSusmit.Surwade%40blenheimchalcot.com%7Cccfa0a7ebc1248ee8f7008dc911a73e7%7Cdd5343bdf2c44f9b81788dfb6445911b%7C0%7C0%7C638544789997848179%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=nFzDTtTzIKQk%2FOebu1FjnGNoVv4e4jKwQvCkG6lImPU%3D&reserved=0"
    # Variables
    total_calls_processed =flag_Details_mail['files_count']
    total_flagged_calls =flag_Details_mail['total_flags_count']
    flagged_calls_percentage = round((total_flagged_calls / total_calls_processed) * 100, 1)
    vulnerability_identified = flag_Details_mail['Vulnerability']
    vulnerability_percentage = round((vulnerability_identified / total_calls_processed) * 100, 1)
    failed_texas = flag_Details_mail['TEXAS Incomplete']
    failed_texas_percentage = round((failed_texas / vulnerability_identified) * 100, 1)
    unrecognized_complaints = flag_Details_mail['Unrecognised Complaint']
    unrecognized_complaints_percentage = round((unrecognized_complaints / total_calls_processed) * 100, 1)
    poor_outcome = flag_Details_mail['Poor Outcome']
    poor_outcome_percentage = round((poor_outcome / total_calls_processed) * 100, 1)
    dpa_failed = flag_Details_mail['DPA Check']
    dpa_failed_percentage = round((dpa_failed / total_calls_processed) * 100, 1)
    profanity = flag_Details_mail['Profanity']
    profanity_percentage = round((profanity / total_calls_processed) * 100, 1)
    thank_fail = flag_Details_mail['Vulnerability - Thank']
    thank_fail_percentage = round((thank_fail / failed_texas) * 100, 1)
    explain_fail = flag_Details_mail['Vulnerability - Explain']
    explain_fail_percentage = round((explain_fail / failed_texas) * 100, 1)
    explicit_consent_fail = flag_Details_mail['Vulnerability - Explicit consent']
    explicit_consent_fail_percentage = round((explicit_consent_fail / failed_texas) * 100, 1)
    ask_fail = flag_Details_mail['Vulnerability - Ask']
    ask_fail_percentage = round((ask_fail/failed_texas)*100,1)
    signpost_fail = flag_Details_mail['Vulnerability - Signpost']
    signpost_fail_percentage = round((signpost_fail / failed_texas) * 100, 1)

    # AWS SMTP credentials
    smtp_username = 'AKIA5YBB6OJ66G2MXV7B'
    smtp_password = 'BMX8OsOi7Gy4OLgEsaKvyICJQbDOYv8XVEHtE2DGcLIE'
    smtp_hostname = 'email-smtp.eu-west-1.amazonaws.com'
    smtp_port = 587  # Adjust the port if necessary

    # Sender and recipient email addresses
    sender_email = 'no-reply@mail.englishscore.com'
    # Recipient email address
    recipient_emails = ["susmit.surwade@blenheimchalcot.com","rinkesh.das@blenheimchalcot.com","ami.jambusaria@blenheimchalcot.com","satyendra.kumar@blenheimchalcot.com","akshay.rahul@blenheimchalcot.com"]
    #recipient_emails = ["susmit.surwade@blenheimchalcot.com","akshay.rahul@blenheimchalcot.com"]

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = formataddr(('Brocaly Support', sender_email))
    msg['To'] = ', '.join(recipient_emails)
    msg['Subject'] = "Brocaly Daily Flagged Calls Report"


    # Create the email message
    body = f"""
    <html>
    <body>
        <p>Your Daily AutoFlag report is ready for {formattedys_date}!</p>
        <p>Detailed Flagged Call Sheet - <a href="{link}">here</a></p>
        <p>Total Calls Processed: {total_calls_processed}<br>
        Total Flagged calls: {flagged_calls_percentage}% ({total_flagged_calls}/{total_calls_processed})</p>

        <h3>Flag Categories</h3>
        <p>Vulnerability Identified: {vulnerability_identified}/{total_calls_processed} ({vulnerability_percentage}%)<br>
        Failed TEXAS (for any reason): {failed_texas}/{vulnerability_identified} ({failed_texas_percentage}%)<br>
        Unrecognized Complaints: {unrecognized_complaints}/{total_calls_processed} ({unrecognized_complaints_percentage}%)<br>
        Poor Outcome: {poor_outcome}/{total_calls_processed} ({poor_outcome_percentage}%)<br>
        DPA Failed: {dpa_failed}/{total_calls_processed} ({dpa_failed_percentage}%)<br>
        Profanity: {profanity}/{total_calls_processed} ({profanity_percentage}%)</p>

        <h3>Additional Insights</h3>
        <h4>Failed TEXAS</h4>
        <p>Out of {failed_texas} calls flagged for ‘Failed TEXAS’:</p>
        <ul>
            <li>{thank_fail} calls ({thank_fail_percentage}%) failed to THANK</li>
            <li>{explain_fail} calls ({explain_fail_percentage}%) failed to EXPLAIN</li>
            <li>{explicit_consent_fail} calls ({explicit_consent_fail_percentage}%) failed to provide EXPLICIT CONSENT</li>
            <li>{ask_fail} calls ({ask_fail_percentage}%) failed to ASK</li>
            <li>{signpost_fail} calls ({signpost_fail_percentage}%) failed to SIGNPOST</li>
        </ul>
        
        <p>Please find attached a sheet with a detailed view on the flagged calls.</p>
        <br>
        <p>Regards,</p>
        <p>Team Brocaly</p>
    </body>
    </html>
    """

    msg.attach(MIMEText(body, 'html'))

    try:
        # Establish a secure connection with the SMTP server
        server = smtplib.SMTP(smtp_hostname, smtp_port)
        server.starttls()

        # Login with your SMTP credentials
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, recipient_emails, msg.as_string())

        print('Email sent successfully!')

    except Exception as e:
        print('Error: Unable to send email.')
        print(e)

    finally:
        # Close the SMTP server connection
        server.quit()