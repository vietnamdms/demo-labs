#!/usr/bin/env python3
"""Render a local two-still-per-shot animatic. Never generates AI media."""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def inside(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError("media paths must be project-relative")
    p = (root / value).resolve()
    try:
        p.relative_to(root)
    except ValueError:
        raise ValueError(f"path escapes project: {value}")
    if not p.is_file() or not p.stat().st_size:
        raise ValueError(f"missing/empty media: {value}")
    return p


def run(argv):
    result = subprocess.run(argv, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:] or f"process failed: {argv[0]}")
    return result.stdout


def probe(path, ffprobe):
    return json.loads(run([ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]))


def finite_positive(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def render(plan_path, output, ffmpeg="ffmpeg", ffprobe="ffprobe"):
    plan_path = Path(plan_path).resolve()
    root = plan_path.parent
    output = Path(output).absolute()
    # Check the output location too; artifact files belong to this project.
    try:
        output.resolve().relative_to(root)
    except ValueError:
        raise ValueError("output must be inside the project")
    if output.exists() or output.is_symlink():
        raise ValueError("output exists; choose a new version filename")
    if output.suffix.lower() != ".mp4":
        raise ValueError("output must use .mp4")
    for binary in (ffmpeg, ffprobe):
        if not shutil.which(binary):
            raise ValueError(f"required binary not found: {binary}")
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("mode") != "animatic":
        raise ValueError("helper supports mode=animatic only")
    allowed = {"schema_version", "project_id", "version", "mode", "width", "height", "fps", "segments", "audio_path"}
    if set(plan) - allowed:
        raise ValueError(f"unsupported plan fields: {sorted(set(plan)-allowed)}; use an editor for richer timelines")
    width, height, fps = plan.get("width"), plan.get("height"), plan.get("fps")
    if not all(isinstance(x, int) and not isinstance(x, bool) and x > 0 and x % 2 == 0 for x in (width, height)):
        raise ValueError("width/height must be positive even integers")
    if not finite_positive(fps) or fps > 120:
        raise ValueError("fps must be finite, positive and <=120")
    segments = plan.get("segments")
    if not isinstance(segments, list) or not segments:
        raise ValueError("segments must be a nonempty array")
    prepared, total_frames = [], 0
    for seg in segments:
        if set(seg) - {"shot_id", "start_frame", "end_frame", "duration_s"}:
            raise ValueError("unsupported segment fields; helper does not implement motion/overlays/transitions")
        if not seg.get("shot_id") or not finite_positive(seg.get("duration_s")):
            raise ValueError("each segment requires shot_id and a positive finite duration_s")
        frames = round(seg["duration_s"] * fps)
        if frames < 2:
            raise ValueError("each shot needs at least two frames at selected fps")
        first = inside(root, seg.get("start_frame"))
        last = inside(root, seg.get("end_frame"))
        prepared.append((first, last, frames))
        total_frames += frames
    duration = total_frames / fps
    audio = inside(root, plan["audio_path"]) if plan.get("audio_path") else None
    if audio:
        info = probe(audio, ffprobe)
        if not any(s.get("codec_type") == "audio" for s in info.get("streams", [])):
            raise ValueError("guide file has no audio stream")
        audio_duration = float(info["format"]["duration"])
        if not math.isfinite(audio_duration) or audio_duration > duration + 1 / fps:
            raise ValueError(f"guide audio ({audio_duration}s) exceeds timeline ({duration}s); adjust timing, not truncate speech")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".animatic-", dir=output.parent) as tmp:
        work = Path(tmp)
        clips = []
        scale = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p"
        # Numeric filenames make concat listing independent of user-controlled path syntax.
        for first, last, frames in prepared:
            for src, count in ((first, frames // 2), (last, frames - frames // 2)):
                clip = work / f"{len(clips):06d}.mp4"
                run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n",
                     "-loop", "1", "-framerate", str(fps), "-i", str(src), "-an",
                     "-vf", scale, "-frames:v", str(count), "-r", str(fps),
                     "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", str(clip)])
                clips.append(clip)
        listing = work / "concat.txt"
        listing.write_text("".join(f"file '{p.name}'\n" for p in clips), encoding="utf-8")
        silent = work / "silent.mp4"
        run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n",
             "-f", "concat", "-safe", "1", "-i", str(listing), "-c", "copy", "-movflags", "+faststart", str(silent)])
        final = silent
        if audio:
            final = work / "with-audio.mp4"
            run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n",
                 "-i", str(silent), "-i", str(audio), "-map", "0:v:0", "-map", "1:a:0",
                 "-c:v", "copy", "-af", "apad", "-c:a", "aac", "-t", f"{duration:.9f}",
                 "-movflags", "+faststart", str(final)])
        metadata = probe(final, ffprobe)
        measured = float(metadata["format"]["duration"])
        if abs(measured - duration) > max(.1, 2 / fps):
            raise ValueError(f"unexpected encoded duration {measured} vs {duration}")
        # Same filesystem; link creation is atomic and refuses an existing destination.
        os.link(final, output)
    return {"output": str(output), "mode": "animatic", "duration_s": measured,
            "frames": total_frames, "shots": len(segments), "audio": bool(audio),
            "review": "unchecked", "note": "Metadata checked; watch/listen before marking ready."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    args = parser.parse_args()
    print(json.dumps(render(args.plan, args.output, args.ffmpeg, args.ffprobe), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, AttributeError, OSError, RuntimeError) as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
