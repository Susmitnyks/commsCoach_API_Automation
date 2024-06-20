import os
import logging
from dotenv import load_dotenv
import pyodbc
import json

# Configuring logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Loading environment variables
load_dotenv()

# Retrieving database credentials from environment variables
host = os.getenv("DB_HOST_UAT")
database = os.getenv("DB_NAME_UAT")
user = os.getenv("DB_USER_UAT")
password = os.getenv("DB_PASSWORD_UAT")


def initialize_db():
    try:
        connection_string = (
            'DRIVER={ODBC Driver 18 for SQL Server};'
            f'SERVER={host};'
            f'DATABASE={database};'
            f'UID={user};'
            f'PWD={password}'
        )

        # Create the connection
        conn = pyodbc.connect(connection_string)
        return conn
    except errors as e:
        logging.error(f"Error connecting to the database: {e}")


def fetch_conversation_ids(cursor):
    query = '''
    SELECT
    crcl.conversation_id,
    TRY_CONVERT(DATETIME, JSON_VALUE(s.meta, '$."start-date-time"'), 103) AS StartDateTime
FROM
    conversation_reports_conversation_links AS crcl
JOIN
    conversation_flag AS cf ON crcl.conversation_id = cf.conversation_id
JOIN
    conversations_source_links AS csl ON csl.conversation_id = crcl.conversation_id
JOIN
    sources AS s ON s.id = csl.source_id
WHERE
    TRY_CONVERT(DATETIME, JSON_VALUE(s.meta, '$."start-date-time"'), 103) >= CAST(GETDATE() - 1 AS DATE)
    AND TRY_CONVERT(DATETIME, JSON_VALUE(s.meta, '$."start-date-time"'), 103) < CAST(GETDATE() AS DATE)
    AND JSON_VALUE(s.meta, '$."start-date-time"') IS NOT NULL -- Ensure it's not null
    '''

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        conversation_ids = [row[0] for row in result]
        return conversation_ids
    except errors as e:
        logging.error(f"Error executing query to fetch conversation IDs: {e}")
        return []


def fetch_flag_details(conversation_id, cursor):
    query = f"""
    SELECT flag from conversation_flag
    where conversation_id = {conversation_id}
    """

    try:
        result = cursor.execute((query)).fetchall()
        # print(f"fetch_transcript(conversation_id, cursor): {type(result)}")
        result_lst = eval(result[0][0])
        return result_lst
    except errors as e:
        logging.error(f"Error executing query for conversation ID {conversation_id}: {e}")
        return []


def get_flag_mapping(cursor):
    '''
    Query to get report using conversation ID
    '''
    query = "SELECT flag_display_name, flag_id FROM flagged_filter_master"

    try:
        result = cursor.execute((query)).fetchall()
        if result:
            flag_mapping = {row[0]: row[1] for row in result}
            return flag_mapping
        else:
            return {"status": False, "message": "Flag mapping data not found"}
    except Exception as e:
        return {"status": False, "message": f"An error occurred while getting flag mapping: {e}"}


def files_count(cursor):
    query = f"""
SELECT
    COUNT(conversations.id) AS ConversationCount
FROM
    conversations
WHERE
    conversations.status = 'success'
    AND CAST(conversations.created_at AS DATETIME) >= DATEADD(HOUR, 0, DATEADD(DAY, -1, CAST(CAST(GETDATE() AS DATE) AS DATETIME)))
GROUP BY
    CAST(conversations.created_at AS DATE)
    """

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except errors as e:
        return []


conn = initialize_db()
cursor = conn.cursor()


def get_conversation_flagged_data(conversation_id, cursor):
    flag_details = fetch_flag_details(conversation_id, cursor)
    #print(flag_details)

    flag_mapping = get_flag_mapping(cursor)

    reverse_lookup_dict = {v: k for k, v in flag_mapping.items()}

    flagged_conversations_keys_mapped = [reverse_lookup_dict[value] for value in flag_details]

    return flagged_conversations_keys_mapped


def fetch_report(conversation_id, cursor):
    query = f"""
    SELECT
        conversation_reports_conversation_links.conversation_id,
        conversation_reports.report
    FROM
        conversation_reports
    JOIN
        conversation_reports_conversation_links
    ON
        conversation_reports_conversation_links.conversation_report_id = conversation_reports.id
    WHERE
        conversation_reports_conversation_links.conversation_id = {conversation_id}
    """

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except errors as e:
        return []


# Function to extract goal scores from a conversation transcript
def get_texas_data(conversation_id, cursor):
    results = fetch_report(conversation_id, cursor)
    if not results or not results[0][1]:
        logging.warning(f"No report found for conversation ID {conversation_id}. Skipping.")
        return {}, {}
    report = results[0][1]
    report = json.loads(report)

    texas_flag_score = {
        'Vulnerability - Thank': 0,
        'Vulnerability - Explain': 0,
        'Vulnerability - Explicit consent': 0,
        'Vulnerability - Ask': 0,
        'Vulnerability - Signpost': 0
    }

    # Process sections and goals
    for section in report['processed_score_json']['sections']:
        for subsection in section['subSections']:
            for goal in subsection['goals']:
                subsection_title = subsection['subSectionTitle']
                goal_name = goal['goalName']
                combined_term = f"{subsection_title} - {goal_name}"
                try:
                    score = goal['score']
                except KeyError:
                    logging.error(
                        f"KeyError for conversation ID {conversation_id}: 'score' key not found in goal object.")
                    return {}

                # Check against each condition in flagged_conditions
                for texas_name in texas_flag_score.keys():
                    if texas_name.lower() in combined_term.lower():
                        texas_flag_score[texas_name] = score

    return texas_flag_score


def flag_count(conversation_id, cursor):
    flag_count_dict = {
        'Vulnerability': 0,
        'TEXAS Incomplete': 0,
        'Poor Outcome': 0,
        'Complaint': 0,
        'Unrecognised Complaint': 0,
        'DPA Check': 0,
        'Low Score': 0,
        'Profanity': 0
    }

    texas_flag_count = {
        'Vulnerability - Thank': 0,
        'Vulnerability - Explain': 0,
        'Vulnerability - Explicit consent': 0,
        'Vulnerability - Ask': 0,
        'Vulnerability - Signpost': 0
    }

    total_flag_count = 0

    for id in conversation_id:
        flag_data = get_conversation_flagged_data(id, cursor)
        #print(f"Flag_data is: {flag_data}")
        total_flag_count = total_flag_count + 1
        #print("conversation_id", id)
        for flag in flag_data:
            flag_count_dict[flag] = flag_count_dict[flag] + 1
            if flag == 'TEXAS Incomplete':
                texas_data = get_texas_data(id, cursor)
               # print(f"Texas details for id = {id} is {texas_data}")
                for texas_flag, score in texas_data.items():
                    if score in ["No"]:
                        texas_flag_count[texas_flag] = texas_flag_count[texas_flag] + 1

    files_count_var = files_count(cursor)

    texas_flag_count['total_flags_count'] = total_flag_count
    texas_flag_count['files_count'] = files_count_var[0][0]

    final_dict = {}

    final_dict.update(flag_count_dict)
    final_dict.update(texas_flag_count)

    return final_dict


def final_method(cursor):
    conv_id_lst = fetch_conversation_ids(cursor)
    #conv_id_lst = [5, 11, 12, 15, 14]
    #print(f"conv_id_lst: {conv_id_lst}")
    final_flag_count = flag_count(conv_id_lst, cursor)
    return final_flag_count


#print(final_method(cursor))