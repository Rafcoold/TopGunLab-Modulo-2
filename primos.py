from fastapi import FastAPI # import FastAPI ...


app = FastAPI(title='Numeros Primos')

@app.get('/')
def root():
    return {'data': 'primes'}

@app.get('/items/{id}')
def read_item(numero: int =100, id: str = '1'):
    
    def primos(numero: int):
        primes_list = []
        for num in range(1, numero + 1):
            prime = True
            for i in range(2, num):
                if num % i == 0:
                    prime = False
            if prime:
                primes_list.append(num)
        return primes_list

    return{'primos': primos(numero)}
