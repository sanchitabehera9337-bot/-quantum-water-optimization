 from itertools import product
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import time

# 1. PROBLEM DATA

water = [10, 20, 15, 25, 10, 20, 15, 25]
benefit = [8, 15, 12, 20, 7, 16, 11, 18]

MAX_WATER = 80
N = 8


# 2. CLASSICAL OPTIMIZATION

start = time.time()

best_solution = None
best_benefit = -1
best_water = 0

for solution in product([0, 1], repeat=N):

    total_water = sum(
        water[i] * solution[i]
        for i in range(N)
    )

    total_benefit = sum(
        benefit[i] * solution[i]
        for i in range(N)
    )

    if total_water <= MAX_WATER:
        if total_benefit > best_benefit:
            best_solution = solution
            best_benefit = total_benefit
            best_water = total_water

classical_time = time.time() - start


# 3. QUANTUM CIRCUIT

qc = QuantumCircuit(N, N)

# Superposition
for i in range(N):
    qc.h(i)

# Entanglement
for i in range(N - 1):
    qc.cx(i, i + 1)

# Measurement
qc.measure(range(N), range(N))


# 4. RUN QUANTUM SIMULATION

simulator = AerSimulator()

start = time.time()

result = simulator.run(
    qc,
    shots=1024
).result()

quantum_time = time.time() - start

counts = result.get_counts()


# 5. FIND BEST VALID QUANTUM RESULT

best_quantum = None
best_q_benefit = -1
best_q_water = 0

for bitstring, count in counts.items():

    # Qiskit bit order is reversed
    solution = tuple(
        int(bitstring[N - 1 - i])
        for i in range(N)
    )

    total_water = sum(
        water[i] * solution[i]
        for i in range(N)
    )

    total_benefit = sum(
        benefit[i] * solution[i]
        for i in range(N)
    )

    if total_water <= MAX_WATER:

        if total_benefit > best_q_benefit:
            best_quantum = solution
            best_q_benefit = total_benefit
            best_q_water = total_water


# 6. METRICS

if best_benefit != 0:
    quality = (best_q_benefit / best_benefit) * 100
else:
    quality = 0


# 7. FINAL OUTPUT

print("\n========== CLASSICAL RESULT ==========")

print("Best allocation:", best_solution)
print("Water used:", best_water)
print("Maximum benefit:", best_benefit)
print("Classical time:", classical_time)


print("\n========== QUANTUM RESULT ==========")

print("Best quantum allocation:", best_quantum)
print("Water used:", best_q_water)
print("Quantum benefit:", best_q_benefit)
print("Quantum simulation time:", quantum_time)


print("\n========== PERFORMANCE ==========")

print("Solution quality:", round(quality, 2), "%")

print("\nMeasurement counts:")
print(counts)