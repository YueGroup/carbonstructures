# Dictionary of bond lengths and angles for common functional groups
# Data are obtained from Computational Chemistry Comparison and Benchmark Database by NIST  https://cccbdb.nist.gov/expbondlengths1x.asp
__all__ = ['grpdata']

grpdata = {
    'OH': {
        'atoms': 2,
        'CO': {
            'added_atom': ['O', '2'],
            'length': 1.47,
            'angle': 0,          # attaches straight off sheet
            'dihedral': 0,
            'parent': 'base'
        },
        'OH': {
            'added_atom': ['H', '3'],
            'length': 0.98,
            'angle': 107.9,      # O–H bond angle
            'dihedral': 0,       # rotate in xz-plane
            'parent': 'CO'
        }
    },
    'CO': {
        'atoms': 2,
        'CC': {
            'added_atom': ['C', '4'], #change carbon number here if needed
            'length': 1.418,
            'angle': 0,
            'dihedral': 0,
            'parent': 'base'
        },
        'CO': {
            'added_atom': ['O', '2'],
            'length': 1.198,
            'angle': 122,
            'dihedral': 0,
            'parent': 'CC'
        }
    },
    'CH3': {
        'atoms': 4,
        'CC': {
            'added_atom': ['C', '4'],   #change carbon number here if needed
            'length': 1.418,
            'angle': 0,
            'dihedral': 0,
            'parent': 'base'
        },
        'CH1': {
            'added_atom': ['H', '2'],
            'length': 1.09,
            'angle': 109.5,
            'dihedral': 180,
            'parent': 'CC'
        },
        'CH2': {
            'added_atom': ['H', '2'],
            'length': 1.09,
            'angle': 109.5,
            'dihedral': 300,
            'parent': 'CC'
        },
        'CH3': {
            'added_atom': ['H', '2'],
            'length': 1.09,
            'angle': 109.5,
            'dihedral': 60,
            'parent': 'CC'
        }
    },
    'COOH': {
        'atoms': 4,
        'CC': {
            'added_atom': ['C', '4'],       #change carbon number here if needed
            'length': 1.418,
            'angle': 0,
            'dihedral': 0,
            'parent': 'base'
        },
        'C=O': {
            'added_atom': ['O', '2'],
            'length': 1.212,
            'angle': 126.6,
            'dihedral': 0, #150,    # one arm of the V
            'parent': 'CC'
        },
        'COH': {
            'added_atom': ['O', '2'],
            'length': 1.361,
            'angle': 110.6,
            'dihedral': 180, #210,    # the other arm of the V
            'parent': 'CC'
        },
        'OH': {
            'added_atom': ['H', '3'],
            'length': 0.98,
            'angle': 107.9,
            'dihedral': 180,
            'parent': 'COH'
        }
    },
    'SH': {
        'atoms': 2,
        'CS': {
            'added_atom': ['S', '4'],
            'length': 1.345,
            'angle': 0,
            'dihedral': 0,
            'parent': 'base'
        },
        'SH': {
            'added_atom': ['H', '3'],
            'length': 1.341,
            'angle': 109.5,
            'dihedral': 0,
            'parent': 'CS'
        }
    },
    'Cl': {
        'atoms': 1,
        'CCl': {
            'added_atom': ['Cl', '5'],
            'length': 2.124,
            'angle': 0,
            'dihedral': 0,
            'parent': 'base'
        }
    },
    'Br': {
        'atoms': 1,
        'CBr': {
            'added_atom': ['Br', '6'],
            'length': 1.937,
            'angle': 0,
            'dihedral': 0,
            'parent': 'base'
        }
    }
}
