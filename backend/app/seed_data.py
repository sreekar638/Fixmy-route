import logging
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.database import engine, SessionLocal, Base
from backend.app.config import settings
from backend.app.models.user import User
from backend.app.models.route import Category, ProblemRoute, ResolutionStep, EvidenceRequirement, SourceReference
from backend.app.services.auth_service import hash_password

logger = logging.getLogger(__name__)

CATEGORIES_DATA = [
    {
        "slug": "government-services",
        "name": "Government Services",
        "icon": "building-columns",
        "description": "Passport, Aadhaar, civil certificates, voter services, and municipal administration.",
        "display_order": 1
    },
    {
        "slug": "college-university",
        "name": "College and University",
        "icon": "graduation-cap",
        "description": "Fee refunds, security deposit returns, certificates, ragging, and UGC/AICTE compliance.",
        "display_order": 2
    },
    {
        "slug": "electricity-water",
        "name": "Electricity and Water",
        "icon": "bolt",
        "description": "Discom billing disputes, meter faults, frequent power cuts, water supply, and leaks.",
        "display_order": 3
    },
    {
        "slug": "banking-payments",
        "name": "Banking and Payments",
        "icon": "credit-card",
        "description": "Failed UPI transactions, unauthorized card debits, ATM failures, and loan/EMI disputes.",
        "display_order": 4
    },
    {
        "slug": "internet-telecom",
        "name": "Internet and Telecom",
        "icon": "wifi",
        "description": "Broadband fiber outages, SIM porting issues, billing discrepancies, and poor network quality.",
        "display_order": 5
    },
    {
        "slug": "transport-public",
        "name": "Transport and Public Services",
        "icon": "car",
        "description": "RTO vehicle transfers, driving licenses, traffic challans, roads, railways, and public transit.",
        "display_order": 6
    },
    {
        "slug": "housing-rental",
        "name": "Housing and Rental Issues",
        "icon": "home",
        "description": "Landlord maintenance neglect, security deposit disputes, RERA builder delays, and RWA issues.",
        "display_order": 7
    },
    {
        "slug": "workplace-problems",
        "name": "Workplace Problems",
        "icon": "briefcase",
        "description": "Unpaid salary, withheld relieving letters, EPFO/Provident Fund issues, and labour compliance.",
        "display_order": 8
    },
    {
        "slug": "consumer-complaints",
        "name": "Consumer Complaints",
        "icon": "shopping-cart",
        "description": "Defective electronics, e-commerce refund refusal, warranty denials, and misleading ads.",
        "display_order": 9
    },
    {
        "slug": "cybercrime-fraud",
        "name": "Everyday Fraud & Cyber Crime",
        "icon": "shield-check",
        "description": "Phishing calls, OTP theft, financial impersonation scams, and cyber stalking.",
        "display_order": 10
    }
]

ROUTES_DATA = [
    # 1. Electricity Bill Dispute
    {
        "slug": "electricity-bill-incorrect-dispute",
        "category_slug": "electricity-water",
        "title": "Electricity Bill Is Abnormally High or Incorrect",
        "subcategory": "Billing & Meter Disputes",
        "problem_description": "My domestic or commercial electricity bill is vastly higher than usual, has incorrect meter readings, or includes charges for disconnected/unoccupied premises.",
        "keywords": "electricity, power bill, high bill, discom, bescom, msedcl, tneb, cesc, meter reading, faulty meter, tariff dispute",
        "jurisdiction": "State-level",
        "applicable_states": "ALL",
        "responsible_authority": "Consumer Grievance Redressal Forum (CGRF) & State Electricity Regulatory Commission (SERC)",
        "authority_type": "Statutory Forum & Ombudsman",
        "reason_for_routing": "Under the Electricity Act 2003, every power distribution licensee (Discom) must operate an independent Consumer Grievance Redressal Forum (CGRF). If the Discom customer care fails to rectify the bill within statutory timelines, the case escalates to the state Electricity Ombudsman.",
        "eligibility_conditions": "User must have a registered Consumer Number / Account Number with their respective state Discom. A formal written complaint or portal ticket must first be submitted to the local Sub-Divisional Officer (SDO) or Assistant Engineer.",
        "official_channel": "State Discom Customer Portal → CGRF Forum → Electricity Ombudsman",
        "official_portal_url": "https://powermin.gov.in/en/content/electricity-rules-rights-consumers-2020",
        "escalation_options": "If the Discom does not resolve within 15–30 days, file petition before CGRF. If CGRF order is unsatisfactory, appeal to the State Electricity Ombudsman within 30 days.",
        "relevant_deadlines": "Discoms must respond within 3 to 15 days for billing inquiries. CGRF must issue an order within 60 days.",
        "verification_status": "verified",
        "confidence_score": 98,
        "steps": [
            {
                "step_number": 1,
                "title": "Take Photo of Physical Meter Reading",
                "description": "Photograph the actual current kWh reading and meter serial number on your physical meter display to compare against the billed units.",
                "official_url": None,
                "action_type": "gather",
                "is_mandatory": True,
                "warnings": "Do not break or tamper with any wire seals on the meter box."
            },
            {
                "step_number": 2,
                "title": "Submit Written Disputed Bill Notice to Local Discom SDO",
                "description": "Visit your local Sub-Divisional Office or use the Discom's official web portal/mobile app. Submit a written request citing the average past consumption and meter photograph. Request an official meter testing report (Accucheck).",
                "official_url": None,
                "action_type": "contact",
                "is_mandatory": True,
                "warnings": "Keep a stamped receiving acknowledgement copy or ticket SMS."
            },
            {
                "step_number": 3,
                "title": "Pay Provisional / Average Bill if Mandated",
                "description": "Under Discom regulations, consumers often must pay an average baseline bill amount under protest to prevent power disconnection while the dispute is pending.",
                "official_url": None,
                "action_type": "action",
                "is_mandatory": False,
                "warnings": "Always write 'Paid under protest subject to meter inspection' on the receipt."
            },
            {
                "step_number": 4,
                "title": "Escalate to Consumer Grievance Redressal Forum (CGRF)",
                "description": "If the Discom does not correct the billing or reply within 30 days, submit a formal petition to the CGRF along with copies of your complaint and past 6 months of paid bills.",
                "official_url": None,
                "action_type": "escalate",
                "is_mandatory": True,
                "warnings": "CGRF is a statutory quasi-judicial forum located at the Discom circle headquarters."
            }
        ],
        "evidence": [
            {"title": "Latest Disputed Electricity Bill", "why_needed": "Shows the erroneous units billed, tariff category, and billed amounts.", "is_mandatory": True},
            {"title": "Clear Photo of Physical Meter Display", "why_needed": "Proves the actual cumulative units consumed vs billed units.", "is_mandatory": True},
            {"title": "Previous 3 to 6 Months Paid Bills", "why_needed": "Demonstrates historic average consumption pattern.", "is_mandatory": True},
            {"title": "Discom Complaint Number / SMS Acknowledgement", "why_needed": "Proves mandatory preliminary notice was given to the service provider.", "is_mandatory": True}
        ],
        "sources": [
            {"title": "Electricity (Rights of Consumers) Rules, 2020", "url": "https://powermin.gov.in/en/content/electricity-rules-rights-consumers-2020", "publisher": "Ministry of Power, Government of India", "description": "National regulations mandating timelines for bill disputes and meter testing."},
            {"title": "Electricity Act 2003, Section 42(5)", "url": "https://cercind.gov.in/Act-with-amendment.pdf", "publisher": "Central Electricity Regulatory Commission (CERC)", "description": "Statutory foundation for CGRF and Ombudsman mechanism."}
        ]
    },

    # 2. Banking Transaction Failure (UPI / ATM / NetBanking)
    {
        "slug": "bank-transaction-failed-money-deducted",
        "category_slug": "banking-payments",
        "title": "Bank Transaction Failed but Money Was Deducted (UPI / ATM / IMPS)",
        "subcategory": "Digital Payments & Account Disputes",
        "problem_description": "Money was debited from my bank account during a UPI, ATM, or online fund transfer, but the recipient never received it, or the ATM failed to dispense cash.",
        "keywords": "bank, upi, gpay, phonepe, paytm, atm, transaction failed, money debited, rbi, ombudsman, auto reversal, t+1, chargeback",
        "jurisdiction": "All India",
        "applicable_states": "ALL",
        "responsible_authority": "Bank Principal Nodal Officer & Reserve Bank Integrated Ombudsman Scheme (RBI CMS)",
        "authority_type": "Statutory Regulator & Ombudsman",
        "reason_for_routing": "Under RBI Master Directions on Harmonisation of Turn Around Time (TAT), banks are legally obligated to auto-reverse failed transactions within T+1 (for UPI) or T+5 (for ATM) days, failing which the bank must pay compensation of ₹100 per day of delay. Unresolved complaints are addressed by the RBI Integrated Ombudsman.",
        "eligibility_conditions": "Must wait for the mandated TAT window (typically T+1 for UPI, T+5 for ATM). Must first log a complaint with the originating bank.",
        "official_channel": "Bank Branch/NetBanking → Principal Nodal Officer (PNO) → RBI Complaint Management System (CMS)",
        "official_portal_url": "https://cms.rbi.org.in/",
        "escalation_options": "If the bank rejects the complaint or fails to resolve within 30 calendar days, submit a complaint on the official RBI CMS portal.",
        "relevant_deadlines": "Auto-reversal TAT: UPI T+1 day; ATM cash dispense T+5 days. Compensation of ₹100/day payable after TAT expiration. Ombudsman appeal allowed after 30 days.",
        "verification_status": "verified",
        "confidence_score": 99,
        "steps": [
            {
                "step_number": 1,
                "title": "Note Down UTR / Transaction Reference Number",
                "description": "Locate the 12-digit Unique Transaction Reference (UTR) number or RRN in your bank passbook/SMS/UPI app statement.",
                "official_url": None,
                "action_type": "gather",
                "is_mandatory": True,
                "warnings": "Never share your UPI PIN, OTP, or password with anyone, including bank staff."
            },
            {
                "step_number": 2,
                "title": "Log a Formal Ticket with Your Bank Customer Care",
                "description": "Report the failure through your bank's official mobile banking app or helpline. Note down the Service Request (SR) or Ticket number.",
                "official_url": None,
                "action_type": "contact",
                "is_mandatory": True,
                "warnings": "Ask for the exact TAT and reference number in writing or via SMS."
            },
            {
                "step_number": 3,
                "title": "Escalate to Bank Principal Nodal Officer (PNO)",
                "description": "If 7 days pass without reversal, email the Principal Nodal Officer of your bank citing the RBI TAT circular and claiming statutory delay compensation (₹100/day).",
                "official_url": None,
                "action_type": "escalate",
                "is_mandatory": True,
                "warnings": "Every commercial bank in India has the PNO email published on its website under 'Grievance Redressal'."
            },
            {
                "step_number": 4,
                "title": "Lodge Online Complaint with RBI Integrated Ombudsman",
                "description": "If unresolved after 30 days from initial bank complaint, lodge a claim on RBI CMS portal (cms.rbi.org.in). Upload bank statements and previous complaint trail.",
                "official_url": "https://cms.rbi.org.in/",
                "action_type": "submit",
                "is_mandatory": True,
                "warnings": "RBI Ombudsman handles claims without any filing fee."
            }
        ],
        "evidence": [
            {"title": "Bank Account Statement showing Debit", "why_needed": "Proves the exact timestamp and amount debited.", "is_mandatory": True},
            {"title": "UPI / Payment App Transaction Screenshot & UTR", "why_needed": "Identifies the 12-digit payment reference.", "is_mandatory": True},
            {"title": "Bank Grievance Ticket / SR Number", "why_needed": "Proves prior complaint was lodged with the bank.", "is_mandatory": True}
        ],
        "sources": [
            {"title": "RBI Harmonisation of Turn Around Time (TAT) and customer compensation", "url": "https://www.rbi.org.in/scripts/FS_Notification.aspx?Id=11693&fn=2&Mode=0", "publisher": "Reserve Bank of India", "description": "Mandates reversal turnaround times and ₹100/day compensation."},
            {"title": "Reserve Bank - Integrated Ombudsman Scheme, 2021", "url": "https://cms.rbi.org.in/", "publisher": "Reserve Bank of India", "description": "One Nation One Ombudsman redressal portal for banking, NBFC, and prepaid payment disputes."}
        ]
    },

    # 3. College / University Deposit Withholding
    {
        "slug": "college-university-withholding-fees-deposit",
        "category_slug": "college-university",
        "title": "College or University Refusing to Refund Security Deposit or Certificates",
        "subcategory": "Higher Education Disputes",
        "problem_description": "My college, university, or coaching institute is refusing to return my caution deposit, original academic certificates, or refund fees after cancellation of admission.",
        "keywords": "college, university, caution deposit, fee refund, certificates withheld, ugc, aicte, migration certificate, degree, admission cancelled",
        "jurisdiction": "All India",
        "applicable_states": "ALL",
        "responsible_authority": "University Grants Commission (UGC) e-Samadhan & National Consumer Disputes Redressal Commission",
        "authority_type": "Regulatory Grievance Portal & Consumer Court",
        "reason_for_routing": "Under UGC Public Notices and Redressal of Grievances of Students Regulations, higher education institutions are legally barred from retaining original student certificates or withholding refundable caution deposits. UGC operates the centralised e-Samadhan portal.",
        "eligibility_conditions": "Institution must be recognized by UGC, AICTE, or State University Act. Student must have applied for formal clearance / cancellation.",
        "official_channel": "College Registrar → University Ombudsperson → UGC e-Samadhan Portal",
        "official_portal_url": "https://samadhan.ugc.ac.in/",
        "escalation_options": "Submit grievance on UGC e-Samadhan. For private coaching institutes or non-responsive universities, file a consumer complaint on National Consumer Helpline (NCH) or e-Daakhil for deficiency in service.",
        "relevant_deadlines": "UGC mandates fee refund within 15 days of admission cancellation request as per yearly fee refund policy.",
        "verification_status": "verified",
        "confidence_score": 96,
        "steps": [
            {
                "step_number": 1,
                "title": "Submit Formal Written Letter to College Principal / Registrar",
                "description": "Send a registered letter or official email to the head of the institution attaching fee receipts and clearance form. Cite the UGC Fee Refund Policy Guidelines.",
                "official_url": None,
                "action_type": "contact",
                "is_mandatory": True,
                "warnings": "Keep postal tracking receipt or email delivery confirmation."
            },
            {
                "step_number": 2,
                "title": "Petition the University Ombudsperson",
                "description": "If affiliated with a central or state university, address a complaint to the designated University Student Ombudsperson.",
                "official_url": None,
                "action_type": "escalate",
                "is_mandatory": True,
                "warnings": "Every university is mandated by UGC to notify the contact details of its Ombudsperson."
            },
            {
                "step_number": 3,
                "title": "File Grievance on UGC e-Samadhan Portal",
                "description": "Register on the UGC e-Samadhan portal (samadhan.ugc.ac.in). Choose 'Student Grievance', select your institution, and attach communication records.",
                "official_url": "https://samadhan.ugc.ac.in/",
                "action_type": "submit",
                "is_mandatory": True,
                "warnings": "UGC directly issues notices to Vice Chancellors and Registrars through this portal."
            }
        ],
        "evidence": [
            {"title": "Fee Payment Receipts & Caution Deposit Slip", "why_needed": "Proves the financial amount paid and refundable status.", "is_mandatory": True},
            {"title": "Admission Offer Letter / ID Card Copy", "why_needed": "Confirms student enrollment status.", "is_mandatory": True},
            {"title": "Copy of Formal Refund / Certificate Request Letter", "why_needed": "Documents the date formal demand was initiated.", "is_mandatory": True}
        ],
        "sources": [
            {"title": "UGC Student Grievance Redressal Regulations", "url": "https://www.ugc.gov.in/", "publisher": "University Grants Commission", "description": "Mandates return of original documents and student ombudsman systems."},
            {"title": "UGC e-Samadhan Portal", "url": "https://samadhan.ugc.ac.in/", "publisher": "Ministry of Education, Government of India", "description": "Single window student grievance resolution portal."}
        ]
    },

    # 4. Internet & Telecom Outage
    {
        "slug": "internet-broadband-down-telecom-dispute",
        "category_slug": "internet-telecom",
        "title": "Broadband / Fiber Internet Connection Down for Multiple Days",
        "subcategory": "Broadband & Mobile Services",
        "problem_description": "My fiber broadband or mobile data connection has experienced prolonged downtime, poor speed below plan commitments, or false restoration closure by the provider.",
        "keywords": "internet, wifi, broadband, fiber, airtel, jio, bsnl, act, outage, no connection, telecom, trai, billing waiver, appellate authority",
        "jurisdiction": "All India",
        "applicable_states": "ALL",
        "responsible_authority": "Telecom Service Provider Appellate Authority & Department of Telecommunications (DoT) / TRAI",
        "authority_type": "Telecom Regulator & Appellate Body",
        "reason_for_routing": "Under TRAI Telecom Consumers Protection Regulations, telecom service providers must maintain a two-tier grievance mechanism: Complaint Center (Call Centre/App) followed by an independent Appellate Authority. Extended outages entitle consumers to pro-rata billing rental rebates.",
        "eligibility_conditions": "Must have an active account/landline number and an unresolved ticket number from the provider's helpdesk.",
        "official_channel": "Service Provider Nodal Officer → Appellate Authority → DoT Public Grievance Portal",
        "official_portal_url": "https://pgportal.gov.in/",
        "escalation_options": "Approach the Appellate Authority designated by the telecom operator for your telecom circle. If non-responsive, submit a petition on the National Public Grievance Portal (CPGRAMS/DoT).",
        "relevant_deadlines": "Service providers must acknowledge complaints within 2 hours and resolve broadband faults within 3 working days. Appellate Authority must decide within 30 days.",
        "verification_status": "verified",
        "confidence_score": 97,
        "steps": [
            {
                "step_number": 1,
                "title": "Log Ticket on Service Provider App and Save Ticket ID",
                "description": "Log an official downtime complaint through Airtel Thanks, MyJio, BSNL Selfcare, or ACT Fibernet portal. Note the exact ticket ID.",
                "official_url": None,
                "action_type": "contact",
                "is_mandatory": True,
                "warnings": "Do not accept phone closures without internet functionality actually restored."
            },
            {
                "step_number": 2,
                "title": "Escalate to the Appellate Authority for Your Circle",
                "description": "Find the designated Appellate Authority email and address for your state/circle on your provider's website. Email them your complaint with the existing ticket ID and claim bill waiver for downtime days.",
                "official_url": None,
                "action_type": "escalate",
                "is_mandatory": True,
                "warnings": "Appeals must generally be filed within 30 days of ticket closure by call centre."
            },
            {
                "step_number": 3,
                "title": "File DoT Grievance on CPGRAMS",
                "description": "If the Appellate Authority does not provide relief, lodge a formal grievance with the Department of Telecommunications on the CPGRAMS portal.",
                "official_url": "https://pgportal.gov.in/",
                "action_type": "submit",
                "is_mandatory": True,
                "warnings": "DoT directly holds telecom operators accountable under license conditions."
            }
        ],
        "evidence": [
            {"title": "Support Ticket Reference ID & SMS timestamps", "why_needed": "Proves the exact duration of continuous downtime.", "is_mandatory": True},
            {"title": "Broadband Account Bill showing billed period", "why_needed": "Proves you are paying active subscription charges.", "is_mandatory": True},
            {"title": "Router LED Status Photo or Speed Test Log", "why_needed": "Shows red LOS indicator or zero connectivity logs.", "is_mandatory": False}
        ],
        "sources": [
            {"title": "TRAI Telecom Consumers Protection and Redressal of Grievances Regulations", "url": "https://trai.gov.in/", "publisher": "Telecom Regulatory Authority of India", "description": "Mandates 2-tier redressal structure and downtime compensations."},
            {"title": "Centralized Public Grievance Redress and Monitoring System (CPGRAMS)", "url": "https://pgportal.gov.in/", "publisher": "Department of Administrative Reforms and Public Grievances", "description": "Government of India central portal for telecom and ministerial grievances."}
        ]
    },

    # 5. Defective Consumer Goods / E-Commerce Scam
    {
        "slug": "consumer-defective-product-refund-denial",
        "category_slug": "consumer-complaints",
        "title": "E-Commerce Refund Refused or Defective Product Received",
        "subcategory": "Consumer Protection & Product Defects",
        "problem_description": "An e-commerce marketplace (Amazon, Flipkart, etc.) or manufacturer delivered a damaged, fake, or non-functional item and is refusing replacement, repair, or full refund.",
        "keywords": "amazon, flipkart, defective product, warranty, refund refused, fake product, consumer court, nch, edaakhil, replacement, broken item",
        "jurisdiction": "All India",
        "applicable_states": "ALL",
        "responsible_authority": "National Consumer Helpline (NCH / INGRAM) & e-Daakhil Consumer Commission Portal",
        "authority_type": "Ministry of Consumer Affairs & Consumer Court",
        "reason_for_routing": "Under the Consumer Protection Act 2019, consumers have a statutory right to be protected against unfair trade practices and product liability. The Department of Consumer Affairs runs the National Consumer Helpline (NCH) as a fast pre-litigation resolution platform, followed by e-Daakhil for e-filing in consumer commissions.",
        "eligibility_conditions": "Proof of purchase required. User must have attempted resolution with the merchant or e-commerce seller first.",
        "official_channel": "Merchant Customer Grievance → National Consumer Helpline (NCH) → e-Daakhil Consumer Commission",
        "official_portal_url": "https://consumerhelpline.gov.in/",
        "escalation_options": "Call 1915 or register grievance on consumerhelpline.gov.in. If the company remains non-compliant, file a case online on e-Daakhil (edaakhil.nic.in) before the District Consumer Commission.",
        "relevant_deadlines": "Consumer cases can be filed within 2 years from the date of the cause of action. NCH typically seeks merchant response within 15–30 days.",
        "verification_status": "verified",
        "confidence_score": 98,
        "steps": [
            {
                "step_number": 1,
                "title": "Gather Tax Invoice, Unboxing Video, and Delivery Receipt",
                "description": "Save the original PDF invoice with seller GST number, order summary, and clear photographs or unboxing video of the defective product.",
                "official_url": None,
                "action_type": "gather",
                "is_mandatory": True,
                "warnings": "Keep original packaging with shipping barcode labels intact."
            },
            {
                "step_number": 2,
                "title": "Submit Grievance to Company Grievance Officer",
                "description": "Send a formal email to the e-commerce platform's designated Grievance Officer (mandated by Consumer Protection E-Commerce Rules 2020).",
                "official_url": None,
                "action_type": "contact",
                "is_mandatory": True,
                "warnings": "E-commerce companies must acknowledge within 48 hours and resolve within 1 month."
            },
            {
                "step_number": 3,
                "title": "Register Complaint on National Consumer Helpline (NCH)",
                "description": "Visit consumerhelpline.gov.in or call toll-free 1915 or WhatsApp +91 8800001915. Enter seller details, invoice value, and relief demanded.",
                "official_url": "https://consumerhelpline.gov.in/",
                "action_type": "submit",
                "is_mandatory": True,
                "warnings": "NCH directly coordinates with partner companies under the Convergence program."
            },
            {
                "step_number": 4,
                "title": "File Formal Case on e-Daakhil Consumer Commission",
                "description": "If NCH mediation fails, file an online consumer case without hiring an advocate on e-Daakhil (edaakhil.nic.in). Claim product refund plus compensation for harassment.",
                "official_url": "https://edaakhil.nic.in/",
                "action_type": "escalate",
                "is_mandatory": False,
                "warnings": "District Consumer Commissions have jurisdiction for claims up to ₹50 Lakhs."
            }
        ],
        "evidence": [
            {"title": "Tax Invoice with GST details", "why_needed": "Statutory proof of purchase and transaction value.", "is_mandatory": True},
            {"title": "Photographs / Video of Defect or Damaged Goods", "why_needed": "Proves physical defect or deficiency in goods received.", "is_mandatory": True},
            {"title": "E-Commerce Return Rejection Screenshot or Email", "why_needed": "Shows unfair denial of legitimate return policy.", "is_mandatory": True}
        ],
        "sources": [
            {"title": "Consumer Protection Act, 2019", "url": "https://consumeraffairs.nic.in/acts-and-rules/consumer-protection", "publisher": "Ministry of Consumer Affairs, Food & Public Distribution", "description": "Governs consumer rights, product liability, and consumer commissions."},
            {"title": "National Consumer Helpline Portal (NCH)", "url": "https://consumerhelpline.gov.in/", "publisher": "Department of Consumer Affairs, Government of India", "description": "Official national helpline for consumer mediation."}
        ]
    },

    # 6. Landlord Water Leak / Maintenance Neglect
    {
        "slug": "landlord-water-leak-rental-maintenance-dispute",
        "category_slug": "housing-rental",
        "title": "Landlord Refusing to Repair Water Leakage or Structural Damage",
        "subcategory": "Tenancy & Property Disputes",
        "problem_description": "My landlord or flat owner refuses to address plumbing leaks, seepage, or essential structural repairs, making the premises hazardous or unlivable, or threatens unlawful eviction.",
        "keywords": "landlord, tenant, rent, water leak, seepage, plumbing, repairs, rwa, maintenance, security deposit, model tenancy act, civil dispute",
        "jurisdiction": "State-level",
        "applicable_states": "ALL",
        "responsible_authority": "Rent Authority / Rent Court (under Tenancy Act) & Society RWA / Municipal Health Officer",
        "authority_type": "Quasi-Judicial Rent Authority & Local RWA",
        "reason_for_routing": "Under the Model Tenancy Act and state rent control legislations, landlords are legally responsible for structural repairs, plumbing maintenance, and external seepage. If the landlord fails to repair after reasonable notice, tenants can carry out essential repairs and deduct costs from rent, or approach the Rent Authority.",
        "eligibility_conditions": "Must possess a signed rental agreement or proof of regular rent payments (bank statements/receipts).",
        "official_channel": "Written Legal Notice → Society Managing Committee / RWA → Rent Authority",
        "official_portal_url": "https://mohua.gov.in/cms/model-tenancy-act.php",
        "escalation_options": "Send formal 14-day notice. If unattended, approach Society RWA to intervene, or file an application before the local Rent Authority / Sub-Divisional Magistrate.",
        "relevant_deadlines": "Tenants must give minimum 24-hour notice for emergency inspections, or 14 days written notice for structural repairs.",
        "verification_status": "verified",
        "confidence_score": 94,
        "steps": [
            {
                "step_number": 1,
                "title": "Document Seepage and Damage with Timestamped Photos",
                "description": "Take clear photos and video recordings of the water leakage, ceiling peel, wall dampness, or affected electrical points.",
                "official_url": None,
                "action_type": "gather",
                "is_mandatory": True,
                "warnings": "Turn off electrical switches near wet walls immediately to prevent fire hazards."
            },
            {
                "step_number": 2,
                "title": "Send Written Repair Notice to Landlord via Email & WhatsApp",
                "description": "Issue a formal written notice giving the landlord 14 calendar days to inspect and execute repairs, citing safety and structural degradation.",
                "official_url": None,
                "action_type": "contact",
                "is_mandatory": True,
                "warnings": "Do not stop paying rent abruptly without written notice, as it weakens your legal standing."
            },
            {
                "step_number": 3,
                "title": "Involve Society Apartment Owners Association (RWA)",
                "description": "If the seepage originates from the flat above or shared building shafts, lodge a complaint with the Resident Welfare Association (RWA) maintenance office.",
                "official_url": None,
                "action_type": "escalate",
                "is_mandatory": True,
                "warnings": "RWA rules empower the committee to inspect source flats."
            },
            {
                "step_number": 4,
                "title": "Approach Rent Authority / Civil Consumer Court",
                "description": "If the landlord neglects repairs causing damage to your personal belongings, file an application before the local Rent Authority or District Consumer Commission for deficiency in service.",
                "official_url": None,
                "action_type": "escalate",
                "is_mandatory": False,
                "warnings": "You may also be entitled to terminate the lease with full deposit refund if premises become unlivable."
            }
        ],
        "evidence": [
            {"title": "Signed Rental Agreement Copy", "why_needed": "Establishes landlord-tenant relationship and maintenance terms.", "is_mandatory": True},
            {"title": "Photographs of Water Leakage / Seepage", "why_needed": "Provides verifiable proof of physical damage.", "is_mandatory": True},
            {"title": "Written Communication / WhatsApp Chat with Landlord", "why_needed": "Demonstrates landlord was properly notified and neglected to act.", "is_mandatory": True}
        ],
        "sources": [
            {"title": "Model Tenancy Act, 2021", "url": "https://mohua.gov.in/cms/model-tenancy-act.php", "publisher": "Ministry of Housing and Urban Affairs", "description": "Guidelines establishing obligations of landlords and tenants regarding repairs."}
        ]
    },

    # 7. Unpaid Wages / Provident Fund (PF) Issue
    {
        "slug": "workplace-unpaid-salary-pf-epfo-issue",
        "category_slug": "workplace-problems",
        "title": "Employer Withholding Salary, Relieving Letter, or PF Deposit",
        "subcategory": "Employment & Labour Rights",
        "problem_description": "My employer has failed to disburse earned wages, is withholding my relieving letter/experience certificate, or has deducted Provident Fund (PF) from salary but not deposited it with EPFO.",
        "keywords": "salary, unpaid wages, employer, pf, provident fund, epfo, relieving letter, experience certificate, labour court, samadhan portal, gratuity",
        "jurisdiction": "All India",
        "applicable_states": "ALL",
        "responsible_authority": "EPFO Grievance Management System (EPFiGMS) & Office of the Labour Commissioner",
        "authority_type": "Statutory Authority & Labour Commission",
        "reason_for_routing": "Under the Payment of Wages Act and Employees' Provident Funds Act 1952, non-deposit of deducted PF is a cognizable criminal breach of trust. EPFO operates the online EPFiGMS portal. For unpaid salary, the state/central Labour Commissioner conducts conciliation under the Industrial Disputes Act.",
        "eligibility_conditions": "Must have appointment letter, payslips, or employment contract. For PF issues, Universal Account Number (UAN) is required.",
        "official_channel": "Employer HR Escalation → EPFiGMS Portal (for PF) → Labour Commissioner (for Wages)",
        "official_portal_url": "https://epfigms.gov.in/",
        "escalation_options": "For PF non-remittance, lodge complaint on epfigms.gov.in (EPFO inspects company accounts directly). For unpaid wages, submit an application to the Deputy Labour Commissioner.",
        "relevant_deadlines": "Wages must be disbursed by the 7th or 10th of every month. EPFO complaints are typically investigated within 15–30 days.",
        "verification_status": "verified",
        "confidence_score": 97,
        "steps": [
            {
                "step_number": 1,
                "title": "Collate Payslips, Bank Statements, and Offer Letter",
                "description": "Download all available salary slips, bank transaction logs showing regular salary deposits, and your official employment appointment contract.",
                "official_url": None,
                "action_type": "gather",
                "is_mandatory": True,
                "warnings": "Back up official company emails to personal storage before your work email account is terminated."
            },
            {
                "step_number": 2,
                "title": "Send Legal Demand Letter to Employer HR and Directors",
                "description": "Send a formal email giving the company 7 working days to release overdue salary, deposit PF, or issue service letters.",
                "official_url": None,
                "action_type": "contact",
                "is_mandatory": True,
                "warnings": "Cite the Payment of Wages Act and Section 406/409 of IPC for criminal breach of trust regarding PF."
            },
            {
                "step_number": 3,
                "title": "Register EPFO Grievance on EPFiGMS",
                "description": "If the employer has deducted PF but your passbook shows no deposit, file a complaint on epfigms.gov.in quoting your UAN and company PF code.",
                "official_url": "https://epfigms.gov.in/",
                "action_type": "submit",
                "is_mandatory": True,
                "warnings": "EPFO enforcement officers can freeze employer bank accounts for unpaid dues."
            },
            {
                "step_number": 4,
                "title": "File Formal Complaint with Labour Commissioner",
                "description": "Visit the local District Labour Office or submit via state labour portal (e.g. Samadhan portal). The Labour Officer will summon company representatives for conciliation.",
                "official_url": "https://samadhan.labour.gov.in/",
                "action_type": "escalate",
                "is_mandatory": True,
                "warnings": "Labour Commissioner services are free and accessible to employees without advocate fees."
            }
        ],
        "evidence": [
            {"title": "Appointment Letter / Employment Agreement", "why_needed": "Proves terms of employment and agreed monthly remuneration.", "is_mandatory": True},
            {"title": "Recent Salary Slips showing PF deductions", "why_needed": "Demonstrates statutory deductions made from your salary.", "is_mandatory": True},
            {"title": "EPFO Member Passbook showing zero or missing deposits", "why_needed": "Conclusive evidence of company default.", "is_mandatory": True}
        ],
        "sources": [
            {"title": "Employees' Provident Funds and Miscellaneous Provisions Act, 1952", "url": "https://www.epfindia.gov.in/", "publisher": "Employees' Provident Fund Organisation", "description": "Statutory rules for employer contributions and penalties for default."},
            {"title": "EPFiGMS - EPFO Grievance Management System", "url": "https://epfigms.gov.in/", "publisher": "EPFO, Ministry of Labour & Employment", "description": "Official public grievance portal for PF subscribers."}
        ]
    },

    # 8. Cyber Crime & Financial Phishing
    {
        "slug": "cyber-crime-financial-phishing-scam",
        "category_slug": "cybercrime-fraud",
        "title": "Online Financial Fraud, Phishing, or Unauthorized Money Transfer",
        "subcategory": "Cyber Fraud & Digital Security",
        "problem_description": "I fell victim to an online cyber scam, phishing link, unauthorized payment transfer, or impersonation fraud and lost funds from my account.",
        "keywords": "cyber, fraud, scam, stolen money, otp, phishing, upi scam, 1930, cybercrime portal, police, unauthorized debit",
        "jurisdiction": "All India",
        "applicable_states": "ALL",
        "responsible_authority": "National Cyber Crime Reporting Portal & Indian Cyber Crime Coordination Centre (I4C)",
        "authority_type": "Law Enforcement & National Coordination Centre",
        "reason_for_routing": "The Ministry of Home Affairs operates the Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS). Dialing 1930 immediately can freeze the defrauded money in beneficiary bank accounts/wallets before scammers withdraw it at ATMs.",
        "eligibility_conditions": "Time is critical: reporting within the 'golden hour' (first 2 to 4 hours) dramatically increases the probability of funds being frozen and recovered.",
        "official_channel": "Toll-Free 1930 Helpline → National Cyber Crime Reporting Portal (cybercrime.gov.in)",
        "official_portal_url": "https://cybercrime.gov.in/",
        "escalation_options": "After dialing 1930, complete formal registration on cybercrime.gov.in. Take the generated acknowledgement to your local cyber police station to register an FIR.",
        "relevant_deadlines": "Report immediately (within 24 hours). Banks must be notified within 3 days for zero consumer liability under RBI fraud guidelines.",
        "verification_status": "verified",
        "confidence_score": 99,
        "steps": [
            {
                "step_number": 1,
                "title": "Call National Cyber Crime Helpline 1930 Immediately",
                "description": "Dial 1930 without delay. Provide the operator with your bank account, fraud transaction amount, transaction ID, and beneficiary account/UPI ID.",
                "official_url": "tel:1930",
                "action_type": "contact",
                "is_mandatory": True,
                "warnings": "Helpline operators coordinate directly with banks to freeze recipient accounts in real-time."
            },
            {
                "step_number": 2,
                "title": "Block Your Compromised Debit Card / NetBanking / UPI",
                "description": "Contact your bank helpline to immediately block cards and suspend netbanking credentials to prevent further unauthorized withdrawals.",
                "official_url": None,
                "action_type": "action",
                "is_mandatory": True,
                "warnings": "Change passwords from a different, secure phone or computer."
            },
            {
                "step_number": 3,
                "title": "Register Formal Complaint on cybercrime.gov.in",
                "description": "Log on to cybercrime.gov.in, select 'Report Financial Fraud', fill out incident details, and upload transaction screenshots and call records.",
                "official_url": "https://cybercrime.gov.in/",
                "action_type": "submit",
                "is_mandatory": True,
                "warnings": "Save the Cyber Complaint Acknowledgement Number."
            },
            {
                "step_number": 4,
                "title": "Submit Fraud Intimation to Your Bank in Writing",
                "description": "Visit your bank branch with a copy of the Cyber Crime Acknowledgement within 3 days to invoke RBI's Zero Liability Policy for third-party cyber breaches.",
                "official_url": None,
                "action_type": "contact",
                "is_mandatory": True,
                "warnings": "Always obtain a signed and stamped branch acknowledgement copy."
            }
        ],
        "evidence": [
            {"title": "SMS Alerts & Bank Statements of Fraudulent Debits", "why_needed": "Documents the exact timing and destination of stolen funds.", "is_mandatory": True},
            {"title": "Screenshots of Scammer Messages / Phishing URLs / Phone Numbers", "why_needed": "Provides digital forensic evidence for police investigation.", "is_mandatory": True},
            {"title": "Cybercrime Portal Acknowledgement Slip", "why_needed": "Required by banks to claim zero liability protection.", "is_mandatory": True}
        ],
        "sources": [
            {"title": "National Cyber Crime Reporting Portal", "url": "https://cybercrime.gov.in/", "publisher": "Ministry of Home Affairs, Government of India", "description": "Central citizen reporting portal and 1930 financial fraud helpline."},
            {"title": "RBI Circular on Customer Protection - Limiting Liability in Unauthorized Electronic Banking Transactions", "url": "https://www.rbi.org.in/", "publisher": "Reserve Bank of India", "description": "Mandates zero customer liability if reported within 3 working days."}
        ]
    }
]

def seed_database(db: Session = None):
    close_db = False
    if db is None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        close_db = True

    try:
        # 1. Seed admin user if not existing
        admin_email = settings.ADMIN_EMAIL
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            admin = User(
                email=admin_email,
                full_name="FixRoute System Administrator",
                hashed_password=hash_password(settings.ADMIN_PASSWORD),
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            logger.info(f"Provisioned Admin user: {admin_email}")

        # 2. Seed Categories
        category_map = {}
        for cat_data in CATEGORIES_DATA:
            existing_cat = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
            if not existing_cat:
                cat = Category(
                    slug=cat_data["slug"],
                    name=cat_data["name"],
                    icon=cat_data["icon"],
                    description=cat_data["description"],
                    display_order=cat_data["display_order"]
                )
                db.add(cat)
                db.flush()
                category_map[cat.slug] = cat.id
            else:
                category_map[existing_cat.slug] = existing_cat.id
        db.commit()

        # 3. Seed Problem Routes
        for r_data in ROUTES_DATA:
            cat_id = category_map.get(r_data["category_slug"])
            if not cat_id:
                continue

            existing_route = db.query(ProblemRoute).filter(ProblemRoute.slug == r_data["slug"]).first()
            if not existing_route:
                route = ProblemRoute(
                    slug=r_data["slug"],
                    title=r_data["title"],
                    category_id=cat_id,
                    subcategory=r_data["subcategory"],
                    problem_description=r_data["problem_description"],
                    keywords=r_data["keywords"],
                    jurisdiction=r_data["jurisdiction"],
                    applicable_states=r_data["applicable_states"],
                    responsible_authority=r_data["responsible_authority"],
                    authority_type=r_data["authority_type"],
                    reason_for_routing=r_data["reason_for_routing"],
                    eligibility_conditions=r_data["eligibility_conditions"],
                    official_channel=r_data["official_channel"],
                    official_portal_url=r_data["official_portal_url"],
                    escalation_options=r_data["escalation_options"],
                    relevant_deadlines=r_data["relevant_deadlines"],
                    verification_status=r_data["verification_status"],
                    confidence_score=r_data["confidence_score"],
                    verified_by="FixRoute Editorial & Regulatory Review",
                    last_verified_at=datetime.utcnow()
                )
                db.add(route)
                db.flush()

                # Add Steps
                for step in r_data.get("steps", []):
                    db.add(ResolutionStep(
                        route_id=route.id,
                        step_number=step["step_number"],
                        title=step["title"],
                        description=step["description"],
                        official_url=step.get("official_url"),
                        action_type=step.get("action_type", "action"),
                        is_mandatory=step.get("is_mandatory", True),
                        warnings=step.get("warnings")
                    ))

                # Add Evidence
                for ev in r_data.get("evidence", []):
                    db.add(EvidenceRequirement(
                        route_id=route.id,
                        title=ev["title"],
                        why_needed=ev["why_needed"],
                        is_mandatory=ev.get("is_mandatory", True),
                        file_type_hint="Document, Bill, or Screenshot"
                    ))

                # Add Sources
                for src in r_data.get("sources", []):
                    db.add(SourceReference(
                        route_id=route.id,
                        title=src["title"],
                        url=src["url"],
                        publisher=src["publisher"],
                        description=src.get("description"),
                        last_checked_at=datetime.utcnow(),
                        is_official=True
                    ))

        db.commit()
        logger.info("Successfully seeded database with Indian categories, routes, steps, evidence, and sources.")
    finally:
        if close_db:
            db.close()

if __name__ == "__main__":
    seed_database()
    print("Database seeding completed.")
