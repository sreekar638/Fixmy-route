from typing import List, Dict, Any, Optional
from datetime import datetime

def generate_complaint_letter(
    user_name: str,
    organization: str,
    category: Optional[str],
    issue_description: str,
    incident_date: Optional[str] = None,
    previous_attempts: Optional[str] = None,
    previous_ref_number: Optional[str] = None,
    desired_resolution: str = "Immediate resolution and formal response",
    evidence_collected: Optional[List[str]] = None,
    style: str = "formal"
) -> Dict[str, Any]:
    
    current_date_str = datetime.now().strftime("%d %B %Y")
    ref_tag = f" [Ref: {previous_ref_number}]" if previous_ref_number else ""
    user_display_name = user_name.strip() if user_name else "[Your Full Name]"
    evidence_list = evidence_collected or []
    
    # 1. Subject generation
    clean_org = organization.strip()
    subject = f"FORMAL GRIEVANCE: {issue_description[:60].strip()}... - {clean_org}{ref_tag}"
    if len(subject) > 120:
        subject = f"FORMAL GRIEVANCE: Complaint regarding {issue_description[:50]}... - {clean_org}"

    # 2. Body composition by style
    if style == "concise":
        body = f"""Date: {current_date_str}

To:
The Grievance Redressal Officer / Nodal Authority
{clean_org}

SUBJECT: {subject}

Dear Sir / Madam,

I am writing to register an urgent formal grievance regarding {clean_org}.

DETAILS OF GRIEVANCE:
- Date of occurrence: {incident_date or 'Recent'}
- Reference / Account ID: {previous_ref_number or '[Mention Account / Order / Tracking ID]'}
- Description: {issue_description.strip()}

PRIOR ACTION:
{previous_attempts.strip() if previous_attempts else 'I have previously contacted customer support without achieving a satisfactory resolution.'}

RELIEF SOUGHT:
I respectfully request {clean_org} to provide the following resolution within 14 working days:
{desired_resolution.strip()}

EVIDENCE ENCLOSED:
""" + "\n".join([f"- {ev}" for ev in evidence_list] if evidence_list else "- [Documentary proof / receipts / transaction statements attached]") + f"""

If this matter is not resolved within the statutory period, I reserve the right to escalate this complaint to the appropriate sector ombudsman or the National Consumer Commission.

Yours sincerely,

{user_display_name}
[Contact Number]
[Email Address]
"""

    elif style == "detailed":
        body = f"""Date: {current_date_str}

To:
The Appellate Authority / Principal Nodal Officer / Grievance Cell
{clean_org}

SUBJECT: FORMAL WRITTEN COMPLAINT & ESCALATION NOTICE - {clean_org.upper()}
{f'Reference Number: {previous_ref_number}' if previous_ref_number else 'Reference: Service / Account Grievance'}

Respected Authority,

1. PRELIMINARY STATEMENT:
I, {user_display_name}, am lodging this formal complaint regarding the deficiency in service, unfair practice, or unresolved dispute with {clean_org}.

2. CHRONOLOGY OF FACTS & OCCURRENCE:
- Incident Date / Period: {incident_date or 'As noted in attached communication records'}
- Matter in Dispute:
{issue_description.strip()}

3. PRIOR REDRESSAL EFFORTS & FAILURE TO RESOLVE:
{previous_attempts.strip() if previous_attempts else 'Prior informal communication and standard customer support tickets have either elapsed without resolution or failed to address the core problem adequately.'}
{f'Existing Ticket / Grievance ID: {previous_ref_number}' if previous_ref_number else ''}

4. REGULATORY & CONSUMER RIGHTS CONSIDERATIONS:
Under applicable regulations (including consumer protection mandates and relevant sector regulator guidelines), consumers and service users are entitled to timely, transparent, and fair grievance redressal. The current lapse has caused unwarranted distress, inconvenience, and hardship.

5. SPECIFIC RESOLUTION DEMANDED:
In light of the substantiated facts, I formally demand the following corrective action:
- {desired_resolution.strip()}
- A formal written acknowledgement and investigation summary confirming corrective measures taken.

6. SCHEDULE OF ENCLOSED EVIDENCE / DOCUMENTATION:
""" + "\n".join([f"  {idx+1}. {ev}" for idx, ev in enumerate(evidence_list)] if evidence_list else "  1. Complete transaction statements / purchase invoices / communication logs") + f"""

7. FINAL NOTICE FOR TIMELY REDRESSAL:
Kindly treat this letter as a statutory escalation notice. Kindly acknowledge receipt within 48 hours and furnish a complete resolution within 15 working days. Failing this, I shall be compelled to escalate this dispute before the relevant statutory authority (e.g., Banking Ombudsman / Electricity Ombudsman / DoT / UGC / RERA / Consumer Disputes Redressal Commission) without further communication.

Yours faithfully,

___________________________________
{user_display_name}
Address: [Your Postal Address / City]
Phone: [Your Phone Number]
Email: [Your Verified Email Address]
"""

    else:  # Standard formal style
        body = f"""Date: {current_date_str}

To:
The Customer Grievance Redressal Officer
{clean_org}

SUBJECT: Formal Complaint Regarding Unresolved Issue - {clean_org}

Dear Grievance Officer,

I am writing to bring to your urgent attention a serious grievance concerning your organization, which remains unresolved despite earlier attempts to seek assistance.

SUMMARY OF THE ISSUE:
- Date/Duration: {incident_date or 'Recent'}
- Account / Reference ID: {previous_ref_number or '[Insert Account / Connection / Transaction ID]'}
- Nature of Problem: {issue_description.strip()}

PREVIOUS RESOLUTION ATTEMPTS:
{previous_attempts.strip() if previous_attempts else 'The issue was reported through standard customer care channels, but no satisfactory resolution has been delivered to date.'}

DESIRED RESOLUTION:
To resolve this grievance fairly and amicably, I request:
{desired_resolution.strip()}

SUPPORTING EVIDENCE:
The following evidence is enclosed to corroborate this claim:
""" + "\n".join([f"- {ev}" for ev in evidence_list] if evidence_list else "- [Receipts, transaction statements, correspondence, or photographs attached]") + f"""

I request you to investigate this matter thoroughly and communicate the outcome within the standard regulatory resolution window (not exceeding 30 calendar days). If no satisfactory resolution is reached within this period, I will be constrained to escalate this matter to the relevant Ombudsman or Consumer Commission.

Thank you for your prompt cooperation.

Yours sincerely,

{user_display_name}
[Contact Number]
[Email Address]
"""

    return {
        "subject": subject,
        "body": body.strip(),
        "style": style,
        "organization": clean_org,
        "user_name": user_display_name,
        "generated_at": datetime.utcnow().isoformat()
    }
