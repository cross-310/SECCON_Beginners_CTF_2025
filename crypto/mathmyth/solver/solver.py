from Crypto.Util.number import *
import math, random
from itertools import product
from sympy.ntheory.residue_ntheory import nthroot_mod


n = 23734771090248698495965066978731410043037460354821847769332817729448975545908794119067452869598412566984925781008642238995593407175153358227331408865885159489921512208891346616583672681306322601209763619655504176913841857299598426155538234534402952826976850019794857846921708954447430297363648280253578504979311210518547
e = 65537
c = 22417329318878619730651705410225614332680840585615239906507789561650353082833855142192942351615391602350331869200198929410120997195750699143505598991770858416937216272158142281144782652750654697847840376002907226725362778292640956434687927315158519324142726613719655726444468707122866655123649786935639872601647255712257
r = 4788463264666184142381766080749720573563355321283908576415551013379


def next_prime(x: int) -> int:
    x += 1
    while not isPrime(x):
        x += 1
    return x


def rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    while True:
        x = random.randrange(2, n - 1)
        y, c, d = x, random.randrange(1, n - 1), 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def factorize(n: int) -> list[int]:
    fac = []
    stack = [n]
    while stack:
        m = stack.pop()
        if isPrime(m):
            fac.append(m)
        else:
            print(f"  {m.bit_length()}ビットの数を分解中...")
            d = rho(m)
            print(f"  -> 因数発見: {d}")
            stack.extend([d, m // d])
    return sorted(set(fac))


def cubic_roots(a: int, p: int) -> list[int]:
    a %= p
    if a == 0:
        return [0]

    try:
        roots = nthroot_mod(a, 3, p, all_roots=True)
        if roots is None:
            return []
        elif isinstance(roots, int):
            return [roots]
        else:
            return list(roots)
    except:
        if p % 3 == 2:
            return [pow(a, (2 * p - 1) // 3, p)]
        else:
            return []


def crt(remainders, moduli) -> int:
    M = math.prod(moduli)
    total = 0
    for r_i, m_i in zip(remainders, moduli):
        M_i = M // m_i
        total += r_i * M_i * pow(M_i, -1, m_i)
    return total % M


def main():
    alpha = next_prime(r) - r
    a = (n * pow(alpha, -1, r)) % r

    print(f"alpha = {alpha}")
    print(f"a = {a}")
    print(f"r のビット長: {r.bit_length()}")

    print("r を素因数分解中...")
    # 実際の素因数分解結果を使用
    primes_r = [39452413263115301, 43791431122423739, 47870133289895101, 57898699815348361]
    print(f"素因数の数: {len(primes_r)}")
    print(f"素因数: {primes_r}")

    roots_lists = [cubic_roots(a, p) for p in primes_r]
    print(f"各素因数での立方根の数: {[len(roots) for roots in roots_lists]}")
    total_combinations = math.prod(len(roots) for roots in roots_lists)
    print(f"CRTの組み合わせ総数: {total_combinations}")

    for i, roots in enumerate(product(*roots_lists)):
        if i % 100 == 0:
            print(f"  進捗: {i}/{total_combinations}")
        Q = crt(roots, primes_r)

        # より正確な推定
        # n ≈ q³ * A より q ≈ (n/A)^(1/3)
        A = next_prime(r)
        q_est = int((n // A) ** (1 / 3))
        k_center = (q_est - Q) // r
        SEARCH_RANGE = 2**20

        for k in range(k_center - SEARCH_RANGE, k_center + SEARCH_RANGE + 1):
            q = Q + k * r
            if q > 0 and n % q == 0:
                p = n // q
                print(f"\n成功！")
                print(f"k = {k}")
                print(f"q = {q}")
                print(f"p = {p}")
                phi = (p - 1) * (q - 1)
                d = pow(e, -1, phi)
                m = pow(c, d, n)
                flag = long_to_bytes(m)
                print(f"FLAG: {flag}")
                return


if __name__ == "__main__":
    main()