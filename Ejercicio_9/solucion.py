#!/usr/bin/env python3
"""Solución Ejercicio 1: Encadenamiento en la biblioteca.

Inferencia con cláusulas definidas de primer orden (Russell & Norvig, AIMA Cap. 9):
- Encadenamiento hacia adelante (Forward Chaining) exhaustivo por rondas.
- Encadenamiento hacia atrás (Backward Chaining) guiado por metas y recursivo.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import yaml


# ==============================================================================
# 1. Representación de Átomos y Reglas
# ==============================================================================

_ATOM_PATTERN = re.compile(r"^([A-Za-z_][\w]*)\s*(?:\((.*)\))?$")


@dataclass(frozen=True)
class Atom:
    predicate: str
    args: Tuple[str, ...]

    def __str__(self) -> str:
        if not self.args:
            return self.predicate
        return f"{self.predicate}({', '.join(self.args)})"

    @classmethod
    def parse(cls, text: str) -> Atom:
        m = _ATOM_PATTERN.match(text.strip())
        if not m:
            raise ValueError(f"Formato de átomo no válido: {text}")
        pred = m.group(1)
        raw_args = m.group(2)
        if raw_args is None or not raw_args.strip():
            return cls(predicate=pred, args=())
        args = tuple(arg.strip() for arg in raw_args.split(","))
        return cls(predicate=pred, args=args)


def is_variable(term: str) -> bool:
    """Una variable inicia con minúscula; una constante inicia con mayúscula."""
    return term[0].islower()


@dataclass
class Rule:
    rule_id: str
    premises: List[Atom]
    conclusion: Atom

    def __str__(self) -> str:
        prems = " ^ ".join(str(p) for p in self.premises)
        return f"[{self.rule_id}] {prems} => {self.conclusion}"


# ==============================================================================
# 2. Unificación y Sustitución
# ==============================================================================

Substitution = Dict[str, str]


def apply_subst(term: str, theta: Substitution) -> str:
    while is_variable(term) and term in theta:
        term = theta[term]
    return term


def apply_subst_atom(atom: Atom, theta: Substitution) -> Atom:
    return Atom(atom.predicate, tuple(apply_subst(arg, theta) for arg in atom.args))


def unify_terms(x: str, y: str, theta: Substitution) -> Optional[Substitution]:
    if theta is None:
        return None
    x = apply_subst(x, theta)
    y = apply_subst(y, theta)

    if x == y:
        return theta
    if is_variable(x):
        new_theta = dict(theta)
        new_theta[x] = y
        return new_theta
    if is_variable(y):
        new_theta = dict(theta)
        new_theta[y] = x
        return new_theta
    return None


def unify_atoms(a1: Atom, a2: Atom, theta: Optional[Substitution] = None) -> Optional[Substitution]:
    if theta is None:
        theta = {}
    if a1.predicate != a2.predicate or len(a1.args) != len(a2.args):
        return None
    curr_theta = dict(theta)
    for arg1, arg2 in zip(a1.args, a2.args):
        res = unify_terms(arg1, arg2, curr_theta)
        if res is None:
            return None
        curr_theta = res
    return curr_theta


# ==============================================================================
# 3. Encadenamiento hacia Adelante (Forward Chaining)
# ==============================================================================

def match_premises(
    premises: List[Atom],
    facts: List[Atom],
    theta: Substitution,
) -> List[Substitution]:
    """Encuentra todas las sustituciones compatibles con las premisas en orden."""
    if not premises:
        return [theta]

    premise = premises[0]
    rest = premises[1:]
    results = []

    for fact in facts:
        subst = unify_atoms(premise, fact, theta)
        if subst is not None:
            results.extend(match_premises(rest, facts, subst))

    return results


def forward_chaining(
    initial_facts: List[Atom],
    rules: List[Rule],
    query: Atom,
) -> Tuple[bool, List[Atom], List[str]]:
    """Encadenamiento hacia adelante por rondas exhaustivas."""
    facts = list(initial_facts)
    derived_new: List[Atom] = []
    trace_lines: List[str] = []

    trace_lines.append(f"Hechos iniciales: {', '.join(str(f) for f in facts)}")
    trace_lines.append(f"Consulta objetivo: {query}")

    round_idx = 1
    while True:
        round_header = f"--- Ronda {round_idx} ---"
        trace_lines.append(round_header)
        new_facts_this_round: List[Atom] = []

        # Evaluación sobre los hechos conocidos al iniciar la ronda
        facts_at_start = list(facts)

        for rule in rules:
            matches = match_premises(rule.premises, facts_at_start, {})
            for match in matches:
                derived = apply_subst_atom(rule.conclusion, match)
                if derived not in facts and derived not in new_facts_this_round:
                    new_facts_this_round.append(derived)
                    derived_new.append(derived)
                    bindings_str = ", ".join(f"{k}={v}" for k, v in match.items())
                    trace_lines.append(f"  Regla disparada {rule.rule_id} con {{{bindings_str}}} => Deriva: {derived}")

        if not new_facts_this_round:
            trace_lines.append("  (No se derivaron átomos nuevos. Punto fijo alcanzado).")
            break

        facts.extend(new_facts_this_round)
        round_idx += 1

    # Verificar si la consulta queda probada en los hechos finales
    proved = any(unify_atoms(query, f) is not None for f in facts)
    status_str = "PROBADA" if proved else "NO PROBADA"
    trace_lines.append(f"Resultado final de {query}: {status_str}")

    return proved, derived_new, trace_lines


# ==============================================================================
# 4. Encadenamiento hacia Atrás (Backward Chaining)
# ==============================================================================

def backward_chaining_prove(
    goal: Atom,
    facts: List[Atom],
    rules: List[Rule],
    goal_stack: List[Atom],
    trace_lines: List[str],
    indent: int = 0,
) -> Optional[Substitution]:
    """Prueba recursiva de metas con corte en la primera solución."""
    prefix = "  " * indent
    trace_lines.append(f"{prefix}Probando meta: {goal}")

    # Chequeo de ciclo
    if any(g == goal for g in goal_stack):
        trace_lines.append(f"{prefix}  [Ciclo detectado en {goal}. Se descarta rama.]")
        return None

    # 1. Intentar unificar primero contra hechos conocidos
    for fact in facts:
        subst = unify_atoms(goal, fact, {})
        if subst is not None:
            trace_lines.append(f"{prefix}  [Éxito con hecho]: {fact}")
            return subst

    # 2. Intentar unificar contra reglas en orden de tabla
    new_stack = goal_stack + [goal]
    for rule in rules:
        subst = unify_atoms(goal, rule.conclusion, {})
        if subst is None:
            continue

        trace_lines.append(f"{prefix}  Intentando regla {rule.rule_id} para {goal}")
        curr_subst = dict(subst)
        rule_success = True

        for premise in rule.premises:
            subst_premise = apply_subst_atom(premise, curr_subst)
            premise_subst = backward_chaining_prove(
                subst_premise, facts, rules, new_stack, trace_lines, indent + 2
            )
            if premise_subst is None:
                trace_lines.append(f"{prefix}  [Fallo en premisa {subst_premise}] => Regla {rule.rule_id} no prospera.")
                rule_success = False
                break
            curr_subst.update(premise_subst)

        if rule_success:
            trace_lines.append(f"{prefix}  [Éxito con regla]: {rule.rule_id} prueba {goal}")
            return curr_subst

    trace_lines.append(f"{prefix}[Fallo]: No se pudo probar {goal}")
    return None


def backward_chaining(
    facts: List[Atom],
    rules: List[Rule],
    query: Atom,
) -> Tuple[bool, List[str]]:
    trace_lines: List[str] = []
    trace_lines.append(f"Iniciando Encadenamiento hacia Atrás para la meta: {query}")
    res = backward_chaining_prove(query, facts, rules, [], trace_lines, indent=0)
    proved = res is not None
    status_str = "PROBADA" if proved else "NO PROBADA"
    trace_lines.append(f"Resultado final de {query}: {status_str}")
    return proved, trace_lines


# ==============================================================================
# 5. Carga de Base de Conocimiento y Ejecución Principal
# ==============================================================================

def load_kb(yaml_path: Path) -> Tuple[List[Atom], List[Rule], Optional[Atom]]:
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    facts = [Atom.parse(item) for item in data.get("facts", [])]

    rules = []
    for r in data.get("rules", []):
        rule_id = r["id"]
        prems = [Atom.parse(p) for p in r["if"]]
        conc = Atom.parse(r["then"])
        rules.append(Rule(rule_id=rule_id, premises=prems, conclusion=conc))

    query = Atom.parse(data["query"]) if "query" in data else None
    return facts, rules, query


def main() -> None:
    current_dir = Path(__file__).resolve().parent
    kb_path = current_dir / "biblioteca.yaml"

    facts, rules, default_query = load_kb(kb_path)

    queries_to_test = [
        Atom.parse("AccesoNoche(Ana)"),
        Atom.parse("AccesoNoche(Luis)"),
        Atom.parse("AccesoNoche(Marta)"),
    ]

    print("=" * 70)
    print(" BASE DE CONOCIMIENTO: CONTROL DE ACCESO A LA BIBLIOTECA")
    print("=" * 70)
    print(f"Hechos ({len(facts)}): {', '.join(str(f) for f in facts)}")
    print(f"Reglas ({len(rules)}):")
    for r in rules:
        print(f"  {r}")
    print()

    # Evaluación de las tres consultas solicitadas
    for q in queries_to_test:
        print("=" * 70)
        print(f" CONSULTA: {q}")
        print("=" * 70)

        # 1. Forward Chaining
        fc_proved, fc_derived, fc_trace = forward_chaining(facts, rules, q)
        print(f"\n[FORWARD CHAINING] - {q}: {'PROBADA' if fc_proved else 'NO PROBADA'}")
        print(f"Átomos nuevos derivados ({len(fc_derived)}):")
        for idx, atom in enumerate(fc_derived, 1):
            print(f"  {idx}. {atom}")
        print("\nTraza de Forward Chaining:")
        for line in fc_trace:
            print(line)

        # 2. Backward Chaining
        bc_proved, bc_trace = backward_chaining(facts, rules, q)
        print(f"\n[BACKWARD CHAINING] - {q}: {'PROBADA' if bc_proved else 'NO PROBADA'}")
        print("\nTraza de Backward Chaining:")
        for line in bc_trace:
            print(line)
        print()

    # Experimento Adicional: Agregar TieneCredencial(Luis)
    print("=" * 70)
    print(" EXPERIMENTO ADICIONAL: Se añade el hecho 'TieneCredencial(Luis)'")
    print("=" * 70)
    mod_facts = list(facts) + [Atom.parse("TieneCredencial(Luis)")]
    q_luis = Atom.parse("AccesoNoche(Luis)")

    fc_p, fc_der, _ = forward_chaining(mod_facts, rules, q_luis)
    bc_p, _ = backward_chaining(mod_facts, rules, q_luis)

    print(f"Consulta AccesoNoche(Luis) con credencial:")
    print(f"  Forward Chaining:  {'PROBADA' if fc_p else 'NO PROBADA'}")
    print(f"  Backward Chaining: {'PROBADA' if bc_p else 'NO PROBADA'}")
    print(f"  Nuevos átomos derivados en FC: {[str(a) for a in fc_der]}")


if __name__ == "__main__":
    main()

