import importlib.util
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('import_enrollment',Path(__file__).parents[1]/'cpanel/import_enrollment.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
OID='39b23f67-7e2c-4f21-bfa3-19b4d3839778'

def record(**changes):
 return dict(object_id=OID,nas_username='Ian',departments=['Executive'],enabled=True,user_principal_name='ian@example.invalid',**changes)

def test_import_preserves_roles_and_does_not_enable_ai_by_default():
 result=module.merge_records({OID:{'roles':['admin','axon'],'enabled':True,'ai_enabled':True}},[record()])
 assert result[OID]['roles']==['admin','axon'] and result[OID]['ai_enabled']
 result=module.merge_records({},[record()])
 assert result[OID]['roles']==[] and result[OID]['ai_enabled'] is False

def test_import_rejects_disabled_collision_and_duplicate():
 with pytest.raises(ValueError): module.merge_records({OID:{'enabled':False}},[record()])
 with pytest.raises(ValueError): module.merge_records({},[record(),record()])
 with pytest.raises(ValueError): module.merge_records({'other':{'nas_username':'Ian'}},[record()])
