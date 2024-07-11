from tinydb import TinyDB
import datetime
import os
from mp_tests.utils import load_atoms
from tqdm import tqdm

class MPMixin():
    """
    Mixin class for tests performed over Materials Project data. 

    Parameters:
        supported_species : list[string]
            List of chemical species supported by the model. 
            Only needed if an ASE Calculator is passed in.

        db_name : string
            Name of TinyDB file to write outputs to


    """
    def __init__(self, supported_species=None, db_name="mp.json"):
        self.db_name = db_name
        self.supported_species = []
        if hasattr(self._calc,"species_map"):
            for k,v in self._calc.species_map.items():
                self.supported_species.append(k)
        else:
            if len(supported_species)>0:
                self.supported_species = supported_species
            else:
                raise Exception("'supported_species' must be given if passing a calculator instead of a KIM model")

    def check_supported_species(self,atoms):
        for a in set(atoms.get_chemical_symbols()):
            if a not in self.supported_species:
                return False
        return True

    def post_process(self):
        raise NotImplementedError

    def mp_tests(self, job_n=0, n_calcs=10733,**kwargs):
        """Loads all structures with computed elastic constants from Materials Project and computes
        elastic constants for it if the model supports the species present
        """
        import pickle

        mp_dict = pickle.load(open("%s/%s/mp_elasticity_conventional_4-9-24.pkl" %(os.path.dirname(__file__), "data"), "rb"))
        for k, v in tqdm(list(mp_dict.items())[job_n*n_calcs:(job_n+1)*n_calcs]):
            atoms = load_atoms(k, v)
            check = self.check_supported_species(atoms)
            if check:
                self(atoms, **kwargs)
                self.post_process(orig_atoms = atoms)

    def insert_mp_outputs(self, mp_id, property_name, gt, comp):
        db = TinyDB(self.db_name)
        db.insert({'mp-id':mp_id, property_name:{'computed':comp, 'ground_truth': gt}, 'timestamp': str(datetime.datetime.now())})
        
