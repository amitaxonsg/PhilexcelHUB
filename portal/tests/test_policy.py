from datetime import timedelta
from policy import TRIAL_START, TRIAL_END, trial_state, allowed_libraries, allowed_source

def test_trial_boundary():
 assert TRIAL_END-TRIAL_START==timedelta(days=30)
 assert not trial_state(TRIAL_END-timedelta(microseconds=1))['expired']
 assert trial_state(TRIAL_END)['expired']
 assert trial_state(TRIAL_END+timedelta(days=1))['days_remaining']==0

def test_department_allowlist():
 assert allowed_libraries({'enabled':True,'departments':['Marketing','Board','Engineering']})==['Company-Shared','Engineering','Marketing']
 assert allowed_libraries({'enabled':False,'departments':['Executive']})==[]
 assert allowed_libraries({})==[]

def test_board_and_cross_department_sources_denied():
 assert allowed_source('https://philexcelbusinesspark.sharepoint.com/sites/PhilexcelHUB/Marketing/file.txt','Marketing')
 for url in ['https://evil.example/sites/PhilexcelHUB/Marketing/f.txt',
 'https://philexcelbusinesspark.sharepoint.com/sites/PhilexcelExecutiveBoard/f.txt',
 'https://philexcelbusinesspark.sharepoint.com/sites/PhilexcelHUB/Executive/f.txt',
 'https://philexcelbusinesspark.sharepoint.com/sites/PhilexcelHUB/Marketing-extra/f.txt']:
  assert not allowed_source(url,'Marketing')

def test_executive_and_ai_disabled():
 from policy import ai_libraries, LIBRARIES
 assert set(ai_libraries({'enabled':True,'ai_enabled':True,'ai_level':'executive'}))==LIBRARIES
 assert not ai_libraries({'enabled':True,'ai_enabled':False,'ai_level':'executive'})
 assert ai_libraries({'enabled':True,'ai_enabled':True,'ai_departments':['Engineering']})==['Company-Shared','Engineering']

def test_restriction_routing_uses_only_public_department_hints():
 from policy import restricted_department
 assert restricted_department('show me finance payroll', ['Marketing','Company-Shared'])=='Finance-Purchasing'
 assert restricted_department('engineering safety policy', ['Engineering','Company-Shared']) is None
