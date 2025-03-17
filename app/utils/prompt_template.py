from langchain.prompts import PromptTemplate

PHISHING_ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["url", "a_tags", "script_tags", "text"],
    template=(
        """
        Sri Lanka Domain & Content Analysis

            Analyze the URL structure, scripts, redirections, and extracted text to determine if the website is associated with Sri Lanka.
            Check if the webpage is hosted under a .lk domain or redirects to any .lk websites.
            Identify any references to Sri Lankan government agencies, businesses, services, or cultural elements.
            Verify whether the website is part of a legitimate service or a third-party using Sri Lankan hosting.

        Political Content Analysis

            Scan the text, metadata, and redirections for references to Sri Lankan political parties, leaders, movements, or elections.
            Identify if the content is neutral, supportive, or critical of any political entity.
            Detect potential bias, misinformation, or propaganda related to Sri Lankan politics.

        Content Type & Hate Speech Detection

            Analyze whether the extracted text contains hate speech, abusive language, or extremist content.
            Determine if the content is political advertising, propaganda, or a legitimate news article.
            Detect polarizing language designed to influence public opinion.

        Phishing & Security Risk Analysis

            Examine the URL structure and embedded scripts for common phishing indicators:
                Misleading domain names (e.g., using numbers, slight typos, or extra subdomains).
                Hidden redirections leading to login pages or credential-harvesting sites.
                Fake branding or cloned websites mimicking real organizations.
            Cross-check extracted brand names against legitimate organizations.
            Flag any deceptive UI elements (e.g., fake login forms, security warnings, urgent call-to-action).

        Social Engineering & Deceptive Tactics Detection

            Identify patterns matching common phishing and scam techniques, including:
                Fake security warnings (e.g., "Your account is at risk!")
                Urgent payment requests (e.g., "Your payment has failed, update now!")
                Fake prizes & surveys (e.g., "You've won! Click here to claim!")
                Subscription renewal fraud (e.g., "Your Netflix account is expiring!")

        Keyword-Based Threat Detection

            Extract keywords from the webpage, URL, metadata, and scripts related to security risks.
            Contextually analyze keywords to reduce false positives (e.g., distinguishing between genuine discussions on security vs. phishing attempts).
            Identify the total number of keyword hits from the predefined list:
                "phishing", "political", "hack", "security", "hate speech".

        Output:
        - Provide a brief description for each of the sub-tasks. Summarize your findings on whether the website is politically related, identifies any political parties or figures, whether it promotes any type of political content or hate speech, whether the site is a phishing attempt, and how many of the specified keywords were found.

        Submit your findings as JSON-formatted output with the following keys:
        - Website related to Sri Lanka: str (Simple "1" or "0" based on whether the website has any relation to Sri Lanka)
        - Political Content: str (Simple "1" or "0" based on whether the website has any political content)
        - Phishing Score: int (Indicates phishing risk on a scale of 0 to 10)
        - Brands: str (Identified brand name or "None" if not applicable)
        - Phishing: boolean (Whether the site is a phishing site or a legitimate site)
        - Keywords Found: int (Count of keyword hits from the list)
        - Keywords: str (List of keywords found during the analysis)

        Limitations:
        - Input data item “Scripts and Redirections” are from a scraped scripts and redirections from the web application’s original HTML.

        Examples of Social Engineering Techniques:
        - Account Problem Alert: User is told their account has a problem and needs verification.
        - Suspicious Activity Notification: User is alerted to unusual activity on their account.
        - Payment Failure Notice: User is informed that a payment didn't go through and needs updating.
        - Invoice Due Reminder: User receives an invoice or payment request, leading to a fake page.
        - Tax Refund Offer: User is promised a tax refund and asked for banking details.
        - Subscription Renewal: User is prompted to renew a subscription that's about to expire.
        - Password Expiration Warning: User is told their password is expiring and needs resetting.
        - Unclaimed Prize: User is notified of a prize win and asked to claim it.
        - Survey Invitation: User is invited to take a survey in exchange for a reward.
        - Social Media Account Warning: User is warned of an issue with their social media account.
        - Displaying fake security warnings.

        Additional Checks:
        - Cross-reference brand names and URLs with known safe domains.
        - Analyze URL patterns for common phishing structures.

        Input Data:
        - URL: {url}
        - Redirections: {a_tags}
        - Scripts: {script_tags}
        - Text extracted: {text}
        - Keywords: ["physhing", "political","hack","security","hate speech"]
        
        """
    )
)