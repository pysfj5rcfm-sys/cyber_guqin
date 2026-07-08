#!/usr/bin/env python3
"""Build deterministic P2 visual candidate lattices without parsing."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


AUTHORITY_FLAGS = {
    "NOT_SCORE_AUTHORITY": True,
    "NOT_DAPU_IR_AUTHORITY": True,
    "NOT_CANON_AUTHORITY": True,
    "NOT_SCORE_EVENT_AUTHORITY": True,
    "NOT_SAMPLE_INGEST": True,
    "NOT_ML_TRAINING_DATA": True,
}


class CandidateLattice:
    """Convert ComponentCandidateSet output into a visual candidate lattice."""

    def build(
        self,
        component_candidates: dict[str, Any] | list[dict[str, Any]],
        grammar_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        candidate_sets = _normalize_candidate_sets(component_candidates)
        nodes_by_crop: list[list[dict[str, Any]]] = []
        unresolved: list[dict[str, Any]] = []

        for candidate_set in candidate_sets:
            crop_id = str(candidate_set.get("crop_id") or "crop")
            candidates = sorted(
                list(candidate_set.get("candidates") or []),
                key=lambda item: (int(item.get("rank", 0)), str(item.get("component_id", ""))),
            )
            crop_nodes = [
                _node_from_candidate(crop_id, candidate, grammar_context or {})
                for candidate in candidates
            ]
            nodes_by_crop.append(crop_nodes)
            if candidate_set.get("status") == "UNKNOWN_COMPONENT" or not candidates:
                state = candidate_set.get("unknown_component_state") or {}
                unresolved.append(
                    {
                        "crop_id": crop_id,
                        "status": "UNKNOWN_COMPONENT",
                        "reason": state.get("unresolved_reason") or "UNKNOWN_COMPONENT",
                    }
                )

        nodes = [node for crop_nodes in nodes_by_crop for node in crop_nodes]
        edges = _build_edges(nodes_by_crop)
        ranking = _ranking(nodes)
        return {
            "nodes": nodes,
            "edges": edges,
            "ranking": ranking,
            "unresolved": unresolved,
            "authority_flags": dict(AUTHORITY_FLAGS),
            "lattice_trace": {
                "runtime_layer": "P2_VISUAL_CANDIDATE_LATTICE",
                "p1_parse_called": False,
                "grammar_hook_only": True,
                "deterministic": True,
            },
        }


def _normalize_candidate_sets(value: dict[str, Any] | list[dict[str, Any]]) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        if "candidates" in value:
            return [value]
        return [{"crop_id": "crop", "status": "MATCHED", "candidates": [value]}]
    if not isinstance(value, list):
        raise TypeError("component_candidates must be a candidate set, candidate list, or list of candidate sets")
    if all(isinstance(item, dict) and "candidates" in item for item in value):
        return value
    return [{"crop_id": "crop", "status": "MATCHED", "candidates": value}]


def _node_from_candidate(crop_id: str, candidate: dict[str, Any], grammar_context: dict[str, Any]) -> dict[str, Any]:
    rank = int(candidate.get("rank", 0))
    component_id = str(candidate.get("component_id") or "")
    breakdown = dict(candidate.get("score_breakdown") or {})
    if grammar_context:
        breakdown = _with_lattice_grammar_adjustment(candidate, breakdown, grammar_context)
    return {
        "node_id": f"{crop_id}:{rank}:{component_id}",
        "crop_id": crop_id,
        "component_id": component_id,
        "label": candidate.get("label", ""),
        "category": candidate.get("category", ""),
        "lexical_component_type": candidate.get("lexical_component_type", "UNKNOWN_COMPONENT"),
        "visual_score": round(float(candidate.get("visual_score", 0.0)), 3),
        "rank": rank,
        "score_breakdown": breakdown,
    }


def _with_lattice_grammar_adjustment(
    candidate: dict[str, Any],
    breakdown: dict[str, Any],
    grammar_context: dict[str, Any],
) -> dict[str, Any]:
    allowed = set(grammar_context.get("allowed_lexical_types") or [])
    if not allowed:
        return breakdown
    grammar = 1.0 if candidate.get("lexical_component_type") in allowed else 0.0
    visual = float(breakdown.get("visual", candidate.get("visual_score", 0.0)))
    lexical = float(breakdown.get("lexical", 1.0))
    penalty = float(breakdown.get("uncertainty_penalty", 0.0))
    final = max(0.0, min(1.0, 0.68 * visual + 0.18 * lexical + 0.14 * grammar - penalty))
    adjusted = dict(breakdown)
    adjusted["grammar"] = round(grammar, 3)
    adjusted["final"] = round(final, 3)
    return adjusted


def _build_edges(nodes_by_crop: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    for index in range(len(nodes_by_crop) - 1):
        for source in nodes_by_crop[index]:
            for target in nodes_by_crop[index + 1]:
                score = min(
                    float(source.get("score_breakdown", {}).get("final", 0.0)),
                    float(target.get("score_breakdown", {}).get("final", 0.0)),
                )
                edges.append(
                    {
                        "edge_id": f"{source['node_id']}->{target['node_id']}",
                        "source": source["node_id"],
                        "target": target["node_id"],
                        "edge_type": "NEXT_CROP_CANDIDATE",
                        "compatibility_score": round(score, 3),
                    }
                )
    return sorted(edges, key=lambda item: item["edge_id"])


def _ranking(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    ranking: dict[str, dict[str, Any]] = {}
    for node in sorted(nodes, key=lambda item: (item["crop_id"], item["rank"], item["component_id"])):
        key = node["component_id"]
        if key in ranking:
            key = node["node_id"]
        ranking[key] = dict(node.get("score_breakdown") or {})
    return ranking


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a P2 visual candidate lattice from matcher JSON.")
    parser.add_argument("candidate_json")
    args = parser.parse_args(argv)
    data = json.loads(Path(args.candidate_json).read_text(encoding="utf-8"))
    print(json.dumps(CandidateLattice().build(data), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
