from mp_tests.test_driver import TestDriver
from mp_tests.mp_mixin import MPMixin
from kim_tools.test_driver.core import add_or_update_property
import os

class Elasticity(TestDriver,MPMixin):

    def __init__(self, model, supported_species, db_name):
        TestDriver.__init__(self, model)
        MPMixin.__init__(self, supported_species, db_name)
        add_or_update_property("%s/%s/bulk-modulus-isothermal-npt.edn" %(os.path.dirname(__file__), "property_definitions"))
        add_or_update_property("%s/%s/elastic-constants-isothermal-npt.edn" %(os.path.dirname(__file__), "property_definitions"))
        
    def post_process(self):
        results = self.property_instances

if __name__ == "__main__":
    from mace.calculators import mace_mp
    from utils import mp_species
    model = mace_mp(default_dtype="float64")
    test = Elasticity(model, supported_species=mp_species, db_name='mp.json' )
    test.mp_tests(job_n=0, n_calcs=10, method="energy-condensed", optimize=True)

