from datetime import datetime, timedelta, timezone

# Amit approved starting today: 22 October 2026 in Philippines/Singapore.
TRIAL_START = datetime(2026, 10, 21, 22, 36, 5, tzinfo=timezone.utc)
TRIAL_END = TRIAL_START + timedelta(days=30)
DEPARTMENTS = {
 'Executive': ('Executive', 'X'),
 'Administration-HR': ('AdminHR', 'H'),
 'Marketing': ('Marketing', 'M'),
 'Administration-Marketing': ('AdminMarketing', 'R'),
 'Finance-Purchasing': ('FinancePurchasing', 'F'),
 'Engineering': ('Engineering', 'E'),
}
LIBRARIES = set(DEPARTMENTS) | {'Company-Shared'}

def trial_state(now=None):
    now = now or datetime.now(timezone.utc)
    return {'expired': now >= TRIAL_END, 'starts': TRIAL_START.isoformat(),
            'expires': TRIAL_END.isoformat(),
            'days_remaining': max(0, int((TRIAL_END-now).total_seconds()+86399)//86400)}

def allowed_libraries(record):
    if not record or not record.get('enabled', False):
        return []
    return sorted((set(record.get('departments', [])) & set(DEPARTMENTS)) | {'Company-Shared'})

def allowed_source(url, library):
    from urllib.parse import urlsplit, unquote
    p = urlsplit(url)
    root = '/sites/PhilexcelHUB/' + library + '/'
    return (library in LIBRARIES and p.scheme == 'https' and
            p.netloc.lower() == 'philexcelbusinesspark.sharepoint.com' and
            unquote(p.path).startswith(root))

RESTRICTION_MESSAGE = ('I can only answer from the departments approved for your account and Company Shared. '
 'Please request access from your administrator, or ask an authorized colleague in that department '
 'to sign in with their own account and ask Linda. Please do not share login details.')

def ai_libraries(record):
    if not record or not record.get('enabled') or not record.get('ai_enabled', False): return []
    if record.get('ai_level') == 'executive': return sorted(LIBRARIES)
    return sorted((set(record.get('ai_departments', record.get('departments', []))) & set(DEPARTMENTS)) | {'Company-Shared'})

def restricted_department(question, scopes):
    # Public routing hints only: never search a restricted index to classify a question.
    import re
    hints={'Executive':['executive'], 'Administration-HR':['human resources','hr'],
      'Marketing':['marketing'], 'Administration-Marketing':['administration marketing'],
      'Finance-Purchasing':['finance','purchasing','payroll'], 'Engineering':['engineering']}
    for department, words in hints.items():
        if department not in scopes and any(re.search(r'\b'+re.escape(w)+r'\b',question,re.I) for w in words):
            return department
    return None
