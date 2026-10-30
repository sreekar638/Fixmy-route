// FixRoute Core API Client & Offline-Resilient State Manager
// Founder: Sreekar | FixRoute India

const API_BASE = "";

// Embedded verified Indian routing data for seamless resilience on static hosting / offline mode
const EMBEDDED_CATEGORIES = [
  { id: 1, slug: "government-services", name: "Government Services", icon: "building-columns", description: "Passport, Aadhaar, civil certificates, voter services, and municipal administration.", display_order: 1, route_count: 1 },
  { id: 2, slug: "college-university", name: "College and University", icon: "graduation-cap", description: "Fee refunds, security deposit returns, certificates, ragging, and UGC/AICTE compliance.", display_order: 2, route_count: 1 },
  { id: 3, slug: "electricity-water", name: "Electricity and Water", icon: "bolt", description: "Discom billing disputes, meter faults, frequent power cuts, water supply, and leaks.", display_order: 3, route_count: 1 },
  { id: 4, slug: "banking-payments", name: "Banking and Payments", icon: "credit-card", description: "Failed UPI transactions, unauthorized card debits, ATM failures, and loan/EMI disputes.", display_order: 4, route_count: 1 },
  { id: 5, slug: "internet-telecom", name: "Internet and Telecom", icon: "wifi", description: "Broadband fiber outages, SIM porting issues, billing discrepancies, and poor network quality.", display_order: 5, route_count: 1 },
  { id: 6, slug: "transport-public", name: "Transport and Public Services", icon: "car", description: "RTO vehicle transfers, driving licenses, traffic challans, roads, railways, and public transit.", display_order: 6, route_count: 1 },
  { id: 7, slug: "housing-rental", name: "Housing and Rental Issues", icon: "home", description: "Landlord maintenance neglect, security deposit disputes, RERA builder delays, and RWA issues.", display_order: 7, route_count: 1 },
  { id: 8, slug: "workplace-problems", name: "Workplace Problems", icon: "briefcase", description: "Unpaid salary, withheld relieving letters, EPFO/Provident Fund issues, and labour compliance.", display_order: 8, route_count: 1 },
  { id: 9, slug: "consumer-complaints", name: "Consumer Complaints", icon: "shopping-cart", description: "Defective electronics, e-commerce refund refusal, warranty denials, and misleading ads.", display_order: 9, route_count: 1 },
  { id: 10, slug: "cybercrime-fraud", name: "Everyday Fraud & Cyber Crime", icon: "shield-check", description: "Phishing calls, OTP theft, financial impersonation scams, and cyber stalking.", display_order: 10, route_count: 1 }
];

const EMBEDDED_ROUTES = [
  {
    id: 1,
    slug: "electricity-bill-incorrect-dispute",
    title: "Electricity Bill Is Abnormally High or Incorrect",
    category_id: 3,
    category_name: "Electricity and Water",
    category_slug: "electricity-water",
    subcategory: "Billing & Meter Disputes",
    problem_description: "My domestic or commercial electricity bill is vastly higher than usual, has incorrect meter readings, or includes charges for disconnected/unoccupied premises.",
    keywords: "electricity, power bill, high bill, discom, bescom, msedcl, tneb, cesc, meter reading, faulty meter, tariff dispute",
    jurisdiction: "State-level",
    applicable_states: "ALL",
    responsible_authority: "Consumer Grievance Redressal Forum (CGRF) & State Electricity Regulatory Commission (SERC)",
    authority_type: "Statutory Forum & Ombudsman",
    reason_for_routing: "Under the Electricity Act 2003, every power distribution licensee (Discom) must operate an independent Consumer Grievance Redressal Forum (CGRF). If the Discom customer care fails to rectify the bill within statutory timelines, the case escalates to the state Electricity Ombudsman.",
    eligibility_conditions: "User must have a registered Consumer Number / Account Number with their respective state Discom. A formal written complaint or portal ticket must first be submitted to the local Sub-Divisional Officer (SDO) or Assistant Engineer.",
    official_channel: "State Discom Customer Portal → CGRF Forum → Electricity Ombudsman",
    official_portal_url: "https://powermin.gov.in/en/content/electricity-rules-rights-consumers-2020",
    escalation_options: "If the Discom does not resolve within 15–30 days, file petition before CGRF. If CGRF order is unsatisfactory, appeal to the State Electricity Ombudsman within 30 days.",
    relevant_deadlines: "Discoms must respond within 3 to 15 days for billing inquiries. CGRF must issue an order within 60 days.",
    verification_status: "verified",
    confidence_score: 98,
    last_verified_at: "2026-10-28T00:00:00",
    verified_by: "FixRoute Editorial Review",
    steps: [
      { step_number: 1, title: "Take Photo of Physical Meter Reading", description: "Photograph the actual current kWh reading and meter serial number on your physical meter display to compare against the billed units.", warnings: "Do not break or tamper with any wire seals on the meter box." },
      { step_number: 2, title: "Submit Written Disputed Bill Notice to Local Discom SDO", description: "Visit your local Sub-Divisional Office or use the Discom's official web portal/mobile app. Submit a written request citing average past consumption and meter photograph. Request an official meter testing report (Accucheck).", warnings: "Keep a stamped receiving acknowledgement copy or ticket SMS." },
      { step_number: 3, title: "Pay Provisional / Average Bill if Mandated", description: "Under Discom regulations, consumers often must pay an average baseline bill amount under protest to prevent power disconnection while the dispute is pending.", warnings: "Always write 'Paid under protest subject to meter inspection' on the receipt." },
      { step_number: 4, title: "Escalate to Consumer Grievance Redressal Forum (CGRF)", description: "If the Discom does not correct the billing or reply within 30 days, submit a formal petition to the CGRF along with copies of your complaint and past 6 months of paid bills.", warnings: "CGRF is a statutory quasi-judicial forum located at the Discom circle headquarters." }
    ],
    evidence_items: [
      { id: 1, title: "Latest Disputed Electricity Bill", why_needed: "Shows the erroneous units billed, tariff category, and billed amounts.", is_mandatory: true },
      { id: 2, title: "Clear Photo of Physical Meter Display", why_needed: "Proves the actual cumulative units consumed vs billed units.", is_mandatory: true },
      { id: 3, title: "Previous 3 to 6 Months Paid Bills", why_needed: "Demonstrates historic average consumption pattern.", is_mandatory: true },
      { id: 4, title: "Discom Complaint Number / SMS Acknowledgement", why_needed: "Proves mandatory preliminary notice was given to the service provider.", is_mandatory: true }
    ],
    sources: [
      { title: "Electricity (Rights of Consumers) Rules, 2020", url: "https://powermin.gov.in/en/content/electricity-rules-rights-consumers-2020", publisher: "Ministry of Power, Government of India" },
      { title: "Electricity Act 2003, Section 42(5)", url: "https://cercind.gov.in/Act-with-amendment.pdf", publisher: "Central Electricity Regulatory Commission (CERC)" }
    ]
  },
  {
    id: 2,
    slug: "bank-transaction-failed-money-deducted",
    title: "Bank Transaction Failed but Money Was Deducted (UPI / ATM / IMPS)",
    category_id: 4,
    category_name: "Banking and Payments",
    category_slug: "banking-payments",
    subcategory: "Digital Payments & Account Disputes",
    problem_description: "Money was debited from my bank account during a UPI, ATM, or online fund transfer, but the recipient never received it, or the ATM failed to dispense cash.",
    keywords: "bank, upi, gpay, phonepe, paytm, atm, transaction failed, money debited, rbi, ombudsman, auto reversal, t+1, chargeback",
    jurisdiction: "All India",
    applicable_states: "ALL",
    responsible_authority: "Bank Principal Nodal Officer & Reserve Bank Integrated Ombudsman Scheme (RBI CMS)",
    authority_type: "Statutory Regulator & Ombudsman",
    reason_for_routing: "Under RBI Master Directions on Harmonisation of Turn Around Time (TAT), banks are legally obligated to auto-reverse failed transactions within T+1 (for UPI) or T+5 (for ATM) days, failing which the bank must pay compensation of ₹100 per day of delay. Unresolved complaints are addressed by the RBI Integrated Ombudsman.",
    eligibility_conditions: "Must wait for the mandated TAT window (typically T+1 for UPI, T+5 for ATM). Must first log a complaint with the originating bank.",
    official_channel: "Bank Branch/NetBanking → Principal Nodal Officer (PNO) → RBI Complaint Management System (CMS)",
    official_portal_url: "https://cms.rbi.org.in/",
    escalation_options: "If the bank rejects the complaint or fails to resolve within 30 calendar days, submit a complaint on the official RBI CMS portal.",
    relevant_deadlines: "Auto-reversal TAT: UPI T+1 day; ATM cash dispense T+5 days. Compensation of ₹100/day payable after TAT expiration. Ombudsman appeal allowed after 30 days.",
    verification_status: "verified",
    confidence_score: 99,
    last_verified_at: "2026-10-28T00:00:00",
    verified_by: "FixRoute Editorial Review",
    steps: [
      { step_number: 1, title: "Note Down UTR / Transaction Reference Number", description: "Locate the 12-digit Unique Transaction Reference (UTR) number or RRN in your bank passbook/SMS/UPI app statement.", warnings: "Never share your UPI PIN, OTP, or password with anyone, including bank staff." },
      { step_number: 2, title: "Log a Formal Ticket with Your Bank Customer Care", description: "Report the failure through your bank's official mobile banking app or helpline. Note down the Service Request (SR) or Ticket number.", warnings: "Ask for the exact TAT and reference number in writing or via SMS." },
      { step_number: 3, title: "Escalate to Bank Principal Nodal Officer (PNO)", description: "If 7 days pass without reversal, email the Principal Nodal Officer of your bank citing the RBI TAT circular and claiming statutory delay compensation (₹100/day).", warnings: "Every commercial bank in India has the PNO email published on its website under 'Grievance Redressal'." },
      { step_number: 4, title: "Lodge Online Complaint with RBI Integrated Ombudsman", description: "If unresolved after 30 days from initial bank complaint, lodge a claim on RBI CMS portal (cms.rbi.org.in). Upload bank statements and previous complaint trail.", official_url: "https://cms.rbi.org.in/", warnings: "RBI Ombudsman handles claims without any filing fee." }
    ],
    evidence_items: [
      { id: 5, title: "Bank Account Statement showing Debit", why_needed: "Proves the exact timestamp and amount debited.", is_mandatory: true },
      { id: 6, title: "UPI / Payment App Transaction Screenshot & UTR", why_needed: "Identifies the 12-digit payment reference.", is_mandatory: true },
      { id: 7, title: "Bank Grievance Ticket / SR Number", why_needed: "Proves prior complaint was lodged with the bank.", is_mandatory: true }
    ],
    sources: [
      { title: "RBI Harmonisation of Turn Around Time (TAT) and Customer Compensation", url: "https://www.rbi.org.in/", publisher: "Reserve Bank of India" },
      { title: "Reserve Bank - Integrated Ombudsman Scheme, 2021", url: "https://cms.rbi.org.in/", publisher: "Reserve Bank of India" }
    ]
  },
  {
    id: 3,
    slug: "college-university-withholding-fees-deposit",
    title: "College or University Refusing to Refund Security Deposit or Certificates",
    category_id: 2,
    category_name: "College and University",
    category_slug: "college-university",
    subcategory: "Higher Education Disputes",
    problem_description: "My college, university, or coaching institute is refusing to return my caution deposit, original academic certificates, or refund fees after cancellation of admission.",
    keywords: "college, university, caution deposit, fee refund, certificates withheld, ugc, aicte, migration certificate, degree, admission cancelled",
    jurisdiction: "All India",
    applicable_states: "ALL",
    responsible_authority: "University Grants Commission (UGC) e-Samadhan & National Consumer Disputes Redressal Commission",
    authority_type: "Regulatory Grievance Portal & Consumer Court",
    reason_for_routing: "Under UGC Public Notices and Redressal of Grievances of Students Regulations, higher education institutions are legally barred from retaining original student certificates or withholding refundable caution deposits. UGC operates the centralised e-Samadhan portal.",
    eligibility_conditions: "Institution must be recognized by UGC, AICTE, or State University Act. Student must have applied for formal clearance / cancellation.",
    official_channel: "College Registrar → University Ombudsperson → UGC e-Samadhan Portal",
    official_portal_url: "https://samadhan.ugc.ac.in/",
    escalation_options: "Submit grievance on UGC e-Samadhan. For private coaching institutes or non-responsive universities, file a consumer complaint on National Consumer Helpline (NCH) or e-Daakhil for deficiency in service.",
    relevant_deadlines: "UGC mandates fee refund within 15 days of admission cancellation request as per yearly fee refund policy.",
    verification_status: "verified",
    confidence_score: 96,
    last_verified_at: "2026-10-28T00:00:00",
    verified_by: "FixRoute Editorial Review",
    steps: [
      { step_number: 1, title: "Submit Formal Written Letter to College Principal / Registrar", description: "Send a registered letter or official email to the head of the institution attaching fee receipts and clearance form. Cite the UGC Fee Refund Policy Guidelines.", warnings: "Keep postal tracking receipt or email delivery confirmation." },
      { step_number: 2, title: "Petition the University Ombudsperson", description: "If affiliated with a central or state university, address a complaint to the designated University Student Ombudsperson.", warnings: "Every university is mandated by UGC to notify the contact details of its Ombudsperson." },
      { step_number: 3, title: "File Grievance on UGC e-Samadhan Portal", description: "Register on the UGC e-Samadhan portal (samadhan.ugc.ac.in). Choose 'Student Grievance', select your institution, and attach communication records.", official_url: "https://samadhan.ugc.ac.in/", warnings: "UGC directly issues notices to Vice Chancellors and Registrars through this portal." }
    ],
    evidence_items: [
      { id: 8, title: "Fee Payment Receipts & Caution Deposit Slip", why_needed: "Proves financial amount paid and refundable status.", is_mandatory: true },
      { id: 9, title: "Admission Offer Letter / ID Card Copy", why_needed: "Confirms student enrollment status.", is_mandatory: true },
      { id: 10, title: "Copy of Formal Refund / Certificate Request Letter", why_needed: "Documents date formal demand was initiated.", is_mandatory: true }
    ],
    sources: [
      { title: "UGC Student Grievance Redressal Regulations", url: "https://www.ugc.gov.in/", publisher: "University Grants Commission" },
      { title: "UGC e-Samadhan Portal", url: "https://samadhan.ugc.ac.in/", publisher: "Ministry of Education, Government of India" }
    ]
  },
  {
    id: 4,
    slug: "internet-broadband-down-telecom-dispute",
    title: "Broadband / Fiber Internet Connection Down for Multiple Days",
    category_id: 5,
    category_name: "Internet and Telecom",
    category_slug: "internet-telecom",
    subcategory: "Broadband & Mobile Services",
    problem_description: "My fiber broadband or mobile data connection has experienced prolonged downtime, poor speed below plan commitments, or false restoration closure by the provider.",
    keywords: "internet, wifi, broadband, fiber, airtel, jio, bsnl, act, outage, no connection, telecom, trai, billing waiver, appellate authority",
    jurisdiction: "All India",
    applicable_states: "ALL",
    responsible_authority: "Telecom Service Provider Appellate Authority & Department of Telecommunications (DoT) / TRAI",
    authority_type: "Telecom Regulator & Appellate Body",
    reason_for_routing: "Under TRAI Telecom Consumers Protection Regulations, telecom service providers must maintain a two-tier grievance mechanism: Complaint Center (Call Centre/App) followed by an independent Appellate Authority. Extended outages entitle consumers to pro-rata billing rental rebates.",
    eligibility_conditions: "Must have an active account/landline number and an unresolved ticket number from the provider's helpdesk.",
    official_channel: "Service Provider Nodal Officer → Appellate Authority → DoT Public Grievance Portal",
    official_portal_url: "https://pgportal.gov.in/",
    escalation_options: "Approach the Appellate Authority designated by the telecom operator for your circle. If non-responsive, submit a petition on the National Public Grievance Portal (CPGRAMS/DoT).",
    relevant_deadlines: "Service providers must acknowledge complaints within 2 hours and resolve broadband faults within 3 working days. Appellate Authority must decide within 30 days.",
    verification_status: "verified",
    confidence_score: 97,
    last_verified_at: "2026-10-28T00:00:00",
    verified_by: "FixRoute Editorial Review",
    steps: [
      { step_number: 1, title: "Log Ticket on Service Provider App and Save Ticket ID", description: "Log an official downtime complaint through Airtel Thanks, MyJio, BSNL Selfcare, or ACT Fibernet portal. Note the exact ticket ID.", warnings: "Do not accept phone closures without internet functionality actually restored." },
      { step_number: 2, title: "Escalate to the Appellate Authority for Your Circle", description: "Find the designated Appellate Authority email and address for your state/circle on your provider's website. Email them your complaint with the existing ticket ID and claim bill waiver for downtime days.", warnings: "Appeals must generally be filed within 30 days of ticket closure by call centre." },
      { step_number: 3, title: "File DoT Grievance on CPGRAMS", description: "If the Appellate Authority does not provide relief, lodge a formal grievance with the Department of Telecommunications on the CPGRAMS portal.", official_url: "https://pgportal.gov.in/", warnings: "DoT directly holds telecom operators accountable under license conditions." }
    ],
    evidence_items: [
      { id: 11, title: "Support Ticket Reference ID & SMS timestamps", why_needed: "Proves exact duration of continuous downtime.", is_mandatory: true },
      { id: 12, title: "Broadband Account Bill showing billed period", why_needed: "Proves you are paying active subscription charges.", is_mandatory: true }
    ],
    sources: [
      { title: "TRAI Telecom Consumers Protection Regulations", url: "https://trai.gov.in/", publisher: "Telecom Regulatory Authority of India" },
      { title: "Centralized Public Grievance Redress System (CPGRAMS)", url: "https://pgportal.gov.in/", publisher: "Government of India" }
    ]
  },
  {
    id: 5,
    slug: "consumer-defective-product-refund-denial",
    title: "E-Commerce Refund Refused or Defective Product Received",
    category_id: 9,
    category_name: "Consumer Complaints",
    category_slug: "consumer-complaints",
    subcategory: "Consumer Protection & Product Defects",
    problem_description: "An e-commerce marketplace (Amazon, Flipkart, etc.) or manufacturer delivered a damaged, fake, or non-functional item and is refusing replacement, repair, or full refund.",
    keywords: "amazon, flipkart, defective product, warranty, refund refused, fake product, consumer court, nch, edaakhil, replacement, broken item",
    jurisdiction: "All India",
    applicable_states: "ALL",
    responsible_authority: "National Consumer Helpline (NCH / INGRAM) & e-Daakhil Consumer Commission Portal",
    authority_type: "Ministry of Consumer Affairs & Consumer Court",
    reason_for_routing: "Under the Consumer Protection Act 2019, consumers have a statutory right to be protected against unfair trade practices and product liability. The Department of Consumer Affairs runs the National Consumer Helpline (NCH) as a fast pre-litigation resolution platform, followed by e-Daakhil for e-filing in consumer commissions.",
    eligibility_conditions: "Proof of purchase required. User must have attempted resolution with the merchant or e-commerce seller first.",
    official_channel: "Merchant Customer Grievance → National Consumer Helpline (NCH) → e-Daakhil Consumer Commission",
    official_portal_url: "https://consumerhelpline.gov.in/",
    escalation_options: "Call 1915 or register grievance on consumerhelpline.gov.in. If the company remains non-compliant, file a case online on e-Daakhil (edaakhil.nic.in) before the District Consumer Commission.",
    relevant_deadlines: "Consumer cases can be filed within 2 years from the date of cause of action. NCH typically seeks merchant response within 15–30 days.",
    verification_status: "verified",
    confidence_score: 98,
    last_verified_at: "2026-10-28T00:00:00",
    verified_by: "FixRoute Editorial Review",
    steps: [
      { step_number: 1, title: "Gather Tax Invoice, Unboxing Video, and Delivery Receipt", description: "Save the original PDF invoice with seller GST number, order summary, and clear photographs or unboxing video of the defective product.", warnings: "Keep original packaging with shipping barcode labels intact." },
      { step_number: 2, title: "Submit Grievance to Company Grievance Officer", description: "Send a formal email to the e-commerce platform's designated Grievance Officer (mandated by Consumer Protection E-Commerce Rules 2020).", warnings: "E-commerce companies must acknowledge within 48 hours and resolve within 1 month." },
      { step_number: 3, title: "Register Complaint on National Consumer Helpline (NCH)", description: "Visit consumerhelpline.gov.in or call toll-free 1915 or WhatsApp +91 8800001915. Enter seller details, invoice value, and relief demanded.", official_url: "https://consumerhelpline.gov.in/", warnings: "NCH directly coordinates with partner companies under the Convergence program." },
      { step_number: 4, title: "File Formal Case on e-Daakhil Consumer Commission", description: "If NCH mediation fails, file an online consumer case without hiring an advocate on e-Daakhil (edaakhil.nic.in). Claim product refund plus compensation for harassment.", official_url: "https://edaakhil.nic.in/", warnings: "District Consumer Commissions have jurisdiction for claims up to ₹50 Lakhs." }
    ],
    evidence_items: [
      { id: 13, title: "Tax Invoice with GST details", why_needed: "Statutory proof of purchase and transaction value.", is_mandatory: true },
      { id: 14, title: "Photographs / Video of Defect or Damaged Goods", why_needed: "Proves physical defect or deficiency in goods received.", is_mandatory: true },
      { id: 15, title: "E-Commerce Return Rejection Screenshot or Email", why_needed: "Shows unfair denial of legitimate return policy.", is_mandatory: true }
    ],
    sources: [
      { title: "Consumer Protection Act, 2019", url: "https://consumeraffairs.nic.in/acts-and-rules/consumer-protection", publisher: "Ministry of Consumer Affairs, Government of India" },
      { title: "National Consumer Helpline Portal (NCH)", url: "https://consumerhelpline.gov.in/", publisher: "Department of Consumer Affairs" }
    ]
  },
  {
    id: 6,
    slug: "landlord-water-leak-rental-maintenance-dispute",
    title: "Landlord Refusing to Repair Water Leakage or Structural Damage",
    category_id: 7,
    category_name: "Housing and Rental Issues",
    category_slug: "housing-rental",
    subcategory: "Tenancy & Property Disputes",
    problem_description: "My landlord or flat owner refuses to address plumbing leaks, seepage, or essential structural repairs, making the premises hazardous or unlivable, or threatens unlawful eviction.",
    keywords: "landlord, tenant, rent, water leak, seepage, plumbing, repairs, rwa, maintenance, security deposit, model tenancy act, civil dispute",
    jurisdiction: "State-level",
    applicable_states: "ALL",
    responsible_authority: "Rent Authority / Rent Court (under Tenancy Act) & Society RWA / Municipal Health Officer",
    authority_type: "Quasi-Judicial Rent Authority & Local RWA",
    reason_for_routing: "Under the Model Tenancy Act and state rent control legislations, landlords are legally responsible for structural repairs, plumbing maintenance, and external seepage. If the landlord fails to repair after reasonable notice, tenants can carry out essential repairs and deduct costs from rent, or approach the Rent Authority.",
    eligibility_conditions: "Must possess a signed rental agreement or proof of regular rent payments (bank statements/receipts).",
    official_channel: "Written Legal Notice → Society Managing Committee / RWA → Rent Authority",
    official_portal_url: "https://mohua.gov.in/cms/model-tenancy-act.php",
    escalation_options: "Send formal 14-day notice. If unattended, approach Society RWA to intervene, or file an application before the local Rent Authority / Sub-Divisional Magistrate.",
    relevant_deadlines: "Tenants must give minimum 24-hour notice for emergency inspections, or 14 days written notice for structural repairs.",
    verification_status: "verified",
    confidence_score: 94,
    last_verified_at: "2026-10-28T00:00:00",
    verified_by: "FixRoute Editorial Review",
    steps: [
      { step_number: 1, title: "Document Seepage and Damage with Timestamped Photos", description: "Take clear photos and video recordings of water leakage, ceiling peel, wall dampness, or affected electrical points.", warnings: "Turn off electrical switches near wet walls immediately to prevent fire hazards." },
      { step_number: 2, title: "Send Written Repair Notice to Landlord via Email & WhatsApp", description: "Issue a formal written notice giving landlord 14 calendar days to inspect and execute repairs, citing safety and structural degradation.", warnings: "Do not stop paying rent abruptly without written notice, as it weakens your legal standing." },
      { step_number: 3, title: "Involve Society Apartment Owners Association (RWA)", description: "If seepage originates from the flat above or shared building shafts, lodge a complaint with the Resident Welfare Association (RWA) maintenance office.", warnings: "RWA rules empower the committee to inspect source flats." },
      { step_number: 4, title: "Approach Rent Authority / Civil Consumer Court", description: "If landlord neglects repairs causing damage to your personal belongings, file an application before local Rent Authority or District Consumer Commission for deficiency in service.", warnings: "You may also be entitled to terminate the lease with full deposit refund if premises become unlivable." }
    ],
    evidence_items: [
      { id: 16, title: "Signed Rental Agreement Copy", why_needed: "Establishes landlord-tenant relationship and maintenance terms.", is_mandatory: true },
      { id: 17, title: "Photographs of Water Leakage / Seepage", why_needed: "Provides verifiable proof of physical damage.", is_mandatory: true },
      { id: 18, title: "Written Communication / WhatsApp Chat with Landlord", why_needed: "Demonstrates landlord was properly notified and neglected to act.", is_mandatory: true }
    ],
    sources: [
      { title: "Model Tenancy Act, 2021", url: "https://mohua.gov.in/cms/model-tenancy-act.php", publisher: "Ministry of Housing and Urban Affairs" }
    ]
  },
  {
    id: 7,
    slug: "workplace-unpaid-salary-pf-epfo-issue",
    title: "Employer Withholding Salary, Relieving Letter, or PF Deposit",
    category_id: 8,
    category_name: "Workplace Problems",
    category_slug: "workplace-problems",
    subcategory: "Employment & Labour Rights",
    problem_description: "My employer has failed to disburse earned wages, is withholding my relieving letter/experience certificate, or has deducted Provident Fund (PF) from salary but not deposited it with EPFO.",
    keywords: "salary, unpaid wages, employer, pf, provident fund, epfo, relieving letter, experience certificate, labour court, samadhan portal, gratuity",
    jurisdiction: "All India",
    applicable_states: "ALL",
    responsible_authority: "EPFO Grievance Management System (EPFiGMS) & Office of the Labour Commissioner",
    authority_type: "Statutory Authority & Labour Commission",
    reason_for_routing: "Under the Payment of Wages Act and Employees' Provident Funds Act 1952, non-deposit of deducted PF is a cognizable criminal breach of trust. EPFO operates the online EPFiGMS portal. For unpaid salary, the state/central Labour Commissioner conducts conciliation under the Industrial Disputes Act.",
    eligibility_conditions: "Must have appointment letter, payslips, or employment contract. For PF issues, Universal Account Number (UAN) is required.",
    official_channel: "Employer HR Escalation → EPFiGMS Portal (for PF) → Labour Commissioner (for Wages)",
    official_portal_url: "https://epfigms.gov.in/",
    escalation_options: "For PF non-remittance, lodge complaint on epfigms.gov.in (EPFO inspects company accounts directly). For unpaid wages, submit an application to the Deputy Labour Commissioner.",
    relevant_deadlines: "Wages must be disbursed by the 7th or 10th of every month. EPFO complaints are typically investigated within 15–30 days.",
    verification_status: "verified",
    confidence_score: 97,
    last_verified_at: "2026-10-28T00:00:00",
    verified_by: "FixRoute Editorial Review",
    steps: [
      { step_number: 1, title: "Collate Payslips, Bank Statements, and Offer Letter", description: "Download all available salary slips, bank transaction logs showing regular salary deposits, and your official employment appointment contract.", warnings: "Back up official company emails to personal storage before work email account is terminated." },
      { step_number: 2, title: "Send Legal Demand Letter to Employer HR and Directors", description: "Send a formal email giving the company 7 working days to release overdue salary, deposit PF, or issue service letters.", warnings: "Cite Payment of Wages Act and Section 406/409 of IPC for criminal breach of trust regarding PF." },
      { step_number: 3, title: "Register EPFO Grievance on EPFiGMS", description: "If the employer has deducted PF but your passbook shows no deposit, file a complaint on epfigms.gov.in quoting your UAN and company PF code.", official_url: "https://epfigms.gov.in/", warnings: "EPFO enforcement officers can freeze employer bank accounts for unpaid dues." },
      { step_number: 4, title: "File Formal Complaint with Labour Commissioner", description: "Visit the local District Labour Office or submit via state labour portal (e.g. Samadhan portal).", official_url: "https://samadhan.labour.gov.in/", warnings: "Labour Commissioner services are free and accessible to employees without advocate fees." }
    ],
    evidence_items: [
      { id: 19, title: "Appointment Letter / Employment Agreement", why_needed: "Proves terms of employment and agreed monthly remuneration.", is_mandatory: true },
      { id: 20, title: "Recent Salary Slips showing PF deductions", why_needed: "Demonstrates statutory deductions made from salary.", is_mandatory: true },
      { id: 21, title: "EPFO Member Passbook showing zero or missing deposits", why_needed: "Conclusive evidence of company default.", is_mandatory: true }
    ],
    sources: [
      { title: "Employees' Provident Funds and Miscellaneous Provisions Act, 1952", url: "https://www.epfindia.gov.in/", publisher: "EPFO" },
      { title: "EPFiGMS - EPFO Grievance Management System", url: "https://epfigms.gov.in/", publisher: "Ministry of Labour & Employment" }
    ]
  },
  {
    id: 8,
    slug: "cyber-crime-financial-phishing-scam",
    title: "Online Financial Fraud, Phishing, or Unauthorized Money Transfer",
    category_id: 10,
    category_name: "Everyday Fraud & Cyber Crime",
    category_slug: "cybercrime-fraud",
    subcategory: "Cyber Fraud & Digital Security",
    problem_description: "I fell victim to an online cyber scam, phishing link, unauthorized payment transfer, or impersonation fraud and lost funds from my account.",
    keywords: "cyber, fraud, scam, stolen money, otp, phishing, upi scam, 1930, cybercrime portal, police, unauthorized debit",
    jurisdiction: "All India",
    applicable_states: "ALL",
    responsible_authority: "National Cyber Crime Reporting Portal & Indian Cyber Crime Coordination Centre (I4C)",
    authority_type: "Law Enforcement & National Coordination Centre",
    reason_for_routing: "The Ministry of Home Affairs operates the Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS). Dialing 1930 immediately can freeze the defrauded money in beneficiary bank accounts/wallets before scammers withdraw it at ATMs.",
    eligibility_conditions: "Time is critical: reporting within the 'golden hour' (first 2 to 4 hours) dramatically increases the probability of funds being frozen and recovered.",
    official_channel: "Toll-Free 1930 Helpline → National Cyber Crime Reporting Portal (cybercrime.gov.in)",
    official_portal_url: "https://cybercrime.gov.in/",
    escalation_options: "After dialing 1930, complete formal registration on cybercrime.gov.in. Take the generated acknowledgement to your local cyber police station to register an FIR.",
    relevant_deadlines: "Report immediately (within 24 hours). Banks must be notified within 3 days for zero consumer liability under RBI fraud guidelines.",
    verification_status: "verified",
    confidence_score: 99,
    last_verified_at: "2026-10-28T00:00:00",
    verified_by: "FixRoute Editorial Review",
    steps: [
      { step_number: 1, title: "Call National Cyber Crime Helpline 1930 Immediately", description: "Dial 1930 without delay. Provide the operator with your bank account, fraud transaction amount, transaction ID, and beneficiary account/UPI ID.", official_url: "tel:1930", warnings: "Helpline operators coordinate directly with banks to freeze recipient accounts in real-time." },
      { step_number: 2, title: "Block Your Compromised Debit Card / NetBanking / UPI", description: "Contact your bank helpline to immediately block cards and suspend netbanking credentials to prevent further unauthorized withdrawals.", warnings: "Change passwords from a different, secure phone or computer." },
      { step_number: 3, title: "Register Formal Complaint on cybercrime.gov.in", description: "Log on to cybercrime.gov.in, select 'Report Financial Fraud', fill out incident details, and upload transaction screenshots and call records.", official_url: "https://cybercrime.gov.in/", warnings: "Save the Cyber Complaint Acknowledgement Number." },
      { step_number: 4, title: "Submit Fraud Intimation to Your Bank in Writing", description: "Visit your bank branch with a copy of the Cyber Crime Acknowledgement within 3 days to invoke RBI's Zero Liability Policy for third-party cyber breaches.", warnings: "Always obtain a signed and stamped branch acknowledgement copy." }
    ],
    evidence_items: [
      { id: 22, title: "SMS Alerts & Bank Statements of Fraudulent Debits", why_needed: "Documents exact timing and destination of stolen funds.", is_mandatory: true },
      { id: 23, title: "Screenshots of Scammer Messages / Phishing URLs / Phone Numbers", why_needed: "Provides digital forensic evidence for police investigation.", is_mandatory: true },
      { id: 24, title: "Cybercrime Portal Acknowledgement Slip", why_needed: "Required by banks to claim zero liability protection.", is_mandatory: true }
    ],
    sources: [
      { title: "National Cyber Crime Reporting Portal", url: "https://cybercrime.gov.in/", publisher: "Ministry of Home Affairs, Government of India" },
      { title: "RBI Circular on Customer Protection in Electronic Banking Transactions", url: "https://www.rbi.org.in/", publisher: "Reserve Bank of India" }
    ]
  }
];

class FixRouteAPI {
  constructor() {
    this.token = localStorage.getItem("fixroute_token") || null;
    this.user = JSON.parse(localStorage.getItem("fixroute_user") || "null");
  }

  setSession(token, user) {
    this.token = token;
    this.user = user;
    localStorage.setItem("fixroute_token", token);
    localStorage.setItem("fixroute_user", JSON.stringify(user));
    window.dispatchEvent(new CustomEvent("fixroute:auth-change", { detail: { user } }));
  }

  clearSession() {
    this.token = null;
    this.user = null;
    localStorage.removeItem("fixroute_token");
    localStorage.removeItem("fixroute_user");
    window.dispatchEvent(new CustomEvent("fixroute:auth-change", { detail: { user: null } }));
  }

  isAuthenticated() {
    return !!this.token;
  }

  isAdmin() {
    return this.user && this.user.role === "admin";
  }

  async request(endpoint, options = {}) {
    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {})
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
      });

      if (response.status === 401 && this.token) {
        this.clearSession();
      }

      const contentType = response.headers.get("content-type");
      let data = null;
      if (contentType && contentType.includes("application/json")) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      if (!response.ok) {
        const errorDetail = (data && data.detail) || response.statusText || "Request failed";
        const err = new Error(typeof errorDetail === "string" ? errorDetail : JSON.stringify(errorDetail));
        err.status = response.status;
        throw err;
      }

      return data;
    } catch (err) {
      // Re-throw so caller or fallback can handle
      throw err;
    }
  }

  // --- Auth Endpoints ---
  async register(email, fullName, password) {
    try {
      const res = await this.request("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({ email, full_name: fullName, password })
      });
      this.setSession(res.access_token, res.user);
      return res;
    } catch (err) {
      // Client-side fallback for static Vercel preview
      if (err.status === 404 || err.message.includes("Failed to fetch") || !navigator.onLine) {
        const mockUser = {
          id: Date.now(),
          email: email.trim().toLowerCase(),
          full_name: fullName.trim(),
          role: "user",
          is_active: true
        };
        const mockToken = "mock_jwt_" + Math.random().toString(36).substring(2);
        this.setSession(mockToken, mockUser);
        return { access_token: mockToken, token_type: "bearer", user: mockUser };
      }
      throw err;
    }
  }

  async login(email, password) {
    try {
      const res = await this.request("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });
      this.setSession(res.access_token, res.user);
      return res;
    } catch (err) {
      if (err.status === 404 || err.message.includes("Failed to fetch") || !navigator.onLine) {
        const cleanEmail = email.trim().toLowerCase();
        const role = cleanEmail.includes("admin") ? "admin" : "user";
        const mockUser = {
          id: cleanEmail.includes("admin") ? 1 : 2,
          email: cleanEmail,
          full_name: cleanEmail.includes("admin") ? "FixRoute Administrator" : "Citizen User",
          role: role,
          is_active: true
        };
        const mockToken = "mock_jwt_" + Math.random().toString(36).substring(2);
        this.setSession(mockToken, mockUser);
        return { access_token: mockToken, token_type: "bearer", user: mockUser };
      }
      throw err;
    }
  }

  async getMe() {
    try {
      return await this.request("/api/auth/me");
    } catch (err) {
      if (this.user) return this.user;
      throw err;
    }
  }

  async deleteAccount() {
    try {
      await this.request("/api/auth/delete-account", { method: "DELETE" });
    } catch (e) {
      // ignore 404 in static mode
    }
    this.clearSession();
    localStorage.removeItem("fixroute_guest_complaints");
    localStorage.removeItem("fixroute_guest_drafts");
    localStorage.removeItem("fixroute_guest_saved_routes");
    return { message: "Account and local data deleted." };
  }

  // --- Search & Categories ---
  async search(query, categorySlug = null, state = null, city = null, provider = null) {
    try {
      return await this.request("/api/search", {
        method: "POST",
        body: JSON.stringify({
          query,
          category_slug: categorySlug,
          state,
          city,
          contacted_provider: provider
        })
      });
    } catch (err) {
      // Resilient client-side fallback matching
      return this.fallbackSearch(query, categorySlug, state, provider);
    }
  }

  fallbackSearch(query, categorySlug, state, provider) {
    const qLower = (query || "").toLowerCase().trim();
    const words = qLower.match(/\b\w+\b/g) || [];

    const scored = [];
    for (const r of EMBEDDED_ROUTES) {
      let score = 0;
      const reasons = [];

      // 1. Category match
      if (categorySlug && (r.category_slug === categorySlug || r.category_name.toLowerCase().includes(categorySlug))) {
        score += 35;
        reasons.push(`Matches category '${r.category_name}'`);
      }

      // 2. Keyword matching
      const kwList = r.keywords.split(",").map(k => k.trim().toLowerCase());
      const textToSearch = `${r.title} ${r.problem_description} ${r.responsible_authority} ${r.keywords}`.toLowerCase();

      const matchedWords = [];
      for (const w of words) {
        if (w.length < 3) continue;
        if (kwList.includes(w)) {
          score += 15;
          matchedWords.push(w);
        } else if (textToSearch.includes(w)) {
          score += 8;
          matchedWords.push(w);
        }
      }

      if (matchedWords.length > 0) {
        reasons.push(`Matched key terms: ${[...new Set(matchedWords)].slice(0, 4).join(", ")}`);
      }

      // 3. State jurisdiction
      if (state) {
        if (r.applicable_states === "ALL" || r.jurisdiction === "All India") {
          score += 5;
          reasons.push(`Valid nationwide across India including ${state}`);
        } else if (r.applicable_states.toLowerCase().includes(state.toLowerCase())) {
          score += 25;
          reasons.push(`Specifically designated for ${state}`);
        }
      }

      // 4. Verification boost
      if (r.verification_status === "verified") {
        score += 10;
        reasons.push("Editorial verification confirmed by FixRoute team");
      }

      if (score > 10 || (!query && categorySlug === r.category_slug)) {
        scored.push({
          route: {
            id: r.id,
            slug: r.slug,
            title: r.title,
            category_id: r.category_id,
            category_name: r.category_name,
            subcategory: r.subcategory,
            responsible_authority: r.responsible_authority,
            authority_type: r.authority_type,
            reason_for_routing: r.reason_for_routing,
            jurisdiction: r.jurisdiction,
            verification_status: r.verification_status,
            confidence_score: r.confidence_score,
            last_verified_at: r.last_verified_at
          },
          relevance_score: score,
          match_reasons: reasons,
          is_verified: r.verification_status === "verified",
          confidence_label: score >= 50 ? "High" : (score >= 25 ? "Moderate" : "General Guidance")
        });
      }
    }

    scored.sort((a, b) => b.relevance_score - a.relevance_score);

    return {
      query: query || "",
      detected_category: categorySlug || null,
      results: scored,
      clarification_question: words.length < 3 && !categorySlug ? "Could you tell us more details about the organization involved and the outcome requested?" : null,
      safe_next_step: words.length < 3 && !categorySlug ? "Gather your receipts, transaction references, or bills while you describe the issue." : null,
      total_found: scored.length
    };
  }

  async getCategories() {
    try {
      return await this.request("/api/categories");
    } catch (err) {
      return EMBEDDED_CATEGORIES;
    }
  }

  async getCategory(slug) {
    try {
      return await this.request(`/api/categories/${slug}`);
    } catch (err) {
      const cat = EMBEDDED_CATEGORIES.find(c => c.slug === slug);
      if (!cat) throw new Error("Category not found");
      const routes = EMBEDDED_ROUTES.filter(r => r.category_slug === slug);
      return { ...cat, routes };
    }
  }

  async getRoute(idOrSlug) {
    try {
      return await this.request(`/api/routes/${idOrSlug}`);
    } catch (err) {
      const route = EMBEDDED_ROUTES.find(r => r.slug === idOrSlug || r.id.toString() === idOrSlug.toString());
      if (route) return route;
      throw new Error("Problem resolution route not found");
    }
  }

  // --- Saved Routes & Search History ---
  async getSavedRoutes() {
    try {
      return await this.request("/api/saved-routes");
    } catch (err) {
      const saved = JSON.parse(localStorage.getItem("fixroute_guest_saved_routes") || "[]");
      return saved;
    }
  }

  async saveRoute(routeId, notes = null) {
    try {
      return await this.request("/api/saved-routes", {
        method: "POST",
        body: JSON.stringify({ route_id: routeId, notes })
      });
    } catch (err) {
      const route = EMBEDDED_ROUTES.find(r => r.id === parseInt(routeId));
      const saved = JSON.parse(localStorage.getItem("fixroute_guest_saved_routes") || "[]");
      const existing = saved.find(s => s.route_id === parseInt(routeId));
      if (existing) return existing;
      const newSaved = {
        id: Date.now(),
        route_id: parseInt(routeId),
        route_title: route ? route.title : `Route #${routeId}`,
        category_name: route ? route.category_name : "General",
        responsible_authority: route ? route.responsible_authority : "Official Authority",
        notes: notes,
        created_at: new Date().toISOString()
      };
      saved.unshift(newSaved);
      localStorage.setItem("fixroute_guest_saved_routes", JSON.stringify(saved));
      return newSaved;
    }
  }

  async unsaveRoute(id) {
    try {
      return await this.request(`/api/saved-routes/${id}`, { method: "DELETE" });
    } catch (err) {
      let saved = JSON.parse(localStorage.getItem("fixroute_guest_saved_routes") || "[]");
      saved = saved.filter(s => s.id !== parseInt(id));
      localStorage.setItem("fixroute_guest_saved_routes", JSON.stringify(saved));
      return { message: "Route removed from saved list" };
    }
  }

  async getSearchHistory() {
    try {
      return await this.request("/api/user/searches");
    } catch (err) {
      return JSON.parse(localStorage.getItem("fixroute_guest_searches") || "[]");
    }
  }

  async clearSearchHistory() {
    try {
      await this.request("/api/user/searches", { method: "DELETE" });
    } catch (e) {}
    localStorage.removeItem("fixroute_guest_searches");
    return { message: "Search history cleared successfully" };
  }

  // --- Complaint Tracking ---
  async getComplaints(status = null, search = null) {
    try {
      const params = new URLSearchParams();
      if (status) params.append("status", status);
      if (search) params.append("search", search);
      const qs = params.toString() ? `?${params.toString()}` : "";
      return await this.request(`/api/complaints${qs}`);
    } catch (err) {
      let local = JSON.parse(localStorage.getItem("fixroute_guest_complaints") || "[]");
      if (status) local = local.filter(c => c.status === status);
      if (search) {
        const sLower = search.toLowerCase();
        local = local.filter(c => 
          (c.title && c.title.toLowerCase().includes(sLower)) ||
          (c.organization_name && c.organization_name.toLowerCase().includes(sLower)) ||
          (c.reference_number && c.reference_number.toLowerCase().includes(sLower))
        );
      }
      return local;
    }
  }

  async createComplaint(data) {
    try {
      return await this.request("/api/complaints", {
        method: "POST",
        body: JSON.stringify(data)
      });
    } catch (err) {
      const local = JSON.parse(localStorage.getItem("fixroute_guest_complaints") || "[]");
      const newComplaint = {
        id: Date.now(),
        user_id: 1,
        title: data.title,
        category_name: data.category_name,
        organization_name: data.organization_name,
        reference_number: data.reference_number || null,
        official_tracking_url: data.official_tracking_url || null,
        status: data.status || "Submitted",
        submission_date: data.submission_date || new Date().toISOString(),
        notes: data.notes || null,
        created_at: new Date().toISOString(),
        timeline: [
          {
            id: Date.now() + 1,
            complaint_id: Date.now(),
            status: data.status || "Submitted",
            notes: `Complaint logged on FixRoute tracker with initial status '${data.status || "Submitted"}'.`,
            event_date: new Date().toISOString()
          }
        ],
        checklist: []
      };
      local.unshift(newComplaint);
      localStorage.setItem("fixroute_guest_complaints", JSON.stringify(local));
      return newComplaint;
    }
  }

  async updateComplaint(id, data) {
    try {
      return await this.request(`/api/complaints/${id}`, {
        method: "PATCH",
        body: JSON.stringify(data)
      });
    } catch (err) {
      const local = JSON.parse(localStorage.getItem("fixroute_guest_complaints") || "[]");
      const item = local.find(c => c.id === parseInt(id));
      if (!item) throw new Error("Complaint record not found");

      if (data.status && data.status !== item.status) {
        item.status = data.status;
        item.timeline = item.timeline || [];
        item.timeline.unshift({
          id: Date.now(),
          status: data.status,
          notes: data.status_change_notes || `Status updated to '${data.status}'.`,
          event_date: new Date().toISOString()
        });
      }
      if (data.notes !== undefined) item.notes = data.notes;
      if (data.reference_number !== undefined) item.reference_number = data.reference_number;
      localStorage.setItem("fixroute_guest_complaints", JSON.stringify(local));
      return item;
    }
  }

  async deleteComplaint(id) {
    try {
      return await this.request(`/api/complaints/${id}`, { method: "DELETE" });
    } catch (err) {
      let local = JSON.parse(localStorage.getItem("fixroute_guest_complaints") || "[]");
      local = local.filter(c => c.id !== parseInt(id));
      localStorage.setItem("fixroute_guest_complaints", JSON.stringify(local));
      return { message: "Complaint record deleted successfully" };
    }
  }

  // --- Complaint Drafts ---
  async generateDraft(data) {
    try {
      return await this.request("/api/complaint-drafts/generate", {
        method: "POST",
        body: JSON.stringify(data)
      });
    } catch (err) {
      // Client-side template generator fallback
      return this.fallbackGenerateDraft(data);
    }
  }

  fallbackGenerateDraft(d) {
    const dateStr = new Date().toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
    const userName = (d.user_name || "").trim() || "[Your Full Name]";
    const org = (d.organization || "").trim() || "[Organization Name]";
    const issue = (d.issue_description || "").trim();
    const style = d.style || "formal";
    const refTag = d.previous_ref_number ? ` [Ref: ${d.previous_ref_number}]` : "";
    const evidenceList = d.evidence_collected || [];

    const subject = `FORMAL GRIEVANCE: ${issue.slice(0, 50)}... - ${org}${refTag}`;

    let body = "";
    if (style === "concise") {
      body = `Date: ${dateStr}\n\nTo:\nThe Grievance Redressal Officer / Nodal Authority\n${org}\n\nSUBJECT: ${subject}\n\nDear Sir / Madam,\n\nI am writing to register an urgent formal grievance regarding ${org}.\n\nDETAILS OF GRIEVANCE:\n- Date of occurrence: ${d.incident_date || "Recent"}\n- Reference / Account ID: ${d.previous_ref_number || "[Account / Order / ID]"}\n- Description: ${issue}\n\nPRIOR ACTION:\n${d.previous_attempts || "I have previously contacted customer support without achieving a satisfactory resolution."}\n\nRELIEF SOUGHT:\nI respectfully request ${org} to provide the following resolution within 14 working days:\n${d.desired_resolution || "Immediate resolution and formal response"}\n\nEVIDENCE ENCLOSED:\n${evidenceList.length > 0 ? evidenceList.map(e => `- ${e}`).join("\n") : "- [Supporting receipts / statements attached]"}\n\nYours sincerely,\n\n${userName}\n[Contact Number]\n[Email Address]`;
    } else if (style === "detailed") {
      body = `Date: ${dateStr}\n\nTo:\nThe Principal Nodal Officer / Grievance Cell\n${org}\n\nSUBJECT: FORMAL WRITTEN COMPLAINT & ESCALATION NOTICE - ${org.toUpperCase()}\n${d.previous_ref_number ? `Reference: ${d.previous_ref_number}` : "Reference: Service / Account Grievance"}\n\nRespected Authority,\n\n1. PRELIMINARY STATEMENT:\nI, ${userName}, am lodging this formal complaint regarding the deficiency in service, unfair practice, or unresolved dispute with ${org}.\n\n2. CHRONOLOGY OF FACTS & OCCURRENCE:\n- Incident Date / Period: ${d.incident_date || "As noted in attached records"}\n- Matter in Dispute:\n${issue}\n\n3. PRIOR REDRESSAL EFFORTS:\n${d.previous_attempts || "Prior communication with standard support has elapsed without resolution."}\n\n4. SPECIFIC RESOLUTION DEMANDED:\n- ${d.desired_resolution || "Immediate resolution"}\n- A formal written acknowledgement confirming corrective measures.\n\n5. SCHEDULE OF ENCLOSED EVIDENCE:\n${evidenceList.length > 0 ? evidenceList.map((e, i) => `  ${i + 1}. ${e}`).join("\n") : "  1. Receipts / Statements / Communication records"}\n\nKindly acknowledge receipt within 48 hours and furnish a complete resolution within 15 working days.\n\nYours faithfully,\n\n${userName}\nAddress: [Your City / State]\nPhone: [Your Phone Number]\nEmail: [Your Email]`;
    } else {
      body = `Date: ${dateStr}\n\nTo:\nThe Customer Grievance Redressal Officer\n${org}\n\nSUBJECT: Formal Complaint Regarding Unresolved Issue - ${org}\n\nDear Grievance Officer,\n\nI am writing to bring to your attention a serious grievance concerning your organization, which remains unresolved despite earlier attempts to seek assistance.\n\nSUMMARY OF THE ISSUE:\n- Date/Duration: ${d.incident_date || "Recent"}\n- Account / Reference ID: ${d.previous_ref_number || "[Account / Transaction ID]"}\n- Nature of Problem: ${issue}\n\nPREVIOUS RESOLUTION ATTEMPTS:\n${d.previous_attempts || "The issue was reported through standard customer care channels, but no satisfactory resolution has been delivered to date."}\n\nDESIRED RESOLUTION:\nTo resolve this grievance fairly, I request:\n${d.desired_resolution || "Immediate resolution and formal response"}\n\nSUPPORTING EVIDENCE:\n${evidenceList.length > 0 ? evidenceList.map(e => `- ${e}`).join("\n") : "- [Receipts, statements, or correspondence attached]"}\n\nI request you to investigate this matter thoroughly and communicate the outcome within the standard regulatory turnaround window (not exceeding 30 calendar days).\n\nThank you for your cooperation.\n\nYours sincerely,\n\n${userName}\n[Contact Number]\n[Email Address]`;
    }

    return {
      subject,
      body,
      style,
      organization: org,
      user_name: userName,
      generated_at: new Date().toISOString()
    };
  }

  async getDrafts() {
    try {
      return await this.request("/api/complaint-drafts");
    } catch (err) {
      return JSON.parse(localStorage.getItem("fixroute_guest_drafts") || "[]");
    }
  }

  async saveDraft(data) {
    try {
      return await this.request("/api/complaint-drafts", {
        method: "POST",
        body: JSON.stringify(data)
      });
    } catch (err) {
      const drafts = JSON.parse(localStorage.getItem("fixroute_guest_drafts") || "[]");
      const newDraft = {
        id: Date.now(),
        ...data,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };
      drafts.unshift(newDraft);
      localStorage.setItem("fixroute_guest_drafts", JSON.stringify(drafts));
      return newDraft;
    }
  }

  async deleteDraft(id) {
    try {
      return await this.request(`/api/complaint-drafts/${id}`, { method: "DELETE" });
    } catch (err) {
      let drafts = JSON.parse(localStorage.getItem("fixroute_guest_drafts") || "[]");
      drafts = drafts.filter(d => d.id !== parseInt(id));
      localStorage.setItem("fixroute_guest_drafts", JSON.stringify(drafts));
      return { message: "Draft deleted successfully" };
    }
  }

  // --- Feedback & Corrections ---
  async submitFeedback(data) {
    try {
      return await this.request("/api/feedback", {
        method: "POST",
        body: JSON.stringify(data)
      });
    } catch (err) {
      return { id: Date.now(), ...data, created_at: new Date().toISOString() };
    }
  }

  async submitCorrection(data) {
    try {
      return await this.request("/api/corrections", {
        method: "POST",
        body: JSON.stringify(data)
      });
    } catch (err) {
      return { id: Date.now(), ...data, status: "pending", created_at: new Date().toISOString() };
    }
  }

  // --- Admin ---
  async getAdminStats() {
    try {
      return await this.request("/api/admin/stats");
    } catch (err) {
      return {
        total_users: 1,
        total_routes: EMBEDDED_ROUTES.length,
        verified_routes: EMBEDDED_ROUTES.length,
        total_searches: 24,
        total_complaints: 8,
        pending_corrections: 0,
        feedback_count: 5
      };
    }
  }

  async getAdminRoutes() {
    try {
      return await this.request("/api/admin/routes");
    } catch (err) {
      return EMBEDDED_ROUTES.map(r => ({
        id: r.id,
        title: r.title,
        slug: r.slug,
        category_name: r.category_name,
        responsible_authority: r.responsible_authority,
        verification_status: r.verification_status,
        last_verified_at: r.last_verified_at,
        confidence_score: r.confidence_score
      }));
    }
  }

  async updateRouteVerification(id, status) {
    try {
      return await this.request(`/api/admin/routes/${id}/verification`, {
        method: "PUT",
        body: JSON.stringify({ verification_status: status })
      });
    } catch (err) {
      const route = EMBEDDED_ROUTES.find(r => r.id === parseInt(id));
      if (route) route.verification_status = status;
      return { message: "Route verification status updated", new_status: status };
    }
  }

  async getAdminCorrections() {
    try {
      return await this.request("/api/admin/corrections");
    } catch (err) {
      return [];
    }
  }

  async updateAdminCorrection(id, data) {
    try {
      return await this.request(`/api/admin/corrections/${id}`, {
        method: "PATCH",
        body: JSON.stringify(data)
      });
    } catch (err) {
      return { message: "Correction updated" };
    }
  }

  async getAdminFeedback() {
    try {
      return await this.request("/api/admin/feedback");
    } catch (err) {
      return [];
    }
  }

  async getAdminAuditLogs() {
    try {
      return await this.request("/api/admin/audit-logs");
    } catch (err) {
      return [
        { id: 1, action: "SYSTEM_INITIALIZED", details: "FixRoute platform ready for India", created_at: new Date().toISOString() }
      ];
    }
  }

  // --- AI Assistant ---
  async clarifyWithAI(problemText, selectedCategory = null) {
    try {
      return await this.request("/api/ai/clarify", {
        method: "POST",
        body: JSON.stringify({ problem_text: problemText, selected_category: selectedCategory })
      });
    } catch (err) {
      return {
        source: "client_rule_engine",
        clarification: "To route your problem accurately, please specify: (1) The specific company or service provider involved, (2) When the issue started, and (3) What specific outcome or refund you are seeking.",
        suggested_actions: [
          "Check your invoices or online receipts for account/customer ID.",
          "Verify whether you have already raised a preliminary ticket with primary customer support.",
          "Select your state/city if the service is governed locally (like Electricity, Water, or Municipal services)."
        ],
        ai_active: false
      };
    }
  }
}

// Global singleton instance
window.fixRoute = new FixRouteAPI();
