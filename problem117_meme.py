from typing import Callable, List, Any


class RuntimeExecutioner(object):
    """
    Wrapper class for safely executing a callable.
    
    Handles execution failure and success at runtime with provided callbacks.
    """

    def __init__(self, func: Callable[[Any], None]):
        """Initalize this instance with a function or callable object func."""

        if not callable(func):
            raise ValueError('func must be callable')

        self._callable = func

    def __str__(self):
        return f'Safety wrapper for: {self._callable}'

    def __repr__(self):
        return f'RuntimeExecutioner instance around: {self._callable}'

    def __execute__(self, *args, **kwargs):
        return self._callable(*args, **kwargs)

    def safe_execute(self,
        on_success: Callable[[Any], Any],
        on_failure: Callable[[Any, Any, Exception], Any],
        *args,
        **kwargs):
        """
        Safely execute the callable.
        
        on_success will be called with the return value after successful execution.
        on_failure will be called with the argument list, the keyword argument dictionary, and the caught exception on failure.
        """

        if not callable(on_success) or not callable(on_failure):
            raise ValueError('success and failure callbacks must be callable')

        try:
            val = self.__execute__(*args, **kwargs)
            on_success(val)
        except Exception as e:
            on_failure(args, kwargs, e)


class RestrictedCompositionAlgorithm(object):
    """
    Represents a callable restricted composition algorithm.

    On call will return the n-th value in the series (aka the total compositions given n-space).
    """

    def __init__(self, initial_vector: List[int]):
        """Initialize the algorithm with a series."""
        if not initial_vector:
            raise ValueError('initial vector must be a list of integers')

        self._vector = initial_vector

    def __call__(self, n: int, *args, **kwargs) -> int:
        """Returns the total number of compositions given n-space."""
        if n < 0:
            raise ValueError('must be postive integer')

        i = 0
        
        # The series is really just a fancy fibonacci series with variable rotational space
        while i < n:

            # Perform the rotation to discard the oldest element and make the new element the sum of the previous
            self._vector = self._vector[1:] + [sum(self._vector)]

            # Increase the step count
            i += 1
        
        # Return the head of the vector, because math
        return self._vector[0]

    def __str__(self):
        return f'Composition Algorithm instance ({len(self._vector)})'

    def __repr__(self):
        return str(self._vector)


class CompositionVectorGenerator(object):
    """
    Generator of initial composition vectors.
    
    This is usually the k-value in the composition series.
    """

    def __init__(self, size: int):
        """Create a vector of size size."""
        if size <= 0:
            raise ValueError('must be greater than zero')

        self._vector = [1] * size

        for i in range(1, size):
            lowerbound_index: int = max(0, i - size)
            self._vector[i] = sum(self._vector[lowerbound_index:i])

    def __str__(self):
        return f'Generated vector: {self._vector}'

    def __repr__(self):
        return str(self._vector)

    def __sizeof__(self) -> int:
        return len(self._vector)

    @property
    def vector(self) -> List[int]:
        """Read-only vector property."""
        return self._vector

    @vector.setter
    def vector(self, value) -> None:
        raise AttributeError('read-only attribute')


if __name__ == "__main__":  # Import guard
    PATTERN_SIZE = 4
    TOTAL_TILES = 50

    # On successful execution, print the return value
    def success_callback(return_value: int) -> None:
        print(f'Succeeded safely with return value: {return_value}')

    # On failure, print the parameters that caused the failure and the exeception thrown
    def failure_callback(args, kwargs, e: Exception) -> None:
        print(f'Failed!\nArgs: {args}\nKeyword Args: {kwargs}\nException: {e}')

    vector_generator = CompositionVectorGenerator(PATTERN_SIZE)
    print(f'Vector generator: {vector_generator}')

    composition_algorithm = RestrictedCompositionAlgorithm(vector_generator.vector)
    print(f'Composition algorithm: {composition_algorithm}')

    execution = RuntimeExecutioner(composition_algorithm)
    print(f'Runtime executioner: {execution}')

    execution.safe_execute(success_callback, failure_callback, TOTAL_TILES)