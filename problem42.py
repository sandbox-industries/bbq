print(
    sum(
        1 for _ in filter(
            lambda w: w in ((i/2)*(i+1) for i in range(2000)),
            map(
                lambda x: sum(map(lambda y: ord(y)-64, x)),
                map(
                    lambda n: n[1:-1],
                    open('p042_words.txt').read().split(',')
                )
            )
        )
    )
)