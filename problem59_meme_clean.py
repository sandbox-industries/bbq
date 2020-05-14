import itertools, string

print(
    sum(
        map(
            ord,
            next(
                filter(
                    lambda d: ' and ' in d,
                    map(
                        lambda k, e: ''.join(
                            [
                                (''.join(
                                        [ chr(ord(k[j]) ^ ord(c))
                                            for j, c in enumerate(e[i:i+3])
                                        ]
                                    )
                                ) for i in range(0, len(e), 3)
                            ]
                        ),
                        itertools.product(string.ascii_lowercase, repeat=3),
                        itertools.repeat(
                            ''.join(
                                map(
                                    lambda x: chr(int(x)),
                                    open('p059_cipher.txt').read().split(',')
                                )
                            )
                        )
                    )
                )
            )
        )
    )
)