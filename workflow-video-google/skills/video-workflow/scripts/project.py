#!/usr/bin/env python3
"""Local video manifest helper. No network, generation, or credit transactions."""
import argparse
import copy
import datetime
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile


def read_json(path):
    with path.open(encoding="utf-8") as f:
        value = json.load(f)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name}: expected JSON object")
    return value


def local_path(root, value):
    if not isinstance(value, str) or not value:
        raise ValueError("nonempty project-relative path required")
    p = Path(value)
    if p.is_absolute():
        raise ValueError(f"absolute path not allowed in manifest: {value}")
    result = (root / p).resolve()
    try:
        result.relative_to(root.resolve())
    except ValueError:
        raise ValueError(f"path escapes project: {value}")
    return result


def atomic_write(path, data, backup=False):
    if backup and path.exists():
        backup_dir = path.parent / ".manifest-backups"
        backup_dir.mkdir(exist_ok=True)
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        shutil.copy2(path, backup_dir / f"project-{stamp}.json")
    fd, tmp = tempfile.mkstemp(prefix=".manifest-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, allow_nan=False)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def positive(n):
    return isinstance(n, (float, int)) and not isinstance(n, bool) and math.isfinite(n) and n > 0


def integer(n):
    return isinstance(n, int) and not isinstance(n, bool) and n > 0


def pointer(doc, selector):
    if selector == "":
        return doc
    if not isinstance(selector, str) or not selector.startswith("/"):
        raise ValueError("selector must be a JSON Pointer")
    node = doc
    for raw in selector.split("/")[1:]:
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", token):
                raise ValueError("invalid array index")
            node = node[int(token)]
        else:
            node = node[token]
    return node


def validate(root):
    root = Path(root).resolve()
    errors, warnings = [], []
    def need(ok, message):
        if not ok:
            errors.append(message)
    def envelope(doc, name):
        need(doc.get("schema_version") == "1.0", f"{name}: schema_version must be 1.0")
        need(doc.get("project_id") == project.get("project_id"), f"{name}: project_id mismatch")
        need(integer(doc.get("version")), f"{name}: positive integer version required")
    def indexed(items, key, name):
        if not isinstance(items, list):
            raise ValueError(f"{name}: expected array")
        result = {}
        for item in items:
            if not isinstance(item, dict):
                raise ValueError(f"{name}: expected object entries")
            identity = item.get(key)
            if not isinstance(identity, str) or not identity:
                errors.append(f"{name}: missing {key}")
                continue
            need(identity not in result, f"{name}: duplicate {identity}")
            result[identity] = item
        return result
    def file_check(value, label, required=True):
        try:
            p = local_path(root, value)
            if required:
                need(p.is_file() and p.stat().st_size > 0, f"{label}: missing or empty file {value}")
            return p
        except (ValueError, OSError) as e:
            errors.append(f"{label}: {e}")
            return None

    project = read_json(root / "project.json")
    envelope(project, "project.json")
    need(bool(project.get("project_id")), "project_id required")
    brief = project.get("brief", {})
    fmt = brief.get("format")
    need(fmt in ("short", "youtube-long"), "brief.format invalid")
    allowed_platforms = ("tiktok", "youtube-shorts") if fmt == "short" else ("youtube",)
    need(brief.get("platform") in allowed_platforms, "platform does not match format")
    need(positive(brief.get("target_duration_s")), "target duration must be positive")
    need(brief.get("aspect_ratio") in ("9:16", "16:9", "1:1"), "invalid aspect_ratio")
    need(brief.get("audio_mode") in ("narration", "sync-dialogue", "ambient", "none"), "invalid audio_mode")
    budget = project.get("budget", {})
    credits = budget.get("max_credits")
    need(credits is None or (isinstance(credits, (int, float)) and not isinstance(credits, bool) and math.isfinite(credits) and credits >= 0), "max_credits must be null or nonnegative")
    need(integer(budget.get("max_attempts_per_shot")), "positive attempt limit required")
    artifacts = indexed(project.get("artifacts", []), "id", "artifacts")
    for aid, a in artifacts.items():
        need(integer(a.get("version")), f"{aid}: positive version required")
        need(a.get("kind") in ("document", "image", "audio", "video"), f"{aid}: invalid kind")
        need(a.get("status") in ("planned", "ready", "needs-revision", "blocked"), f"{aid}: invalid status")
        review = a.get("review", {}).get("status")
        need(review in ("unchecked", "pass", "needs-revision"), f"{aid}: invalid review")
        ready = a.get("status") == "ready"
        p = file_check(a.get("path"), aid, ready)
        if ready:
            need(review == "pass", f"{aid}: ready requires review pass")
        if "selector" in a and p and p.is_file():
            try:
                pointer(read_json(p), a["selector"])
            except (ValueError, KeyError, IndexError, TypeError) as e:
                errors.append(f"{aid}: invalid selector ({e})")
        for dep in a.get("depends_on", []):
            source = artifacts.get(dep.get("id"))
            need(source is not None, f"{aid}: unknown dependency {dep.get('id')}")
            need(integer(dep.get("version")), f"{aid}: dependency version required")
            if source and ready:
                need(source.get("version") == dep.get("version"), f"{aid}: stale dependency {dep['id']}")
                need(source.get("status") == "ready", f"{aid}: dependency {dep['id']} not ready")
    visiting, visited = set(), set()
    def visit(aid):
        if aid in visiting:
            errors.append(f"dependency cycle at {aid}")
            return
        if aid in visited:
            return
        visiting.add(aid)
        for dep in artifacts[aid].get("depends_on", []):
            if dep.get("id") in artifacts:
                visit(dep["id"])
        visiting.remove(aid)
        visited.add(aid)
    for aid in artifacts:
        visit(aid)

    docs = {}
    for name in ("script", "shotlist", "assets", "frames", "audio-plan", "renders", "edit-plan"):
        path = root / f"{name}.json"
        if path.exists():
            docs[name] = read_json(path)
            envelope(docs[name], path.name)
    beats, shots = {}, {}
    if "script" in docs:
        s = docs["script"]
        need(s.get("format") == fmt, "script format mismatch")
        need(s.get("platform") == brief.get("platform"), "script platform mismatch")
        beats = indexed(s.get("beats", []), "beat_id", "beats")
        need(bool(beats), "script must have beats")
        chapters = indexed(s.get("chapters", []), "chapter_id", "chapters")
        for bid, b in beats.items():
            need(b.get("role") in ("hook", "content", "payoff", "ending"), f"{bid}: invalid role")
            need(positive(b.get("estimated_duration_s")), f"{bid}: invalid estimated duration")
            need(isinstance(b.get("spoken"), str) and bool(b.get("visual")), f"{bid}: spoken/visual required")
            if fmt == "youtube-long":
                need(b.get("chapter_id") in chapters, f"{bid}: unknown chapter")
        if fmt == "youtube-long":
            need(bool(chapters), "long script requires chapters")
            package = s.get("packaging", {})
            need(all(package.get(k) for k in ("title_concept", "thumbnail_concept", "promise")), "long script requires packaging concepts")
        hook = s.get("hook", {})
        h, pay = hook.get("beat_id"), hook.get("payoff_beat_id")
        need(bool(hook.get("hook_id")) and bool(hook.get("promise")) and bool(hook.get("visual")), "hook id/promise/visual required")
        need(h in beats and beats[h].get("role") == "hook", "hook beat missing or wrong role")
        need(pay in beats and beats[pay].get("role") == "payoff", "payoff beat missing or wrong role")
        order = list(beats)
        if h in beats and pay in beats:
            need(order.index(h) == 0 and order.index(pay) > order.index(h), "hook must open script and precede payoff")
    if "shotlist" in docs:
        doc = docs["shotlist"]
        need(doc.get("timing_basis") in ("estimated", "measured", "action"), "shot timing basis invalid")
        shots = indexed(doc.get("shots", []), "shot_id", "shots")
        need(bool(shots), "shotlist must have shots")
        covered = set()
        for sid, s in shots.items():
            need(all(s.get(k) for k in ("scene_id", "start_state", "end_state", "motion", "camera")), f"{sid}: missing direction/state")
            need(positive(s.get("duration_s")), f"{sid}: invalid duration")
            need(bool(s.get("beat_ids")), f"{sid}: missing beat link")
            for bid in s.get("beat_ids", []):
                covered.add(bid)
                if "script" in docs:
                    need(bid in beats, f"{sid}: unknown beat {bid}")
            transition = s.get("transition", {})
            target = transition.get("target_shot_id")
            need(transition.get("type") in ("cut", "match-cut", "continuous", "dissolve", "end"), f"{sid}: invalid transition")
            need(target is None or target in shots, f"{sid}: unknown next shot")
            handles = s.get("handles", {})
            head, tail = handles.get("head_s", 0), handles.get("tail_s", 0)
            need(all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x >= 0 for x in (head, tail)), f"{sid}: invalid trim handles")
            gen = s.get("generation_duration_s")
            if gen is not None:
                need(positive(gen), f"{sid}: invalid generation duration")
                if positive(gen) and positive(s.get("duration_s")) and all(isinstance(x, (int, float)) for x in (head, tail)):
                    need(gen + 1e-6 >= s["duration_s"] + head + tail, f"{sid}: generation shorter than edit plus handles")
        if beats:
            need(set(beats) <= covered, "shotlist does not cover all beats")
        if all(positive(s.get("duration_s")) for s in shots.values()) and positive(brief.get("target_duration_s")):
            total = sum(s["duration_s"] for s in shots.values())
            if abs(total - brief["target_duration_s"]) > .1:
                warnings.append(f"shot durations total {total}s vs brief {brief['target_duration_s']}s; review timeline/overlap")
    if "assets" in docs:
        assets = indexed(docs["assets"].get("assets", []), "asset_id", "assets")
        for aid, a in assets.items():
            for p in a.get("image_paths", []):
                file_check(p, aid, a.get("review", {}).get("status") == "pass")
        for sid, s in shots.items():
            for aid in s.get("reference_ids", []):
                need(aid in assets, f"{sid}: unknown reference {aid}")
    if "frames" in docs:
        pairs = indexed(docs["frames"].get("pairs", []), "shot_id", "frame pairs")
        if "shotlist" in docs:
            need(set(pairs) == set(shots), "frame pairs must cover exactly the shotlist")
        for sid, p in pairs.items():
            for end in ("start", "end"):
                path = p.get(f"{end}_path")
                file_check(path, f"{sid}.{end}", p.get("review", {}).get("status") == "pass")
                aid = p.get(f"{end}_artifact_id")
                need(aid in artifacts, f"{sid}: unknown {end} artifact")
                if aid in artifacts:
                    need(path == artifacts[aid].get("path"), f"{sid}: {end} path differs from registry")
    if "audio-plan" in docs:
        a = docs["audio-plan"]
        duration = a.get("duration_s")
        if a.get("path"):
            file_check(a["path"], "audio")
        if a.get("timing_basis") == "measured":
            need(bool(a.get("path")) and positive(duration), "measured audio requires file and duration")
        cues = indexed(a.get("cues", []), "cue_id", "audio cues")
        for cid, cue in cues.items():
            start, end = cue.get("start_s"), cue.get("end_s")
            valid = isinstance(start, (int, float)) and not isinstance(start, bool) and math.isfinite(start) and start >= 0 and positive(end) and end > start
            need(valid, f"{cid}: invalid cue interval")
            if valid and positive(duration):
                need(end <= duration + .05, f"{cid}: cue exceeds measured audio")
            for bid in cue.get("beat_ids", []):
                if "script" in docs:
                    need(bid in beats, f"{cid}: unknown beat")
    if "renders" in docs:
        renders = docs["renders"]
        takes = indexed(renders.get("takes", []), "take_id", "takes")
        for tid, take in takes.items():
            need(take.get("status") in ("planned", "submitted", "running", "succeeded", "failed", "unknown", "downloaded"), f"{tid}: invalid job status")
            if "shotlist" in docs:
                need(take.get("shot_id") in shots, f"{tid}: unknown shot")
            if take.get("status") == "downloaded":
                file_check(take.get("path"), tid)
        for sid, tid in renders.get("selected", {}).items():
            take = takes.get(tid)
            need(take is not None, f"selected {sid}: unknown take")
            if not take:
                continue
            need(take.get("shot_id") == sid, f"selected {sid}: take belongs to another shot")
            need(take.get("status") == "downloaded" and take.get("review", {}).get("status") == "pass", f"selected {tid}: requires downloaded and review pass")
            need(bool(take.get("input_versions")), f"selected {tid}: input versions required")
            for inp in take.get("input_versions", []):
                source = artifacts.get(inp.get("id"))
                need(source is not None and source.get("version") == inp.get("version") and source.get("status") == "ready", f"selected {tid}: stale/unready input {inp.get('id')}")
    if "edit-plan" in docs:
        edit = docs["edit-plan"]
        need(edit.get("mode") in ("animatic", "final"), "edit mode invalid")
        for s in edit.get("segments", []):
            need(positive(s.get("duration_s")), "edit segment duration invalid")
            if "shotlist" in docs:
                need(s.get("shot_id") in shots, "edit has unknown shot")
            keys = ("start_frame", "end_frame") if edit.get("mode") == "animatic" else ("video_path",)
            for key in keys:
                file_check(s.get(key), f"edit {s.get('shot_id')}")
            if edit.get("mode") == "final" and "renders" in docs:
                need(docs["renders"].get("selected", {}).get(s.get("shot_id")) == s.get("take_id"), "edit uses unselected take")
        if edit.get("audio_path"):
            file_check(edit["audio_path"], "edit audio")
    return errors, warnings


def revise(root, artifact_id, reason):
    root = Path(root).resolve()
    path = root / "project.json"
    project = read_json(path)
    entries = project.get("artifacts", [])
    by_id = {a["id"]: a for a in entries}
    if len(by_id) != len(entries):
        raise ValueError("duplicate artifact IDs; repair manifest before revise")
    if artifact_id not in by_id:
        raise ValueError(f"unknown artifact: {artifact_id}")
    affected = {artifact_id}
    while True:
        expanded = affected | {aid for aid, a in by_id.items() if any(d.get("id") in affected for d in a.get("depends_on", []))}
        if expanded == affected:
            break
        affected = expanded
    if not integer(by_id[artifact_id].get("version")):
        raise ValueError("invalid version")
    by_id[artifact_id]["version"] += 1
    for aid in affected:
        by_id[aid]["status"] = "needs-revision"
        by_id[aid]["review"] = {"status": "unchecked", "notes": reason}
    project["version"] += 1
    atomic_write(path, project, backup=True)
    return sorted(affected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("root", type=Path)
    init.add_argument("--id", required=True)
    init.add_argument("--format", choices=["short", "youtube-long"], required=True)
    init.add_argument("--platform", choices=["tiktok", "youtube-shorts", "youtube"], required=True)
    init.add_argument("--idea", required=True)
    init.add_argument("--duration", type=float, required=True)
    init.add_argument("--audio-mode", choices=["narration", "sync-dialogue", "ambient", "none"], default="narration")
    check = sub.add_parser("validate")
    check.add_argument("root", type=Path)
    change = sub.add_parser("revise")
    change.add_argument("root", type=Path)
    change.add_argument("--artifact", required=True)
    change.add_argument("--reason", required=True)
    args = parser.parse_args()
    if args.command == "init":
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.id) or not positive(args.duration):
            raise ValueError("use a lowercase slug id and positive finite duration")
        if (args.format == "short") != (args.platform in ("tiktok", "youtube-shorts")):
            raise ValueError("platform does not match format")
        args.root.mkdir(parents=True, exist_ok=True)
        dest = args.root / "project.json"
        data = {"schema_version": "1.0", "project_id": args.id, "version": 1,
                "brief": {"idea": args.idea, "format": args.format, "platform": args.platform,
                          "language": "vi", "audience": "", "goal": "", "target_duration_s": args.duration,
                          "aspect_ratio": "9:16" if args.format == "short" else "16:9",
                          "style": "", "audio_mode": args.audio_mode,
                          "assumptions": ["Tỉ lệ mặc định theo định dạng; bổ sung audience, goal và style trước sản xuất."]},
                "budget": {"max_credits": None, "max_attempts_per_shot": 2}, "artifacts": []}
        with dest.open("x", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, allow_nan=False)
            f.write("\n")
        print(json.dumps({"created": str(dest.resolve())}, ensure_ascii=False))
    elif args.command == "validate":
        errors, warnings = validate(args.root)
        print(json.dumps({"valid": not errors, "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    else:
        print(json.dumps({"affected": revise(args.root, args.artifact, args.reason)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, TypeError, AttributeError, OSError, RecursionError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
