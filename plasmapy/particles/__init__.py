"""
The `plasmapy.particles` subpackage provides access to information about
atoms, isotopes, ions, and other particles.
"""
# __all__ will be auto populated below
__all__ = []

from plasmapy.particles.atomic import (
    atomic_number,
    common_isotopes,
    electric_charge,
    half_life,
    integer_charge,
    is_stable,
    isotopic_abundance,
    known_isotopes,
    mass_number,
    particle_mass,
    reduced_mass,
    stable_isotopes,
    standard_atomic_weight,
)
from plasmapy.particles.decorators import particle_input
from plasmapy.particles.ionization_state import IonizationState, State
from plasmapy.particles.ionization_states import IonizationStates
from plasmapy.particles.nuclear import nuclear_binding_energy, nuclear_reaction_energy
from plasmapy.particles.particle_class import (
    AbstractParticle,
    CustomParticle,
    DimensionlessParticle,
    Particle,
)
from plasmapy.particles.serialization import (
    json_load_particle,
    json_loads_particle,
    ParticleJSONDecoder,
)
from plasmapy.particles.special_particles import ParticleZoo
from plasmapy.particles.symbols import (
    atomic_symbol,
    element_name,
    ionic_symbol,
    isotope_symbol,
    particle_symbol,
)

# Create instances of the most commonly used particles

#: PlasmaPy particle object for a proton
proton = Particle("p+")

#: PlasmaPy particle object for an electron
electron = Particle("e-")

#: PlasmaPy particle object for a neutron
neutron = Particle("n")

#: PlasmaPy particle object for a positron
positron = Particle("e+")

#: PlasmaPy particle object for a deuteron
deuteron = Particle("D 1+")

#: PlasmaPy particle object for a triton
triton = Particle("T 1+")

#: PlasmaPy particle object for an alpha particle
alpha = Particle("He-4 2+")

# auto populate __all__
for obj_name in list(globals()):
    if not (obj_name.startswith("__") or obj_name.endswith("__")):
        __all__.append(obj_name)
__all__.sort()
