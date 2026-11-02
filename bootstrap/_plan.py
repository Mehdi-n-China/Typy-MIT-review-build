"""Which Typy sources compile to which package modules."""
from .. import tools
NOT_GENERATED: tuple = ('bootstrap/_stage0.py', 'test.py')
NOT_COMPILER: tuple = ('source', 'tests', 'example_project', 'output', 'docs', 'assets', 'stats')

def planned_outputs(package_dir: tools.path.Path) -> list:
    """``[(source, target)]`` for every ``.typy`` file under
    ``package_dir/source``: each one compiles to the same relative path, as a
    ``.py`` file, inside the package itself."""
    source_dir: tools.path.Path = package_dir / 'source'
    plan: list = []
    for source in sorted(source_dir.rglob('*.typy')):
        plan.append((source, package_dir / source.relative_to(source_dir).with_suffix('.py')))
    return plan

def orphaned_modules(package_dir: tools.path.Path, plan: list) -> list:
    """Compiler modules no source produces any more (the leftovers of a
    deleted ``.typy`` file), which would otherwise linger unnoticed."""
    produced: set = {target for _, target in plan}
    orphans: list = []
    for path in sorted(package_dir.rglob('*.py')):
        relative: tools.path.Path = path.relative_to(package_dir)
        if not (relative.parts[0] in NOT_COMPILER or '__pycache__' in relative.parts):
            if relative.as_posix() not in NOT_GENERATED and path not in produced:
                orphans.append(relative.as_posix())
    return orphans
