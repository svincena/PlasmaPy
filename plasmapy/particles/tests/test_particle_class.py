import collections
import inspect
import io
import json
import numpy as np
import pytest

from astropy import constants as const
from astropy import units as u
from astropy.constants import c, e, m_e, m_n, m_p

from plasmapy.particles import json_load_particle, json_loads_particle
from plasmapy.particles.atomic import known_isotopes
from plasmapy.particles.exceptions import (
    AtomicError,
    AtomicWarning,
    ChargeError,
    InvalidElementError,
    InvalidIonError,
    InvalidIsotopeError,
    InvalidParticleError,
    MissingAtomicDataError,
    MissingAtomicDataWarning,
)
from plasmapy.particles.isotopes import _Isotopes
from plasmapy.particles.particle_class import (
    CustomParticle,
    DimensionlessParticle,
    Particle,
)
from plasmapy.particles.special_particles import ParticleZoo
from plasmapy.utils import call_string, roman
from plasmapy.utils.pytest_helpers import run_test_equivalent_calls

# (arg, kwargs, results_dict)
test_Particle_table = [
    (
        "neutron",
        {},
        {
            "particle": "n",
            "element": None,
            "isotope": None,
            "isotope_name": InvalidElementError,
            "ionic_symbol": None,
            "roman_symbol": None,
            "is_ion": False,
            "is_electron": False,
            "integer_charge": 0,
            "atomic_number": InvalidElementError,
            "mass_number": InvalidIsotopeError,
            "baryon_number": 1,
            "lepton_number": 0,
            "mass": m_n,
            "nuclide_mass": m_n,
            "binding_energy": 0 * u.J,
            "periodic_table.group": InvalidElementError,
        },
    ),
    (
        "p+",
        {},
        {
            "particle": "p+",
            "element": "H",
            "element_name": "hydrogen",
            "isotope": "H-1",
            "isotope_name": "hydrogen-1",
            "ionic_symbol": "p+",
            "roman_symbol": "H-1 II",
            "is_ion": True,
            "mass": m_p,
            "nuclide_mass": m_p,
            "integer_charge": 1,
            "charge.value": e.si.value,
            "spin": 1 / 2,
            "half_life": np.inf * u.s,
            "atomic_number": 1,
            "mass_number": 1,
            "lepton_number": 0,
            "baryon_number": 1,
            "__str__()": "p+",
            "__repr__()": 'Particle("p+")',
            'is_category("fermion")': True,
            'is_category(["fermion"])': True,
            'is_category({"fermion"})': True,
            'is_category(any_of=("boson", "fermion"))': True,
            'is_category(require=["boson", "fermion"])': False,
            'is_category(("element", "isotope", "ion"))': True,
            'is_category("charged")': True,
            "periodic_table.group": 1,
            "periodic_table.block": "s",
            "periodic_table.period": 1,
            "periodic_table.category": "nonmetal",
            "binding_energy": 0 * u.J,
            "recombine()": "H-1 0+",
        },
    ),
    (
        "p-",
        {},
        {
            "particle": "p-",
            "element": None,
            "element_name": InvalidElementError,
            "isotope": None,
            "isotope_name": InvalidElementError,
            "ionic_symbol": None,
            "roman_symbol": None,
            "is_ion": False,
            "mass": m_p,
            "integer_charge": -1,
            "spin": 1 / 2,
            "half_life": np.inf * u.s,
            "atomic_number": InvalidElementError,
            "mass_number": InvalidIsotopeError,
            "lepton_number": 0,
            "baryon_number": -1,
            "__str__()": "p-",
            "__repr__()": 'Particle("p-")',
            "periodic_table.group": InvalidElementError,
        },
    ),
    (
        "e-",
        {},
        {
            "particle": "e-",
            "element": None,
            "element_name": InvalidElementError,
            "isotope": None,
            "isotope_name": InvalidElementError,
            "ionic_symbol": None,
            "roman_symbol": None,
            "is_ion": False,
            "mass": m_e,
            "integer_charge": -1,
            "spin": 1 / 2,
            "half_life": np.inf * u.s,
            "atomic_number": InvalidElementError,
            "lepton_number": 1,
            "baryon_number": 0,
            "__str__()": "e-",
            "__repr__()": 'Particle("e-")',
            "binding_energy": InvalidIsotopeError,
            "periodic_table.group": InvalidElementError,
            "periodic_table.block": InvalidElementError,
            "periodic_table.period": InvalidElementError,
            "periodic_table.category": InvalidElementError,
        },
    ),
    (
        "e+",
        {},
        {
            "particle": "e+",
            "element": None,
            "isotope": None,
            "isotope_name": InvalidElementError,
            "ionic_symbol": None,
            "roman_symbol": None,
            "is_ion": False,
            "mass": m_e,
            "mass_energy": (m_e * c ** 2).to("J"),
            "nuclide_mass": InvalidIsotopeError,
            "integer_charge": 1,
            "spin": 1 / 2,
            "half_life": np.inf * u.s,
            "atomic_number": InvalidElementError,
            "lepton_number": -1,
            "baryon_number": 0,
            'is_category(require="positron")': True,
            'is_category(any_of={"positron"})': True,
            'is_category(exclude="positron")': False,
            'is_category("ion")': False,
            "__str__()": "e+",
            "__repr__()": 'Particle("e+")',
            "periodic_table.group": InvalidElementError,
            "periodic_table.block": InvalidElementError,
            "periodic_table.period": InvalidElementError,
            "periodic_table.category": InvalidElementError,
        },
    ),
    (
        "H",
        {},
        {
            "particle": "H",
            "element": "H",
            "isotope": None,
            "isotope_name": InvalidIsotopeError,
            "ionic_symbol": None,
            "roman_symbol": ChargeError,
            "is_ion": False,
            "charge": ChargeError,
            "integer_charge": ChargeError,
            "mass_number": InvalidIsotopeError,
            "baryon_number": AtomicError,
            "lepton_number": 0,
            "half_life": InvalidIsotopeError,
            "standard_atomic_weight": (1.008 * u.u).to(u.kg),
            "mass": (1.008 * u.u).to(u.kg),
            "nuclide_mass": InvalidIsotopeError,
            'is_category("charged")': False,
            'is_category("nonmetal")': True,
            'is_category("proton")': False,
        },
    ),
    (
        "H 1-",
        {},
        {
            "particle": "H 1-",
            "element": "H",
            "isotope": None,
            "isotope_name": InvalidIsotopeError,
            "ionic_symbol": "H 1-",
            "roman_symbol": roman.OutOfRangeError,
            "is_ion": True,
            "integer_charge": -1,
            "mass_number": InvalidIsotopeError,
            "baryon_number": MissingAtomicDataError,
            "lepton_number": 0,
            "half_life": InvalidIsotopeError,
            "standard_atomic_weight": InvalidElementError,
            "nuclide_mass": InvalidIsotopeError,
            'is_category("charged")': True,
            'is_category("nonmetal")': True,
            'is_category("proton")': False,
        },
    ),
    (
        "H-1 0+",
        {},
        {
            "particle": "H-1 0+",
            "element": "H",
            "isotope": "H-1",
            "isotope_name": "hydrogen-1",
            "ionic_symbol": "H-1 0+",
            "roman_symbol": "H-1 I",
            "is_ion": False,
            "charge": 0 * u.C,
            "integer_charge": 0,
            "mass_number": 1,
            "baryon_number": 1,
            "lepton_number": 0,
            "half_life": np.inf * u.s,
            "nuclide_mass": m_p,
            'is_category("charged")': False,
            'is_category("uncharged")': True,
            'is_category("ion")': False,
            'is_category("nonmetal")': True,
            'is_category("proton")': False,
        },
    ),
    (
        "D+",
        {},
        {
            "particle": "D 1+",
            "element": "H",
            "element_name": "hydrogen",
            "isotope": "D",
            "isotope_name": "deuterium",
            "ionic_symbol": "D 1+",
            "roman_symbol": "D II",
            "is_ion": True,
            "integer_charge": 1,
            "atomic_number": 1,
            "mass_number": 2,
            "baryon_number": 2,
            "lepton_number": 0,
            "neutron_number": 1,
            'is_category(require=("ion", "isotope"))': True,
            "periodic_table.group": 1,
            "periodic_table.block": "s",
            "periodic_table.period": 1,
            "periodic_table.category": "nonmetal",
        },
    ),
    (
        "tritium",
        {"Z": 1},
        {
            "particle": "T 1+",
            "element": "H",
            "isotope": "T",
            "isotope_name": "tritium",
            "ionic_symbol": "T 1+",
            "roman_symbol": "T II",
            "is_ion": True,
            "integer_charge": 1,
            "atomic_number": 1,
            "mass_number": 3,
            "baryon_number": 3,
            "lepton_number": 0,
            "neutron_number": 2,
            'is_category("ion", "isotope")': True,
            'is_category(require="uncharged")': False,
            "periodic_table.group": 1,
        },
    ),
    (
        "Fe",
        {"Z": 17, "mass_numb": 56},
        {
            "particle": "Fe-56 17+",
            "element": "Fe",
            "element_name": "iron",
            "isotope": "Fe-56",
            "isotope_name": "iron-56",
            "ionic_symbol": "Fe-56 17+",
            "roman_symbol": "Fe-56 XVIII",
            "is_electron": False,
            "is_ion": True,
            "integer_charge": 17,
            "atomic_number": 26,
            "mass_number": 56,
            "baryon_number": 56,
            "__str__()": "Fe-56 17+",
            "__repr__()": 'Particle("Fe-56 17+")',
            'is_category("element")': True,
            'is_category("ion")': True,
            'is_category("isotope")': True,
        },
    ),
    (
        "alpha",
        {},
        {
            "particle": "He-4 2+",
            "element": "He",
            "element_name": "helium",
            "isotope": "He-4",
            "isotope_name": "helium-4",
            "ionic_symbol": "He-4 2+",
            "roman_symbol": "He-4 III",
            "mass_energy": 5.971919969131517e-10 * u.J,
            "is_ion": True,
            "integer_charge": 2,
            "atomic_number": 2,
            "mass_number": 4,
            "baryon_number": 4,
            "lepton_number": 0,
            "half_life": np.inf * u.s,
            "recombine()": Particle("He-4 1+"),
        },
    ),
    (
        "He-4 0+",
        {},
        {
            "particle": "He-4 0+",
            "element": "He",
            "isotope": "He-4",
            "mass_energy": 5.971919969131517e-10 * u.J,
        },
    ),
    (
        "Li",
        {"mass_numb": 7},
        {
            "particle": "Li-7",
            "element": "Li",
            "element_name": "lithium",
            "isotope": "Li-7",
            "isotope_name": "lithium-7",
            "ionic_symbol": None,
            "roman_symbol": ChargeError,
            "is_ion": False,
            "integer_charge": ChargeError,
            "atomic_number": 3,
            "mass_number": 7,
            "neutron_number": 4,
            "baryon_number": 7,
            "half_life": np.inf * u.s,
            "nuclide_mass": 1.1647614796180463e-26 * u.kg,
        },
    ),
    (
        "Cn-276",
        {"Z": 22},
        {
            "particle": "Cn-276 22+",
            "element": "Cn",
            "isotope": "Cn-276",
            "isotope_name": "copernicium-276",
            "ionic_symbol": "Cn-276 22+",
            "roman_symbol": "Cn-276 XXIII",
            "is_ion": True,
            "element_name": "copernicium",
            "integer_charge": 22,
            "atomic_number": 112,
            "mass_number": 276,
            "neutron_number": 164,
            "baryon_number": 276,
            "lepton_number": 0,
        },
    ),
    (
        "muon",
        {},
        {
            "particle": "mu-",
            "element": None,
            "isotope": None,
            "isotope_name": InvalidElementError,
            "ionic_symbol": None,
            "roman_symbol": None,
            "is_ion": False,
            "integer_charge": -1,
            "atomic_number": InvalidElementError,
            "mass_number": InvalidIsotopeError,
            "baryon_number": 0,
            "lepton_number": 1,
        },
    ),
    (
        "nu_tau",
        {},
        {
            "particle": "nu_tau",
            "element": None,
            "isotope": None,
            "isotope_name": InvalidElementError,
            "mass": MissingAtomicDataError,
            "mass_energy": MissingAtomicDataError,
            "integer_charge": 0,
            "mass_number": InvalidIsotopeError,
            "element_name": InvalidElementError,
            "baryon_number": 0,
            "lepton_number": 1,
            "half_life": np.inf * u.s,
            "is_electron": False,
            "is_ion": False,
            'is_category("fermion")': True,
            'is_category("neutrino")': True,
            'is_category("boson")': False,
            'is_category("matter", exclude={"antimatter"})': True,
            'is_category("matter", exclude=["antimatter"])': True,
            'is_category("matter", exclude="antimatter")': True,
            'is_category(any_of={"matter", "boson"})': True,
            'is_category(any_of=["antimatter", "boson", "charged"])': False,
            'is_category(["fermion", "lepton"], exclude="matter")': False,
            'is_category("lepton", "invalid")': AtomicError,
            'is_category(["boson"], exclude=["lepton", "invalid"])': AtomicError,
            'is_category("boson", exclude="boson")': AtomicError,
            'is_category(any_of="boson", exclude="boson")': AtomicError,
        },
    ),
    (Particle("C"), {}, {"particle": "C", "atomic_number": 6, "element": "C"}),
    (
        Particle("C"),
        {"Z": 3, "mass_numb": 14},
        {
            "particle": "C-14 3+",
            "element": "C",
            "isotope": "C-14",
            "ionic_symbol": "C-14 3+",
        },
    ),
]


@pytest.mark.parametrize("arg, kwargs, expected_dict", test_Particle_table)
def test_Particle_class(arg, kwargs, expected_dict):
    """
    Test that `~plasmapy.particles.Particle` objects for different
    subatomic particles, elements, isotopes, and ions return the
    expected properties.  Provide a detailed error message that lists
    all of the inconsistencies with the expected results.
    """

    call = call_string(Particle, arg, kwargs)
    errmsg = ""

    try:
        particle = Particle(arg, **kwargs)
    except Exception as exc:
        raise AtomicError(f"Problem creating {call}") from exc

    for key in expected_dict.keys():
        expected = expected_dict[key]

        if inspect.isclass(expected) and issubclass(expected, Exception):

            # Exceptions are expected to be raised when accessing certain
            # attributes for some particles.  For example, accessing a
            # neutrino's mass should raise a MissingAtomicDataError since
            # only upper limits of neutrino masses are presently available.
            # If expected_dict[key] is an exception, then check to make
            # sure that this exception is raised.

            try:
                with pytest.raises(expected):
                    exec(f"particle.{key}")
            except pytest.fail.Exception:
                errmsg += f"\n{call}[{key}] does not raise {expected}."
            except Exception:
                errmsg += (
                    f"\n{call}[{key}] does not raise {expected} but "
                    f"raises a different exception."
                )

        else:

            try:
                result = eval(f"particle.{key}")
                assert result == expected or u.isclose(result, expected)
            except AssertionError:
                errmsg += (
                    f"\n{call}.{key} returns {result} instead "
                    f"of the expected value of {expected}."
                )
            except Exception:
                errmsg += f"\n{call}.{key} raises an unexpected exception."

    if len(errmsg) > 0:
        raise Exception(f"Problems with {call}:{errmsg}")


equivalent_particles_table = [
    ["H", "hydrogen", "hYdRoGeN"],
    ["p+", "proton", "H-1+", "H-1 1+", "H-1 +1"],
    ["D", "H-2", "Hydrogen-2", "deuterium"],
    ["T", "H-3", "Hydrogen-3", "tritium"],
    ["alpha", "He-4++", "He-4 2+", "He-4 +2", "He-4 III"],
    ["e-", "electron", "e"],
    ["e+", "positron"],
    ["p-", "antiproton"],
    ["n", "n-1", "neutron", "NEUTRON"],
    ["muon", "mu-", "muon-"],
    ["tau", "tau-"],
    [Particle("Fe 5+"), Particle("Fe 4+").ionize()],
    [Particle("He-4 0+"), Particle("alpha").recombine(2)],
]


@pytest.mark.parametrize("equivalent_particles", equivalent_particles_table)
def test_Particle_equivalent_cases(equivalent_particles):
    """Test that all instances of a list of particles are equivalent."""
    run_test_equivalent_calls(Particle, *equivalent_particles)


# arg, kwargs, attribute, exception
test_Particle_error_table = [
    ("a", {}, "", InvalidParticleError),
    ("d+", {"mass_numb": 9}, "", InvalidParticleError),
    ("H", {"mass_numb": 99}, "", InvalidParticleError),
    ("Au-818", {}, "", InvalidParticleError),
    ("Au-12", {}, "", InvalidParticleError),
    ("Au", {"mass_numb": 13}, "", InvalidParticleError),
    ("Au", {"mass_numb": 921}, "", InvalidParticleError),
    ("e-", {"Z": -1}, "", InvalidParticleError),
    ("e-", {}, ".atomic_number", InvalidElementError),
    ("alpha", {}, ".standard_atomic_weight", InvalidElementError),
    ("Fe-56", {}, ".standard_atomic_weight", InvalidElementError),
    ("e-", {}, ".standard_atomic_weight", InvalidElementError),
    ("tau-", {}, ".element_name", InvalidElementError),
    ("tau+", {}, ".atomic_number", InvalidElementError),
    ("neutron", {}, ".atomic_number", InvalidElementError),
    ("H", {"Z": 0}, ".mass_number", InvalidIsotopeError),
    ("neutron", {}, ".mass_number", InvalidIsotopeError),
    ("He", {"mass_numb": 4}, ".charge", ChargeError),
    ("He", {"mass_numb": 4}, ".integer_charge", ChargeError),
    ("Fe", {}, ".spin", MissingAtomicDataError),
    ("nu_e", {}, ".mass", MissingAtomicDataError),
    ("Og", {}, ".standard_atomic_weight", MissingAtomicDataError),
    (Particle("C-14"), {"mass_numb": 13}, "", InvalidParticleError),
    (Particle("Au 1+"), {"Z": 2}, "", InvalidParticleError),
    ([], {}, "", TypeError),
    ("Fe", {}, ".ionize()", ChargeError),
    ("D", {}, ".recombine()", ChargeError),
    ("Fe 26+", {}, ".ionize()", InvalidIonError),
    ("Fe 6+", {}, ".ionize(-1)", ValueError),
    ("Fe 25+", {}, ".recombine(0)", ValueError),
    ("Fe 6+", {}, ".ionize(4.6)", TypeError),
    ("Fe 25+", {}, ".recombine(8.2)", TypeError),
    ("e-", {}, ".ionize()", InvalidElementError),
    ("e+", {}, ".recombine()", InvalidElementError),
]


@pytest.mark.parametrize("arg, kwargs, attribute, exception", test_Particle_error_table)
def test_Particle_errors(arg, kwargs, attribute, exception):
    """
    Test that the appropriate exceptions are raised during the creation
    and use of a `~plasmapy.particles.Particle` object.
    """
    with pytest.raises(exception):
        exec(f"Particle(arg, **kwargs){attribute}")
        pytest.fail(
            f"The following command: "
            f"\n\n  {call_string(Particle, arg, kwargs)}{attribute}\n\n"
            f"did not raise a {exception.__name__} as expected"
        )


# arg, kwargs, attribute, exception
test_Particle_warning_table = [
    ("H----", {}, "", AtomicWarning),
    ("alpha", {"mass_numb": 4}, "", AtomicWarning),
    ("alpha", {"Z": 2}, "", AtomicWarning),
]


@pytest.mark.parametrize("arg, kwargs, attribute, warning", test_Particle_warning_table)
def test_Particle_warnings(arg, kwargs, attribute, warning):
    """
    Test that the appropriate warnings are issued during the creation
    and use of a `~plasmapy.particles.Particle` object.
    """
    with pytest.warns(warning) as record:
        exec(f"Particle(arg, **kwargs){attribute}")
        if not record:
            pytest.fail(
                f"The following command: "
                f"\n\n >>> {call_string(Particle, arg, kwargs)}{attribute}\n\n"
                f"did not issue a {warning.__name__} as expected"
            )


def test_Particle_cmp():
    """Test ``__eq__`` and ``__ne__`` in the Particle class."""
    proton1 = Particle("p+")
    proton2 = Particle("proton")
    electron = Particle("e-")

    assert proton1 == proton2, "Particle('p+') == Particle('proton') is False."
    assert proton1 != electron, "Particle('p+') == Particle('e-') is True."

    with pytest.raises(TypeError):
        electron == 1

    with pytest.raises(AtomicError):
        electron == "dfasdf"


nuclide_mass_and_mass_equiv_table = [
    ("n", "neutron"),
    ("p+", "proton"),
    ("H-1", "p+"),
    ("H-1 0+", "p+"),
    ("D", "D+"),
    ("T", "T+"),
    ("He-4", "alpha"),
    ("Fe-56", "Fe-56 26+"),
]


@pytest.mark.parametrize("isotope, ion", nuclide_mass_and_mass_equiv_table)
def test_particle_class_mass_nuclide_mass(isotope: str, ion: str):
    """
    Test that the ``mass`` and ``nuclide_mass`` attributes return
    equivalent values when appropriate.  The inputs should generally be
    an isotope with no charge information, and a fully ionized ion of
    that isotope, in order to make sure that the nuclide mass of the
    isotope equals the mass of the fully ionized ion.  This method may
    also check neutrons and protons.
    """

    Isotope = Particle(isotope)
    Ion = Particle(ion)

    if Isotope.categories & {"isotope", "baryon"} and Ion.categories & {
        "ion",
        "baryon",
    }:

        particle = Isotope.particle

        assert Isotope.nuclide_mass == Ion.mass, (
            f"Particle({repr(particle)}).nuclide_mass does not equal "
            f"Particle({repr(particle)}).mass"
        )

    else:

        inputerrmsg = (
            f"isotope = {repr(isotope)} and ion = {repr(ion)} are "
            f"not valid inputs to this test. The inputs should be "
            f"an isotope with no charge information, and a fully "
            f"ionized ion of that isotope, in order to make sure "
            f"that the nuclide mass of the isotope equals the mass "
            f"of the ion."
        )

        assert Isotope.isotope and not Isotope.ion, inputerrmsg
        assert Isotope.isotope == Ion.isotope, inputerrmsg
        assert Ion.integer_charge == Ion.atomic_number, inputerrmsg

        assert Isotope.nuclide_mass == Ion.mass, (
            f"The nuclide mass of {isotope} does not equal the mass of {ion} "
            f"which is the fully ionized ion of that isotope. The results of "
            f"the test are:\n\n"
            f"Particle({repr(ion)}).mass = {Ion.mass}\n"
            f"Particle({repr(isotope)}).nuclide_mass = {Isotope.nuclide_mass}"
            "\n"
        )


def test_particle_half_life_string():
    """
    Find the first isotope where the half-life is stored as a string
    (because the uncertainties are too great), and tests that requesting
    the half-life of that isotope causes a `MissingAtomicDataWarning`
    whilst returning a string.
    """

    for isotope in known_isotopes():
        half_life = _Isotopes[isotope].get("half-life", None)
        if isinstance(half_life, str):
            break

    with pytest.warns(MissingAtomicDataWarning):
        assert isinstance(Particle(isotope).half_life, str)


@pytest.mark.parametrize("p, is_one", [(Particle("e-"), True), (Particle("p+"), False)])
def test_particle_is_electron(p, is_one):
    assert p.is_electron == is_one


def test_particle_bool_error():
    with pytest.raises(AtomicError):
        bool(Particle("e-"))


particle_antiparticle_pairs = [
    ("p+", "p-"),
    ("n", "antineutron"),
    ("e-", "e+"),
    ("mu-", "mu+"),
    ("tau-", "tau+"),
    ("nu_e", "anti_nu_e"),
    ("nu_mu", "anti_nu_mu"),
    ("nu_tau", "anti_nu_tau"),
]


@pytest.mark.parametrize("particle, antiparticle", particle_antiparticle_pairs)
def test_particle_inversion(particle, antiparticle):
    """Test that particles have the correct antiparticles."""
    assert Particle(particle).antiparticle == Particle(antiparticle), (
        f"The antiparticle of {particle} is found to be "
        f"{~Particle(particle)} instead of {antiparticle}."
    )


@pytest.mark.parametrize("particle, antiparticle", particle_antiparticle_pairs)
def test_antiparticle_inversion(particle, antiparticle):
    """Test that antiparticles have the correct antiparticles."""
    assert Particle(antiparticle).antiparticle == Particle(particle), (
        f"The antiparticle of {antiparticle} is found to be "
        f"{~Particle(antiparticle)} instead of {particle}."
    )


def test_unary_operator_for_elements():
    with pytest.raises(AtomicError):
        Particle("C").antiparticle


@pytest.fixture(params=ParticleZoo.everything)
def particle(request):
    return Particle(request.param)


@pytest.fixture()
def opposite(particle):
    try:
        opposite_particle = ~particle
    except Exception as exc:
        raise InvalidParticleError(
            f"The unary ~ (invert) operator is unable to find the "
            f"antiparticle of {particle}."
        ) from exc
    return opposite_particle


class Test_antiparticle_properties_inversion:
    """
    Test particle and antiparticle inversion and properties for Particle
    instances.
    """

    def test_inverted_inversion(self, particle):
        """
        Test that the antiparticle of the antiparticle of a particle is
        the original particle.
        """
        assert particle == ~~particle, (
            f"~~{repr(particle)} equals {repr(~~particle)} instead of "
            f"{repr(particle)}."
        )

    def test_opposite_charge(self, particle, opposite):
        """
        Test that a particle and its antiparticle have the opposite
        charge.
        """
        assert particle.integer_charge == -opposite.integer_charge, (
            f"The charges of {particle} and {opposite} are not "
            f"opposites, as expected of a particle/antiparticle pair."
        )

    def test_equal_mass(self, particle, opposite):
        """
        Test that a particle and its antiparticle have the same mass.
        """
        assert particle._attributes["mass"] == opposite._attributes["mass"], (
            f"The masses of {particle} and {opposite} are not equal, "
            f"as expected of a particle/antiparticle pair."
        )

    def test_antiparticle_attribute_and_operator(self, particle, opposite):
        """
        Test that the Particle.antiparticle attribute returns the same
        value as the unary ~ (invert) operator acting on the same
        Particle instance.
        """
        assert particle.antiparticle == ~particle, (
            f"{repr(particle)}.antiparticle returned "
            f"{particle.antiparticle}, whereas ~{repr(particle)} "
            f"returned {~particle}."
        )


@pytest.mark.parametrize("arg", ["e-", "D+", "Fe 25+", "H-", "mu+"])
def test_particleing_a_particle(arg):
    """
    Test that Particle(arg) is equal to Particle(Particle(arg)), but is
    not the same object in memory.
    """
    particle = Particle(arg)

    assert particle == Particle(particle), (
        f"Particle({repr(arg)}) does not equal " f"Particle(Particle({repr(arg)})."
    )

    assert particle == Particle(Particle(Particle(particle))), (
        f"Particle({repr(arg)}) does not equal "
        f"Particle(Particle(Particle({repr(arg)}))."
    )

    assert particle is not Particle(particle), (
        f"Particle({repr(arg)}) is the same object in memory as "
        f"Particle(Particle({repr(arg)})), when it is intended to "
        f"create a new object in memory (e.g., a copy)."
    )


@pytest.mark.parametrize("key", [Particle("H"), Particle("e+")])
def test_that_object_can_be_dict_key(key):
    """
    Test that ``key`` can be used as the key of a `dict`.

    This test will fail if ``key`` does not equal itself or if ``key``
    is not hashable.  If this test fails, there is a problem with the
    ``__eq__`` and ``__hash__`` methods of ``key``.

    In most cases, objects that are mutable should not be hashable since
    they may change.

    """
    # TODO: I wrote this to be pretty general since I felt like
    # TODO: procrastinating other things, so we can probably put this
    # TODO: into utils.pytest_helpers later on.  There are likely other
    # TODO: classes that should be able to be used as keys of dicts.

    value = 42

    try:
        dictionary = {key: value}
    except Exception as exc:
        error_message = f"{key} is not a valid key for a dict. "
        if not isinstance(key, collections.Hashable):
            error_message += f"{key} is not hashable. "
        try:
            key_equals_itself = key == key
        except Exception:
            error_message += f"{key} == {key} cannot be evaluated. "
        else:
            if not key_equals_itself:
                error_message += f"{key} does not equal itself."
        raise TypeError(error_message) from exc

    assert dictionary[key] is value


# TODO: These tests may be refactored using forthcoming functionality in
#       plasmapy.tests.helpers.  It may be necessary to case the expected
#       results as certain types (e.g., numpy.float64).

customized_particle_tests = [
    (DimensionlessParticle, {"mass": 1.0, "charge": -1.0}, "mass", 1.0),
    (DimensionlessParticle, {"mass": 0.0, "charge": -1.0}, "charge", -1.0),
    (DimensionlessParticle, {}, "mass", np.nan),
    (DimensionlessParticle, {}, "charge", np.nan),
    (DimensionlessParticle, {"mass": np.inf}, "mass", np.inf),
    (DimensionlessParticle, {"charge": np.inf}, "charge", np.inf),
    (DimensionlessParticle, {"charge": 1.0 * u.dimensionless_unscaled}, "charge", 1.0),
    (DimensionlessParticle, {"mass": 1.0 * u.dimensionless_unscaled}, "mass", 1.0),
    (CustomParticle, {}, "mass", np.nan * u.kg),
    (CustomParticle, {}, "charge", np.nan * u.C),
    (CustomParticle, {"mass": 1.1 * u.kg, "charge": -0.1 * u.C}, "mass", 1.1 * u.kg),
    (CustomParticle, {"charge": -0.1 * u.C}, "charge", -0.1 * u.C),
    (CustomParticle, {"charge": -2}, "charge", -2 * const.e.si),
    (CustomParticle, {"mass": np.inf * u.g}, "mass", np.inf * u.kg),
    (CustomParticle, {"mass": "100.0 g"}, "mass", 100.0 * u.g),
    (CustomParticle, {"charge": -np.inf * u.kC}, "charge", -np.inf * u.C),
    (CustomParticle, {"charge": "5.0 C"}, "charge", 5.0 * u.C),
]


@pytest.mark.parametrize("cls, kwargs, attr, expected", customized_particle_tests)
def test_customized_particles(cls, kwargs, attr, expected):
    """Test the attributes of dimensionless and custom particles."""
    instance = cls(**kwargs)
    value = getattr(instance, attr)

    if not u.isclose(value, expected, equal_nan=True):
        pytest.fail(
            f"{call_string(cls, kwargs=kwargs)}.{attr} should return a value "
            f"of {expected}, but instead returned a value of {value}."
        )


customized_particle_errors = [
    (DimensionlessParticle, {"mass": -1e-36}, InvalidParticleError),
    (DimensionlessParticle, {"mass": [1, 1]}, InvalidParticleError),
    (DimensionlessParticle, {"charge": [-1, 1]}, InvalidParticleError),
    (DimensionlessParticle, {"mass": True}, InvalidParticleError),
    (
        DimensionlessParticle,
        {"mass": np.array([1, 2]) * u.dimensionless_unscaled},
        InvalidParticleError,
    ),
    (
        DimensionlessParticle,
        {"charge": np.array([1, 2]) * u.dimensionless_unscaled},
        InvalidParticleError,
    ),
    (
        DimensionlessParticle,
        {"charge": (1 + 2j) * u.dimensionless_unscaled},
        InvalidParticleError,
    ),
    (CustomParticle, {"charge": 5 + 2j}, InvalidParticleError),
    (CustomParticle, {"mass": 5 + 2j}, InvalidParticleError),
    (CustomParticle, {"charge": np.complex128(5 + 2j)}, InvalidParticleError),
    (CustomParticle, {"mass": np.complex128(5 + 2j)}, InvalidParticleError),
    (CustomParticle, {"mass": -1e-36 * u.kg}, InvalidParticleError),
    (CustomParticle, {"mass": "not a mass"}, InvalidParticleError),
    (CustomParticle, {"mass": "5.0 km"}, InvalidParticleError),
    (CustomParticle, {"mass": np.array([1, 1]) * u.kg}, InvalidParticleError),
    (CustomParticle, {"charge": np.array([1, 1]) * u.C}, InvalidParticleError),
    (CustomParticle, {"charge": (5 + 2j) * u.C}, InvalidParticleError),
    (CustomParticle, {"mass": (5 + 2j) * u.kg}, InvalidParticleError),
    (CustomParticle, {"charge": np.complex128(5 + 2j) * u.C}, InvalidParticleError),
    (CustomParticle, {"mass": np.complex128(5 + 2j) * u.kg}, InvalidParticleError),
    (CustomParticle, {"charge": "not a charge"}, InvalidParticleError),
    (CustomParticle, {"charge": "5.0 km"}, InvalidParticleError),
]


@pytest.mark.parametrize("cls, kwargs, exception", customized_particle_errors)
def test_customized_particles_errors(cls, kwargs, exception):
    """
    Test that attempting to create invalid dimensionless or custom particles
    results in an InvalidParticleError.
    """
    with pytest.raises(exception):
        cls(**kwargs)
        pytest.fail(f"{cls.__name__}(**{kwargs}) did not raise: {exception.__name__}.")


customized_particle_repr_table = [
    (
        CustomParticle,
        {"mass": 5.12 * u.kg, "charge": 6.2 * u.C},
        "CustomParticle(mass=5.12 kg, charge=6.2 C)",
    ),
    (
        DimensionlessParticle,
        {"mass": 5.2, "charge": 6.3},
        "DimensionlessParticle(mass=5.2, charge=6.3)",
    ),
]


@pytest.mark.parametrize("cls, kwargs, expected_repr", customized_particle_repr_table)
def test_customized_particle_repr(cls, kwargs, expected_repr):
    """Test the string representations of dimensionless and custom particles."""
    instance = cls(**kwargs)
    from_repr = repr(instance)
    from_str = str(instance)
    if not expected_repr == from_repr == from_str:
        pytest.fail(
            f"Problem with a string representation of {cls.__name__} "
            f"with kwargs = {kwargs}.\n\n"
            f"expected_repr = {expected_repr}"
            f"from_str: {from_str}"
            f"from_repr: {from_repr}"
        )


custom_particles_from_json_tests = [
    (
        DimensionlessParticle,
        {"mass": 5.2, "charge": 6.3},
        '{"plasmapy_particle": {"type": "DimensionlessParticle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": { \
            "args": [], \
            "kwargs": {"mass": 5.2, "charge": 6.3}}}}',
        None,
    ),
    (
        DimensionlessParticle,
        {"mass": 5.2},
        '{"plasmapy_particle": {"type": "DimensionlessParticle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": { \
            "args": [], \
            "kwargs": {"mass": 5.2, "charge": NaN}}}}',
        None,
    ),
    (
        CustomParticle,
        {"mass": 5.12 * u.kg, "charge": 6.2 * u.C},
        '{"plasmapy_particle": {"type": "CustomParticle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": { \
            "args": [], \
            "kwargs": {"mass": "5.12 kg", "charge": "6.2 C"}}}}',
        None,
    ),
    (
        CustomParticle,
        {"mass": 5.12 * u.kg},
        '{"plasmapy_particle": {"type": "CustomParticle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": { \
            "args": [], \
            "kwargs": {"mass": "5.12 kg", "charge": "nan C"}}}}',
        None,
    ),
    (
        DimensionlessParticle,
        {"mass": 5.2, "charge": 6.3},
        '{"plasmapy_particle": {"notatype": "DimensionlessParticle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": { \
            "args": [], \
            "kwargs": {"mass": 5.2, "charge": 6.3}}}}',
        InvalidElementError,
    ),
    (
        CustomParticle,
        {"mass": 5.12 * u.kg},
        '{"plasmapy_particle": {"notatype": "CustomParticle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": { \
            "args": [], \
            "kwargs": {"mass": "5.12 kg", "charge": "nan C"}}}}',
        InvalidElementError,
    ),
    (
        DimensionlessParticle,
        {"mass": 5.2, "charge": 6.3},
        '{"plasmapy_particle": {"type": "DimensionlessParticle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "fake__init__": { \
            "args": [], \
            "kwargs": {"mass": 5.2, "charge": 6.3}}}}',
        InvalidElementError,
    ),
    (
        CustomParticle,
        {"mass": 5.12 * u.kg},
        '{"plasmapy_particle": {"type": "CustomParticle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "fake__init__": { \
            "args": [], \
            "kwargs": {"mass": "5.12 kg", "charge": "nan C"}}}}',
        InvalidElementError,
    ),
]


@pytest.mark.parametrize(
    "cls, kwargs, json_string, expected_exception", custom_particles_from_json_tests
)
def test_custom_particles_from_json_string(
    cls, kwargs, json_string, expected_exception
):
    """Test the attributes of dimensionless and custom particles generated from
    JSON representation"""
    if expected_exception is None:
        instance = cls(**kwargs)
        instance_from_json = json_loads_particle(json_string)
        assert u.isclose(
            instance.mass, instance_from_json.mass, equal_nan=True
        ), pytest.fail(
            f"Expected a mass value of {instance.mass}\n"
            f"Received a mass value of {instance_from_json.mass}"
        )
        assert u.isclose(
            instance.charge, instance_from_json.charge, equal_nan=True
        ), pytest.fail(
            f"Expected a charge value of {instance.charge}\n"
            f"Received a charge value of {instance_from_json.charge}"
        )
    else:
        with pytest.raises(expected_exception):
            instance_from_json = json_loads_particle(json_string)
            pytest.fail(
                f"{cls.__name__} with ({json_string})"
                f" did not raise: {expected_exception.__name__}."
            )


@pytest.mark.parametrize(
    "cls, kwargs, json_string, expected_exception", custom_particles_from_json_tests
)
def test_custom_particles_from_json_file(cls, kwargs, json_string, expected_exception):
    """Test the attributes of dimensionless and custom particles generated from
    JSON representation"""
    if expected_exception is None:
        instance = cls(**kwargs)
        test_file_object = io.StringIO(json_string)
        instance_from_json = json_load_particle(test_file_object)
        assert u.isclose(
            instance.mass, instance_from_json.mass, equal_nan=True
        ), pytest.fail(
            f"Expected a mass value of {instance.mass}\n"
            f"Received a mass value of {instance_from_json.mass}"
        )
        assert u.isclose(
            instance.charge, instance_from_json.charge, equal_nan=True
        ), pytest.fail(
            f"Expected a charge value of {instance.charge}\n"
            f"Received a charge value of {instance_from_json.charge}"
        )
    else:
        with pytest.raises(expected_exception):
            test_file_object = io.StringIO(json_string)
            instance_from_json = json_load_particle(test_file_object)
            pytest.fail(
                f"{cls.__name__} with ({json_string})"
                f" did not raise: {expected_exception.__name__}."
            )


particles_from_json_tests = [
    (
        Particle,
        {"argument": "Pb"},
        '{"plasmapy_particle": {"type": "Particle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": {"args": ["Pb"], "kwargs": {}}}}',
        None,
    ),
    (
        Particle,
        {"argument": "e-"},
        '{"plasmapy_particle": {"type": "Particle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": {"args": ["e-"], "kwargs": {}}}}',
        None,
    ),
    (
        Particle,
        {"argument": "e-"},
        '{"plasmapy_particle": {"notatype": "Particle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": {"args": ["e-"], "kwargs": {}}}}',
        InvalidElementError,
    ),
    (
        Particle,
        {"argument": "e-"},
        '{"plasmapy_particle": {"type": "Particle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "fake__init__": {"args": ["e-"], "kwargs": {}}}}',
        InvalidElementError,
    ),
]


@pytest.mark.parametrize(
    "cls, kwargs, json_string, expected_exception", particles_from_json_tests
)
def test_particles_from_json_string(cls, kwargs, json_string, expected_exception):
    """Test the attributes of Particle objects created from JSON representation."""
    if expected_exception is None:
        instance = cls(**kwargs)
        instance_from_json = json_loads_particle(json_string)
        expected_particle = instance.particle
        actual_particle = instance_from_json.particle
        assert expected_particle == actual_particle, pytest.fail(
            f"Expected {expected_particle}\n" f"Got {actual_particle}"
        )
    else:
        with pytest.raises(expected_exception):
            instance_from_json = json_loads_particle(json_string)
            pytest.fail(
                f"{cls.__name__} with ({json_string})"
                f" did not raise: {expected_exception.__name__}."
            )


@pytest.mark.parametrize(
    "cls, kwargs, json_string, expected_exception", particles_from_json_tests
)
def test_particles_from_json_file(cls, kwargs, json_string, expected_exception):
    """Test the attributes of Particle objects created from JSON representation."""
    if expected_exception is None:
        instance = cls(**kwargs)
        test_file_object = io.StringIO(json_string)
        test_file_object.seek(0, io.SEEK_SET)
        instance_from_json = json_load_particle(test_file_object)
        expected_particle = instance.particle
        actual_particle = instance_from_json.particle
        assert expected_particle == actual_particle, pytest.fail(
            f"Expected {expected_particle}\n" f"Got {actual_particle}"
        )
    else:
        with pytest.raises(expected_exception):
            test_file_object = io.StringIO(json_string)
            instance_from_json = json_load_particle(test_file_object)
            pytest.fail(
                f"{cls.__name__} with ({json_string})"
                f" did not raise: {expected_exception.__name__}."
            )


particle_json_repr_table = [
    (
        Particle,
        {"argument": "lead"},
        '{"plasmapy_particle": {"type": "Particle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", \
        "__init__": {"args": ["Pb"], "kwargs": {}}}}',
    ),
    (
        Particle,
        {"argument": "lead"},
        '{"plasmapy_particle": {"type": "Particle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": {"args": ["Pb"], "kwargs": {}}}}',
    ),
    (
        CustomParticle,
        {"mass": 5.12 * u.kg, "charge": 6.2 * u.C},
        '{"plasmapy_particle": {"type": "CustomParticle", \
        "module": "plasmapy.particles.particle_class", \
        "date_created": "...", "__init__": {\
            "args": [], \
            "kwargs": {"mass": "5.12 kg", "charge": "6.2 C"}}}}',
    ),
    (
        DimensionlessParticle,
        {"mass": 5.2, "charge": 6.3},
        '{"plasmapy_particle": {"type": "DimensionlessParticle",\
        "module": "plasmapy.particles.particle_class",\
        "date_created": "...", "__init__": {\
            "args": [], \
            "kwargs": {"mass": 5.2, "charge": 6.3}}}}',
    ),
]


@pytest.mark.parametrize("cls, kwargs, expected_repr", particle_json_repr_table)
def test_particle_to_json_string(cls, kwargs, expected_repr):
    """Test the JSON representations of normal, dimensionless and custom particles."""
    instance = cls(**kwargs)
    json_repr = instance.json_dumps()
    test_dict = json.loads(json_repr)["plasmapy_particle"]
    expected_repr = json.loads(expected_repr)["plasmapy_particle"]
    assert test_dict["type"] == expected_repr["type"], pytest.fail(
        f"Problem with JSON representation of {cls.__name__} "
        f"with kwargs = {kwargs}.\n\n"
        f"expected type = {expected_repr['type']}\n\n"
        f"got type: {test_dict['type']}"
    )
    assert expected_repr["__init__"] == test_dict["__init__"], pytest.fail(
        f"Problem with JSON representation of {cls.__name__} "
        f"with kwargs = {kwargs}.\n\n"
        f"expected_repr = {expected_repr['__init__']}.\n\n"
        f"json_repr: {test_dict['__init__']}"
    )


@pytest.mark.parametrize("cls, kwargs, expected_repr", particle_json_repr_table)
def test_particle_to_json_file(cls, kwargs, expected_repr):
    """Test the JSON representations of normal, dimensionless and custom particles."""
    instance = cls(**kwargs)
    test_file_object = io.StringIO("")
    instance.json_dump(test_file_object)
    test_file_object.seek(0, io.SEEK_SET)
    json_repr = test_file_object.read()
    test_dict = json.loads(json_repr)["plasmapy_particle"]
    expected_repr = json.loads(expected_repr)["plasmapy_particle"]
    assert test_dict["type"] == expected_repr["type"], pytest.fail(
        f"Problem with JSON representation of {cls.__name__} "
        f"with kwargs = {kwargs}.\n\n"
        f"expected type = {expected_repr['type']}\n\n"
        f"got type: {test_dict['type']}"
    )
    assert expected_repr["__init__"] == test_dict["__init__"], pytest.fail(
        f"Problem with JSON representation of {cls.__name__} "
        f"with kwargs = {kwargs}.\n\n"
        f"expected_repr = {expected_repr['__init__']}.\n\n"
        f"json_repr: {test_dict['__init__']}"
    )
