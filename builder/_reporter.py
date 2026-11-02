"""Build progress messages."""

class Reporter:
    """Prints progress. ``info`` always prints; ``step`` only with
    ``--veritasium`` (the verbose flag), prefixed so it stands out."""

    def __init__(self: Reporter, verbose: bool=False) -> None:
        self.verbose = verbose

    def info(self: Reporter, message: str) -> None:
        print(message)

    def step(self: Reporter, message: str) -> None:
        if self.verbose:
            print(f'[veritasium] {message}')
