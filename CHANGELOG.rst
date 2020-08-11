Plasmapy v0.4.0 (2020-07-20)
============================

Backwards Incompatible Changes
------------------------------

- Rename ``plasmapy.atomic`` to `~plasmapy.particles`.  In
  `~plasmapy.formulary.collisions` and `~plasmapy.formulary.braginskii`,
  change arguments named particles to ``species`` and arguments named
  ``ion_particle`` to ``ion`` for multiple functions. (`#742 <https://github.com/plasmapy/plasmapy/pull/742>`__)
- Officially delete :mod:`plasmapy.examples`. (`#822 <https://github.com/plasmapy/plasmapy/pull/822>`__)
- Move :mod:`plasmapy.data` to :mod:`plasmapy.particle.data`. (`#823 <https://github.com/plasmapy/plasmapy/pull/823>`__)
- Renamed the `plasmapy.classes` subpackage to `plasmapy.plasma`. (`#842 <https://github.com/plasmapy/plasmapy/pull/842>`__)


Features
--------

- Added units to reprs of .formulary.magnetostatics classes. (`#743 <https://github.com/plasmapy/plasmapy/pull/743>`__)
- Create prototype abstract interfaces for plasma simulations (`#753 <https://github.com/plasmapy/plasmapy/pull/753>`__)
- Created classes to represent custom and dimensionless particles in ``plasmapy.particles``. (`#755 <https://github.com/plasmapy/plasmapy/pull/755>`__)
- Create :func:`~plasmapy.formulary.relativity.relativistic_energy` function, which uses the established :func:`~plamsapy.formulary.relativity.Lorentz_factor` function to aid in the calculation of the relativistic energy of an object. (`#805 <https://github.com/plasmapy/plasmapy/pull/805>`__)
- Create :func:`~plasmapy.formulary.dimensionless.Reynolds_number` function. (`#815 <https://github.com/plasmapy/plasmapy/pull/815>`__)
- Create :func:`~plasmapy.formulary.dimensionless.Mag_Reynolds` function. (`#820 <https://github.com/plasmapy/plasmapy/pull/820>`__)
- Create :func:`~plasmapy.formulary.parameters.Bohm_diffusion` function. (`#830 <https://github.com/plasmapy/plasmapy/pull/830>`__)
- Added a new diagnostics module `thomson` containing a function
  `spectral_density` that calculates Thomson scattering spectra for
  Maxwellian plasmas in both the collective and non-collective regimes. As
  a followup to PR #835, set the minimal required Numpy version to 1.18.1 to
  finally fix unit dropping bugs. (`#831 <https://github.com/plasmapy/plasmapy/pull/831>`__)
- Revised parameters.thermal_speed to support 1D and 2D distributions as well as 3D, and added an example notebook for this function. (`#850 <https://github.com/plasmapy/plasmapy/pull/850>`__)
- Create `plasmapy/formulary/ionization.py`
  Create :func:`~plasmapy.formulary.ionization.Z_bal` function. (`#851 <https://github.com/plasmapy/plasmapy/pull/851>`__)
- Create :func:`~plasmapy.formulary.ionization.Saha` function. (`#860 <https://github.com/plasmapy/plasmapy/pull/860>`__)
- Added aliases (with trailing underscores) for parameters in the formulary:

      * `plasmapy.formulary.dimensionless.Reynolds_number` -> `~plasmapy.formulary.dimensionless.Re_`
      * `plasmapy.formulary.dimensionless.Mag_Reynolds` -> `~plasmapy.formulary.dimensionless.Rm_`
      * `plasmapy.formulary.drifts.ExB_drift` -> `~plasmapy.formulary.drifts.veb_`
      * `plasmapy.formulary.drifts.force_drift` -> `~plasmapy.formulary.drifts.vfd_`
      * `plasmapy.formulary.parameters.mass_density` -> `~plasmapy.formulary.parameters.rho_`
      * `plasmapy.formulary.parameters.Afven_speed` -> `~plasmapy.formulary.parameters.va_`
      * `plasmapy.formulary.parameters.ion_sound_speed` -> `~plasmapy.formulary.parameters.cs_`
      * `plasmapy.formulary.parameters.thermal_speed` -> `~plasmapy.formulary.parameters.vth_`
      * `plasmapy.formulary.parameters.thermal_pressure` -> `~plasmapy.formulary.parameters.pth_`
      * `plasmapy.formulary.parameters.kappa_thermal_speed` -> `~plasmapy.formulary.parameters.vth_kappa_`
      * `plasmapy.formulary.parameters.inertial_length` -> `~plasmapy.formulary.parameters.cwp_`
      * `plasmapy.formulary.parameters.Hall_parameter` -> `~plasmapy.formulary.parameters.betaH_`
      * `plasmapy.formulary.parameters.gyrofrequency` -> `~plasmapy.formulary.parameters.oc_`, `~plasmapy.formulary.parameters.wc_`
      * `plasmapy.formulary.parameters.gyroradius` -> `~plasmapy.formulary.parameters.rc_`, `~plasmapy.formulary.parameters.rhoc_`
      * `plasmapy.formulary.parameters.plasma_frequency` -> `~plasmapy.formulary.parameters.wp_`
      * `plasmapy.formulary.parameters.Debye_length` -> `~plasmapy.formulary.parameters.lambdaD_`
      * `plasmapy.formulary.parameters.Debye_number` -> `~plasmapy.formulary.parameters.nD_`
      * `plasmapy.formulary.parameters.magnetic_pressure` -> `~plasmapy.formulary.parameters.pmag_`
      * `plasmapy.formulary.parameters.magnetic_energy_density` -> `~plasmapy.formulary.parameters.ub_`
      * `plasmapy.formulary.parameters.upper_hybrid_frequency` -> `~plasmapy.formulary.parameters.wuh_`
      * `plasmapy.formulary.parameters.lower_hybrid_frequency` -> `~plasmapy.formulary.parameters.wlh_`
      * `plasmapy.formulary.parameters.Bohm_diffusion` -> `~plasmapy.formulary.parameters.DB_`
      * `plasmapy.formulary.quantum.deBroglie_wavelength` -> `~plasmapy.formulary.quantum.lambdaDB_`
      * `plasmapy.formulary.quantum.thermal_deBroglie_wavelength` -> `~plasmapy.formulary.quantum.lambdaDB_th_`
      * `plasmapy.formulary.quantum.Fermi_energy` -> `~plasmapy.formulary.quantum.Ef_` (`#865 <https://github.com/plasmapy/plasmapy/pull/865>`__)
- Add `json_dumps` method to `~plasmapy.particles.particle_class.AbstractParticle` to
  convert a particle object into a JSON string. Add `json_dump` method to
  `~plasmapy.particles.particle_class.AbstractParticle` to serialize a particle
  object and writes it to a file.  Add JSON decoder
  `~plasmapy.particles.serialization.ParticleJSONDecoder` to deserialize JSON objects
  into particle objects.  Add `plasmapy.particles.serialization.json_loads_particle`
  function to convert JSON strings to particle objects (using
  `~plasmapy.particles.serialization.ParticleJSONDecoder`). Add
  `plasmapy.particles.json_load_particle` function to deserialize a JSON file into a
  particle object (using `~plasmapy.particles.serialization.ParticleJSONDecoder`).
  (`#836 <https://github.com/plasmapy/plasmapy/pull/836>`__)


Bug Fixes
---------

- Fix incorrect use of `pkg.resources` when defining `plasmapy.__version__`.  Add
  `setuptools` to package dependencies.  Add a definition of `__version__` for
  developers using source files. (`#774 <https://github.com/plasmapy/plasmapy/pull/774>`__)
- Repair notebook links that are defined in the `nbsphinx_prolog` sphinx configuration
  variable. (`#828 <https://github.com/plasmapy/plasmapy/pull/828>`__)
- Increase the required Astropy version from 3.1 to 4.0, Numpy from 1.14 to 1.16.6, Scipy from 0.19 to 1.2 and lmfit from 0.9.7 to 1.0.1. This fixes long-standing issues with Numpy operations dropping units from AstroPy quantities. (`#835 <https://github.com/plasmapy/plasmapy/pull/835>`__)


Improved Documentation
----------------------

- - Added documentation to file test_converters (`#756 <https://github.com/plasmapy/plasmapy/pull/756>`__)
- - Updated installation instructions. (`#772 <https://github.com/plasmapy/plasmapy/pull/772>`__)
- Reorder documentation page (`#777 <https://github.com/plasmapy/plasmapy/pull/777>`__)
- Fix failing documentation build due to duplicate docstrings for
  `ParticleTracker.kinetic_energy_history` and incompatibility of `sphinx-automodapi`
  with `sphinx` `v3.0.0`. (`#780 <https://github.com/plasmapy/plasmapy/pull/780>`__)
- Automate definition of documentation `release` and `version` in `docs/conf.py` with
  `plasmapy.__version__`. (`#781 <https://github.com/plasmapy/plasmapy/pull/781>`__)
- Add a docstring to ``__init__.py`` in `plasmapy.formulary`. (`#788 <https://github.com/plasmapy/plasmapy/pull/788>`__)
- Replaced sphinx-gallery with nbsphinx, turning `.py` example files into `.ipynb` files and allowing for easier example submission. (`#792 <https://github.com/plasmapy/plasmapy/pull/792>`__)
- Linked various instances of classes and functions in the `.ipynb` examples in `docs/notebooks/` to the respective API docs. (`#825 <https://github.com/plasmapy/plasmapy/pull/825>`__)
- Fixed a few documentation formatting errors. (`#827 <https://github.com/plasmapy/plasmapy/pull/827>`__)
- Add notes on the PlasmaPy benchmarks repository to documentation. (`#841 <https://github.com/plasmapy/plasmapy/pull/841>`__)
- Improve readability of the `plasmapy.formulary` page by replacing the `toctree`
  list with a cleaner reST table. (`#867 <https://github.com/plasmapy/plasmapy/pull/867>`__)


Trivial/Internal Changes
------------------------

- Remove mutable arguments from `Particle.is_category` method. (`#751 <https://github.com/plasmapy/plasmapy/pull/751>`__)
- Remove all occurrences of default mutable arguments (`#754 <https://github.com/plasmapy/plasmapy/pull/754>`__)
- Handle `ModuleNotFoundError` when trying to import `__version__` but `setuptools_scm` has not
  generated the `version.py` file.  This commonly happens during development when `plasmapy` is
  not installed in the python environment. (`#763 <https://github.com/plasmapy/plasmapy/pull/763>`__)
- Updated pep8speaks/flake8 configuration and added `.pre-commit-config.yaml` to simplify automated style checks during development. (`#770 <https://github.com/plasmapy/plasmapy/pull/770>`__)
- Removes some lint from setup.py and setup.cfg. Use pkg_resources for version
  checking in code. Remove version.py file in favor of pkg_resources. (`#771 <https://github.com/plasmapy/plasmapy/pull/771>`__)
- Default settings for isort were set to be consistent with default settings for black. (`#773 <https://github.com/plasmapy/plasmapy/pull/773>`__)
- Update community meeting and funding information in docs. (`#784 <https://github.com/plasmapy/plasmapy/pull/784>`__)
- Improved pull request template to include more information about changelog entries. (`#843 <https://github.com/plasmapy/plasmapy/pull/843>`__)
- Added GitHub actions that apply pre-commit and flake8 (separately) to incoming pull requests. (`#845 <https://github.com/plasmapy/plasmapy/pull/845>`__)
- Apply pre-commit hooks to entire repository, so that GitHub actions do not shout at contributors needlessly. (`#846 <https://github.com/plasmapy/plasmapy/pull/846>`__)
- Update :class:`~plasmapy.particles.particle_class.CustomParticle` so input parameters
  `mass` and `charge` can accept string representations of astropy `Quantities`. (`#862 <https://github.com/plasmapy/plasmapy/pull/862>`__)


Plasmapy v0.3.0 (2020-01-25)
============================

Backwards Incompatible Changes
------------------------------

- Create simulation subpackage; move Species particle tracker there; rename to particletracker (`#665 <https://github.com/plasmapy/plasmapy/pull/665>`__)
- Changed `plasmapy.classes.Species` to `plasmapy.simulation.ParticleTracker` (`#668 <https://github.com/plasmapy/plasmapy/pull/668>`__)
- Move pytest helper functionality from `plasmapy.utils` to
  `~plasmapy.utils.pytest_helpers` (`#674 <https://github.com/plasmapy/plasmapy/pull/674>`__)
- Move `plasmapy.physics`, `plasmapy.mathematics` and `plasmapy.transport` into the common `plasmapy.formulary` subpackage (`#692 <https://github.com/plasmapy/plasmapy/pull/692>`__)
- Change `ClassicalTransport` methods into attributes (`#705 <https://github.com/plasmapy/plasmapy/pull/705>`__)

Deprecations and Removals
-------------------------

- Remove `parameters_cython.pyx`, switching to Numba for the future of computationally intensive code in PlasmaPy (`#650 <https://github.com/plasmapy/plasmapy/pull/650>`__)
- Remove plasmapy.constants, which was a thin wrapper around astropy.constants
  with no added value (`#651 <https://github.com/plasmapy/plasmapy/pull/651>`__)

Features
--------

- Generalize `ion_sound_speed` function to work for all values of :math:`k^2 \lambda_{D}^2` (i.e. not just in the non-dispersive limit). (`#700 <https://github.com/plasmapy/plasmapy/pull/700>`__)
- Optimize `add__magnetostatics` for a 16x speedup in tests! (`#703 <https://github.com/plasmapy/plasmapy/pull/703>`__)

Bug Fixes
---------

- Define `preserve_signature` decorator to help IDEs parse signatures of decorated functions. (`#640 <https://github.com/plasmapy/plasmapy/pull/640>`__)
- Fix Pytest deprecations of `message` argument to `raise` and `warn` functions. (`#666 <https://github.com/plasmapy/plasmapy/pull/666>`__)
- Fix `h5py` warning in OpenPMD module, opening files in read mode by default (`#717 <https://github.com/plasmapy/plasmapy/pull/717>`__)


Improved Documentation
----------------------

- Added real-world examples to examples/plot_physics.py and adjusted the plots to be more human-friendly. (`#448 <https://github.com/plasmapy/plasmapy/pull/448>`__)
- Add examples images to the top of the main doc page in `docs\index.rst` (`#655 <https://github.com/plasmapy/plasmapy/pull/655>`__)
- Added exampes to the documentation to mass_density
   and Hall_parameter functions (`#709 <https://github.com/plasmapy/plasmapy/pull/709>`__)
- Add docstrings to decorator :func:`plasmapy.utils.decorators.converter.angular_freq_to_hz`. (`#729 <https://github.com/plasmapy/plasmapy/pull/729>`__)


Trivial/Internal Changes
------------------------

- Replace decorator :func:`plasmapy.utils.decorators.checks.check_quantity` with decorator
  :func:`plasmapy.utils.decorators.validators.validate_quantities`.  Permanently delete decorator
  :func:`~plasmapy.utils.decorators.checks.check_quantity` and its supporting code.  For functions
  :func:`plasmapy.formulary.quantum.chemical_potential` and
  :func:`plasmapy.formulary.quantum._chemical_potential_interp`, add a `RaiseNotImplementedError` due
  to bug outlined in issue `<https://github.com/PlasmaPy/PlasmaPy/issues/726>`_.  Associated pytests
  are marked with `pytest.mark.xfails` and doctests are marked with `doctests: +SKIP`. (`#722 <https://github.com/plasmapy/plasmapy/pull/722>`__)
- Add `Towncrier <https://github.com/hawkowl/towncrier>`_ automated changelog creation support (`#643 <https://github.com/plasmapy/plasmapy/pull/643>`__)
- Move existing "check" decorators to new ``plasmapy.utils.decorators`` module (`#647 <https://github.com/plasmapy/plasmapy/pull/647>`__)
- Allow running our sphinx-gallery examples as Jupyter notebooks via Binder (`#656 <https://github.com/plasmapy/plasmapy/pull/656>`__)
- Overhaul CI setup, following the example of SunPy (`#657 <https://github.com/plasmapy/plasmapy/pull/657>`__)
- Patch `sphinx_gallery.binder` to output custom links to Binder instance (`#658 <https://github.com/plasmapy/plasmapy/pull/658>`__)
- Remove the now unnecessary `astropy_helpers` submodule (`#663 <https://github.com/plasmapy/plasmapy/pull/663>`__)
- Followup PR to CI overhaul (`#664 <https://github.com/plasmapy/plasmapy/pull/664>`__)
- Add a Codemeta file (``codemeta.json``) (`#676 <https://github.com/plasmapy/plasmapy/pull/676>`__)
- Overhaul and simplify CI, add Python 3.8 to tests, bump minimal required package versions, fix docs. (`#712 <https://github.com/plasmapy/plasmapy/pull/712>`__)
- Update communication channels in docs (`#715 <https://github.com/plasmapy/plasmapy/pull/715>`__)
- Code style fixes to the `atomic` subpackage (`#716 <https://github.com/plasmapy/plasmapy/pull/716>`__)
- Clean up main package namespace, removing `plasmapy.test` (`#718 <https://github.com/plasmapy/plasmapy/pull/718>`__)
- Reduce precision of tests and doctests to allow for refinements of
  fundamental constants. (`#731 <https://github.com/plasmapy/plasmapy/pull/731>`__)
- Create decorators for checking/validating values and units of function/method input
  and return arguments.  Defined decorators include
  :func:`~plasmapy.utils.decorators.checks.check_values`,
  :func:`~plasmapy.utils.decorators.checks.check_units`, and
  :func:`~plasmapy.utils.decorators.validators.validate_quantities`.  These decorators are
  fully defined by "decorator classes" :class:`~plasmapy.utils.decorators.checks.CheckBase`,
  :class:`~plasmapy.utils.decorators.checks.CheckValues`,
  :class:`~plasmapy.utils.decorators.checks.CheckUnits`, and
  :class:`~plasmapy.utils.decorators.validators.ValidateQuantities`. (`#648 <https://github.com/plasmapy/plasmapy/pull/648>`__)
- Create a decorator to change output of physics functions from "radians/s" to "hz" (`#667 <https://github.com/plasmapy/plasmapy/pull/667>`__)
- Added pytest.mark.slow to pytest markers.
  Updated documentation to notify developers of functionality. (`#677 <https://github.com/plasmapy/plasmapy/pull/677>`__)
