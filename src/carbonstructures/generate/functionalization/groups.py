# dictionary of bond lengths and angles for common functional groups
# data are obtained from Computational Chemistry Comparison and Benchmark Database by NIST  https://cccbdb.nist.gov/expbondlengths1x.asp
__all__ = ['grpdata']

grpdata = {
    'OH': {
        'atoms': 2,
        'CO': {
            'added_atom': ['O', '2'],
            'length': 1.47
        },
        'OH': {
            'added_atom': ['H', '3'],
            'length': 0.98,
            'angle': 107.9
        }
    },
    'SH': {
        'atoms': 2,
        'CS': {
            'added_atom': ['S', '4'],
            'length': 1.345
        },
        'SH': {
            'added_atom': ['H', '3'],
            'length': 1.341,
            'angle': 109.5
        }
    },
    'Cl': {
        'atoms': 1,
        'CCl': {
            'added_atom': ['Cl', '5'],
            'length': 2.124
        }
    },
    'Br': {
        'atoms': 1,
        'CBr': {
            'added_atom': ['Br', '6'],
            'length': 1.937
        }
    }   
}