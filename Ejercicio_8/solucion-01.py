#!/usr/bin/env python3
"""Solución Ejercicio 1: Q-learning en Cliff Walking.

Implementación del algoritmo de control por diferencias temporales Q-learning tabular
(Watkins, 1989) sobre el entorno de la cuadrícula con acantilado (Cliff Walking)
descrito en el libro 'Reinforcement Learning: An Introduction' (Sutton & Barto, 2018).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml

# Configuración de matplotlib para entornos sin pantalla gráfica
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# Mapeo de vectores de desplazamiento por acción: (delta_fila, delta_columna)
# Fila 0 es la parte superior, Fila 3 es la inferior.
ACTION_DELTAS: Dict[str, Tuple[int, int]] = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

ACTION_SYMBOLS: Dict[str, str] = {
    "N": "↑",
    "E": "→",
    "S": "↓",
    "W": "←",
}


@dataclass(frozen=True)
class StepResult:
    next_state: Tuple[int, int]
    reward: float
    done: bool


class CliffWalkingEnv:
    """Entorno Cliff Walking (Sutton & Barto 4x12).

    - Cuadrícula de 4 filas x 12 columnas.
    - S = (3, 0)
    - G = (3, 11)
    - Acantilado = (3, 1) hasta (3, 10)
    - Caer al acantilado penaliza con -100.0 y regresa al agente a S sin terminar el episodio.
    - Llegar a G concluye el episodio con recompensa -1.0.
    - Movimientos normales o choques con muros reciben penalización de -1.0.
    """

    def __init__(
        self,
        rows: int = 4,
        cols: int = 12,
        start: Tuple[int, int] = (3, 0),
        goal: Tuple[int, int] = (3, 11),
        cliffs: Optional[List[Tuple[int, int]]] = None,
        step_reward: float = -1.0,
        cliff_reward: float = -100.0,
        goal_reward: float = -1.0,
    ) -> None:
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.cliffs = set(cliffs if cliffs is not None else [(3, c) for c in range(1, 11)])
        self.step_reward = step_reward
        self.cliff_reward = cliff_reward
        self.goal_reward = goal_reward
        self.state: Tuple[int, int] = self.start

    def reset(self) -> Tuple[int, int]:
        self.state = self.start
        return self.state

    def step(self, action: str) -> StepResult:
        df, dc = ACTION_DELTAS[action]
        nr = self.state[0] + df
        nc = self.state[1] + dc

        # Control de límites de la cuadrícula
        if nr < 0 or nr >= self.rows or nc < 0 or nc >= self.cols:
            next_state = self.state
        else:
            next_state = (nr, nc)

        # Verificación de colisión con acantilado o llegada a la meta
        if next_state in self.cliffs:
            self.state = self.start
            return StepResult(next_state=self.start, reward=self.cliff_reward, done=False)

        if next_state == self.goal:
            self.state = next_state
            return StepResult(next_state=next_state, reward=self.goal_reward, done=True)

        self.state = next_state
        return StepResult(next_state=next_state, reward=self.step_reward, done=False)


class QLearningAgent:
    """Agente Q-learning tabular (off-policy TD control)."""

    def __init__(
        self,
        actions: List[str],
        alpha: float = 0.5,
        gamma: float = 1.0,
        epsilon: float = 0.1,
        seed: Optional[int] = 42,
    ) -> None:
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table: Dict[Tuple[Tuple[int, int], str], float] = {}

        import random
        self.rng = random.Random(seed)

    def get_q(self, state: Tuple[int, int], action: str) -> float:
        return self.q_table.get((state, action), 0.0)

    def set_q(self, state: Tuple[int, int], action: str, value: float) -> None:
        self.q_table[(state, action)] = value

    def max_q(self, state: Tuple[int, int]) -> float:
        return max(self.get_q(state, a) for a in self.actions)

    def best_action(self, state: Tuple[int, int]) -> str:
        """Selección greedy con desempate determinista en el orden de acciones."""
        best_val = -float("inf")
        best_act = self.actions[0]
        for a in self.actions:
            val = self.get_q(state, a)
            if val > best_val:
                best_val = val
                best_act = a
        return best_act

    def choose_action(self, state: Tuple[int, int], epsilon: Optional[float] = None) -> str:
        eps = self.epsilon if epsilon is None else epsilon
        if self.rng.random() < eps:
            return self.rng.choice(self.actions)
        return self.best_action(state)

    def update(
        self,
        state: Tuple[int, int],
        action: str,
        reward: float,
        next_state: Tuple[int, int],
        done: bool,
    ) -> None:
        """Actualización de Bellman para Q-learning:
        Q(s, a) <- Q(s, a) + alpha * [ r + gamma * max_a' Q(s', a') - Q(s, a) ]
        """
        old_val = self.get_q(state, action)
        target = reward if done else reward + self.gamma * self.max_q(next_state)
        new_val = old_val + self.alpha * (target - old_val)
        self.set_q(state, action, new_val)


def train(
    env: CliffWalkingEnv,
    agent: QLearningAgent,
    num_episodes: int = 500,
    max_steps_per_episode: int = 200,
) -> List[float]:
    rewards_history: List[float] = []

    for ep in range(num_episodes):
        state = env.reset()
        ep_reward = 0.0

        for step in range(max_steps_per_episode):
            action = agent.choose_action(state)
            result = env.step(action)
            agent.update(state, action, result.reward, result.next_state, result.done)

            ep_reward += result.reward
            state = result.next_state

            if result.done:
                break

        rewards_history.append(ep_reward)

    return rewards_history


def evaluate_greedy(env: CliffWalkingEnv, agent: QLearningAgent, max_steps: int = 50) -> Tuple[float, List[Tuple[int, int]], List[str]]:
    state = env.reset()
    path = [state]
    actions_taken = []
    total_reward = 0.0

    for _ in range(max_steps):
        action = agent.best_action(state)
        actions_taken.append(action)
        result = env.step(action)
        total_reward += result.reward
        state = result.next_state
        path.append(state)
        if result.done:
            break

    return total_reward, path, actions_taken


def render_policy_grid(rows: int, cols: int, cliffs: set[Tuple[int, int]], goal: Tuple[int, int], agent: QLearningAgent) -> str:
    lines = []
    header = "     " + " ".join(f"{c:2d}" for c in range(cols))
    lines.append(header)
    lines.append("    +" + "--" * cols + "+")

    for r in range(rows):
        row_str = f" {r:2d} |"
        for c in range(cols):
            st = (r, c)
            if st == goal:
                row_str += "  G"
            elif st in cliffs:
                row_str += "  C"
            elif st == (3, 0):
                act = agent.best_action(st)
                row_str += f"  {ACTION_SYMBOLS[act]}"
            else:
                act = agent.best_action(st)
                row_str += f"  {ACTION_SYMBOLS[act]}"
        row_str += " |"
        lines.append(row_str)

    lines.append("    +" + "--" * cols + "+")
    return "\n".join(lines)


def plot_learning_curve(rewards: List[float], output_path: Path, window: int = 15) -> None:
    plt.figure(figsize=(9, 5))
    plt.plot(rewards, color="#aec7e8", alpha=0.6, label="Recompensa por Episodio")

    # Media móvil para suavizar
    if len(rewards) >= window:
        moving_avg = []
        for i in range(len(rewards)):
            start_idx = max(0, i - window + 1)
            moving_avg.append(sum(rewards[start_idx : i + 1]) / (i - start_idx + 1))
        plt.plot(moving_avg, color="#1f77b4", lw=2.2, label=f"Media Móvil ({window} ep.)")

    plt.axhline(y=-13.0, color="#d62728", linestyle="--", lw=1.5, label="Óptimo Greedy (-13)")
    plt.xlabel("Episodios de Entrenamiento", fontsize=11)
    plt.ylabel("Recompensa Acumulada", fontsize=11)
    plt.title("Curva de Aprendizaje: Q-learning en Cliff Walking (4x12)", fontsize=13)
    plt.ylim(-120, 5)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()


def main() -> None:
    current_dir = Path(__file__).resolve().parent
    config_path = current_dir / "envs" / "cliff.yaml"

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    else:
        cfg = {}

    rows = cfg.get("rows", 4)
    cols = cfg.get("cols", 12)
    start = tuple(cfg.get("start", [3, 0]))
    goal = tuple(cfg.get("goal", [3, 11]))
    raw_cliffs = cfg.get("cliffs", [[3, c] for c in range(1, 11)])
    cliffs = [tuple(c) for c in raw_cliffs]

    actions = cfg.get("actions", ["N", "E", "S", "W"])
    alpha = float(cfg.get("alpha", 0.5))
    gamma = float(cfg.get("gamma", 1.0))
    epsilon = float(cfg.get("epsilon", 0.1))
    episodes = int(cfg.get("episodes", 500))
    max_steps = int(cfg.get("max_steps_per_episode", 200))
    seed = int(cfg.get("seed", 42))

    print("=" * 60)
    print(" INICIANDO ENTRENAMIENTO Q-LEARNING: CLIFF WALKING")
    print("=" * 60)
    print(f"Dimensiones: {rows}x{cols} | Episodios: {episodes}")
    print(f"Hiperparámetros: alpha={alpha}, gamma={gamma}, epsilon={epsilon}, seed={seed}")

    env = CliffWalkingEnv(
        rows=rows,
        cols=cols,
        start=start,
        goal=goal,
        cliffs=cliffs,
        step_reward=float(cfg.get("step_reward", -1.0)),
        cliff_reward=float(cfg.get("cliff_reward", -100.0)),
        goal_reward=float(cfg.get("goal_reward", -1.0)),
    )

    agent = QLearningAgent(actions=actions, alpha=alpha, gamma=gamma, epsilon=epsilon, seed=seed)

    rewards = train(env, agent, num_episodes=episodes, max_steps_per_episode=max_steps)

    # Exportar historial a CSV
    csv_path = current_dir / "recompensas_entrenamiento.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["episodio", "recompensa"])
        for idx, r in enumerate(rewards, 1):
            writer.writerow([idx, r])
    print(f"[OK] Recompensas exportadas a: {csv_path.name}")

    # Generar gráfico de curva de aprendizaje
    plot_path = current_dir / "curva_aprendizaje.png"
    plot_learning_curve(rewards, plot_path)
    print(f"[OK] Curva de aprendizaje guardada en: {plot_path.name}")

    # Evaluación de la política greedy
    greedy_return, path, actions_seq = evaluate_greedy(env, agent)

    print("\n" + "=" * 60)
    print(" EVALUACIÓN DE LA POLÍTICA GREEDY (epsilon = 0)")
    print("=" * 60)
    print(f"Retorno acumulado obtenido: {greedy_return}")
    print(f"Número total de pasos: {len(actions_seq)}")
    print(f"Secuencia de acciones: {' -> '.join(actions_seq)}")
    print(f"Camino recorrido: {path}")

    print("\nMapa de la política aprendida:")
    print(render_policy_grid(rows, cols, set(cliffs), goal, agent))

    if greedy_return == -13.0:
        print("\n[ÉXITO] La política aprendida es estrictamente la óptima (-13.0).")
    else:
        print(f"\n[AVISO] Retorno greedy: {greedy_return} (esperado: -13.0)")


if __name__ == "__main__":
    main()

