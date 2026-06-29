"use client";
import { KV } from "@/lib/types";

export default function KeyValueEditor({
  rows,
  onChange,
  keyPlaceholder = "Key",
  valuePlaceholder = "Value",
}: {
  rows: KV[];
  onChange: (rows: KV[]) => void;
  keyPlaceholder?: string;
  valuePlaceholder?: string;
}) {
  const ensureTrailing = (arr: KV[]) => {
    const last = arr[arr.length - 1];
    if (!last || last.key || last.value)
      return [...arr, { key: "", value: "", enabled: true }];
    return arr;
  };
  const display = ensureTrailing(rows);

  const update = (i: number, patch: Partial<KV>) => {
    const next = display.map((r, idx) => (idx === i ? { ...r, ...patch } : r));
    onChange(next.filter((r, idx) => idx === next.length - 1 || r.key || r.value));
  };
  const remove = (i: number) => {
    onChange(display.filter((_, idx) => idx !== i));
  };

  return (
    <div className="border border-[var(--border)] rounded">
      <div className="grid grid-cols-[32px_1fr_1fr_32px] bg-[var(--bg-2)] text-[var(--text-dim)] text-[11px] uppercase tracking-wide">
        <div className="p-2"></div>
        <div className="p-2 border-l border-[var(--border)]">{keyPlaceholder}</div>
        <div className="p-2 border-l border-[var(--border)]">{valuePlaceholder}</div>
        <div className="p-2 border-l border-[var(--border)]"></div>
      </div>
      {display.map((r, i) => (
        <div
          key={i}
          className="grid grid-cols-[32px_1fr_1fr_32px] border-t border-[var(--border)] hover:bg-[var(--bg-2)]"
        >
          <div className="p-2 flex items-center justify-center">
            <input
              type="checkbox"
              checked={r.enabled}
              onChange={(e) => update(i, { enabled: e.target.checked })}
            />
          </div>
          <input
            className="p-2 border-l border-[var(--border)] w-full"
            placeholder={keyPlaceholder}
            value={r.key}
            onChange={(e) => update(i, { key: e.target.value })}
          />
          <input
            className="p-2 border-l border-[var(--border)] w-full"
            placeholder={valuePlaceholder}
            value={r.value}
            onChange={(e) => update(i, { value: e.target.value })}
          />
          <button
            className="border-l border-[var(--border)] text-[var(--text-mute)] hover:text-[var(--red)]"
            onClick={() => remove(i)}
            title="Remove"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
