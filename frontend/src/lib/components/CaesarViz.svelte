<script>
  let { data, step = -1 } = $props()
  const steps = $derived(data.steps ?? [])
  const active = $derived(steps.length ? (step < 0 ? steps.length - 1 : Math.min(step, steps.length - 1)) : -1)
</script>

<div class="space-y-4">
  <div class="text-xs uppercase tracking-widest text-cyan-400/80">
    Geseran {data.key.shift} · {data.mode === 'encrypt' ? 'Enkripsi' : 'Dekripsi'}
  </div>

  <div class="flex flex-wrap gap-2">
    {#each steps as s, i}
      <div class="flex flex-col items-center gap-1">
        <div
          class="w-9 h-9 grid place-items-center rounded-md font-mono text-sm border
          {i <= active ? 'bg-cyan-500/15 border-cyan-400/50 text-cyan-200' : 'bg-slate-800/50 border-slate-700 text-slate-500'}
          {i === active ? 'glow' : ''}">
          {s.char}
        </div>
        <div class="text-[10px] text-slate-500 font-mono">{s.index}→{s.new_index}</div>
        <div
          class="w-9 h-9 grid place-items-center rounded-md font-mono text-sm border
          {i <= active ? 'bg-amber-500/15 border-amber-400/50 text-amber-200' : 'bg-slate-800/50 border-slate-700 text-slate-600'}
          {i === active ? 'pop' : ''}">
          {i <= active ? s.cipher : '?'}
        </div>
      </div>
    {/each}
  </div>

  <div class="flex flex-wrap items-center gap-3 text-xs text-slate-400 font-mono">
    <span class="px-2 py-1 rounded bg-slate-800/60 border border-slate-700">A=0 … Z=25</span>
    <span class="px-2 py-1 rounded bg-slate-800/60 border border-slate-700">
      rumus: (P + {data.key.shift}) mod 26
    </span>
  </div>

  {#if data.brute_force && data.brute_force.length}
    <div class="pt-2">
      <div class="text-xs uppercase tracking-widest text-slate-400 mb-2">
        Brute force — coba semua geseran (bantu temukan kunci)
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2">
        {#each data.brute_force as b}
          <div class="font-mono text-xs px-2 py-1.5 rounded border border-slate-700 bg-slate-800/40">
            <span class="text-slate-500">k={b.shift}</span>
            <span class="text-slate-200 ml-2">{b.hasil}</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>
